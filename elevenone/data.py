import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from .unit import Quantity, Unit, RADIAN, _scheme_view
from .unit_scheme import get_scheme, convert_to_scheme
from .dimension import DIMENSIONLESS, ANGULAR
from .styles import DEFAULT_STYLES

class Data:
    _styles = DEFAULT_STYLES.copy()
    _current_style = "elevenone"

    _primary_color = DEFAULT_STYLES["elevenone"]["primary"]
    _secondary_color = DEFAULT_STYLES["elevenone"]["secondary"]
    _facecolor = DEFAULT_STYLES["elevenone"]["facecolor"]
    _figure_facecolor = DEFAULT_STYLES["elevenone"]["figure_facecolor"]
    _grid_color = DEFAULT_STYLES["elevenone"]["grid_color"]
    _text_color = DEFAULT_STYLES["elevenone"]["text_color"]
    _error_color = DEFAULT_STYLES["elevenone"]["error_color"]

    @classmethod
    def register_style(cls, name: str, primary: str = "#00ccff", secondary: str = "#ff2ad4", 
                       facecolor: str = "#fcfcfc", figure_facecolor: str = "#ffffff", 
                       grid_color: str = "#ebebeb", text_color: str = "#1a1a1a", error_color: str = "#888888"):
        """Registers or updates a custom style in the style catalog."""
        cls._styles[name] = {
            "primary": primary,
            "secondary": secondary,
            "facecolor": facecolor,
            "figure_facecolor": figure_facecolor,
            "grid_color": grid_color,
            "text_color": text_color,
            "error_color": error_color
        }

    @classmethod
    def list_styles(cls):
        """Returns the list of available style names."""
        return list(cls._styles.keys())

    @classmethod
    def set_style(cls, style_name: str = None, **kwargs):
        """Sets the visual style by loading a saved style or specifying colors directly.
        
        Parameters
        ----------
        style_name : str, optional
            Name of the predefined or registered style to load (e.g., 'elevenone', 'dark_mode').
        **kwargs :
            Allows overriding individual style attributes (primary, secondary, facecolor, 
            figure_facecolor, grid_color, text_color, error_color).
        """
        if style_name is not None:
            if style_name not in cls._styles:
                raise ValueError(f"Style '{style_name}' not found. Available styles: {cls.list_styles()}")
            style_dict = cls._styles[style_name].copy()
            cls._current_style = style_name
        else:
            style_dict = cls._styles[cls._current_style].copy()

        style_dict.update({k: v for k, v in kwargs.items() if k in style_dict})

        cls._primary_color = style_dict["primary"]
        cls._secondary_color = style_dict["secondary"]
        cls._facecolor = style_dict["facecolor"]
        cls._figure_facecolor = style_dict["figure_facecolor"]
        cls._grid_color = style_dict["grid_color"]
        cls._text_color = style_dict["text_color"]
        cls._error_color = style_dict["error_color"]

        cls._apply_global_rc_params()

    @classmethod
    def set_theme(cls, *args, **kwargs):
        """Backward-compatible alias for set_style."""
        if args and isinstance(args[0], str) and args[0] in cls._styles:
            cls.set_style(args[0], **kwargs)
        else:
            if args:
                keys = ["primary", "secondary", "facecolor", "figure_facecolor", "grid_color", "text_color", "error_color"]
                for k, v in zip(keys, args):
                    kwargs[k] = v
            cls.set_style(style_name=None, **kwargs)

    @classmethod
    def _apply_global_rc_params(cls):
        plt.rcParams.update({
            'font.family': 'sans-serif',
            'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans', 'Liberation Sans'],
            'text.color': cls._text_color,
            'axes.labelcolor': cls._text_color,
            'xtick.color': '#666666',
            'ytick.color': '#666666',
            'xtick.direction': 'in',
            'ytick.direction': 'in',
            'axes.linewidth': 0.8,
            'grid.linestyle': '--',
            'grid.alpha': 0.4,
            'figure.autolayout': True
        })

    def __init__(self, data_dict: dict):
        self.dict = {}
        self._length = None
        self._apply_global_rc_params()

        for col_name, val in data_dict.items():
            if isinstance(val, Quantity):
                col_data = val
            elif isinstance(val, (list, np.ndarray, tuple)):
                col_data = np.asarray(val)
            else:
                col_data = np.asarray([val])

            length = len(col_data)
            if self._length is None:
                self._length = length
            elif length != self._length:
                raise ValueError(f"Column '{col_name}' has length {length}, but expected {self._length}.")

            self.dict[col_name] = col_data

        self.columns = list(self.dict.keys())

    def __getitem__(self, key):
        if isinstance(key, str):
            if key not in self.dict:
                raise KeyError(f"Column '{key}' not found in Data.")
            return self.dict[key]

        if isinstance(key, (list, tuple)) and len(key) > 0 and all(isinstance(col, str) for col in key):
            sub_dict = {}
            for col in key:
                if col not in self.dict:
                    raise KeyError(f"Column '{col}' not found in Data.")
                sub_dict[col] = self.dict[col]
            return Data(sub_dict)

        is_bool_array = isinstance(key, np.ndarray) and key.dtype == bool
        is_bool_list = isinstance(key, (list, tuple)) and len(key) == self._length and all(isinstance(x, (bool, np.bool_)) for x in key)

        if is_bool_array or is_bool_list:
            mask = np.asarray(key)
            if len(mask) != self._length:
                raise ValueError(f"Boolean mask length ({len(mask)}) does not match data length ({self._length}).")
            
            filtered_dict = {}
            for col, val in self.dict.items():
                if isinstance(val, Quantity):
                    filtered_dict[col] = Quantity(val.value[mask], val.unit, val.error[mask])
                elif isinstance(val, np.ndarray):
                    filtered_dict[col] = val[mask]
                else:
                    filtered_dict[col] = np.asarray(val)[mask]
            
            return Data(filtered_dict)

        is_int = isinstance(key, (int, np.integer))
        is_slice = isinstance(key, slice)
        is_int_array = isinstance(key, np.ndarray) and np.issubdtype(key.dtype, np.integer)
        is_int_list = isinstance(key, (list, tuple)) and (len(key) == 0 or all(isinstance(x, (int, np.integer)) for x in key))

        if is_int:
            indices = [key]
        elif is_slice:
            indices = list(range(self._length)[key])
        elif is_int_array or is_int_list:
            indices = list(key)
        else:
            indices = None

        if indices is not None:
            filtered_dict = {}
            for col, val in self.dict.items():
                if isinstance(val, Quantity):
                    filtered_dict[col] = Quantity(val.value[indices], val.unit, val.error[indices])
                elif isinstance(val, np.ndarray):
                    filtered_dict[col] = val[indices]
                else:
                    filtered_dict[col] = np.asarray(val)[indices]
            return Data(filtered_dict)

        raise TypeError("Invalid key type for indexing Data.")

    def query(self, expr: str):
        local_dict = {}
        for col_name, val in self.dict.items():
            if isinstance(val, Quantity):
                local_dict[col_name] = _scheme_view(val).value
            else:
                local_dict[col_name] = val

        try:
            mask = eval(expr, {"np": np}, local_dict)
        except Exception as e:
            raise ValueError(f"Error evaluating query expression '{expr}': {e}")

        return self[mask]

    def head(self, n: int = 5):
        n = min(max(0, n), self._length)
        return self[np.arange(n)]

    def tail(self, n: int = 5):
        n = min(max(0, n), self._length)
        start = max(0, self._length - n)
        return self[np.arange(start, self._length)]

    def sample(self, n: int = None, frac: float = None, replace: bool = False, random_state: int = None):
        if random_state is not None:
            np.random.seed(random_state)
        
        if n is None and frac is None:
            n = 1
        elif frac is not None:
            if not (0.0 <= frac <= 1.0):
                raise ValueError("frac must be between 0.0 and 1.0")
            n = int(round(self._length * frac))
        
        if not replace and n > self._length:
            raise ValueError("Cannot sample larger than population when replace=False")
            
        indices = np.random.choice(self._length, size=n, replace=replace)
        return self[indices]

    def sort_values(self, by, ascending=True):
        if isinstance(by, str):
            by = [by]
        
        for col in by:
            if col not in self.dict:
                raise KeyError(f"Column '{col}' not found in Data.")
        
        primary_col = by[0]
        val = self.dict[primary_col]
        arr = val.value if isinstance(val, Quantity) else val
        
        sorted_indices = np.argsort(arr)
        if not ascending:
            sorted_indices = sorted_indices[::-1]
            
        return self[sorted_indices]

    def drop_duplicates(self, subset=None, keep='first'):
        if subset is None:
            cols = self.columns
        elif isinstance(subset, str):
            cols = [subset]
        else:
            cols = list(subset)
            
        for col in cols:
            if col not in self.dict:
                raise KeyError(f"Column '{col}' not found in Data.")
                
        columns_data = [
            (self.dict[c].value if isinstance(self.dict[c], Quantity) else self.dict[c])
            for c in cols
        ]
        
        seen = set()
        keep_indices = []
        
        if keep == 'first':
            for i in range(self._length):
                row_key = tuple(col_data[i] for col_data in columns_data)
                if row_key not in seen:
                    seen.add(row_key)
                    keep_indices.append(i)
        elif keep == 'last':
            last_seen = {}
            for i in range(self._length):
                row_key = tuple(col_data[i] for col_data in columns_data)
                last_seen[row_key] = i
            keep_indices = sorted(list(last_seen.values()))
        elif keep is False:
            from collections import Counter
            row_keys = [tuple(col_data[i] for col_data in columns_data) for i in range(self._length)]
            counts = Counter(row_keys)
            keep_indices = [i for i, rk in enumerate(row_keys) if counts[rk] == 1]
        else:
            raise ValueError("keep must be 'first', 'last', or False")
            
        return self[np.array(keep_indices)]

    def rename(self, columns: dict):
        new_dict = {}
        for k, v in self.dict.items():
            new_key = columns.get(k, k)
            new_dict[new_key] = v
        return Data(new_dict)

    def set_error(self, columns, errors):
        if isinstance(columns, str):
            columns = [columns]

        if isinstance(errors, dict):
            for col, err in errors.items():
                if col not in self.dict:
                    raise KeyError(f"Column '{col}' not found in Data.")
                val = self.dict[col]
                if isinstance(val, Quantity):
                    val.set_error(err)
                else:
                    self.dict[col] = Quantity(val, Unit(DIMENSIONLESS), err)
        else:
            for col in columns:
                if col not in self.dict:
                    raise KeyError(f"Column '{col}' not found in Data.")
                val = self.dict[col]
                if isinstance(val, Quantity):
                    val.set_error(errors)
                else:
                    self.dict[col] = Quantity(val, Unit(DIMENSIONLESS), errors)
        return self

    def __setitem__(self, key, value):
        if self._length is not None:
            if isinstance(value, Quantity):
                val = np.atleast_1d(value.value)
                err = np.atleast_1d(value.error)
                if len(val) == 1 and self._length > 1:
                    val_arr = np.full(self._length, val[0])
                    err_arr = np.full(self._length, err[0])
                    col_data = Quantity(val_arr, value.unit, err_arr)
                else:
                    col_data = value
            else:
                arr = np.asarray(value)
                if arr.ndim == 0 or (arr.ndim == 1 and len(arr) == 1 and self._length > 1):
                    scalar_val = arr.item() if arr.ndim == 0 else arr[0]
                    col_data = np.full(self._length, scalar_val)
                else:
                    col_data = arr
        else:
            if isinstance(value, Quantity):
                col_data = value
            elif isinstance(value, (list, np.ndarray, tuple)):
                col_data = np.asarray(value)
            else:
                col_data = np.asarray([value])

        if self._length is not None and len(col_data) != self._length:
            raise ValueError(f"Length of new data ({len(col_data)}) does not match Data length ({self._length}).")

        if self._length is None:
            self._length = len(col_data)

        self.dict[key] = col_data
        self.columns = list(self.dict.keys())

    def __delitem__(self, key):
        if key in self.dict:
            del self.dict[key]
            self.columns = list(self.dict.keys())
            if not self.dict:
                self._length = None
        else:
            raise KeyError(f"Column '{key}' not found in Data.")

    def copy(self):
        new_dict = {}
        for k, v in self.dict.items():
            if isinstance(v, Quantity):
                val_copy = v.value.copy() if hasattr(v.value, 'copy') else v.value
                err_copy = v.error.copy() if hasattr(v.error, 'copy') else v.error
                new_dict[k] = Quantity(val_copy, v.unit, err_copy)
            elif isinstance(v, np.ndarray):
                new_dict[k] = v.copy()
            else:
                new_dict[k] = np.copy(v) if hasattr(v, '__array__') else v
        return Data(new_dict)

    def to_scheme(self, scheme=None):
        """Returns a copy of the data with every Quantity column expressed in a unit scheme.

        ``scheme`` can be a registered name, a UnitScheme, or None (the active scheme).
        Without any scheme this is just a copy.

        Note that while a scheme is active, tables, plots and reports always follow the
        *active* scheme. To see or plot data in another scheme temporarily, prefer
        ``with use_scheme("CGS"): ...``; ``to_scheme`` is meant for getting converted
        data (e.g. to export it) or for working with no scheme active.
        """
        converted = self.copy()
        for name, col in converted.dict.items():
            if isinstance(col, Quantity):
                converted.dict[name] = convert_to_scheme(col, scheme)
        return converted

    @property
    def shape(self):
        return (self._length, len(self.dict))

    def __len__(self):
        return self._length

    def _to_dataframe(self):
        representation_dict = {}
        for col_name, col_data in self.dict.items():
            if isinstance(col_data, Quantity):
                col_data = _scheme_view(col_data)
                representation_dict[f"{col_name} [{col_data.unit.symbol}]"] = col_data.value
                representation_dict[f"{col_name}_err"] = col_data.error
            else:
                representation_dict[col_name] = col_data
        return pd.DataFrame(representation_dict)

    def __repr__(self):
        return str(self._to_dataframe())

    def _repr_html_(self):
        return self._to_dataframe()._repr_html_()

    # ------------------------------------------------------------------
    # pandas interoperability
    # ------------------------------------------------------------------

    def to_pandas(self, errors="auto", units=True, scheme=True, err_suffix="_err"):
        """Converts the Data into a pandas DataFrame.

        Every Quantity column becomes a numeric column named ``"name [unit]"`` followed (if it has
        uncertainty) by ``"name_err"``. This is the same convention understood by ``load_data`` and
        by ``Data.from_pandas``, so ``Data.from_pandas(d.to_pandas())`` recovers units and errors.

        Parameters
        ----------
        errors : {"auto", True, False}
            "auto": add the error column only for quantities with some non-zero uncertainty.
            True: always add it. False: never add it.
        units : bool
            If True the unit goes in the column name; if False the names are left bare.
        scheme : bool
            If True (default) quantities are expressed in the active unit scheme, like tables
            and plots do. With False the units each column carries are used.
        err_suffix : str
            Suffix of the uncertainty columns.
        """
        if errors not in (True, False, "auto"):
            raise ValueError("errors must be 'auto', True or False.")

        out = {}
        for name, col in self.dict.items():
            if isinstance(col, Quantity):
                q = _scheme_view(col) if scheme else col
                key = f"{name} [{q.unit.symbol}]" if units else str(name)
                out[key] = np.array(q.value, copy=True)
                has_err = bool(np.any(q.error != 0))
                if errors is True or (errors == "auto" and has_err):
                    out[f"{name}{err_suffix}"] = np.array(q.error, copy=True)
            else:
                out[name] = np.array(col, copy=True)
        return pd.DataFrame(out)

    @classmethod
    def from_pandas(cls, df, units=None, errors=None, parse=True):
        """Builds a Data from a pandas DataFrame (or Series).

        Parameters
        ----------
        df : pandas.DataFrame or pandas.Series
            The index is ignored.
        units : dict, optional
            ``{"column": Unit}``. Declares the unit of the numbers in that column (it replaces any
            unit detected from the header), e.g. ``units={"t": s, "x": m}``.
        errors : dict, optional
            ``{"column": error}`` where error is a scalar, an array, a Quantity, or the NAME of another
            column of ``df`` holding the uncertainties (that column is then not kept as data).
        parse : bool
            True (default): units in headers/cells and ``_err`` columns are detected automatically
            (same rules as ``load_data``). False: the columns are taken as plain numbers.
        """
        if isinstance(df, pd.Series):
            df = df.to_frame(name=df.name if df.name is not None else "value")
        if not isinstance(df, pd.DataFrame):
            raise TypeError("from_pandas expects a pandas DataFrame or Series.")

        if parse:
            from .load import dataframe_to_data
            data = dataframe_to_data(df)
        else:
            data = cls({str(c): df[c].to_numpy() for c in df.columns})

        if units:
            for col, unit in units.items():
                if col not in data.dict:
                    raise KeyError(f"Column '{col}' not found in Data.")
                val = data.dict[col]
                if isinstance(val, Quantity):
                    data.dict[col] = Quantity(val.value, unit, val.error)
                else:
                    data.dict[col] = Quantity(np.asarray(val, dtype=float), unit)

        if errors:
            resolved, to_drop = {}, []
            for col, err in errors.items():
                if isinstance(err, str):
                    if err not in df.columns:
                        raise KeyError(f"Error column '{err}' not found in the DataFrame.")
                    resolved[col] = df[err].to_numpy(dtype=float)
                    if err in data.dict:
                        to_drop.append(err)
                else:
                    resolved[col] = err
            data.set_error(list(resolved.keys()), resolved)
            for name in to_drop:
                del data[name]
        return data

    def to_csv(self, path, **kwargs):
        """Writes the data to CSV (units in the headers, uncertainties as ``_err`` columns).
        The file can be read back with ``load_data``."""
        kwargs.setdefault("index", False)
        return self.to_pandas().to_csv(path, **kwargs)

    def to_excel(self, path, **kwargs):
        """Writes the data to Excel (same layout as ``to_csv``; readable with ``load_data``)."""
        kwargs.setdefault("index", False)
        return self.to_pandas().to_excel(path, **kwargs)

    def _numeric_columns(self):
        return {k: (_scheme_view(v) if isinstance(v, Quantity) else v)
                for k, v in self.dict.items()
                if isinstance(v, Quantity) or np.issubdtype(v.dtype, np.number)}

    def describe(self):
        stats_rows = ['count', 'mean', 'std', 'min', 'Q1', 'Q2', 'Q3', 'max']
        numeric_cols = self._numeric_columns()
        summary_data = {}

        for k, v in numeric_cols.items():
            is_qty = isinstance(v, Quantity)
            unit_sym = v.unit.symbol if is_qty else ""
            vals = v.value if is_qty else np.asarray(v)

            count = len(vals)
            mean_val = np.mean(vals)
            std_val = np.std(vals, ddof=1) if len(vals) > 1 else 0.0
            min_val = np.min(vals)
            p25_val = np.percentile(vals, 25)
            med_val = np.median(vals)
            p75_val = np.percentile(vals, 75)
            max_val = np.max(vals)

            col_stats = []
            for val in [count, mean_val, std_val, min_val, p25_val, med_val, p75_val, max_val]:
                if is_qty:
                    if val is count:
                        col_stats.append(val)
                    else:
                        col_stats.append(f"{val:.4g} {unit_sym}")
                else:
                    col_stats.append(val if val is count else f"{val:.4g}" if isinstance(val, (int, float, np.number)) else val)
            
            summary_data[k] = col_stats

        df_summary = pd.DataFrame(summary_data, index=stats_rows)
        return DataDescribeResult(df_summary)

    def mean(self):
        res = {k: (v.mean() if isinstance(v, Quantity) else np.mean(v)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def median(self):
        res = {k: (Quantity(np.median(v.value), v.unit, np.median(v.error)) if isinstance(v, Quantity) else np.median(v)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def min(self):
        res = {k: (v.min() if isinstance(v, Quantity) else np.min(v)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def max(self):
        res = {k: (v.max() if isinstance(v, Quantity) else np.max(v)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def std(self, ddof=1):
        res = {k: (v.std(ddof=ddof) if isinstance(v, Quantity) else np.std(v, ddof=ddof)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def var(self, ddof=1):
        res = {k: (v.var(ddof=ddof) if isinstance(v, Quantity) else np.var(v, ddof=ddof)) for k, v in self._numeric_columns().items()}
        return DataStatsResult(res)

    def corr(self):
        num_cols = self._numeric_columns()
        data_for_corr = {k: (v.value if isinstance(v, Quantity) else v) for k, v in num_cols.items()}
        return pd.DataFrame(data_for_corr).corr()

    def _get_plot_series(self, col_name: str):
        if col_name not in self.dict:
            raise KeyError(f"Column '{col_name}' not found in Data.")
        
        col_data = self.dict[col_name]
        if isinstance(col_data, Quantity):
            col_data = _scheme_view(col_data)
            values = col_data.value
            errors = col_data.error
            label = f"{col_name} [{col_data.unit.symbol}]"
        else:
            values = col_data
            errors = np.zeros_like(values, dtype=float)
            label = col_name
        return values, errors, label

    def _init_plot_figure(self, ax, figsize):
        if ax is None:
            fig, ax = plt.subplots(figsize=figsize, dpi=200)
        else:
            fig = ax.get_figure()
        
        fig.patch.set_facecolor(self._figure_facecolor)
        ax.set_facecolor(self._facecolor)
        
        for spine_name in ['top', 'right']:
            ax.spines[spine_name].set_visible(False)
        for spine_name in ['left', 'bottom']:
            ax.spines[spine_name].set_color('#d0d0d0')
            ax.spines[spine_name].set_linewidth(1.0)

        ax.tick_params(colors='#555555', which='both', labelsize=10, length=4, width=0.8)
        return fig, ax

    def _apply_grid(self, ax, axis='both'):
        ax.grid(True, linestyle='--', alpha=0.45, color=self._grid_color, axis=axis, zorder=0)

    def _format_labels(self, ax, xlabel, ylabel, title):
        ax.set_xlabel(xlabel, fontsize=11, fontweight='bold', color=self._text_color, labelpad=10)
        ax.set_ylabel(ylabel, fontsize=11, fontweight='bold', color=self._text_color, labelpad=10)
        if title:
            ax.set_title(title, fontsize=13, fontweight='bold', color=self._text_color, pad=15, loc='left')

    def plot(self, x: str, y: str, ax=None, figsize=(8, 4.5), color=None, linestyle='-', linewidth=2.2, 
             marker='o', markersize=True, fill_area=True, sort_x=True, title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, x_errs, x_label = self._get_plot_series(x)
        y_vals, y_errs, y_label = self._get_plot_series(y)
        
        if sort_x:
            sort_idx = np.argsort(x_vals)
            x_vals = x_vals[sort_idx]
            x_errs = x_errs[sort_idx]
            y_vals = y_vals[sort_idx]
            y_errs = y_errs[sort_idx]

        fig, ax = self._init_plot_figure(ax, figsize)
        line_color = color if color is not None else self._primary_color
        
        if fill_area:
            ax.fill_between(x_vals, y_vals, color=line_color, alpha=0.08, zorder=1)

        if markersize:
            markersize = 0 if len(x_vals) > 25 else 4.5

        if (np.any(y_errs != 0) or np.any(x_errs != 0)) and len(x_vals) <= 25:
            ax.errorbar(x_vals, y_vals, yerr=y_errs if np.any(y_errs!=0) else None, 
                        xerr=x_errs if np.any(x_errs!=0) else None, fmt='none', ecolor=self._error_color, 
                        elinewidth=1.2, capsize=3, zorder=2)

        ax.plot(x_vals, y_vals, color=line_color, linestyle=linestyle, linewidth=linewidth, 
                marker=marker, markersize=markersize, zorder=3, markeredgecolor='white', markeredgewidth=0.8, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: 
            self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def scatter(self, x: str, y: str, ax=None, figsize=(8, 4.5), color=None, s=45, alpha=1, 
                marker='o', fit=False, title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, x_errs, x_label = self._get_plot_series(x)
        y_vals, y_errs, y_label = self._get_plot_series(y)
        fig, ax = self._init_plot_figure(ax, figsize)

        scatter_color = color if color is not None else self._primary_color
        
        if s == 45 and len(x_vals) > 25:
            s = 15

        if (np.any(y_errs != 0) or np.any(x_errs != 0)) and len(x_vals) <= 25:
            ax.errorbar(x_vals, y_vals, yerr=y_errs if np.any(y_errs!=0) else None, 
                        xerr=x_errs if np.any(x_errs!=0) else None, fmt='none', ecolor=self._error_color, 
                        elinewidth=1.2, capsize=3, zorder=2)

        ax.scatter(x_vals, y_vals, color=scatter_color, s=s, alpha=alpha, marker=marker, zorder=3, **kwargs)

        if fit and len(x_vals) > 1:
            m, b = np.polyfit(x_vals, y_vals, 1)
            y_fit = m * x_vals + b
            ax.plot(x_vals, y_fit, color=self._secondary_color, linestyle='-', linewidth=1.8, 
                    zorder=4, label=f'Fit: $y = {m:.3g}x + {b:.3g}$')
            ax.legend(frameon=True, facecolor=self._figure_facecolor, edgecolor='none', fontsize=9)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def errorbar(self, x: str, y: str, yerr: str = None, xerr: str = None, ax=None, figsize=(8, 4.5), 
                 color=None, ecolor=None, capsize=4, title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, internal_xerr, x_label = self._get_plot_series(x)
        y_vals, internal_yerr, y_label = self._get_plot_series(y)
        
        yerr_vals = self._get_plot_series(yerr)[0] if yerr else (internal_yerr if np.any(internal_yerr!=0) else None)
        xerr_vals = self._get_plot_series(xerr)[0] if xerr else (internal_xerr if np.any(internal_xerr!=0) else None)

        fig, ax = self._init_plot_figure(ax, figsize)
        main_color = color if color is not None else self._primary_color
        err_color = ecolor if ecolor is not None else self._secondary_color

        actual_capsize = capsize if len(x_vals) <= 25 else 0
        actual_elinewidth = 1.5 if len(x_vals) <= 25 else 0.8

        ax.errorbar(x_vals, y_vals, yerr=yerr_vals, xerr=xerr_vals, fmt='o', color=main_color, 
                    ecolor=err_color, elinewidth=actual_elinewidth, capsize=actual_capsize, capthick=actual_elinewidth, zorder=3, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def bar(self, x: str, y: str, ax=None, figsize=(8, 4.5), color=None, width=0.6, 
            title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, _, x_label = self._get_plot_series(x)
        y_vals, y_errs, y_label = self._get_plot_series(y)
        fig, ax = self._init_plot_figure(ax, figsize)

        bar_color = color if color is not None else self._primary_color
        
        if np.any(y_errs != 0) and len(x_vals) <= 25:
            ax.bar(x_vals, y_vals, yerr=y_errs, capsize=3, ecolor=self._secondary_color, color=bar_color, width=width, edgecolor='none', zorder=3, **kwargs)
        else:
            ax.bar(x_vals, y_vals, color=bar_color, width=width, edgecolor='none', zorder=3, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax, axis='y')

        fig.tight_layout()
        return fig, ax

    def hist(self, column: str, bins=12, ax=None, figsize=(8, 4.5), color=None, 
             title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        vals, _, label = self._get_plot_series(column)
        fig, ax = self._init_plot_figure(ax, figsize)

        hist_color = color if color is not None else self._primary_color
        ax.hist(vals, bins=bins, color=hist_color, alpha=0.85, edgecolor='white', linewidth=1.0, zorder=3, **kwargs)

        self._format_labels(ax, xlabel or label, ylabel or "Frequency", title)
        if grid: self._apply_grid(ax, axis='y')

        fig.tight_layout()
        return fig, ax

    def boxplot(self, columns: list = None, ax=None, figsize=(8, 4.5), title=None, ylabel=None, grid=True, **kwargs):
        num_cols = self._numeric_columns()
        cols_to_plot = columns or list(num_cols.keys())
        
        series_data = [self._get_plot_series(col) for col in cols_to_plot]
        data_to_plot = [s[0] for s in series_data]
        labels_with_units = [s[2] for s in series_data]
        
        fig, ax = self._init_plot_figure(ax, figsize)
        bp = ax.boxplot(data_to_plot, patch_artist=True, zorder=3, **kwargs)

        for patch in bp['boxes']:
            patch.set_facecolor(self._primary_color)
            patch.set_alpha(0.7)
            patch.set_edgecolor(self._primary_color)
            patch.set_linewidth(1.2)

        for element in ['whiskers', 'caps']:
            plt.setp(bp[element], color='#666666', linewidth=1.2)

        plt.setp(bp['medians'], color=self._secondary_color, linewidth=2.0)
        plt.setp(bp['fliers'], marker='o', color=self._secondary_color, alpha=0.6, markersize=4)

        ax.set_xticklabels(labels_with_units, fontsize=10, fontweight='bold')
        self._format_labels(ax, "", ylabel or "Value", title)
        if grid: self._apply_grid(ax, axis='y')

        fig.tight_layout()
        return fig, ax

    def violin(self, columns: list = None, ax=None, figsize=(8, 4.5), title=None, ylabel=None, grid=True, **kwargs):
        num_cols = self._numeric_columns()
        cols_to_plot = columns or list(num_cols.keys())
        
        series_data = [self._get_plot_series(col) for col in cols_to_plot]
        data_to_plot = [s[0] for s in series_data]
        labels_with_units = [s[2] for s in series_data]
        
        fig, ax = self._init_plot_figure(ax, figsize)
        vp = ax.violinplot(data_to_plot, showmedians=True, showextrema=True, **kwargs)

        for pc in vp['bodies']:
            pc.set_facecolor(self._primary_color)
            pc.set_alpha(0.6)
            pc.set_edgecolor(self._primary_color)

        for partname in ('cbars', 'cmins', 'cmaxes'):
            vp[partname].set_edgecolor('#666666')
            vp[partname].set_linewidth(1.0)

        vp['cmedians'].set_edgecolor(self._secondary_color)
        vp['cmedians'].set_linewidth(2.0)

        ax.set_xticks(np.arange(1, len(cols_to_plot) + 1))
        ax.set_xticklabels(labels_with_units, fontsize=10, fontweight='bold')
        self._format_labels(ax, "", ylabel or "Value", title)
        if grid: self._apply_grid(ax, axis='y')

        fig.tight_layout()
        return fig, ax

    def residual_plot(self, x: str, y: str, ax=None, figsize=(8, 4.5), title="Residual Plot", grid=True, **kwargs):
        x_vals, _, x_label = self._get_plot_series(x)
        y_vals, _, y_label = self._get_plot_series(y)
        
        m, b = np.polyfit(x_vals, y_vals, 1)
        y_pred = m * x_vals + b
        residuals = y_vals - y_pred

        fig, ax = self._init_plot_figure(ax, figsize)
        ax.axhline(0, color=self._secondary_color, linestyle='--', linewidth=1.5, zorder=2)
        
        scatter_s = 45 if len(x_vals) <= 25 else 15
        ax.scatter(x_vals, residuals, color=self._primary_color, s=scatter_s, zorder=3, **kwargs)

        self._format_labels(ax, x_label, f"Residuals ({y_label})", title)
        if grid: self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def pairplot(self, columns: list = None, figsize=(9, 9)):
        num_cols = self._numeric_columns()
        cols = columns or list(num_cols.keys())
        n = len(cols)

        fig, axes = plt.subplots(n, n, figsize=figsize, dpi=180)
        fig.patch.set_facecolor(self._figure_facecolor)

        for i in range(n):
            for j in range(n):
                ax = axes[i, j] if n > 1 else axes
                ax.set_facecolor(self._facecolor)

                if i == j:
                    vals, _, _ = self._get_plot_series(cols[i])
                    ax.hist(vals, color=self._primary_color, alpha=0.85, edgecolor='white')
                else:
                    x_vals, _, _ = self._get_plot_series(cols[j])
                    y_vals, _, _ = self._get_plot_series(cols[i])
                    point_s = 20 if len(x_vals) <= 25 else 8
                    ax.scatter(x_vals, y_vals, color=self._primary_color, s=point_s, alpha=0.7, edgecolors='none')

                for spine in ax.spines.values():
                    spine.set_color('#d0d0d0')

                if i == n - 1:
                    _, _, x_lbl = self._get_plot_series(cols[j])
                    ax.set_xlabel(x_lbl, fontsize=9, fontweight='bold')
                else:
                    ax.set_xticklabels([])

                if j == 0:
                    _, _, y_lbl = self._get_plot_series(cols[i])
                    ax.set_ylabel(y_lbl, fontsize=9, fontweight='bold')
                else:
                    ax.set_yticklabels([])

        fig.tight_layout()
        return fig, axes

    def corr_heatmap(self, ax=None, figsize=(7, 6), title="Correlation Matrix", cmap=None, annot=True, fmt=".2f", **kwargs):
        corr_df = self.corr()
        fig, ax = self._init_plot_figure(ax, figsize)

        if cmap is None:
            cmap = LinearSegmentedColormap.from_list(
                "brand_corr", 
                [self._secondary_color, "#ffffff", self._primary_color]
            )

        cax = ax.imshow(corr_df.values, cmap=cmap, vmin=-1, vmax=1, aspect='auto', **kwargs)
        cbar = fig.colorbar(cax, ax=ax, fraction=0.046, pad=0.04)
        cbar.ax.tick_params(labelsize=9, colors='#555555')
        cbar.outline.set_edgecolor('#d0d0d0')

        columns = list(corr_df.columns)
        ax.set_xticks(np.arange(len(columns)))
        ax.set_yticks(np.arange(len(columns)))
        ax.set_xticklabels(columns, rotation=45, ha='right', fontsize=10, fontweight='bold')
        ax.set_yticklabels(columns, fontsize=10, fontweight='bold')

        if annot:
            for i in range(len(columns)):
                for j in range(len(columns)):
                    val = corr_df.values[i, j]
                    text_color = "#ffffff" if abs(val) > 0.55 else self._text_color
                    ax.text(j, i, f"{val:{fmt}}", ha="center", va="center", color=text_color, fontsize=9, fontweight='bold')

        ax.grid(False)
        for spine in ax.spines.values():
            spine.set_visible(False)

        if title:
            ax.set_title(title, fontsize=13, fontweight='bold', color=self._text_color, pad=15, loc='left')

        fig.tight_layout()
        return fig, ax

    # ------------------------------------------------------------------
    # Helpers for phase_space / vector_field / fit_plot
    # ------------------------------------------------------------------

    @staticmethod
    def _convex_hull(points):
        """Andrew's monotone chain. Returns the hull vertices in counter-clockwise order."""
        pts = np.unique(np.asarray(points, dtype=float), axis=0).tolist()
        if len(pts) <= 2:
            return np.asarray(pts, dtype=float)

        def cross(o, a, b):
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

        lower = []
        for q in pts:
            while len(lower) >= 2 and cross(lower[-2], lower[-1], q) <= 0:
                lower.pop()
            lower.append(q)
        upper = []
        for q in reversed(pts):
            while len(upper) >= 2 and cross(upper[-2], upper[-1], q) <= 0:
                upper.pop()
            upper.append(q)
        return np.asarray(lower[:-1] + upper[:-1], dtype=float)

    @classmethod
    def _error_ribbon_path(cls, xv, yv, ex, ey, n_arc=32):
        """Builds the exact region swept by the error ellipses (semi-axes ex, ey, in data units)
        centred on every point of the trajectory.

        For each pair of consecutive points the region is the convex hull of both ellipses
        (Minkowski sum of the segment with the ellipse). All the pieces are put in a single
        compound path, so the union is filled only once (no darker overlaps with alpha).
        """
        from matplotlib.path import Path

        n_arc = int(max(8, 4 * round(n_arc / 4)))  # multiple of 4 -> axis extremes are hit exactly
        th = np.linspace(0.0, 2.0 * np.pi, n_arc, endpoint=False)
        cos_t, sin_t = np.cos(th), np.sin(th)
        ell = np.stack([xv[:, None] + ex[:, None] * cos_t,
                        yv[:, None] + ey[:, None] * sin_t], axis=-1)   # (n, n_arc, 2)

        n = len(xv)
        pairs = [(i, i + 1) for i in range(n - 1)] if n > 1 else [(0, 0)]

        verts, codes = [], []
        for i, j in pairs:
            hull = cls._convex_hull(np.vstack([ell[i], ell[j]]))
            if len(hull) < 3:
                continue
            k = len(hull)
            verts.append(np.vstack([hull, hull[:1]]))
            codes.append(np.array([Path.MOVETO] + [Path.LINETO] * (k - 1) + [Path.CLOSEPOLY]))

        if not verts:
            return None
        return Path(np.vstack(verts), np.concatenate(codes))

    @staticmethod
    def _min_pair_ratio(px, py, r, eps=1e-9, chunk=512):
        """min over pairs (i, j) of d_ij / (r_i + r_j), with d_ij in inches. Used to size the arrows
        so they cannot overlap. Coincident points (d ~ 0) are ignored: overlap there is unavoidable."""
        best = np.inf
        n = len(px)
        for s in range(0, n, chunk):
            e = min(s + chunk, n)
            d = np.hypot(px[s:e, None] - px[None, :], py[s:e, None] - py[None, :])
            w = r[s:e, None] + r[None, :]
            ok = (d > eps) & (w > 0)
            if ok.any():
                best = min(best, float((d[ok] / w[ok]).min()))
        return best

    @staticmethod
    def _median_nn_distance(px, py, chunk=512):
        """Median distance from each point to its nearest neighbour (ignores coincident points)."""
        n = len(px)
        if n < 2:
            return np.inf
        nn = np.full(n, np.inf)
        for s in range(0, n, chunk):
            e = min(s + chunk, n)
            d = np.hypot(px[s:e, None] - px[None, :], py[s:e, None] - py[None, :])
            d[d < 1e-9] = np.inf
            nn[s:e] = d.min(axis=1)
        nn = nn[np.isfinite(nn)]
        return float(np.median(nn)) if len(nn) else np.inf

    @staticmethod
    def _max_free_length(px, py, r, theta, cap, sep, pivot, tol=0.0, max_pairs=2_000_000, iters=16):
        """Largest k in [0, cap] such that the arrows (segments of length k*r_i starting at the point
        (px, py) along ``theta``, according to ``pivot``) stay at least ``sep`` apart.
        All units are inches. Pairs of points closer than ``sep`` are ignored (overlap unavoidable) and
        up to a fraction ``tol`` of the arrows may touch another one (best effort for irregular clouds).
        Returns None if there are too many candidate pairs (caller falls back to a cheaper bound)."""
        n = len(px)
        o0, o1 = {'middle': (-0.5, 0.5), 'mid': (-0.5, 0.5), 'tail': (0.0, 1.0), 'tip': (-1.0, 0.0)}[pivot]
        reach = max(abs(o0), abs(o1))

        # Candidate pairs: only those that could touch for some k <= cap
        I, J, D, Wt, total = [], [], [], [], 0
        for s in range(0, n, 512):
            e = min(s + 512, n)
            d = np.hypot(px[s:e, None] - px[None, :], py[s:e, None] - py[None, :])
            w = r[s:e, None] + r[None, :]
            ii, jj = np.nonzero((d >= sep) & (w > 0) & (d <= cap * reach * 2 * w + sep))
            keep = jj > ii + s
            ii, jj = ii[keep], jj[keep]
            D.append(d[ii, jj])
            Wt.append(w[ii, jj])
            I.append(ii + s)
            J.append(jj)
            total += int(keep.sum())
            if total > max_pairs:
                return None
        if total == 0:
            return cap
        I, J, D, Wt = np.concatenate(I), np.concatenate(J), np.concatenate(D), np.concatenate(Wt)
        cx, cy = np.cos(theta), np.sin(theta)
        allowed = int(np.floor(tol * n))

        def pt_seg(qx, qy, ax_, ay_, bx, by):
            dx, dy = bx - ax_, by - ay_
            l2 = dx * dx + dy * dy
            t = np.clip(((qx - ax_) * dx + (qy - ay_) * dy) / np.where(l2 > 0, l2, 1.0), 0.0, 1.0)
            return np.hypot(qx - (ax_ + t * dx), qy - (ay_ + t * dy))

        def collides(k, I, J):
            L = k * r
            a0x, a0y = px + o0 * L * cx, py + o0 * L * cy
            a1x, a1y = px + o1 * L * cx, py + o1 * L * cy
            Ax0, Ay0, Ax1, Ay1 = a0x[I], a0y[I], a1x[I], a1y[I]
            Bx0, By0, Bx1, By1 = a0x[J], a0y[J], a1x[J], a1y[J]

            def cross(ox, oy, ax_, ay_, bx, by):
                return (ax_ - ox) * (by - oy) - (ay_ - oy) * (bx - ox)

            d1 = cross(Bx0, By0, Bx1, By1, Ax0, Ay0)
            d2 = cross(Bx0, By0, Bx1, By1, Ax1, Ay1)
            d3 = cross(Ax0, Ay0, Ax1, Ay1, Bx0, By0)
            d4 = cross(Ax0, Ay0, Ax1, Ay1, Bx1, By1)
            dist = np.minimum.reduce([
                pt_seg(Ax0, Ay0, Bx0, By0, Bx1, By1), pt_seg(Ax1, Ay1, Bx0, By0, Bx1, By1),
                pt_seg(Bx0, By0, Ax0, Ay0, Ax1, Ay1), pt_seg(Bx1, By1, Ax0, Ay0, Ax1, Ay1)])
            bad = ((d1 * d2 < 0) & (d3 * d4 < 0)) | (dist < sep)
            if not bad.any():
                return False
            return np.unique(np.concatenate([I[bad], J[bad]])).size > allowed

        if not collides(cap, I, J):
            return cap
        lo, hi = 0.0, cap
        for _ in range(iters):
            mid = 0.5 * (lo + hi)
            if collides(mid, I, J):
                hi = mid
                # pairs that cannot touch for k <= hi never will for smaller k: drop them
                live = D <= hi * reach * 2 * Wt + sep
                I, J, D, Wt = I[live], J[live], D[live], Wt[live]
                if len(I) == 0:
                    return hi
            else:
                lo = mid
        return lo

    @staticmethod
    def _fmt_value_err(val, err):
        """Formats value ± error using 1-2 significant figures for the error."""
        if not np.isfinite(err) or err <= 0:
            return f"{val:.4g}"
        if abs(val) >= 1e5 or (val != 0 and abs(val) < 1e-3) or err < 1e-6:
            return f"({val:.3e} ± {err:.1e})"
        e = int(np.floor(np.log10(err)))
        lead = int(err / 10 ** e)
        sig = 2 if lead < 3 else 1
        decimals = max(0, sig - 1 - e)
        return f"{val:.{decimals}f} ± {err:.{decimals}f}"

    # ==========================================
    # NEW CHART TYPES
    # ==========================================

    def phase_space(self, x: str, p: str, ax=None, figsize=(8, 4.5), color=None, linestyle='-', linewidth=2.2,
                    show_errors=True, error_alpha=0.22, error_scale=1.0, marker='o', markersize=None,
                    title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        """Plots a phase space trajectory (e.g., position vs momentum) preserving trajectory order.

        If ``show_errors`` is True and the columns carry uncertainties, the trajectory is surrounded
        by a halo of the same colour as the line (just fainter, see ``error_alpha``). The halo is drawn
        in data coordinates: around every point it spans exactly ±error in x and ±error in p, so it
        widens and narrows following the error of each point. ``error_scale`` multiplies the errors
        (e.g. 2 to show a 2σ halo).
        """
        from matplotlib.patches import PathPatch

        x_vals, x_errs, x_label = self._get_plot_series(x)
        p_vals, p_errs, p_label = self._get_plot_series(p)

        xv = np.asarray(x_vals, dtype=float)
        pv = np.asarray(p_vals, dtype=float)
        ex = np.abs(np.asarray(x_errs, dtype=float)) * error_scale
        ep = np.abs(np.asarray(p_errs, dtype=float)) * error_scale

        fig, ax = self._init_plot_figure(ax, figsize)
        line_color = color if color is not None else self._primary_color

        if show_errors and (np.any(ex != 0) or np.any(ep != 0)):
            finite = np.isfinite(xv) & np.isfinite(pv) & np.isfinite(ex) & np.isfinite(ep)
            path = self._error_ribbon_path(xv[finite], pv[finite], ex[finite], ep[finite])
            if path is not None:
                ax.add_patch(PathPatch(path, facecolor=line_color, edgecolor='none',
                                       alpha=error_alpha, zorder=1))

        ax.plot(xv, pv, color=line_color, linestyle=linestyle, linewidth=linewidth,
                marker=marker, markersize=markersize if markersize is not None else (3 if len(xv) <= 50 else 0),
                zorder=2, markeredgecolor='white', markeredgewidth=0.5, **kwargs)
        ax.autoscale_view()

        self._format_labels(ax, xlabel or x_label, ylabel or p_label, title)
        if grid:
            self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def vector_field(self, x: str, y: str, u: str, v: str, ax=None, figsize=(8, 4.5), scale=None,
                     angles='uv', pivot='middle', color=None, color_by_magnitude=False, cmap=None,
                     max_length=0.12, gap=0.85, overlap_tolerance=0.05, title=None, xlabel=None, ylabel=None, grid=True,
                     **kwargs):
        """Plots a 2D vector field from position columns (x, y) and vector component columns (u, v).

        The arrows are sized automatically so that they do not overlap:

        * ``scale=None``: lengths are proportional to the magnitude of each vector; the longest one is
          as long as possible without touching its neighbours.
        * ``scale=s``: ALL arrows have the same length (same modulus). ``s`` is a fraction of the longest
          length that avoids overlap: ``s=1`` -> as long as possible without touching, ``s=0.5`` -> half
          of that. Values above 1 may overlap. (Note: this is NOT matplotlib's quiver ``scale``.)

        Parameters
        ----------
        angles : {'uv', 'xy'}
            'uv': the arrow direction is atan2(v, u) on screen (robust when x/y and u/v have different
            units or scales). 'xy': the direction follows the data axes (u in x units, v in y units).
        max_length : float
            Upper bound of the arrow length, as a fraction of the axes width (avoids giant arrows when
            there are few points).
        gap : float
            Fraction (<= 1) of the maximum overlap-free length that is actually used.
        overlap_tolerance : float
            Fraction of arrows (0-1) that may touch another one. 0 = strictly no overlaps (can force tiny
            arrows in irregular point clouds with a few very close points); the default 0.05 ignores
            the few worst-placed points (default 5%) so the rest can be drawn at a useful size.
        color_by_magnitude : bool
            Colours the arrows by |(u, v)| and adds a colorbar (useful when ``scale`` equalises lengths).
        """
        kwargs.pop('scale_units', None)  # legacy argument: the length is now handled internally
        if angles not in ('uv', 'xy'):
            raise ValueError("angles must be 'uv' or 'xy'.")

        x_vals, _, x_label = self._get_plot_series(x)
        y_vals, _, y_label = self._get_plot_series(y)
        u_vals, _, u_label = self._get_plot_series(u)
        v_vals, _, v_label = self._get_plot_series(v)

        xv, yv, uv, vv = (np.asarray(a, dtype=float) for a in (x_vals, y_vals, u_vals, v_vals))
        finite = np.isfinite(xv) & np.isfinite(yv) & np.isfinite(uv) & np.isfinite(vv)
        xv, yv, uv, vv = xv[finite], yv[finite], uv[finite], vv[finite]
        if len(xv) == 0:
            raise ValueError("vector_field: there are no finite (x, y, u, v) points to plot.")

        own_axes = ax is None
        fig, ax = self._init_plot_figure(ax, figsize)
        vec_color = color if color is not None else self._primary_color
        mag_phys = np.hypot(uv, vv)

        # Colorbar first, so the axes size is final before sizing the arrows
        norm = None
        if color_by_magnitude:
            from matplotlib.colors import Normalize
            from matplotlib.cm import ScalarMappable
            if cmap is None:
                cmap = LinearSegmentedColormap.from_list("brand_field", [self._secondary_color, self._primary_color])
            vmin, vmax = float(mag_phys.min()), float(mag_phys.max())
            norm = Normalize(vmin=vmin, vmax=vmax if vmax > vmin else vmin + 1.0)
            cbar = fig.colorbar(ScalarMappable(norm=norm, cmap=cmap), ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label(f"|({u_label}, {v_label})|", fontsize=10, color=self._text_color)
            cbar.ax.tick_params(labelsize=9, colors='#555555')
            cbar.outline.set_edgecolor('#d0d0d0')

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid:
            self._apply_grid(ax)
        fig.tight_layout()

        # Axes size in inches
        pos = ax.get_position()
        fig_w, fig_h = fig.get_size_inches()
        W, H = pos.width * fig_w, pos.height * fig_h

        factor = 1.0 if scale is None else float(scale)
        is_mid = pivot in ('middle', 'mid')
        reach = max_length * max(factor, 1.0) * (0.5 if is_mid else 1.0)  # how far arrows stick out of a point

        def _span(a):
            r = float(np.ptp(a))
            return r if r > 0 else max(abs(float(a[0])) * 0.1, 1.0)

        # Axis limits leave room for the arrows
        if own_axes:
            pad_x = min(reach + 0.04, 0.3)
            pad_y = min(reach * W / H + 0.04, 0.3)
            rx, ry = _span(xv), _span(yv)
            ax.set_xlim(xv.min() - pad_x / (1 - 2 * pad_x) * rx, xv.max() + pad_x / (1 - 2 * pad_x) * rx)
            ax.set_ylim(yv.min() - pad_y / (1 - 2 * pad_y) * ry, yv.max() + pad_y / (1 - 2 * pad_y) * ry)
        else:
            ax.update_datalim(np.column_stack([xv, yv]))
            ax.autoscale_view()

        xlo, xhi = ax.get_xlim()
        ylo, yhi = ax.get_ylim()
        sx, sy = W / abs(xhi - xlo), H / abs(yhi - ylo)          # inches per data unit
        px, py = (xv - xlo) * sx, (yv - ylo) * sy                # positions on screen (inches)

        # Direction and relative length on screen
        if angles == 'xy':
            dx, dy = uv * sx, vv * sy
        else:
            dx, dy = uv, vv
        mag = np.hypot(dx, dy)
        theta = np.arctan2(dy, dx)

        if scale is None:
            r = mag / mag.max() if mag.max() > 0 else np.zeros_like(mag)
        else:
            r = (mag > 0).astype(float)   # same modulus; null vectors are not drawn

        # Longest common factor k such that no pair of arrows touches (exact segment test);
        # for huge fields it falls back to a cheaper, more conservative bound.
        cap = max_length * W
        sep = min(0.015 * W, 0.1 * self._median_nn_distance(px, py))   # min. clearance (~ arrow head)
        free = self._max_free_length(px, py, r, theta, cap, sep, 'middle' if is_mid else pivot,
                                     tol=overlap_tolerance)
        if free is None:
            ratio = self._min_pair_ratio(px, py, r)
            free = cap if not np.isfinite(ratio) else min((2.0 if is_mid else 1.0) * ratio, cap)
        base = min(free * gap, cap)
        lengths = factor * base * r                              # inches

        U = lengths / W * np.cos(theta)
        V = lengths / W * np.sin(theta)

        qkw = dict(angles='uv', scale_units='width', scale=1, pivot=pivot, zorder=3)
        qkw.update(kwargs)
        sel = lengths > 0                                        # null vectors are not drawn (no stray dots)
        if sel.any():
            if color_by_magnitude:
                ax.quiver(xv[sel], yv[sel], U[sel], V[sel], mag_phys[sel], cmap=cmap, norm=norm, **qkw)
            else:
                ax.quiver(xv[sel], yv[sel], U[sel], V[sel], color=vec_color, **qkw)

        fig.tight_layout()
        return fig, ax

    def fit_plot(self, x: str, y: str, degree: int = 1, model=None, p0=None, param_names=None, ax=None,
                 figsize=(8, 6), color=None, fit_color=None, residuals=True, band=True, show_stats=True,
                 use_x_errors=True, n_sigma=1.0, return_fit=False, title=None, xlabel=None, ylabel=None,
                 grid=True, **kwargs):
        """Fit (polynomial or custom model) with confidence band, parameter uncertainties and residuals.

        * Data points are drawn with their error bars; the fit is weighted by the uncertainty of y
          (and, if ``use_x_errors``, by the effective variance σ_y² + (f'(x)·σ_x)²).
        * ``degree`` sets the polynomial degree (1 = straight line). Alternatively pass
          ``model=f(x, *params)`` (needs scipy) and optionally ``p0``.
        * The shaded band is the ``n_sigma`` uncertainty of the fitted curve (from the covariance matrix).
        * The bottom panel shows the residuals, normalised by σ when there are errors (the ±1 zone is
          shaded), together with χ²_red and R² in the text box.
        * With ``return_fit=True`` it also returns a dict with params, errors, covariance, chi2, chi2_red, dof, r2.
        """
        from mpl_toolkits.axes_grid1 import make_axes_locatable

        x_vals, x_errs, x_label = self._get_plot_series(x)
        y_vals, y_errs, y_label = self._get_plot_series(y)
        xv, yv = np.asarray(x_vals, dtype=float), np.asarray(y_vals, dtype=float)
        ex, ey = np.abs(np.asarray(x_errs, dtype=float)), np.abs(np.asarray(y_errs, dtype=float))

        ok = np.isfinite(xv) & np.isfinite(yv)
        xv, yv, ex, ey = xv[ok], yv[ok], ex[ok], ey[ok]

        has_y_err = bool(np.any(ey > 0))
        has_x_err = bool(np.any(ex > 0))
        if has_y_err:
            sig_y = np.where(ey > 0, ey, ey[ey > 0].min())   # points without error get the smallest one
        else:
            sig_y = np.ones_like(yv)
        absolute = has_y_err

        if model is None:
            npar = int(degree) + 1

            def model_fn(xx, *c):
                return np.polynomial.polynomial.polyval(xx, c)

            def jac_fn(xx, popt):
                return np.vander(xx, npar, increasing=True)

            default_names = [f"c{k}" for k in range(npar)]
        else:
            from scipy.optimize import curve_fit
            if p0 is None:
                raise ValueError("fit_plot: with a custom model you must provide p0 (initial parameters).")
            npar = len(p0)
            model_fn = model

            def jac_fn(xx, popt):
                J = np.empty((len(xx), npar))
                for k in range(npar):
                    h = 1e-6 * max(abs(popt[k]), 1e-3)
                    pp, pm = np.array(popt, float), np.array(popt, float)
                    pp[k] += h
                    pm[k] -= h
                    J[:, k] = (model_fn(xx, *pp) - model_fn(xx, *pm)) / (2 * h)
                return J

            default_names = [f"p{k}" for k in range(npar)]

        names = list(param_names) if param_names is not None else default_names

        def do_fit(sig):
            if model is None:
                A = np.vander(xv, npar, increasing=True) / sig[:, None]
                popt, *_ = np.linalg.lstsq(A, yv / sig, rcond=None)
                pcov = np.linalg.pinv(A.T @ A)
                if not absolute:
                    dof_ = len(xv) - npar
                    if dof_ > 0:
                        pcov = pcov * (np.sum(((yv - model_fn(xv, *popt)) / sig) ** 2) / dof_)
            else:
                popt, pcov = curve_fit(model_fn, xv, yv, p0=p0, sigma=sig if has_y_err else None,
                                       absolute_sigma=absolute, maxfev=20000)
            return np.asarray(popt, float), np.asarray(pcov, float)

        use_eff = use_x_errors and has_x_err
        sig = sig_y.copy()
        for _ in range(6 if use_eff else 1):
            popt, pcov = do_fit(sig)
            if not use_eff:
                break
            h = 1e-6 * max(float(np.ptp(xv)), 1e-12)
            slope = (model_fn(xv + h, *popt) - model_fn(xv - h, *popt)) / (2 * h)
            sig = np.sqrt(sig_y ** 2 + (slope * ex) ** 2)

        y_fit_pts = model_fn(xv, *popt)
        resid = yv - y_fit_pts
        dof = len(xv) - npar
        chi2 = float(np.sum((resid / sig) ** 2))
        chi2_red = chi2 / dof if dof > 0 else np.nan
        ss_tot = float(np.sum((yv - yv.mean()) ** 2))
        r2 = 1.0 - float(np.sum(resid ** 2)) / ss_tot if ss_tot > 0 else np.nan
        perr = np.sqrt(np.clip(np.diag(pcov), 0, None))

        # ----- figure -----
        fig, ax = self._init_plot_figure(ax, figsize)
        main_color = color if color is not None else self._primary_color
        line_color = fit_color if fit_color is not None else self._secondary_color

        ax_res = None
        if residuals:
            divider = make_axes_locatable(ax)
            ax_res = divider.append_axes("bottom", size="28%", pad=0.12, sharex=ax)
            self._init_plot_figure(ax_res, None)

        pad = 0.04 * (float(np.ptp(xv)) or 1.0)
        xs = np.linspace(xv.min() - pad, xv.max() + pad, 400)
        ys = model_fn(xs, *popt)

        if band:
            J = jac_fn(xs, popt)
            var = np.einsum('ij,jk,ik->i', J, pcov, J)
            dy = n_sigma * np.sqrt(np.clip(var, 0, None))
            ax.fill_between(xs, ys - dy, ys + dy, color=line_color, alpha=0.18, linewidth=0, zorder=1)

        ax.plot(xs, ys, color=line_color, linewidth=2.0, zorder=3)
        n_pts = len(xv)
        if has_x_err or has_y_err:
            ax.errorbar(xv, yv, yerr=ey if has_y_err else None, xerr=ex if has_x_err else None, fmt='o',
                        color=main_color, ecolor=self._error_color, elinewidth=1.2,
                        capsize=3 if n_pts <= 25 else 0, markersize=4.5 if n_pts <= 25 else 3,
                        markeredgecolor='white', markeredgewidth=0.6, zorder=4, **kwargs)
        else:
            ax.scatter(xv, yv, color=main_color, s=45 if n_pts <= 25 else 15, edgecolors='white',
                       linewidths=0.6, zorder=4, **kwargs)

        if show_stats:
            lines = [f"{nm} = {self._fmt_value_err(val, err)}" for nm, val, err in zip(names, popt, perr)]
            lines.append(rf"$\chi^2_{{red}}$ = {chi2_red:.3g}  (dof = {dof})" if dof > 0 else "dof = 0")
            lines.append(f"$R^2$ = {r2:.5f}" if np.isfinite(r2) else "")
            ax.text(0.02, 0.97, "\n".join(l for l in lines if l), transform=ax.transAxes, va='top', ha='left',
                    fontsize=8.5, color=self._text_color, zorder=5,
                    bbox=dict(boxstyle='round,pad=0.4', facecolor=self._figure_facecolor,
                              edgecolor='#d0d0d0', alpha=0.9))

        if residuals:
            if has_y_err or use_eff:
                res_plot = resid / sig
                res_label = "Residuals (σ)"
                ax_res.axhspan(-1, 1, color=line_color, alpha=0.10, linewidth=0, zorder=1)
            else:
                res_plot = resid
                res_label = f"Residuals ({y_label})"
            ax_res.axhline(0, color=line_color, linestyle='--', linewidth=1.3, zorder=2)
            ax_res.scatter(xv, res_plot, color=main_color, s=35 if n_pts <= 25 else 12, edgecolors='white',
                           linewidths=0.5, zorder=3)
            ax.tick_params(labelbottom=False)
            self._format_labels(ax, "", ylabel or y_label, title)
            self._format_labels(ax_res, xlabel or x_label, res_label, None)
            if grid:
                self._apply_grid(ax)
                self._apply_grid(ax_res)
        else:
            self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
            if grid:
                self._apply_grid(ax)

        fig.tight_layout()
        axes_out = (ax, ax_res) if residuals else ax

        if return_fit:
            fit = dict(names=names, params=popt, errors=perr, covariance=pcov, chi2=chi2,
                       chi2_red=chi2_red, dof=dof, r2=r2)
            return fig, axes_out, fit
        return fig, axes_out

    def scatter_3d(self, x: str, y: str, z: str, ax=None, figsize=(8, 6), color=None, s=30, alpha=1, 
                   marker='o', title=None, xlabel=None, ylabel=None, zlabel=None, grid=True, **kwargs):
        """Plots a 3D scatter plot from Data columns."""
        x_vals, _, x_label = self._get_plot_series(x)
        y_vals, _, y_label = self._get_plot_series(y)
        z_vals, _, z_label = self._get_plot_series(z)

        if ax is None:
            fig = plt.figure(figsize=figsize, dpi=200)
            fig.patch.set_facecolor(self._figure_facecolor)
            ax = fig.add_subplot(projection='3d')
        else:
            fig = ax.get_figure()

        ax.set_facecolor(self._facecolor)
        scatter_color = color if color is not None else self._primary_color

        sc = ax.scatter(x_vals, y_vals, z_vals, color=scatter_color, s=s, alpha=alpha, marker=marker, **kwargs)

        ax.set_xlabel(xlabel or x_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)
        ax.set_ylabel(ylabel or y_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)
        ax.set_zlabel(zlabel or z_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)

        if title:
            ax.set_title(title, fontsize=12, fontweight='bold', color=self._text_color, pad=15)

        fig.tight_layout()
        return fig, ax

    def surface_3d(self, x: str, y: str, z: str, ax=None, figsize=(8, 6), cmap=None, edgecolor='none', 
                   alpha=1, title=None, xlabel=None, ylabel=None, zlabel=None, grid=True, **kwargs):
        """Plots a 3D surface plot using triangulated surface (plot_trisurf) for 1D Data columns."""
        x_vals, _, x_label = self._get_plot_series(x)
        y_vals, _, y_label = self._get_plot_series(y)
        z_vals, _, z_label = self._get_plot_series(z)

        if ax is None:
            fig = plt.figure(figsize=figsize, dpi=200)
            fig.patch.set_facecolor(self._figure_facecolor)
            ax = fig.add_subplot(projection='3d')
        else:
            fig = ax.get_figure()

        ax.set_facecolor(self._facecolor)

        if cmap is None:
            cmap = LinearSegmentedColormap.from_list(
                "brand_surface", 
                [self._secondary_color, self._primary_color]
            )

        surf = ax.plot_trisurf(x_vals, y_vals, z_vals, cmap=cmap, edgecolor=edgecolor, alpha=alpha, **kwargs)

        ax.set_xlabel(xlabel or x_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)
        ax.set_ylabel(ylabel or y_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)
        ax.set_zlabel(zlabel or z_label, fontsize=10, fontweight='bold', color=self._text_color, labelpad=10)

        if title:
            ax.set_title(title, fontsize=12, fontweight='bold', color=self._text_color, pad=15)

        fig.tight_layout()
        return fig, ax

    # ------------------------------------------------------------------
    # Polar (circular) chart
    # ------------------------------------------------------------------

    def _get_polar_angles(self, col_name: str, degrees=None):
        """Returns (theta in radians, error in radians, show_degrees, label) for a column.

        * Quantity with ANGULAR dimension: converted to radians; the ticks are shown in degrees
          if its unit is not the radian.
        * Plain numbers (or any other Quantity): if ``degrees`` is None they are assumed to be
          degrees when some |value| exceeds 2*pi, radians otherwise.
        """
        if col_name not in self.dict:
            raise KeyError(f"Column '{col_name}' not found in Data.")

        col = self.dict[col_name]
        if isinstance(col, Quantity):
            q = _scheme_view(col)
            label = f"{col_name} [{q.unit.symbol}]"
            if q.unit.dimension == ANGULAR:
                q_rad = q.convert_to(RADIAN)
                show_deg = (not np.isclose(q.unit.factor, 1.0)) if degrees is None else bool(degrees)
                return (np.asarray(q_rad.value, dtype=float), np.asarray(q_rad.error, dtype=float),
                        show_deg, label)
            vals = np.asarray(q.value, dtype=float)
            errs = np.asarray(q.error, dtype=float)
        else:
            vals = np.asarray(col, dtype=float)
            errs = np.zeros_like(vals)
            label = col_name

        finite = vals[np.isfinite(vals)]
        if degrees is None:
            degrees = bool(finite.size and np.max(np.abs(finite)) > 2 * np.pi * 1.0001)
        if degrees:
            vals, errs = np.deg2rad(vals), np.deg2rad(errs)
        return vals, errs, bool(degrees), label

    def polar_plot(self, theta: str, r: str = None, ax=None, figsize=(6, 6), color=None, kind='line',
                   linestyle='-', linewidth=2.2, marker='o', markersize=None, fill_area=False,
                   close=False, sort_theta=False, show_errors=True, degrees=None, bins=24,
                   zero_location='E', clockwise=False, rmin=None, rmax=None,
                   title=None, thetalabel=None, rlabel=None, grid=True, **kwargs):
        """Polar chart: like ``plot`` but the x axis (``theta``) is a circle and y (``r``) the radius.

        Angles are handled automatically:

        * If ``theta`` is a Quantity with angular dimension (rad, deg, ...) it is converted to radians
          internally and the circle is labelled in degrees (if its unit is not the radian) or in
          multiples of pi.
        * If ``theta`` is a plain column, it is assumed to be in degrees when some |value| > 2*pi and in
          radians otherwise. Force it with ``degrees=True/False``.
        * ``r=None`` draws an angular histogram (rose diagram) of ``theta`` with ``bins`` sectors.

        Parameters
        ----------
        kind : {'line', 'scatter', 'bar'}
            Line (trajectory order is kept unless ``sort_theta=True``), points, or radial bars.
        close : bool
            Joins the last point to the first one (closed curves). Only for ``kind='line'``.
        fill_area : bool
            Fills the area enclosed by the line (like ``plot``).
        show_errors : bool
            Draws the uncertainties of theta and r when present (<= 25 points, as in the other plots).
        zero_location : str
            Where theta = 0 sits: 'E' (default, mathematical convention), 'N', 'W', 'S', 'NE', ...
        clockwise : bool
            Increasing angles go clockwise (e.g. compass bearings: ``zero_location='N', clockwise=True``).
        rmin, rmax : float, optional
            Radial limits.
        """
        if kind not in ('line', 'scatter', 'bar'):
            raise ValueError("kind must be 'line', 'scatter' or 'bar'.")

        t_vals, t_errs, show_deg, t_label = self._get_polar_angles(theta, degrees)

        if r is None:
            rv, re_ = None, None
            r_label = "Frequency"
        else:
            r_vals, r_errs, r_label = self._get_plot_series(r)
            rv = np.asarray(r_vals, dtype=float)
            re_ = np.abs(np.asarray(r_errs, dtype=float))
            ok = np.isfinite(t_vals) & np.isfinite(rv)
            t_vals, t_errs, rv, re_ = t_vals[ok], t_errs[ok], rv[ok], re_[ok]
            if sort_theta:
                idx = np.argsort(t_vals)
                t_vals, t_errs, rv, re_ = t_vals[idx], t_errs[idx], rv[idx], re_[idx]
        t_errs = np.abs(t_errs)

        if ax is None:
            fig = plt.figure(figsize=figsize, dpi=200)
            ax = fig.add_subplot(projection='polar')
        else:
            fig = ax.get_figure()
            if getattr(ax, 'name', None) != 'polar':
                raise ValueError("polar_plot: the given ax must be a polar axes "
                                 "(fig.add_subplot(projection='polar')).")

        fig.patch.set_facecolor(self._figure_facecolor)
        ax.set_facecolor(self._facecolor)
        ax.spines['polar'].set_color('#d0d0d0')
        ax.spines['polar'].set_linewidth(1.0)
        ax.tick_params(colors='#555555', which='both', labelsize=10)
        ax.set_theta_zero_location(zero_location)
        ax.set_theta_direction(-1 if clockwise else 1)

        main_color = color if color is not None else self._primary_color
        n = len(t_vals)

        if r is None:
            counts, edges = np.histogram(np.mod(t_vals[np.isfinite(t_vals)], 2 * np.pi),
                                         bins=bins, range=(0, 2 * np.pi))
            centers = 0.5 * (edges[:-1] + edges[1:])
            ax.bar(centers, counts, width=2 * np.pi / bins, color=main_color, alpha=0.85,
                   edgecolor='white', linewidth=1.0, zorder=3, **kwargs)
        else:
            draw_errors = show_errors and n <= 25 and (np.any(re_ != 0) or np.any(t_errs != 0))

            if kind == 'line':
                lt, lr = (np.append(t_vals, t_vals[:1]), np.append(rv, rv[:1])) if (close and n > 1) \
                    else (t_vals, rv)
                if fill_area:
                    ax.fill(lt, lr, color=main_color, alpha=0.08, zorder=1)
                ax.plot(lt, lr, color=main_color, linestyle=linestyle, linewidth=linewidth, marker=marker,
                        markersize=markersize if markersize is not None else (4.5 if n <= 25 else 0),
                        zorder=3, markeredgecolor='white', markeredgewidth=0.8, **kwargs)
            elif kind == 'scatter':
                ax.scatter(t_vals, rv, color=main_color, s=45 if n <= 25 else 15, zorder=3, **kwargs)
            else:  # bar
                width = kwargs.pop('width', None)
                if width is None:
                    gaps = np.diff(np.unique(np.round(np.mod(t_vals, 2 * np.pi), 9)))
                    gaps = gaps[gaps > 1e-9]
                    width = min(0.9 * gaps.min(), 2 * np.pi) if gaps.size else 2 * np.pi / 24
                ax.bar(t_vals, rv, width=width, color=main_color, alpha=0.85, edgecolor='white',
                       linewidth=1.0, zorder=3, **kwargs)

            if draw_errors:
                ax.errorbar(t_vals, rv, yerr=re_ if np.any(re_ != 0) else None,
                            xerr=t_errs if np.any(t_errs != 0) else None, fmt='none',
                            ecolor=self._error_color, elinewidth=1.2, capsize=3, zorder=2)

        # Circle labels: degrees or multiples of pi
        if show_deg:
            ticks_deg = np.arange(0, 360, 45)
            ax.set_xticks(np.deg2rad(ticks_deg))
            ax.set_xticklabels([f"{int(d)}°" for d in ticks_deg])
        else:
            ax.set_xticks(np.arange(8) * np.pi / 4)
            ax.set_xticklabels(['0', 'π/4', 'π/2', '3π/4', 'π', '5π/4', '3π/2', '7π/4'])

        if rmin is not None or rmax is not None:
            ax.set_rlim(rmin, rmax)
        ax.set_rlabel_position(22.5)

        ax.set_xlabel(thetalabel or t_label, fontsize=11, fontweight='bold', color=self._text_color, labelpad=12)
        ax.set_ylabel(rlabel or r_label, fontsize=11, fontweight='bold', color=self._text_color, labelpad=28)
        if title:
            ax.set_title(title, fontsize=13, fontweight='bold', color=self._text_color, pad=20, loc='left')
        if grid:
            ax.grid(True, linestyle='--', alpha=0.45, color=self._grid_color, zorder=0)
        else:
            ax.grid(False)

        fig.tight_layout()
        return fig, ax

    def generate_report(self, output_path, format_type="html", **kwargs):
        from .report import generate_report
        # With an active unit scheme the report is built from a copy expressed in that scheme
        source = self.to_scheme() if get_scheme() is not None else self
        return generate_report(
            source, output_path=output_path, format_type=format_type, **kwargs
        )


class DataStatsResult:
    def __init__(self, stats_dict: dict):
        self.stats = stats_dict

    def __repr__(self):
        return "\n".join([f"  {k}: {v}" for k, v in self.stats.items()])

    def _repr_html_(self):
        data_formatted = {}
        for k, v in self.stats.items():
            if isinstance(v, Quantity):
                v = _scheme_view(v)
                if np.any(v.error != 0):
                    data_formatted[k] = f"({v.value} ± {v.error}) {v.unit.symbol}"
                else:
                    data_formatted[k] = f"{v.value} {v.unit.symbol}"
            else:
                data_formatted[k] = v
        df = pd.DataFrame([data_formatted], index=["value"])
        return df.T.rename(columns={0: "Statistic"})._repr_html_()


class DataDescribeResult:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __repr__(self):
        return str(self.df)

    def _repr_html_(self):
        return self.df._repr_html_()