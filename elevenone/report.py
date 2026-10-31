import os
import base64
import io
import datetime
import urllib.request
import urllib.error
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Default logo URL from GitHub (raw content)
DEFAULT_LOGO_URL = "https://raw.githubusercontent.com/MarioSultan/ElevenOne/main/banner.png"


class ReportGenerator:
    """
    Holy Grail Scientific Report Generator for Data objects.
    Provides complete automated statistical analysis and next-gen visualizations
    without displaying raw data rows.
    """
    def __init__(self, data_obj, logo_path: str = DEFAULT_LOGO_URL, title: str = "Comprehensive Scientific Data Report", author: str = None):
        self.data = data_obj
        self.logo_path = logo_path
        self.title = title
        self.author = author or "ElevenOne"
        
        # Color palette inherited from Data object attributes
        self.primary_color = getattr(data_obj, '_primary_color', '#00ccff')
        self.secondary_color = getattr(data_obj, '_secondary_color', '#ff2ad4')
        self.facecolor = getattr(data_obj, '_facecolor', '#fcfcfc')
        self.figure_facecolor = getattr(data_obj, '_figure_facecolor', '#ffffff')
        self.grid_color = getattr(data_obj, '_grid_color', '#ebebeb')
        self.text_color = getattr(data_obj, '_text_color', '#1a1a1a')

    def _fig_to_base64(self, fig):
        """Converts a Matplotlib figure into a Base64-encoded PNG string."""
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
        plt.close(fig)
        buf.seek(0)
        return base64.b64encode(buf.read()).decode('utf-8')

    def _get_logo_base64(self):
        """Retrieves the logo image as base64 from a URL or local file path."""
        if not self.logo_path:
            return None

        target_path = self.logo_path
        if "github.com" in target_path and "/blob/" in target_path:
            target_path = target_path.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")

        if target_path.startswith("http://") or target_path.startswith("https://"):
            try:
                req = urllib.request.Request(
                    target_path, 
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    data = response.read()
                    encoded = base64.b64encode(data).decode('utf-8')
                    ext = target_path.split('?')[0].split('.')[-1].lower()
                    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/svg+xml'
                    return f"data:{mime};base64,{encoded}"
            except Exception as e:
                print(f"[Warning] Failed to download logo from URL ({target_path}): {e}")
                return None

        elif os.path.exists(target_path):
            try:
                with open(target_path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode('utf-8')
                    ext = target_path.split('.')[-1].lower()
                    mime = 'image/png' if ext == 'png' else 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/svg+xml'
                    return f"data:{mime};base64,{encoded}"
            except Exception as e:
                print(f"[Warning] Failed to load local logo ({target_path}): {e}")
                return None

        return None

    def _generate_plots(self):
        """Generates extended analytics visualizations matching the Data theme."""
        plots_b64 = []
        numeric_cols = list(self.data._numeric_columns().keys())

        if not numeric_cols:
            return plots_b64

        # 1. Distribution Analysis (Histograms)
        for col in numeric_cols:
            fig, _ = self.data.hist(column=col, title=f"Distribution: {col}")
            plots_b64.append({
                'title': f"Distribution of {col}",
                'description': f"Frequency distribution histogram illustrating variation and central tendencies for quantitative variable '{col}'.",
                'image': self._fig_to_base64(fig)
            })

        # 2. Global Distribution Comparisons (Box Plot & Violin Plot)
        if len(numeric_cols) >= 1:
            fig_box, _ = self.data.boxplot(columns=numeric_cols, title="Comparative Box Plot Analysis")
            plots_b64.append({
                'title': "Global Outlier & Quartile Analysis (Box Plot)",
                'description': "Side-by-side box-and-whisker plot highlighting medians, interquartile ranges, and extreme outliers across variables.",
                'image': self._fig_to_base64(fig_box)
            })

            fig_violin, _ = self.data.violin(columns=numeric_cols, title="Kernel Density & Distribution Shape (Violin Plot)")
            plots_b64.append({
                'title': "Comparative Density Profiles (Violin Plot)",
                'description': "Violin plot presenting empirical distribution density structures and medians for each numeric variable.",
                'image': self._fig_to_base64(fig_violin)
            })

        # 3. Bivariate Relationships & Regression Analysis
        if len(numeric_cols) >= 2:
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    x_col, y_col = numeric_cols[i], numeric_cols[j]
                    
                    # Scatter Plot with Fit Line
                    fig_scat, _ = self.data.scatter(x=x_col, y=y_col, fit=True, title=f"Bivariate Fit: {x_col} vs {y_col}")
                    plots_b64.append({
                        'title': f"Linear Regression Analysis ({x_col} vs {y_col})",
                        'description': f"Scatter plot with a fitted linear trendline evaluating relationship strength between {x_col} and {y_col}.",
                        'image': self._fig_to_base64(fig_scat)
                    })

                    # Residual Analysis Plot
                    fig_res, _ = self.data.residual_plot(x=x_col, y=y_col, title=f"Regression Residuals: {x_col} vs {y_col}")
                    plots_b64.append({
                        'title': f"Model Residual Analysis ({x_col} vs {y_col})",
                        'description': f"Residual error dispersion plot used to verify homoscedasticity and zero-mean assumption for linear modeling.",
                        'image': self._fig_to_base64(fig_res)
                    })

        # 4. Pairwise Relationships (Pairplot)
        if len(numeric_cols) >= 2:
            fig_pair, _ = self.data.pairplot(columns=numeric_cols)
            plots_b64.append({
                'title': "Multivariate Pairwise Grid (Pairplot)",
                'description': "Comprehensive pairwise interaction matrix displaying univariate distributions along the diagonal and bivariate scatter plots elsewhere.",
                'image': self._fig_to_base64(fig_pair)
            })

        # 5. Correlation Heatmap
        corr_df = self.data.corr()
        if not corr_df.empty and len(corr_df.columns) > 1:
            fig_heatmap, _ = self.data.corr_heatmap(title="Pearson Correlation Matrix")
            plots_b64.append({
                'title': "Variable Correlation Matrix Heatmap",
                'description': "Heatmap visualizing pairwise Pearson correlation coefficients ($r$) across all numerical variables.",
                'image': self._fig_to_base64(fig_heatmap)
            })

        return plots_b64

    def _compute_dataset_overview(self):
        """Computes structural metadata and dataset metrics."""
        rows, cols = self.data.shape
        num_cols = len(self.data._numeric_columns())
        non_num_cols = cols - num_cols
        
        overview = {
            "Total Observations (Rows)": rows,
            "Total Variables (Columns)": cols,
            "Numeric Variables": num_cols,
            "Non-Numeric / Categorical Variables": non_num_cols
        }
        return pd.DataFrame([overview], index=["Value"]).T

    def _compute_advanced_stats(self):
        """Calculates extended statistical indicators (Variance, Skewness, Kurtosis, IQR)."""
        numeric_cols = self.data._numeric_columns()
        extended_data = {}
        
        for k, v in numeric_cols.items():
            is_qty = hasattr(v, 'value')
            vals = v.value if is_qty else np.asarray(v)
            
            p25 = np.percentile(vals, 25)
            p75 = np.percentile(vals, 75)
            iqr = p75 - p25
            var_val = np.var(vals, ddof=1) if len(vals) > 1 else 0.0
            
            mean_val = np.mean(vals)
            std_val = np.std(vals, ddof=1) if len(vals) > 1 else 1.0
            if std_val > 0 and len(vals) > 2:
                skew_val = np.mean(((vals - mean_val) / std_val) ** 3)
                kurt_val = np.mean(((vals - mean_val) / std_val) ** 4) - 3.0
            else:
                skew_val, kurt_val = 0.0, 0.0

            unit_suffix = f" {v.unit.symbol}" if is_qty else ""
            
            extended_data[k] = [
                f"{var_val:.4g}{unit_suffix}",
                f"{iqr:.4g}{unit_suffix}",
                f"{skew_val:.4f}",
                f"{kurt_val:.4f}"
            ]
            
        return pd.DataFrame(extended_data, index=["Variance", "IQR (Q3 - Q1)", "Skewness", "Excess Kurtosis"])

    def _build_html_content(self):
        """Constructs the complete HTML scientific report layout."""
        df_overview_html = self._compute_dataset_overview().to_html(classes='styled-table', header=False)
        
        describe_res = self.data.describe()
        df_stats = describe_res.df.to_html(classes='styled-table')
        df_ext_stats = self._compute_advanced_stats().to_html(classes='styled-table')
        
        corr_df = self.data.corr()
        df_corr = corr_df.to_html(classes='styled-table') if not corr_df.empty else "<p>Insufficient numerical columns for correlation matrix.</p>"

        logo_src = self._get_logo_base64()
        logo_html = f'<img src="{logo_src}" class="module-logo" alt="Module Logo" />' if logo_src else '<div class="logo-placeholder"><span>Module Logo</span></div>'

        plots = self._generate_plots()
        plots_html = ""
        for plot in plots:
            plots_html += f"""
            <div class="card">
                <h3>{plot['title']}</h3>
                <p class="plot-desc">{plot['description']}</p>
                <div class="img-container">
                    <img src="data:image/png;base64,{plot['image']}" alt="{plot['title']}" />
                </div>
            </div>
            """

        timestamp = datetime.datetime.now().strftime("%B %d, %Y - %H:%M")

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{self.title}</title>
    <style>
        :root {{
            --primary-color: {self.primary_color};
            --secondary-color: {self.secondary_color};
            --bg-color: {self.figure_facecolor};
            --card-bg: {self.facecolor};
            --grid-color: {self.grid_color};
            --text-color: {self.text_color};
        }}
        body {{
            font-family: 'Helvetica', 'Arial', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 35px;
            line-height: 1.5;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 3px solid var(--primary-color);
            padding-bottom: 18px;
            margin-bottom: 30px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            color: var(--text-color);
            letter-spacing: -0.5px;
        }}
        .header-meta {{
            margin: 6px 0 0 0;
            color: #666666;
            font-size: 13px;
        }}
        .module-logo {{
            max-height: 65px;
            max-width: 280px;
            object-fit: contain;
        }}
        .logo-placeholder {{
            width: 200px;
            height: 50px;
            border: 2px dashed var(--primary-color);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #888888;
            font-size: 11px;
            background-color: var(--card-bg);
        }}
        .section-title {{
            font-size: 19px;
            font-weight: bold;
            color: var(--primary-color);
            margin-top: 35px;
            margin-bottom: 15px;
            border-left: 4px solid var(--secondary-color);
            padding-left: 12px;
            letter-spacing: -0.3px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--grid-color);
            border-radius: 8px;
            padding: 22px;
            margin-bottom: 25px;
            box-shadow: 0 2px 6px rgba(0,0,0,0.03);
        }}
        .card h3 {{
            margin-top: 0;
            margin-bottom: 8px;
            font-size: 16px;
            color: var(--text-color);
        }}
        .plot-desc {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 13px;
            color: #666666;
        }}
        .styled-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 13px;
        }}
        .styled-table th {{
            background-color: var(--primary-color);
            color: #ffffff;
            text-align: left;
            padding: 10px 12px;
            font-weight: bold;
        }}
        .styled-table td {{
            padding: 9px 12px;
            border-bottom: 1px solid var(--grid-color);
        }}
        .styled-table tr:nth-of-type(even) {{
            background-color: rgba(0, 0, 0, 0.02);
        }}
        .img-container {{
            text-align: center;
        }}
        .img-container img {{
            max-width: 100%;
            height: auto;
            border-radius: 6px;
        }}
        .footer {{
            margin-top: 50px;
            padding-top: 15px;
            border-top: 1px solid var(--grid-color);
            text-align: center;
            font-size: 12px;
            color: #888888;
        }}
        @media print {{
            body {{ padding: 0; }}
            .card {{ page-break-inside: avoid; }}
        }}
    </style>
</head>
<body>

    <div class="header">
        <div>
            <h1>{self.title}</h1>
            <p class="header-meta">Generated by <strong>{self.author}</strong> | {timestamp}</p>
        </div>
        {logo_html}
    </div>

    <div class="section-title">1. Executive Dataset Overview</div>
    <div class="card" style="overflow-x: auto;">
        {df_overview_html}
    </div>

    <div class="section-title">2. Primary Descriptive Statistics</div>
    <div class="card" style="overflow-x: auto;">
        {df_stats}
    </div>

    <div class="section-title">3. Advanced Statistical Indicators</div>
    <div class="card" style="overflow-x: auto;">
        {df_ext_stats}
    </div>

    <div class="section-title">4. Pearson Correlation Matrix</div>
    <div class="card" style="overflow-x: auto;">
        {df_corr}
    </div>

    <div class="section-title">5. Data Visualizations & Analytics</div>
    {plots_html}

    <div class="footer">
        Report generated by ElevenOne
    </div>

</body>
</html>
"""

    def generate(self, output_path: str, format_type: str = "html"):
        """Generates the final report in HTML or PDF format."""
        html_content = self._build_html_content()
        format_type = format_type.lower()

        if format_type == "html":
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"HTML report successfully generated at: {output_path}")

        elif format_type == "pdf":
            try:
                import pdfkit
                pdfkit.from_string(html_content, output_path)
                print(f"PDF report successfully generated at: {output_path}")
            except ImportError:
                try:
                    from weasyprint import HTML
                    HTML(string=html_content).write_pdf(output_path)
                    print(f"PDF report successfully generated at: {output_path}")
                except ImportError:
                    raise RuntimeError("To export as PDF, please install 'weasyprint' or 'pdfkit' (with wkhtmltopdf).")
        else:
            raise ValueError(f"Format '{format_type}' is not supported. Use 'html' or 'pdf'.")


def generate_report(data_obj, output_path: str, format_type: str = "html", logo_path: str = DEFAULT_LOGO_URL, title: str = "Comprehensive Scientific Data Report", author: str = None):
    """Direct function call to trigger scientific report generation."""
    reporter = ReportGenerator(data_obj, logo_path=logo_path, title=title, author=author)
    reporter.generate(output_path, format_type=format_type)