# Introduction to ElevenOne

> **Physics, Uncertainty, Data Analysis, and Automated Reporting — Unified into One Elegant Python Engine.**

Stop wrestling with lost units, manual error propagation, clunky dataframes, and boilerplate plotting scripts.  
**ElevenOne** bridges the gap between raw scientific measurements and publication-ready reporting in Python.

---

## What is ElevenOne?

ElevenOne is designed for scientific computing, physics engineering, data analysis, and laboratory work. It brings together unit-aware quantities, automatic $1\sigma$ error propagation, custom dataframes, statistical fitting, and instant report generation into a single intuitive interface.

With **over 400+ built-in physical units** (spanning fundamental SI, kinematics, electromagnetism, thermodynamics, astrophysics, and fluid dynamics), ElevenOne handles unit conversions and uncertainty calculations automatically so you can focus on the science.

---

## Key Highlights

* **400+ Units & Physical Dimensions:** Work effortlessly with everything from kilometers ($\text{km}$) and microvolts ($\mu\text{V}$) to light-years ($\text{ly}$), atmospheres ($\text{atm}$), and farads ($\text{F}$).
* **Automatic Error Propagation:** Every physical operation automatically calculates $1\sigma$ standard uncertainties, including through complex mathematical and trigonometric functions ($\sin$, $\cos$, $\exp$, $\log$, $\sqrt{\cdot}$, etc.).
* **Smart Data Ingestion (`load_data`):** Automatically imports `.csv` and `.xlsx` files, recognizes unit symbols in column headers (e.g., `Time (s)`, `Voltage [mV]`), and automatically pairs data with its uncertainty columns (e.g., `time_err`).
* **Built-in Styled Data Analysis:** `Data` objects provide statistical summaries, intuitive query filtering, and built-in visualization presets (`plot`, `scatter`, `errorbar`, `violin`, `corr_heatmap`, `pairplot`) styled instantly with customizable themes.
* **Rigorous Curve Fitting:** Perform weighted least squares or Orthogonal Distance Regression (ODR) with `fit_linear`, `fit_polynomial`, `fit_exponential`, `fit_custom`, and more.
* **Automated 11-Section Scientific Reports:** Export complete HTML or native PDF analytical reports with a single method call (`data.generate_report(...)`).

---

## How It Works (At a Glance)

### 1. Physical Quantities & Automatic Uncertainty

Operations automatically convert units and propagate errors:

```python
from elevenone import kg, m, s, N, sin, Quantity

# Define physical values with standard uncertainties
mass = Quantity(5.0, kg, error=0.1)      # (5.0 ± 0.1) kg
dist = 100.0 * m                           # 100 m
time = Quantity(10.0, s, error=0.2)       # (10.0 ± 0.2) s

# Velocity & Force calculation with automatic error propagation
velocity = dist / time                     # Output in m/s with propagated uncertainty
force = mass * (dist / (time**2))          # Automatically resolves to Newtons (N)

# Convert to target units seamlessly
force_in_N = force.to(N)
```

---

### 2. Smart Loading & Instant Visualizations

Load data files containing unit annotations and plot error-bar representations out-of-the-box:

```python
from elevenone import load_data, Data

# Loads columns and automatically links uncertainty pairs (e.g., 'Voltage' & 'Voltage_err')
data = load_data("experiment_results.csv")

# Set global visual styling (e.g., 'elevenone', 'dark_mode', 'cyberpunk', 'nordic')
Data.set_style("dark_mode")

# Scatter plot with auto-detected units, error bars, and linear fit line
fig, ax = data.scatter(x="Time", y="Voltage", fit=True)
```

---

### 3. Data Fitting & Automatic Parameter Units

Fit theoretical models to experimental data while preserving dimension checks:

```python
from elevenone import fit_linear

# Perform Orthogonal Distance Regression (ODR) or weighted least squares
fit = fit_linear(data, x="Time", y="Voltage")

# Inspect statistics (R², Reduced χ², DoF) and parameters with inferred units
print(fit.summary())

# Plot data, fit line, and residual subplots automatically
fit.plot(show_residuals=True)
```

---

### 4. One-Click Report Generation

Transform your analyzed `Data` objects into comprehensive, 11-section PDF or HTML scientific documents:

```python
# Generates a complete report with overview stats, distribution plots, 
# correlation matrices, and linear fits
data.generate_report("final_lab_report.pdf", format_type="pdf")
```

---

## How Far Can You Take ElevenOne?

* **Laboratory Automation:** Ingest raw experimental outputs directly into clean data structures with standard uncertainty tracking.
* **Physics Simulations:** Run multi-variable physical calculations without worrying about dimensional errors or manual partial derivatives.
* **Research & Academic Publications:** Generate publication-standard figures, curve fits with full residual diagnostics, and full summary PDFs in seconds.

---

Ready to elevate your scientific workflow? **Give ElevenOne a spin in your next project!**
