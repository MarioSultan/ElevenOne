"""Scientific report generator for ElevenOne Data objects.

Generates an HTML report with exactly eleven numbered sections and an optional
PDF report built directly with ReportLab (no wkhtmltopdf/WeasyPrint required).
"""

from __future__ import annotations

import os
import io
import base64
import html
import datetime
import urllib.request
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

DEFAULT_LOGO_URL = "https://raw.githubusercontent.com/MarioSultan/ElevenOne/main/banner.png"


class ReportGenerator:
    """Create fixed-structure, eleven-section scientific reports for Data objects."""

    def __init__(
        self,
        data_obj,
        logo_path: str = DEFAULT_LOGO_URL,
        title: str = "Comprehensive Scientific Data Report",
        author: str = None,
    ):
        self.data = data_obj
        self.logo_path = logo_path
        self.title = title
        self.author = author or "ElevenOne"
        self.primary_color = getattr(data_obj, "_primary_color", "#00ccff")
        self.secondary_color = getattr(data_obj, "_secondary_color", "#ff2ad4")
        self.facecolor = getattr(data_obj, "_facecolor", "#fcfcfc")
        self.figure_facecolor = getattr(data_obj, "_figure_facecolor", "#ffffff")
        self.grid_color = getattr(data_obj, "_grid_color", "#ebebeb")
        self.text_color = getattr(data_obj, "_text_color", "#1a1a1a")
        self._plot_cache = None

    # ------------------------------------------------------------------
    # General helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _safe_text(value):
        if isinstance(value, (np.integer,)):
            return str(int(value))
        if isinstance(value, (np.floating,)):
            return f"{float(value):.6g}"
        return str(value)

    @staticmethod
    def _fig_to_bytes(fig):
        buffer = io.BytesIO()
        fig.savefig(
            buffer, format="png", dpi=160, bbox_inches="tight",
            facecolor=fig.get_facecolor(),
        )
        plt.close(fig)
        buffer.seek(0)
        return buffer.getvalue()

    @staticmethod
    def _fig_to_base64(fig):
        return base64.b64encode(ReportGenerator._fig_to_bytes(fig)).decode("ascii")

    def _get_logo_bytes(self):
        if not self.logo_path:
            return None
        path = str(self.logo_path)
        if "github.com" in path and "/blob/" in path:
            path = path.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
        try:
            if path.startswith(("http://", "https://")):
                request = urllib.request.Request(path, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(request, timeout=5) as response:
                    return response.read()
            if os.path.isfile(path):
                with open(path, "rb") as image_file:
                    return image_file.read()
        except Exception as exc:
            warnings.warn(f"Could not load report logo: {exc}")
        return None

    def _numeric_columns(self):
        return list(self.data._numeric_columns().keys())

    def _overview(self):
        rows, columns = self.data.shape
        numeric = len(self._numeric_columns())
        return pd.DataFrame(
            {"Value": [rows, columns, numeric, columns - numeric]},
            index=["Total observations (rows)", "Total variables (columns)",
                   "Numeric variables", "Non-numeric / categorical variables"],
        )

    def _advanced_stats(self):
        numeric_columns = self.data._numeric_columns()
        result = {}
        for name, column in numeric_columns.items():
            is_quantity = hasattr(column, "value") and hasattr(column, "unit")
            values = np.asarray(column.value if is_quantity else column, dtype=float)
            unit = f" {column.unit.symbol}" if is_quantity else ""
            if values.size == 0:
                result[name] = ["—"] * 4
                continue
            q1, q3 = np.percentile(values, [25, 75])
            variance = np.var(values, ddof=1) if len(values) > 1 else 0.0
            mean = np.mean(values)
            std = np.std(values, ddof=1) if len(values) > 1 else 0.0
            if std > 0 and len(values) > 2:
                skewness = np.mean(((values - mean) / std) ** 3)
                excess_kurtosis = np.mean(((values - mean) / std) ** 4) - 3
            else:
                skewness, excess_kurtosis = 0.0, 0.0
            result[name] = [
                f"{variance:.4g}{unit}", f"{q3 - q1:.4g}{unit}",
                f"{skewness:.4f}", f"{excess_kurtosis:.4f}",
            ]
        return pd.DataFrame(
            result,
            index=["Variance", "Interquartile range (IQR)", "Skewness", "Excess kurtosis"],
        )

    @staticmethod
    def _table_html(frame, index=True):
        if frame is None or frame.empty:
            return '<p class="empty">Not available for this dataset.</p>'
        return frame.to_html(classes="report-table", border=0, escape=True, index=index)

    def _make_plot(self, function, *args, **kwargs):
        try:
            result = function(*args, **kwargs)
            fig = result[0] if isinstance(result, tuple) else result
            return self._fig_to_bytes(fig)
        except Exception as exc:
            warnings.warn(f"A report plot could not be generated: {exc}")
            return None

    def _generate_plot_groups(self):
        """Build the plot collections used by sections 5–11."""
        if self._plot_cache is not None:
            return self._plot_cache

        columns = self._numeric_columns()
        groups = {key: [] for key in (
            "histograms", "boxplot", "violin", "scatter", "residuals", "pairplot", "heatmap"
        )}
        if not columns:
            self._plot_cache = groups
            return groups

        for column in columns:
            image = self._make_plot(self.data.hist, column=column, title=f"Distribution: {column}")
            if image:
                groups["histograms"].append((f"Distribution of {column}", image))

        image = self._make_plot(self.data.boxplot, columns=columns, title="Comparative box plot")
        if image:
            groups["boxplot"].append(("Box plot", image))

        image = self._make_plot(self.data.violin, columns=columns, title="Comparative violin plot")
        if image:
            groups["violin"].append(("Violin plot", image))

        if len(columns) >= 2:
            for i, x_column in enumerate(columns):
                for y_column in columns[i + 1:]:
                    image = self._make_plot(
                        self.data.scatter, x=x_column, y=y_column, fit=True,
                        title=f"{x_column} vs {y_column}",
                    )
                    if image:
                        groups["scatter"].append((f"{x_column} vs {y_column}", image))
                    image = self._make_plot(
                        self.data.residual_plot, x=x_column, y=y_column,
                        title=f"Residuals: {x_column} vs {y_column}",
                    )
                    if image:
                        groups["residuals"].append((f"{x_column} vs {y_column}", image))

            image = self._make_plot(self.data.pairplot, columns=columns)
            if image:
                groups["pairplot"].append(("Pairwise plot matrix", image))

        if len(columns) >= 2:
            image = self._make_plot(self.data.corr_heatmap, title="Pearson correlation matrix")
            if image:
                groups["heatmap"].append(("Correlation heatmap", image))

        self._plot_cache = groups
        return groups

    def _report_sections(self):
        """Return exactly eleven sections, even if some analyses are unavailable."""
        describe = self.data.describe().df
        correlation = self.data.corr()
        groups = self._generate_plot_groups()
        return [
            ("Executive dataset overview", self._overview(), None),
            ("Primary descriptive statistics", describe, None),
            ("Advanced statistical indicators", self._advanced_stats(), None),
            ("Pearson correlation matrix", correlation, None),
            ("Univariate distribution analysis", None, groups["histograms"]),
            ("Global quartile and outlier analysis", None, groups["boxplot"]),
            ("Distribution density analysis", None, groups["violin"]),
            ("Bivariate relationships and linear regression", None, groups["scatter"]),
            ("Regression residual analysis", None, groups["residuals"]),
            ("Multivariate pairwise analysis", None, groups["pairplot"]),
            ("Correlation heatmap", None, groups["heatmap"]),
        ]

    @staticmethod
    def _plot_description(section_number):
        descriptions = {
            5: "Histograms showing the frequency distribution of each numerical variable.",
            6: "Box plots summarising medians, quartiles, spread and potential outliers.",
            7: "Violin plots showing the shape of the observed distributions.",
            8: "Scatter plots with a fitted straight line for each numerical variable pair.",
            9: "Residual plots for the corresponding linear fits; useful for inspecting systematic deviations.",
            10: "Pairwise matrix combining univariate distributions and bivariate scatter plots.",
            11: "Graphical representation of Pearson correlation coefficients.",
        }
        return descriptions.get(section_number, "")

    # ------------------------------------------------------------------
    # HTML
    # ------------------------------------------------------------------
    def _build_html_content(self):
        sections = self._report_sections()
        timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
        logo = self._get_logo_bytes()
        logo_html = (
            f'<img class="logo" src="data:image/png;base64,{base64.b64encode(logo).decode("ascii")}" alt="Logo">'
            if logo else ""
        )
        section_html = []
        for number, (heading, frame, plots) in enumerate(sections, start=1):
            content = ""
            if frame is not None:
                content = self._table_html(frame)
            else:
                plot_items = plots or []
                if plot_items:
                    for plot_title, image_bytes in plot_items:
                        encoded = base64.b64encode(image_bytes).decode("ascii")
                        content += (
                            '<figure class="plot">'
                            f'<figcaption>{html.escape(plot_title)}</figcaption>'
                            f'<img src="data:image/png;base64,{encoded}" alt="{html.escape(plot_title)}">'
                            '</figure>'
                        )
                else:
                    content = '<p class="empty">This analysis is not available for the current dataset.</p>'
            section_html.append(
                f'<details class="section" {"open" if number == 1 else ""}>'
                f'<summary><span class="number">{number:02d}</span>'
                f'<span>{html.escape(heading)}</span></summary>'
                f'<div class="section-content">{content}</div></details>'
            )

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(self.title)}</title>
<style>
:root {{ --primary:{self.primary_color}; --secondary:{self.secondary_color}; --bg:{self.figure_facecolor};
--card:{self.facecolor}; --grid:{self.grid_color}; --text:{self.text_color}; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; padding:32px; background:var(--bg); color:var(--text);
font-family:Arial,Helvetica,sans-serif; line-height:1.55; }}
main {{ max-width:1100px; margin:0 auto; }}
header {{ display:flex; justify-content:space-between; align-items:center; gap:24px;
border-bottom:3px solid var(--primary); padding-bottom:20px; margin-bottom:28px; }}
h1 {{ font-size:clamp(23px,4vw,32px); margin:0 0 6px; }}
.meta {{ margin:0; color:#777; font-size:13px; }}
.logo {{ max-width:220px; max-height:65px; object-fit:contain; }}
.section {{ background:var(--card); border:1px solid var(--grid); border-left:4px solid var(--secondary);
border-radius:8px; margin:13px 0; overflow:hidden; box-shadow:0 2px 6px rgba(0,0,0,.03); }}
.section summary {{ list-style:none; cursor:pointer; display:flex; align-items:center; gap:14px;
padding:16px 19px; font-weight:700; user-select:none; }}
.section summary::-webkit-details-marker {{ display:none; }}
.section summary::after {{ content:'+'; margin-left:auto; font-size:22px; color:var(--secondary); }}
.section[open] summary::after {{ content:'−'; }}
.section summary:hover {{ background:rgba(0,0,0,.025); }}
.number {{ display:inline-flex; align-items:center; justify-content:center; flex:0 0 34px;
height:30px; border-radius:6px; background:var(--primary); color:white; font-size:13px; }}
.section-content {{ padding:2px 19px 20px; overflow-x:auto; border-top:1px solid var(--grid); }}
.report-table {{ width:100%; border-collapse:collapse; margin-top:13px; font-size:13px; }}
.report-table th {{ text-align:left; padding:10px; background:var(--primary); color:white; }}
.report-table td {{ padding:9px 10px; border-bottom:1px solid var(--grid); }}
.report-table tr:nth-child(even) {{ background:rgba(0,0,0,.025); }}
.plot {{ margin:20px auto 8px; text-align:center; padding:16px 18px;
border:1px solid var(--grid); border-radius:8px; box-shadow:0 2px 6px rgba(0,0,0,.025); }}
.plot figcaption {{ font-weight:700; margin-bottom:9px; color:var(--text); }}
.plot img {{ display:block; max-width:100%; height:auto; margin:0 auto; border-radius:5px; }}
.empty {{ color:#777; font-style:italic; }}
footer {{ text-align:center; margin-top:32px; padding-top:14px; border-top:1px solid var(--grid);
font-size:12px; color:#888; }}
@media(max-width:650px) {{ body {{ padding:15px; }} header {{ align-items:flex-start; }} .logo {{ max-width:100px; }} }}
@media print {{ body {{ padding:0; }} .section {{ break-inside:avoid; }} .section:not([open]) .section-content {{ display:block; }} }}
</style>
</head>
<body><main>
<header><div><h1>{html.escape(self.title)}</h1>
<p class="meta">Generated by <strong>{html.escape(self.author)}</strong> · {html.escape(timestamp)}</p></div>{logo_html}</header>
{''.join(section_html)}
<footer>Report generated by ElevenOne · Exactly 11 sections</footer>
</main></body></html>'''

    # ------------------------------------------------------------------
    # PDF (ReportLab)
    # ------------------------------------------------------------------
    def _build_pdf(self, output_path):
        """Build a standards-compliant PDF directly with ReportLab.

        No PDF post-processing, external converter, or metadata rewriting is
        performed. Keeping a single writer avoids cross-reference and trailer
        inconsistencies between PDF libraries.
        """
        try:
            from reportlab.lib import colors
            from reportlab.lib.enums import TA_LEFT
            from reportlab.lib.pagesizes import A4
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import mm
            from reportlab.platypus import (
                SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                Image as RLImage, KeepTogether,
            )
        except ImportError as exc:
            raise RuntimeError(
                "PDF export requires ReportLab. Install it with: pip install reportlab"
            ) from exc

        import unicodedata
        from pathlib import Path

        def pdf_metadata(value, fallback):
            """Return conservative PDFDocEncoding-safe metadata text."""
            value = str(value or fallback)
            normalized = unicodedata.normalize("NFKD", value)
            ascii_value = normalized.encode("ascii", "ignore").decode("ascii")
            # PDF metadata should be short, plain text, and free of control chars.
            ascii_value = " ".join(ascii_value.split())
            return ascii_value[:200] or fallback

        title_meta = pdf_metadata(self.title, "ElevenOne Scientific Report")
        author_meta = pdf_metadata(self.author, "ElevenOne")
        primary = colors.HexColor(self.primary_color)
        secondary = colors.HexColor(self.secondary_color)
        grid = colors.HexColor(self.grid_color)
        text = colors.HexColor(self.text_color)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(
            name="ElevenOneReportTitle", parent=styles["Title"],
            fontName="Helvetica-Bold", fontSize=19, leading=23,
            alignment=TA_LEFT, textColor=text, spaceAfter=5,
        ))
        styles.add(ParagraphStyle(
            name="ElevenOneSectionHeading", parent=styles["Heading2"],
            fontName="Helvetica-Bold", fontSize=12, leading=15,
            textColor=primary, spaceBefore=11, spaceAfter=8,
            borderColor=secondary, borderWidth=1, borderPadding=5,
        ))
        styles.add(ParagraphStyle(
            name="ElevenOneSmallCell", parent=styles["BodyText"],
            fontName="Helvetica", fontSize=7.5, leading=9,
        ))
        styles.add(ParagraphStyle(
            name="ElevenOneSmallCellHeader", parent=styles["BodyText"],
            fontName="Helvetica-Bold", fontSize=7.5, leading=9,
            textColor=colors.white,
        ))
        styles.add(ParagraphStyle(
            name="ElevenOneReportMeta", parent=styles["BodyText"],
            fontName="Helvetica", fontSize=8, textColor=colors.grey,
            spaceAfter=12,
        ))

        destination = os.path.abspath(os.fspath(output_path))
        os.makedirs(os.path.dirname(destination) or os.getcwd(), exist_ok=True)
        doc = SimpleDocTemplate(
            destination, pagesize=A4,
            rightMargin=16 * mm, leftMargin=16 * mm,
            topMargin=16 * mm, bottomMargin=17 * mm,
            title=title_meta, author=author_meta,
            subject="Scientific data analysis report",
            creator="ElevenOne Report Generator",
        )

        story = [Paragraph(html.escape(str(self.title)), styles["ElevenOneReportTitle"])]
        timestamp = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
        story.append(Paragraph(
            f"Generated by <b>{html.escape(str(self.author))}</b> &middot; "
            f"{html.escape(timestamp)}",
            styles["ElevenOneReportMeta"],
        ))

        logo_bytes = self._get_logo_bytes()
        if logo_bytes:
            try:
                logo_image = RLImage(io.BytesIO(logo_bytes), width=42 * mm, height=14 * mm,
                                     kind="proportional")
                logo_image.hAlign = "RIGHT"
                story.extend([logo_image, Spacer(1, 5 * mm)])
            except Exception as exc:
                warnings.warn(f"Could not embed report logo in PDF: {exc}")

        def dataframe_table(frame):
            if frame is None or frame.empty:
                return Paragraph("Not available for this dataset.", styles["BodyText"])

            display = frame.copy().reset_index()
            headers = [str(column) for column in display.columns]
            rows = [[Paragraph(html.escape(header), styles["ElevenOneSmallCellHeader"])
                     for header in headers]]
            for row in display.itertuples(index=False, name=None):
                rows.append([
                    Paragraph(html.escape(self._safe_text(value)), styles["ElevenOneSmallCell"])
                    for value in row
                ])

            available_width = A4[0] - 32 * mm
            ncols = max(1, len(headers))
            table = Table(
                rows, repeatRows=1, hAlign="LEFT",
                colWidths=[available_width / ncols] * ncols,
            )
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), primary),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 0.35, grid),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                 [colors.white, colors.HexColor("#f5f5f5")]),
            ]))
            return table

        for number, (heading, frame, plots) in enumerate(self._report_sections(), start=1):
            story.append(Paragraph(
                f"{number}. {html.escape(heading)}",
                styles["ElevenOneSectionHeading"],
            ))
            if frame is not None:
                story.append(dataframe_table(frame))
            elif plots:
                for plot_title, image_bytes in plots:
                    story.append(Paragraph(
                        html.escape(plot_title), styles["Heading4"]
                    ))
                    try:
                        image = RLImage(
                            io.BytesIO(image_bytes), width=170 * mm,
                            height=110 * mm, kind="proportional",
                        )
                        image.hAlign = "CENTER"
                        story.append(image)
                    except Exception as exc:
                        warnings.warn(f"Could not embed a plot in the PDF: {exc}")
                        story.append(Paragraph(
                            "This plot could not be embedded.", styles["BodyText"]
                        ))
                    story.append(Spacer(1, 3 * mm))
            else:
                story.append(Paragraph(
                    "This analysis is not available for the current dataset.",
                    styles["BodyText"],
                ))
            story.append(Spacer(1, 3 * mm))

        def draw_page(canvas, document):
            canvas.saveState()
            # Set metadata on the PDF document itself; ReportLab writes the
            # Info dictionary and cross-reference structure when build() closes.
            canvas.setTitle(title_meta)
            canvas.setAuthor(author_meta)
            canvas.setSubject("Scientific data analysis report")
            canvas.setCreator("ElevenOne Report Generator")
            canvas.setProducer("ReportLab")
            canvas.setFont("Helvetica", 8)
            canvas.setFillColor(colors.grey)
            canvas.drawCentredString(A4[0] / 2, 9 * mm, str(document.page))
            canvas.restoreState()

        # One writer, one output file: no pypdf/PyPDF2 rewrite step.
        doc.build(story, onFirstPage=draw_page, onLaterPages=draw_page)

        # Basic sanity check without modifying the generated file.
        with open(destination, "rb") as pdf_file:
            header = pdf_file.read(8)
        if not header.startswith(b"%PDF-"):
            try:
                os.remove(destination)
            except OSError:
                pass
            raise RuntimeError("ReportLab did not produce a valid PDF header.")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def generate(self, output_path: str, format_type: str = "html"):
        format_type = str(format_type).lower().strip()
        if format_type not in ("html", "pdf"):
            raise ValueError(f"Format '{format_type}' is not supported. Use 'html' or 'pdf'.")
        if format_type == "html":
            content = self._build_html_content()
            with open(output_path, "w", encoding="utf-8") as file:
                file.write(content)
        else:
            self._build_pdf(output_path)
        print(f"{format_type.upper()} report successfully generated at: {output_path}")
        return output_path


def generate_report(
    data_obj,
    output_path: str,
    format_type: str = "html",
    logo_path: str = DEFAULT_LOGO_URL,
    title: str = "Comprehensive Scientific Data Report",
    author: str = None,
):
    """Convenience function to generate an HTML or PDF report."""
    reporter = ReportGenerator(
        data_obj, logo_path=logo_path, title=title, author=author,
    )
    return reporter.generate(output_path, format_type=format_type)
