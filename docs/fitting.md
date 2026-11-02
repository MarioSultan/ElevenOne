# Data Fitting Routines & Fit Results (`fitting`)

ElevenOne's `fitting` module provides robust curve fitting tools designed specifically for physical measurements. It seamlessly handles **experimental uncertainties ($1\sigma$) in both $x$ and $y$ variables**, respects **physical units**, and works directly with `Data` containers and `Quantity` objects.

When fitting, ElevenOne automatically selects the optimal statistical approach:
* **Orthogonal Distance Regression (ODR)**: Used when uncertainties are present in both $x$ and $y$.
* **Weighted Non-Linear Least Squares**: Used when uncertainties are present only in $y$.
* **Standard Least Squares**: Used when no uncertainties are specified.

To use the data fitting, import the following module:

```python
from elevenone.fitting import *
```

---

## 1. Quickstart Example

Fitting a linear relationship ($y = m \cdot x + b$) with full error handling and visual output:

```python
from elevenone import *
from elevenone.fitting import *

# 1. Prepare experimental dataset with uncertainties
data = Data({
    "Time": [0.0, 1.0, 2.0, 3.0, 4.0] * s,
    "Position": [0.2, 2.1, 4.3, 5.9, 8.2] * m
})

# Add measurement errors
data.set_error("Time", 0.05)       # 0.05 s error on time
data.set_error("Position", 0.2)    # 0.2 m error on position

# 2. Perform linear fit
result = fit_linear(data, x="Time", y="Position")

# 3. Print complete fit summary
print(result)

# 4. Plot data, fit line, and residuals
fig, axes = result.plot(title="Position vs. Time Fit")
```

---

## 2. The `FitResult` Object

All fitting routines return a `FitResult` instance. This object holds all parameter values, uncertainties, covariance matrices, and goodness-of-fit statistics.

### Key Attributes

| Attribute | Type | Description |
| :--- | :--- | :--- |
| `params` | `Dict[str, Quantity]` | Dictionary mapping parameter names to `Quantity` instances (value $\pm$ uncertainty with inferred units). |
| `popt` | `np.ndarray` | Optimal values for the fitted parameters. |
| `punc` | `np.ndarray` | $1\sigma$ standard uncertainties of the parameters. |
| `pcov` | `np.ndarray` | Covariance matrix of parameter estimates. |
| `residuals` | `np.ndarray` | Residual values ($y_{\text{data}} - y_{\text{fit}}$). |
| `chi2` | `float` | Weighted sum of squared residuals ($\chi^2$). |
| `reduced_chi2` | `float` | Reduced chi-squared ($\chi_\nu^2 = \chi^2 / \nu$). |
| `dof` | `int` | Degrees of freedom ($\nu = N - p$). |
| `r_squared` | `float` | Coefficient of determination ($R^2$). |
| `method` | `str` | Statistical method used (`'odr'` or `'weighted_leastsquares'`). |

### Accessing Parameters & Units

Fitted parameters are stored as `Quantity` objects, automatically maintaining dimensional consistency:

```python
# Access parameters directly
slope = result.params["m"]        # Returns Quantity e.g., 1.98 ± 0.06 m·s⁻¹
intercept = result.params["b"]    # Returns Quantity e.g., 0.21 ± 0.12 m

print(f"Speed: {slope.value:.3f} +/- {slope.error:.3f} {slope.unit.symbol}")
```

### Model Evaluation (`.eval()`)

Evaluate the fitted function at arbitrary point(s). If you pass a `Quantity`, it respects unit conversion:

```python
# Evaluate at scalar value or array
y_pred = result.eval(2.5)

# Evaluate using a Quantity (automatically converted to matching x_unit)
y_pred_qty = result.eval(2.5 * s)  # Returns Quantity with y_unit (m)
```

### Visualization (`.plot()`)

Generate publication-ready plots matching ElevenOne's visual theme:

```python
# Plot with error bars, fit curve, and bottom residual panel
fig, (ax_main, ax_res) = result.plot(
    show_residuals=True,
    num_points=500,
    title="Kinematic Fit"
)

# Plot without residual panel
fig, ax = result.plot(show_residuals=False)
```

---

## 3. Built-in Fitting Functions

ElevenOne includes pre-configured functions for common physical models.

### Linear Fit (`fit_linear`)
Fits $y = m \cdot x + b$. Automatically assigns parameter units: $[m] = [y]/[x]$ and $[b] = [y]$.

```python
from elevenone.fitting import fit_linear

res = fit_linear(data, x="Time", y="Position")
```

📚 For more info, read [linear fit documentation](fit_linear.md).


### Polynomial Fit (`fit_polynomial`)
Fits $y = a_n \cdot x^n + \dots + a_1 \cdot x + a_0$.

```python
from elevenone.fitting import fit_polynomial

# Second-order polynomial (quadratic fit: y = a2*x² + a1*x + a0)
res = fit_polynomial(degree=2, data=data, x="Time", y="Position")

accel = res.params["a2"] * 2  # Parameter units correctly scale with x^n
```

📚 For more info, read [polynomial fit documentation](fit_polynomial.md).


### Exponential Fit (`fit_exponential`)
Fits $y = a \cdot e^{b \cdot x}$. Inferred parameter units: $[a] = [y]$ and $[b] = [x]^{-1}$.

```python
from elevenone.fitting import fit_exponential

res = fit_exponential(data, x="Time", y="Voltage", p0=[5.0, -0.5])
```

📚 For more info, read [exponential fit documentation](fit_exponential.md).


### Power Law Fit (`fit_power`)
Fits $y = a \cdot x^b$.

```python
from elevenone.fitting import fit_power

res = fit_power(data, x="Distance", y="Intensity")
```

📚 For more info, read [power law fit documentation](fit_power_law.md).


### Logarithmic Fit (`fit_logarithmic`)
Fits $y = a \cdot \ln(x) + b$.

```python
from elevenone.fitting import fit_logarithmic

res = fit_logarithmic(data, x="Pressure", y="Volume")
```

📚 For more info, read [logarithmic fit documentation](fit_logarithmic.md).


---

## 4. Custom Model Fitting (`fit_custom`)

Fit any arbitrary non-linear user-defined Python function.

```python
import numpy as np
from elevenone import *
from elevenone.fitting import fit_custom

# Define model: damped harmonic oscillator y = A * exp(-gamma * t) * cos(omega * t)
def damped_oscillator(t, A, gamma, omega):
    return A * np.exp(-gamma * t) * np.cos(omega * t)

# Perform fit on Data container or raw arrays
res = fit_custom(
    model_func=damped_oscillator,
    param_names=["A", "gamma", "omega"],
    data=data,
    x="Time",
    y="Voltage",
    p0=[10.0, 0.1, 5.0],                           # Initial parameter guesses
    param_units=[V, s**(-1), Hz]                   # Assign parameter physical units
)

print(res.summary())
```

📚 For more info, read [custom fit documentation](fit_custom.md).


---

## 5. Input Flexibility

Fitting functions accept either a `Data` container or raw arrays / `Quantity` objects directly:

```python
# Option A: Passing column names from a Data object
res = fit_linear(data, x="Time", y="Position")

# Option B: Passing standalone Quantity objects with uncertainties
res = fit_linear(x=time_qty, y=position_qty)

# Option C: Passing standard NumPy arrays with explicit error arguments
res = fit_linear(x=x_np, y=y_np, xerr=x_err_np, yerr=y_err_np)
```