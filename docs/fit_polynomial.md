# `fit_polynomial` (Polynomial Fitting)

The `fit_polynomial` function fits polynomial curves of any degree $n$ to experimental data with full error handling and dimensional awareness.

---

## 1. Mathematical Model

$$y(x) = a_n \cdot x^n + a_{n-1} \cdot x^{n-1} + \dots + a_1 \cdot x + a_0$$

* **`a_i`**: Coefficient corresponding to $x^i$.

---

## 2. Inferred Parameter Units

Parameter units scale according to the power of $x$:
* **`a_i`**: $[y] / [x]^i$

*(e.g., for a quadratic trajectory $y = a_2 x^2 + a_1 x + a_0$ where $x$ is in seconds $\text{s}$ and $y$ is in meters $\text{m}$, $a_2$ has units $\text{m}\cdot\text{s}^{-2}$)*.

---

## 3. Function Signature & Parameters

```python
fit_polynomial(
    degree: int = 2,
    data: Optional[Data] = None,
    x: Optional[Union[str, np.ndarray, Quantity]] = None,
    y: Optional[Union[str, np.ndarray, Quantity]] = None,
    xerr: Optional[Union[str, np.ndarray, Quantity, float]] = None,
    yerr: Optional[Union[str, np.ndarray, Quantity, float]] = None
) -> FitResult
```

---

## 4. Usage Example

```python
from elevenone import *
from elevenone.fitting import fit_polynomial

# Free-fall trajectory data (quadratic relationship)
data = Data({
    "Time": [0.0, 0.5, 1.0, 1.5, 2.0] * s,
    "Height": [20.0, 18.7, 15.1, 8.9, 0.4] * m
})
data.set_error("Height", 0.3)

# Quadratic fit (degree=2)
res = fit_polynomial(degree=2, data=data, x="Time", y="Height")

# Extract acceleration from a2 coefficient (y = a2*t^2 + a1*t + a0)
a2 = res.params["a2"]
g_measured = -2 * a2  # Acceleration g = -2 * a2

print(f"Measured g: {g_measured.value:.2f} +/- {g_measured.error:.2f} {g_measured.unit.symbol}")
fig, ax = res.plot(title="Free Fall Trajectory Fit")
```