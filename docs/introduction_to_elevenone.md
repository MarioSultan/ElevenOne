# Introduction to ElevenOne

**ElevenOne** is a Python library designed for laboratory data analysis, scientific computing, and experimental data handling. It bridges the gap between general-purpose data science toolkits (such as Pandas, NumPy, and Matplotlib) and physical measurement analysis by making physical dimensions, unit conversions, and uncertainty propagation first-class citizens in data workflows.

---

## Why ElevenOne?

In standard data science pipelines, datasets consist of raw floating-point numbers. Physical units and measurement uncertainties are typically tracked via manual column naming schemes (e.g., `length_m`, `time_s_err`) or auxiliary documentation. This introduces several risks:

- **Manual Unit Tracking Errors:** Mixing units during calculations (e.g., adding meters to feet) leads to silent, undetected errors.
- **Manual Uncertainty Propagation:** Calculating standard error propagation ($1\sigma$) through derivatives or mathematical expressions requires repetitive, error-prone boilerplate code.
- **Disconnected Visualization & Reporting:** Generating plots or scientific summary tables with units, error bars, and dimensional labels requires manual axis formatting and metadata extractions.

**ElevenOne solves these challenges by combining data frame management, automatic unit conversion, error propagation, and physical-aware visualization into a single unified library.**

---

## Key Features & Capabilities

```
+-----------------------------------------------------------------------+
|                              ElevenOne                                |
|                                                                       |
|  +------------------+  +-------------------+  +--------------------+  |
|  | Dimensional Unit |  |  Uncertainty (1σ) |  | Smart CSV / Excel  |  |
|  | Tracking (SI/Imp)|  |    Propagation    |  | Auto-Parsing Engine|  |
|  +--------+---------+  +---------+---------+  +---------+----------+  |
|           |                      |                      |             |
|           +----------------------+----------------------+             |
|                                  |                                    |
|                                  v                                    |
|             +------------------------------------------+              |
|             | Unified Data Frame Container (`Data`)    |              |
|             +--------------------+---------------------+              |
|                                  |                                    |
|           +----------------------+----------------------+             |
|           |                                             |             |
|           v                                             v             |
|  +--------------------+                     +----------------------+  |
|  | Modern Matplotlib  |                     |  Automated HTML /    |  |
|  | Plotting & Errorbars |                   |  PDF Report Generation| |
|  +--------------------+                     +----------------------+  |
+-----------------------------------------------------------------------+
```

### 1. First-Class Physical Quantities & Dimensions
Every numerical quantity in ElevenOne can be associated with standard physical dimensions (Length, Mass, Time, Current, Temperature, Amount of Substance, Luminous Intensity, and Angular measure). Mathematical operations automatically scale unit factors and derive resultant physical dimensions.

### 2. Automatic Uncertainty ($1\sigma$) Propagation
All physical measurements preserve their standard uncertainties. When performing algebraic operations, mathematical transformations, or statistical aggregations (mean, standard deviation, variance, min/max), standard error propagation rules are computed dynamically under the hood.

### 3. Intelligent Data Ingestion (`load_data`)
The data loader automatically parses CSV and Excel headers as well as cell contents:
- **Header Unit Extraction:** Column names like `Time (s)` or `Velocity [m/s]` are automatically recognized as physical quantities with their respective units.
- **Error Column Pairing:** Columns designated with suffixes such as `_err`, `_error`, `_unc`, or `_sigma` are automatically attached to their corresponding measurement variables.
- **Cell Unit Parsing:** Handles mixed string inputs inside tabular data (e.g., `"12.5 mA"`).

### 4. Physical Data Frame Engine (`Data`)
The core `Data` structure combines array-based filtering, indexing, query execution, and statistical summaries with dimensional safety. It ensures operations between incompatible physical dimensions (e.g., adding Mass to Time) raise immediate errors.

### 5. Automated Publication-Ready Plotting
High-level plotting functions (scatter plots, line charts, error bars, histograms, box plots, residual plots, pair plots, and correlation heatmaps) automatically:
- Render $1\sigma$ uncertainty error bars whenever errors exist.
- Extract unit symbols and attach them directly to axis labels.
- Apply clean, consistent graphic themes without requiring Matplotlib setup code.

### 6. Built-in Scientific Report Generation
ElevenOne includes a dedicated reporting engine that converts any `Data` structure into an 11-section structured HTML or standalone PDF report complete with statistical summaries, distribution metrics, regression analyses, and embedded high-resolution plots.

---

## High-Level Workflow Overview

The general operational flow of ElevenOne moves seamlessly from raw data ingestion to scientific analysis and publication:

```
[ Raw CSV / Excel Dataset ]
           │
           ▼
   load_data Engine ──► Auto-detects Units & Error Columns
           │
           ▼
    Data Container  ──► Encapsulates Values, Units, and Uncertainties
           │
  ┌────────┴────────────────────────┬────────────────────────┐
  ▼                                 ▼                        ▼
Physical Calculations      Statistical Summaries      Publication Graphics
 & Unit Conversions         & Query Filtering        & Scientific Reports
```

1. **Ingest:** Load experimental raw data files. ElevenOne detects physical units and pairs values with their corresponding uncertainties.
2. **Compute:** Perform physical calculations. Units convert automatically, dimensions are derived, and uncertainties propagate at every step.
3. **Analyze & Query:** Filter datasets using boolean masks, sort variables, and generate full statistical descriptions.
4. **Visualize & Report:** Produce publication-ready plots with automated error bar formatting and generate full 11-section PDF/HTML documentation with a single function call.