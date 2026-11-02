# `fit_custom` (Custom Model Fitting)

The `fit_custom` function fits any user-defined non-linear Python function $y = f(x, *params)$ to data, automatically handling errors in $x$ and $y$ via ODR or weighted least squares.

---

## 1. Mathematical Model

$$y = f(x, p_1, p_2, \dots, p_k)$$

You define the function signature in Python, where the first argument is $x$ and the remaining positional arguments are the parameters to be fitted.

---

## 2. Inferred Parameter Units

Parameter units are not automatically guessed for non-standard functions, so you can explicitly pass a list of target `Unit` objects via the `param_units` argument.

---

## 3. Function Signature & Parameters

```python
fit_custom(
    model_func: Callable,
    param_names: List[str],
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    p0: Optional[List[float]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    param_units: Optional[List[Unit]] = None
) -> FitResult
```

---

## 4. Usage Example

```python
import numpy as np
from elevenone import *
from elevenone.fitting import fit_custom

# 1. Define custom model: Damped Oscillation
# y(t) = A * exp(-gamma * t) * cos(omega * t)
def damped_oscillator(t, A, gamma, omega):
    return A * np.exp(-gamma * t) * np.cos(omega * t)

# 2. Prepare experimental data
data = Data({
    "Time": np.linspace(0, 5, 20) * s,
    "Voltage": [10.0, 7.2, 2.1, -3.5, -6.0, -4.2, 0.1, 3.8, 4.5, 2.1,
                -1.1, -3.0, -2.2, -0.2, 1.8, 1.9, 0.8, -0.5, -1.1, -0.6] * V
})
data.set_error("Time", 0.02)
data.set_error("Voltage", 0.2)

# 3. Perform fit
res = fit_custom(
    model_func=damped_oscillator,
    param_names=["A", "gamma", "omega"],
    data=data,
    x="Time",
    y="Voltage",
    p0=[10.0, 0.3, 3.0],                  # Initial guesses
    param_units=[V, s**(-1), Hz]          # Assign explicit units to parameters
)

# 4. Results & Plotting
print(res.summary())
fig, axes = res.plot(title="Damped Harmonic Oscillator Fit")
```