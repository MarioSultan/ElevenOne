import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.odr import ODR, Model, RealData
from typing import Callable, Union, List, Optional, Tuple, Dict, Any

from .unit import Quantity, Unit
from .dimension import DIMENSIONLESS
from .data import Data


class FitResult:
    """
    Container class for data fitting results.
    
    Attributes
    ----------
    popt : np.ndarray or List[Quantity]
        Optimal values for the parameters.
    pcov : np.ndarray
        Estimated covariance matrix of popt.
    punc : np.ndarray
        Standard uncertainties (1-sigma errors) of the parameters.
    param_names : List[str]
        Names of the fitted parameters.
    model_func : Callable
        The fitting function used $f(x, *params)$.
    x_data : np.ndarray
        Independent variable data values.
    y_data : np.ndarray
        Dependent variable data values.
    x_err : Optional[np.ndarray]
        Errors in the independent variable.
    y_err : Optional[np.ndarray]
        Errors in the dependent variable.
    x_unit : Unit
        Unit of the independent variable.
    y_unit : Unit
        Unit of the dependent variable.
    param_units : List[Unit]
        Inferred units for each fitted parameter.
    params : Dict[str, Quantity]
        Dictionary mapping parameter names to Quantity objects (value ± error with units).
    y_fit : np.ndarray
        Fitted model values evaluated at `x_data`.
    residuals : np.ndarray
        Residuals ($y_{data} - y_{fit}$).
    chi2 : float
        Sum of squared weighted residuals ($\chi^2$).
    reduced_chi2 : float
        Reduced chi-squared ($\chi_\nu^2 = \chi^2 / \nu$).
    dof : int
        Degrees of freedom ($\nu = N - p$).
    r_squared : float
        Coefficient of determination ($R^2$).
    method : str
        Method used for fitting ('weighted_leastsquares' or 'odr').
    """

    def __init__(
        self,
        popt: np.ndarray,
        pcov: np.ndarray,
        param_names: List[str],
        model_func: Callable,
        x_data: np.ndarray,
        y_data: np.ndarray,
        x_err: Optional[np.ndarray],
        y_err: Optional[np.ndarray],
        x_unit: Unit,
        y_unit: Unit,
        param_units: Optional[List[Unit]] = None,
        method: str = "weighted_leastsquares"
    ):
        self.popt = popt
        self.pcov = pcov
        self.param_names = param_names
        self.model_func = model_func
        self.x_data = x_data
        self.y_data = y_data
        self.x_err = x_err
        self.y_err = y_err
        self.x_unit = x_unit
        self.y_unit = y_unit
        self.method = method

        # Parameter uncertainties (sqrt of diagonal elements of covariance matrix)
        if pcov is not None and pcov.ndim == 2:
            self.punc = np.sqrt(np.diag(pcov))
        else:
            self.punc = np.zeros_like(popt)

        # Default unit logic for parameters if not explicitly provided
        if param_units is None:
            self.param_units = [Unit(DIMENSIONLESS)] * len(popt)
        else:
            self.param_units = param_units

        # Construct Quantity dict for parameters
        self.params: Dict[str, Quantity] = {}
        for name, val, err, unit in zip(self.param_names, self.popt, self.punc, self.param_units):
            self.params[name] = Quantity(val, unit, err)

        # Fitted values & residuals
        self.y_fit = self.model_func(self.x_data, *self.popt)
        self.residuals = self.y_data - self.y_fit

        # Degrees of freedom
        n_obs = len(self.y_data)
        n_params = len(self.popt)
        self.dof = max(1, n_obs - n_params)

        # Calculate Chi-Squared & Reduced Chi-Squared
        if self.y_err is not None and np.any(self.y_err > 0):
            weights = np.where(self.y_err > 0, 1.0 / (self.y_err ** 2), 1.0)
            self.chi2 = float(np.sum(weights * (self.residuals ** 2)))
        else:
            self.chi2 = float(np.sum(self.residuals ** 2))

        self.reduced_chi2 = self.chi2 / self.dof

        # Calculate R-squared
        ss_res = np.sum(self.residuals ** 2)
        ss_tot = np.sum((self.y_data - np.mean(self.y_data)) ** 2)
        self.r_squared = float(1.0 - (ss_res / ss_tot)) if ss_tot != 0 else 1.0

    def eval(self, x: Union[float, np.ndarray, Quantity]) -> Union[np.ndarray, Quantity]:
        """Evaluates the fitted model at arbitrary x value(s)."""
        if isinstance(x, Quantity):
            # Convert x to internal x_unit value
            x_val = x.value if x.unit == self.x_unit else (x / Quantity(1, self.x_unit)).value
            y_val = self.model_func(x_val, *self.popt)
            return Quantity(y_val, self.y_unit)
        else:
            x_arr = np.asarray(x)
            return self.model_func(x_arr, *self.popt)

    def summary(self) -> str:
        """Returns a formatted summary text of the fit result."""
        lines = [
            "==================================================",
            f" Fitting Summary ({self.method})",
            "==================================================",
            f"Degrees of Freedom (dof) : {self.dof}",
            f"Chi-Squared (chi2)       : {self.chi2:.4g}",
            f"Reduced Chi-Squared      : {self.reduced_chi2:.4g}",
            f"R-Squared (R2)           : {self.r_squared:.5f}",
            "--------------------------------------------------",
            "Fitted Parameters:"
        ]
        for name, q in self.params.items():
            unit_str = f" [{q.unit.symbol}]" if q.unit.symbol else ""
            lines.append(f"  {name:<10} = {q.value:.5g} +/- {q.error:.5g}{unit_str}")
        lines.append("==================================================")
        return "\n".join(lines)

    def plot(
        self,
        num_points: int = 500,
        show_residuals: bool = True,
        figsize: Tuple[float, float] = (8, 6),
        title: Optional[str] = "Model Fit Result",
        ax: Optional[plt.Axes] = None,
        **kwargs
    ) -> Tuple[plt.Figure, Any]:
        """
        Plots the experimental data, fit curve, and optionally residuals using Data styling.
        """
        primary_color = Data._primary_color
        secondary_color = Data._secondary_color
        facecolor = Data._facecolor
        figure_facecolor = Data._figure_facecolor
        grid_color = Data._grid_color
        text_color = Data._text_color
        error_color = Data._error_color

        x_min, x_max = np.min(self.x_data), np.max(self.x_data)
        margin = (x_max - x_min) * 0.05 if x_max != x_min else 1.0
        x_dense = np.linspace(x_min - margin, x_max + margin, num_points)
        y_dense = self.model_func(x_dense, *self.popt)

        x_lbl = f"x [{self.x_unit.symbol}]" if self.x_unit.symbol else "x"
        y_lbl = f"y [{self.y_unit.symbol}]" if self.y_unit.symbol else "y"

        if show_residuals:
            if ax is None:
                fig, (ax_main, ax_res) = plt.subplots(
                    2, 1, figsize=figsize, dpi=180, gridspec_kw={'height_ratios': [3, 1]}, sharex=True
                )
            else:
                fig = ax.get_figure()
                # If single ax is passed, create twin/grid setup or plot inside provided
                ax_main = ax
                ax_res = None
        else:
            if ax is None:
                fig, ax_main = plt.subplots(figsize=figsize, dpi=180)
            else:
                fig = ax.get_figure()
                ax_main = ax
            ax_res = None

        fig.patch.set_facecolor(figure_facecolor)

        for axes in ([ax_main, ax_res] if ax_res is not None else [ax_main]):
            axes.set_facecolor(facecolor)
            for spine in ['top', 'right']:
                axes.spines[spine].set_visible(False)
            for spine in ['left', 'bottom']:
                axes.spines[spine].set_color('#d0d0d0')
                axes.spines[spine].set_linewidth(1.0)
            axes.tick_params(colors='#555555', which='both', labelsize=9, length=4, width=0.8)
            axes.grid(True, linestyle='--', alpha=0.45, color=grid_color, zorder=0)

        # Plot Data Points with Error Bars
        ax_main.errorbar(
            self.x_data,
            self.y_data,
            xerr=self.x_err if (self.x_err is not None and np.any(self.x_err != 0)) else None,
            yerr=self.y_err if (self.y_err is not None and np.any(self.y_err != 0)) else None,
            fmt='o',
            color=primary_color,
            ecolor=error_color,
            elinewidth=1.2,
            capsize=3,
            markersize=5,
            label='Data',
            zorder=3
        )

        # Plot Fit Line
        ax_main.plot(
            x_dense,
            y_dense,
            color=secondary_color,
            linestyle='-',
            linewidth=2.0,
            label='Fit',
            zorder=4
        )

        ax_main.set_ylabel(y_lbl, fontsize=10, fontweight='bold', color=text_color)
        if title:
            ax_main.set_title(title, fontsize=12, fontweight='bold', color=text_color, loc='left', pad=12)

        ax_main.legend(frameon=True, facecolor=figure_facecolor, edgecolor='none', fontsize=9)

        # Residuals subplot
        if ax_res is not None:
            ax_res.axhline(0, color=secondary_color, linestyle='--', linewidth=1.2, zorder=2)
            ax_res.errorbar(
                self.x_data,
                self.residuals,
                yerr=self.y_err if (self.y_err is not None and np.any(self.y_err != 0)) else None,
                fmt='o',
                color=primary_color,
                ecolor=error_color,
                elinewidth=1.0,
                capsize=2,
                markersize=4,
                zorder=3
            )
            ax_res.set_xlabel(x_lbl, fontsize=10, fontweight='bold', color=text_color)
            ax_res.set_ylabel("Residuals", fontsize=9, fontweight='bold', color=text_color)
        else:
            ax_main.set_xlabel(x_lbl, fontsize=10, fontweight='bold', color=text_color)

        fig.tight_layout()
        return fig, (ax_main, ax_res) if ax_res is not None else ax_main

    def __repr__(self) -> str:
        return self.summary()

    def _repr_html_(self) -> str:
        import pandas as pd
        data_summary = {
            "Parameter": self.param_names,
            "Value": [q.value for q in self.params.values()],
            "Uncertainty": [q.error for q in self.params.values()],
            "Unit": [q.unit.symbol for q in self.params.values()]
        }
        df_params = pd.DataFrame(data_summary)
        stats_html = f"""
        <div style="font-family: sans-serif; font-size: 13px;">
            <h4>Fit Results ({self.method})</h4>
            <p><b>R²:</b> {self.r_squared:.5f} | <b>Reduced χ²:</b> {self.reduced_chi2:.4g} | <b>DoF:</b> {self.dof}</p>
            {df_params._repr_html_()}
        </div>
        """
        return stats_html


# ==============================================================================
# Helper Functions for Extraction and Fitting Logic
# ==============================================================================

def _extract_fit_arrays(
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None
) -> Tuple[np.ndarray, np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Unit, Unit]:
    """Extracts numpy arrays, errors, and units from input Data/Quantity/array arguments."""
    if data is not None:
        if not isinstance(x, str) or not isinstance(y, str):
            raise TypeError("When passing 'data', 'x' and 'y' must be column names (strings).")
        
        x_obj = data[x]
        y_obj = data[y]
    else:
        x_obj = x
        y_obj = y

    # Process X
    if isinstance(x_obj, Quantity):
        x_vals = np.asarray(x_obj.value, dtype=float)
        x_errors = np.asarray(x_obj.error, dtype=float)
        x_unit = x_obj.unit
    else:
        x_vals = np.asarray(x_obj, dtype=float)
        x_errors = np.zeros_like(x_vals)
        x_unit = Unit(DIMENSIONLESS)

    # Process Y
    if isinstance(y_obj, Quantity):
        y_vals = np.asarray(y_obj.value, dtype=float)
        y_errors = np.asarray(y_obj.error, dtype=float)
        y_unit = y_obj.unit
    else:
        y_vals = np.asarray(y_obj, dtype=float)
        y_errors = np.zeros_like(y_vals)
        y_unit = Unit(DIMENSIONLESS)

    # Override/specify errors explicitly if provided
    if xerr is not None:
        if isinstance(xerr, str) and data is not None:
            col_err = data[xerr]
            x_errors = col_err.value if isinstance(col_err, Quantity) else np.asarray(col_err, dtype=float)
        elif isinstance(xerr, Quantity):
            x_errors = np.asarray(xerr.value, dtype=float)
        else:
            x_errors = np.broadcast_to(np.asarray(xerr, dtype=float), x_vals.shape)

    if yerr is not None:
        if isinstance(yerr, str) and data is not None:
            col_err = data[yerr]
            y_errors = col_err.value if isinstance(col_err, Quantity) else np.asarray(col_err, dtype=float)
        elif isinstance(yerr, Quantity):
            y_errors = np.asarray(yerr.value, dtype=float)
        else:
            y_errors = np.broadcast_to(np.asarray(yerr, dtype=float), y_vals.shape)

    x_err_final = x_errors if np.any(x_errors > 0) else None
    y_err_final = y_errors if np.any(y_errors > 0) else None

    return x_vals, y_vals, x_err_final, y_err_final, x_unit, y_unit


def fit_custom(
    model_func: Callable,
    param_names: List[str],
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    p0: Optional[List[float]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    param_units: Optional[List[Unit]] = None
) -> FitResult:
    """
    Fits an arbitrary model function $y = f(x, *params)$ to data.
    Uses Orthogonal Distance Regression (ODR) if both xerr and yerr exist, 
    otherwise weighted Non-Linear Least Squares (`scipy.optimize.curve_fit`).
    """
    x_data, y_data, x_err, y_err, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)

    has_xerr = x_err is not None and np.any(x_err > 0)
    has_yerr = y_err is not None and np.any(y_err > 0)

    if p0 is None:
        import inspect
        sig = inspect.signature(model_func)
        p0 = [1.0] * (len(sig.parameters) - 1)

    if has_xerr and has_yerr:
        # ODR Fitting
        def odr_wrapper(beta, x):
            return model_func(x, *beta)

        odr_model = Model(odr_wrapper)
        odr_data = RealData(x_data, y_data, sx=x_err, sy=y_err)
        odr_inst = ODR(odr_data, odr_model, beta0=p0)
        output = odr_inst.run()

        popt = output.beta
        pcov = output.cov_beta
        method = "odr"
    else:
        # Non-Linear Least Squares Fitting
        popt, pcov = curve_fit(
            model_func,
            x_data,
            y_data,
            p0=p0,
            sigma=y_err if has_yerr else None,
            absolute_sigma=has_yerr
        )
        method = "weighted_leastsquares"

    return FitResult(
        popt=popt,
        pcov=pcov,
        param_names=param_names,
        model_func=model_func,
        x_data=x_data,
        y_data=y_data,
        x_err=x_err,
        y_err=y_err,
        x_unit=x_unit,
        y_unit=y_unit,
        param_units=param_units,
        method=method
    )


# ==============================================================================
# Dedicated Fitting Routines
# ==============================================================================

def fit_linear(
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None
) -> FitResult:
    """
    Fits a linear model: $y = m \\cdot x + b$.
    """
    def linear_model(x_val, m, b):
        return m * x_val + b

    _, _, _, _, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)
    
    m_unit = y_unit / x_unit if (x_unit and y_unit) else Unit(DIMENSIONLESS)
    b_unit = y_unit

    return fit_custom(
        model_func=linear_model,
        param_names=["m", "b"],
        data=data,
        x=x,
        y=y,
        p0=[1.0, 0.0],
        xerr=xerr,
        yerr=yerr,
        param_units=[m_unit, b_unit]
    )


def fit_polynomial(
    degree: int = 2,
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None
) -> FitResult:
    """
    Fits a polynomial model: $y = a_n \\cdot x^n + \\dots + a_1 \\cdot x + a_0$.
    """
    def poly_model(x_val, *coeffs):
        return sum(c * (x_val ** (degree - i)) for i, c in enumerate(coeffs))

    param_names = [f"a{degree - i}" for i in range(degree + 1)]
    _, _, _, _, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)

    param_units = [y_unit / (x_unit ** (degree - i)) for i in range(degree + 1)]

    return fit_custom(
        model_func=poly_model,
        param_names=param_names,
        data=data,
        x=x,
        y=y,
        p0=[1.0] * (degree + 1),
        xerr=xerr,
        yerr=yerr,
        param_units=param_units
    )


def fit_exponential(
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    p0: Optional[List[float]] = None
) -> FitResult:
    """
    Fits an exponential model: $y = a \\cdot e^{b \\cdot x}$.
    """
    def exp_model(x_val, a, b):
        return a * np.exp(b * x_val)

    _, _, _, _, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)
    
    a_unit = y_unit
    b_unit = x_unit ** (-1)

    return fit_custom(
        model_func=exp_model,
        param_names=["a", "b"],
        data=data,
        x=x,
        y=y,
        p0=p0 or [1.0, 0.1],
        xerr=xerr,
        yerr=yerr,
        param_units=[a_unit, b_unit]
    )


def fit_power(
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    p0: Optional[List[float]] = None
) -> FitResult:
    """
    Fits a power law model: $y = a \\cdot x^b$.
    """
    def power_model(x_val, a, b):
        return a * np.power(x_val, b)

    _, _, _, _, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)

    return fit_custom(
        model_func=power_model,
        param_names=["a", "b"],
        data=data,
        x=x,
        y=y,
        p0=p0 or [1.0, 1.0],
        xerr=xerr,
        yerr=yerr,
        param_units=[y_unit, Unit(DIMENSIONLESS)]
    )


def fit_logarithmic(
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    p0: Optional[List[float]] = None
) -> FitResult:
    """
    Fits a logarithmic model: $y = a \\cdot \\ln(x) + b$.
    """
    def log_model(x_val, a, b):
        return a * np.log(x_val) + b

    _, _, _, _, x_unit, y_unit = _extract_fit_arrays(data, x, y, xerr, yerr)

    return fit_custom(
        model_func=log_model,
        param_names=["a", "b"],
        data=data,
        x=x,
        y=y,
        p0=p0 or [1.0, 0.0],
        xerr=xerr,
        yerr=yerr,
        param_units=[y_unit, y_unit]
    )