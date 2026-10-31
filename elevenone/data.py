import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from .unit import Quantity, Unit

class Data:
    # =========================================================================
    # ULTRA-MODERN SCIENTIFIC BRAND IDENTITY & CONFIGURATION
    # =========================================================================
    _primary_color = "#00ccff"       # Primary Cyan (Main graphs, lines, bars, histograms, scatter)
    _secondary_color = "#ff2ad4"     # Secondary Magenta/Pink (Trendlines, fits, accents)
    _facecolor = "#fcfcfc"           # Soft off-white/grey axis background
    _figure_facecolor = "#ffffff"    # Clean pure white outer canvas
    _grid_color = "#ebebeb"          # Ultra-subtle grid lines
    _text_color = "#1a1a1a"          # Deep charcoal for high readability

    @classmethod
    def set_theme(cls, primary="#00ccff", secondary="#ff2ad4", facecolor="#fcfcfc", 
                  figure_facecolor="#ffffff", grid_color="#ebebeb", text_color="#1a1a1a"):
        """Updates the global brand identity theme for all plots."""
        cls._primary_color = primary
        cls._secondary_color = secondary
        cls._facecolor = facecolor
        cls._figure_facecolor = figure_facecolor
        cls._grid_color = grid_color
        cls._text_color = text_color
        cls._apply_global_rc_params()

    @classmethod
    def _apply_global_rc_params(cls):
        """Forces Matplotlib to drop its default look and adopt a modern design system."""
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
        """Permite acceder a una columna individual o crear un nuevo objeto Data usando una lista/tupla de columnas."""
        if isinstance(key, (list, tuple)):
            sub_dict = {}
            for col in key:
                if col not in self.dict:
                    raise KeyError(f"Column '{col}' not found in Data.")
                sub_dict[col] = self.dict[col]
            return Data(sub_dict)
        else:
            return self.dict[key]

    def __setitem__(self, key, value):
        """Permite añadir o modificar columnas respetando el motor de unidades y longitudes."""
        if isinstance(value, Quantity):
            col_data = value
        elif isinstance(value, (list, np.ndarray, tuple)):
            col_data = np.asarray(value)
        else:
            col_data = np.asarray([value])
        
        if self._length is not None and len(col_data) != self._length:
            raise ValueError("The new column does not match the length of the other data.")
        
        if self._length is None:
            self._length = len(col_data)

        self.dict[key] = col_data
        self.columns = list(self.dict.keys())

    def __delitem__(self, key):
        """Permite eliminar columnas usando del df['columna']."""
        if key in self.dict:
            del self.dict[key]
            self.columns = list(self.dict.keys())
            if not self.dict:
                self._length = None
        else:
            raise KeyError(f"Column '{key}' not found in Data.")

    def copy(self):
        """Devuelve una copia profunda del objeto Data (al estilo de pandas.DataFrame.copy)."""
        new_dict = {}
        for k, v in self.dict.items():
            if isinstance(v, Quantity):
                # Copia profunda del array interno manteniendo la unidad
                val_copy = v.value.copy() if hasattr(v, 'value') else v.value
                new_dict[k] = Quantity(val_copy, v.unit)
            elif isinstance(v, np.ndarray):
                new_dict[k] = v.copy()
            else:
                new_dict[k] = np.copy(v) if hasattr(v, '__array__') else v
        return Data(new_dict)

    @property
    def shape(self):
        return (self._length, len(self.dict))

    def __len__(self):
        return self._length

    def _to_dataframe(self):
        representation_dict = {}
        for col_name, col_data in self.dict.items():
            if isinstance(col_data, Quantity):
                representation_dict[f"{col_name} [{col_data.unit.symbol}]"] = col_data.value
            else:
                representation_dict[col_name] = col_data
        return pd.DataFrame(representation_dict)

    def __repr__(self):
        return str(self._to_dataframe())

    def _repr_html_(self):
        return self._to_dataframe()._repr_html_()

    def _numeric_columns(self):
        return {k: v for k, v in self.dict.items() if isinstance(v, Quantity) or np.issubdtype(v.dtype, np.number)}

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
        res = {k: (Quantity(np.median(v.value), v.unit) if isinstance(v, Quantity) else np.median(v)) for k, v in self._numeric_columns().items()}
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

    # =========================================================================
    # NEXT-GEN SCIENTIFIC PLOTTING ENGINE
    # =========================================================================

    def _get_plot_series(self, col_name: str):
        if col_name not in self.dict:
            raise KeyError(f"Column '{col_name}' not found in Data.")
        
        col_data = self.dict[col_name]
        if isinstance(col_data, Quantity):
            values = col_data.value
            label = f"{col_name} [{col_data.unit.symbol}]"
        else:
            values = col_data
            label = col_name
        return values, label

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
             marker='o', markersize=4.5, fill_area=True, title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, x_label = self._get_plot_series(x)
        y_vals, y_label = self._get_plot_series(y)
        fig, ax = self._init_plot_figure(ax, figsize)

        line_color = color if color is not None else self._primary_color
        
        if fill_area:
            ax.fill_between(x_vals, y_vals, color=line_color, alpha=0.08, zorder=1)

        ax.plot(x_vals, y_vals, color=line_color, linestyle=linestyle, linewidth=linewidth, 
                marker=marker, markersize=markersize, zorder=3, markeredgecolor='white', markeredgewidth=0.8, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def scatter(self, x: str, y: str, ax=None, figsize=(8, 4.5), color=None, s=45, alpha=1, 
                marker='o', fit=False, title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, x_label = self._get_plot_series(x)
        y_vals, y_label = self._get_plot_series(y)
        fig, ax = self._init_plot_figure(ax, figsize)

        scatter_color = color if color is not None else self._primary_color
        ax.scatter(x_vals, y_vals, color=scatter_color, s=s, alpha=alpha, marker=marker, 
                   edgecolors='white', linewidths=.5, zorder=3, **kwargs)

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
        x_vals, x_label = self._get_plot_series(x)
        y_vals, y_label = self._get_plot_series(y)
        
        yerr_vals = self._get_plot_series(yerr)[0] if yerr else None
        xerr_vals = self._get_plot_series(xerr)[0] if xerr else None

        fig, ax = self._init_plot_figure(ax, figsize)
        main_color = color if color is not None else self._primary_color
        err_color = ecolor if ecolor is not None else self._secondary_color

        ax.errorbar(x_vals, y_vals, yerr=yerr_vals, xerr=xerr_vals, fmt='o', color=main_color, 
                    ecolor=err_color, elinewidth=1.5, capsize=capsize, capthick=1.5, 
                    markeredgecolor='white', markeredgewidth=0.8, zorder=3, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax)

        fig.tight_layout()
        return fig, ax

    def bar(self, x: str, y: str, ax=None, figsize=(8, 4.5), color=None, width=0.6, 
            title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        x_vals, x_label = self._get_plot_series(x)
        y_vals, y_label = self._get_plot_series(y)
        fig, ax = self._init_plot_figure(ax, figsize)

        bar_color = color if color is not None else self._primary_color
        ax.bar(x_vals, y_vals, color=bar_color, width=width, edgecolor='none', zorder=3, **kwargs)

        self._format_labels(ax, xlabel or x_label, ylabel or y_label, title)
        if grid: self._apply_grid(ax, axis='y')

        fig.tight_layout()
        return fig, ax

    def hist(self, column: str, bins=12, ax=None, figsize=(8, 4.5), color=None, 
             title=None, xlabel=None, ylabel=None, grid=True, **kwargs):
        vals, label = self._get_plot_series(column)
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
        labels_with_units = [s[1] for s in series_data]
        
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
        labels_with_units = [s[1] for s in series_data]
        
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
        x_vals, x_label = self._get_plot_series(x)
        y_vals, y_label = self._get_plot_series(y)
        
        m, b = np.polyfit(x_vals, y_vals, 1)
        y_pred = m * x_vals + b
        residuals = y_vals - y_pred

        fig, ax = self._init_plot_figure(ax, figsize)

        ax.axhline(0, color=self._secondary_color, linestyle='--', linewidth=1.5, zorder=2)
        ax.scatter(x_vals, residuals, color=self._primary_color, edgecolor='white', linewidths=0.8, s=45, zorder=3, **kwargs)

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
                    vals, _ = self._get_plot_series(cols[i])
                    ax.hist(vals, color=self._primary_color, alpha=0.85, edgecolor='white')
                else:
                    x_vals, _ = self._get_plot_series(cols[j])
                    y_vals, _ = self._get_plot_series(cols[i])
                    ax.scatter(x_vals, y_vals, color=self._primary_color, s=20, alpha=0.7, edgecolors='none')

                for spine in ax.spines.values():
                    spine.set_color('#d0d0d0')

                if i == n - 1:
                    _, x_lbl = self._get_plot_series(cols[j])
                    ax.set_xlabel(x_lbl, fontsize=9, fontweight='bold')
                else:
                    ax.set_xticklabels([])

                if j == 0:
                    _, y_lbl = self._get_plot_series(cols[i])
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


class DataStatsResult:
    def __init__(self, stats_dict: dict):
        self.stats = stats_dict

    def __repr__(self):
        return "\n".join([f"  {k}: {v}" for k, v in self.stats.items()])

    def _repr_html_(self):
        data_formatted = {}
        for k, v in self.stats.items():
            if isinstance(v, Quantity):
                data_formatted[k] = f"{v.value} {v.unit.symbol}"
            else:
                data_formatted[k] = v
        df = pd.DataFrame([data_formatted], index=["valor"])
        return df.T.rename(columns={0: "Estadística"})._repr_html_()


class DataDescribeResult:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def __repr__(self):
        return str(self.df)

    def _repr_html_(self):
        return self.df._repr_html_()