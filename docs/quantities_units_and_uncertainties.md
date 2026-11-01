# Quantities, Units, and Uncertainties

At the core of **ElevenOne** are three interrelated concepts:

1. **`Dimension`**: Represents basic physical dimensions (Length, Mass, Time, etc.).
2. **`Unit`**: Defines scale factors, offsets, and symbols for specific units (e.g., meters, kilometers, degrees Celsius).
3. **`Quantity`**: Encapsulates a numerical value (scalar or NumPy array), its associated `Unit`, and its standard measurement uncertainty ($1\sigma$).

---

## 1. Physical Dimensions (`Dimension`)

ElevenOne tracks fundamental SI dimensions using an internal vector representation corresponding to eight basic dimensions:
`[Length, Mass, Time, Current, Temperature, Amount of Substance, Luminous Intensity, Angular]`

### Fundamental & Derived Dimensions

Predefined dimensions are available in `elevenone.dimension`:

```python
from elevenone.dimension import LENGTH, MASS, TIME, FORCE, ENERGY, PRESSURE
```

Dimensions can be combined using standard algebraic operations:

```python
VELOCITY = LENGTH / TIME
AREA = LENGTH ** 2
ACCELERATION = LENGTH / (TIME ** 2)
FORCE = MASS * ACCELERATION
```

---

## 2. Units (`Unit`)

A `Unit` object wraps a `Dimension` along with a scaling factor relative to base SI units, optional temperature offsets, and a unit symbol.

### Predefined Units

ElevenOne comes with a rich set of predefined units in `elevenone.basic_units`:

```python
from elevenone.basic_units import (
    # Length
    m, km, cm, mm, um, nm, inch, ft, yd, mi, angstrom,
    # Mass
    kg, g, mg, ug, ton, lb, oz,
    # Time
    s, ms, us, ns, min_unit, h, day, week, year,
    # Temperature
    K, degC, degF, R,
    # Electricity & Magnetism
    A, mA, uA, C, Ah, mAh, V, mV, kV, Ohm, kOhm, MOhm,
    # Force & Pressure
    N, kN, lbf, dyn, Pa, kPa, MPa, bar, mbar, psi, atm, mmHg,
    # Energy & Power
    J, kJ, MJ, cal, kcal, kWh, eV, BTU, W, kW, MW, HP,
    # Volume & Angular
    L, mL, m3, gal, rad, deg, counts
)
```

### Creating Custom Units

You can build new units by scaling existing units or defining them explicitly:

```python
from elevenone import Unit
from elevenone.dimension import LENGTH

# Custom unit by multiplication
light_minute = 17987547.48 * m

# Explicit custom unit initialization
nautical_mile = Unit(LENGTH, symbol="nmi", factor=1852.0)
```

### Unit Arithmetic

Multiplying or dividing unit objects automatically computes resulting derived units and symbols:

```python
speed_unit = m / s        # Symbol: 'm·s⁻¹'
density_unit = kg / (m**3) # Symbol: 'kg·m⁻³'
```

---

## 3. Quantities (`Quantity`)

A `Quantity` pairs numerical data (scalars or arrays) with a `Unit` and an uncertainty standard error ($1\sigma$).

### Construction

Quantities can be constructed using multiplication with a `Unit` or via the `Quantity` constructor:

```python
import numpy as np
import elevenone as eo
from elevenone.basic_units import m, s

# 1. Scalar quantity without error
d = 50 * m

# 2. Scalar quantity with uncertainty (1σ)
# Quantity(value, unit, error)
t = eo.Quantity(4.2, s, 0.1)

# 3. Array quantity with uniform error
v_arr = eo.Quantity([10.1, 12.3, 15.6], m / s, error=0.2)

# 4. Array quantity with individual uncertainties per measurement
x_arr = eo.Quantity(
    value=np.array([1.0, 2.0, 3.0]),
    unit=m,
    error=np.array([0.05, 0.08, 0.04])
)
```

### Attributes and Properties

Every `Quantity` instance provides key properties to access underlying data:

| Attribute / Property | Type | Description |
| :--- | :--- | :--- |
| `.value` / `.magnitude` | `np.ndarray` | Raw numerical array representing magnitude(s). |
| `.unit` / `.units` | `Unit` | Associated unit object. |
| `.error` | `np.ndarray` | $1\sigma$ standard error array (same shape as `.value`). |

Example usage:

```python
q = eo.Quantity([10, 20, 30], m, error=[0.1, 0.2, 0.3])

print(q.value)  # Output: array([10, 20, 30])
print(q.unit)   # Output: m
print(q.error)  # Output: array([0.1, 0.2, 0.3])
```

---

## 4. Modifying Uncertainties (`set_error`)

Uncertainty values can be updated or assigned post-creation using the `.set_error()` method:

```python
q = 15.5 * m

# Assign scalar uncertainty
q.set_error(0.3)

# Assign error using another Quantity (unit conversion applied automatically)
q.set_error(5 * cm) # Converts 5 cm (0.05 m) to the base unit 'm'
```

---

## 5. Unit Conversions (`convert_to` / `to`)

To express a `Quantity` in different, dimensionally compatible units, use `.convert_to()` (or its shorthand `.to()`):

```python
from elevenone.basic_units import km, h, cm

distance = 1500 * m
distance.set_error(10 * m)

# Convert to kilometers
d_km = distance.to(km)
print(d_km)  # Output: (1.5 ± 0.01) km

# Thermal units conversion (handles offset logic)
from elevenone.basic_units import degC, K
temp_c = eo.Quantity(25.0, degC, 0.5)
temp_k = temp_c.to(K)
print(temp_k) # Output: (298.15 ± 0.5) K
```

> **Note:** Attempting to convert between incompatible dimensions (e.g., converting meters to seconds) raises a `ValueError`.

---

## 6. Uncertainty Propagation Mathematics

ElevenOne automatically tracks and propagates standard measurement errors ($1\sigma$) under linear perturbation assumptions.

Given independent variables $x \pm \sigma_x$ and $y \pm \sigma_y$:

### Addition & Subtraction ($z = x \pm y$)
$$\sigma_z = \sqrt{\sigma_x^2 + \sigma_y^2}$$

```python
a = eo.Quantity(10.0, m, 0.3)
b = eo.Quantity(5.0, m, 0.4)
c = a + b  # Value = 15.0 m, Error = sqrt(0.3^2 + 0.4^2) = 0.5 m
```

### Multiplication ($z = x \cdot y$)
$$\sigma_z = \sqrt{(y \cdot \sigma_x)^2 + (x \cdot \sigma_y)^2}$$

```python
width = eo.Quantity(2.0, m, 0.05)
height = eo.Quantity(5.0, m, 0.1)
area = width * height # (10.0 ± 0.316) m²
```

### Division ($z = x / y$)
$$\sigma_z = \sqrt{\left(\frac{\sigma_x}{y}\right)^2 + \left(\frac{x \cdot \sigma_y}{y^2}\right)^2}$$

### Power Transformation ($z = x^n$)
$$\sigma_z = |n \cdot x^{n-1}| \cdot \sigma_x$$

```python
side = eo.Quantity(3.0, m, 0.1)
volume = side ** 3 # Value = 27.0 m³, Error = |3 * (3.0^2)| * 0.1 = 2.7 m³
```

---

## 7. Statistical Methods on Quantities

Array-based `Quantity` instances support basic statistical methods that aggregate values and recalculate combined uncertainties:

```python
q_data = eo.Quantity([10.0, 12.0, 11.0, 13.0], m, error=0.5)

print("Sum:", q_data.sum())
print("Mean:", q_data.mean())
print("Std Dev:", q_data.std())
print("Min:", q_data.min())
print("Max:", q_data.max())
```