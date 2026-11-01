# Basic Usage: A Practical Introduction

If you want to start using **ElevenOne** right away without worrying about the underlying mathematical theory or internal classes, this guide is for you.

---

## 1. Defining Quantities (`5 * m`)

Working with physical values in ElevenOne is as simple as multiplying a number by a unit:

```python
from elevenone.basic_units import m, cm, s, kg, degC

# Basic scalar quantities
distance = 5 * m        # 5 meters
length   = 25 * cm      # 25 centimeters
time     = 10.5 * s     # 10.5 seconds
mass     = 2 * kg       # 2 kilograms
temp     = 20 * degC    # 20 degrees Celsius
```

You can also create quantities from lists or NumPy arrays:

```python
# Array of measurements
times = [1.0, 2.0, 3.0, 4.0] * s
distances = [10.2, 20.5, 30.1, 40.8] * m
```

---

## 2. Basic Arithmetic & Automatic Units

ElevenOne handles unit calculations automatically when you perform arithmetic:

```python
from elevenone.basic_units import m, s

distance = 100 * m
time = 9.58 * s

# Speed calculation (m/s)
speed = distance / time
print(speed)  # Output: 10.4384... m·s⁻¹

# Area calculation (m²)
width = 5 * m
height = 3 * m
area = width * height
print(area)   # Output: 15 m²
```

> **Dimensional Protection:** If you try to perform physically impossible operations (like adding meters to seconds), ElevenOne will stop you immediately:
> ```python
> 5 * m + 10 * s  # Raises TypeError / ValueError!
> ```

---

## 3. Quick Unit Conversions (`.to()`)

To express any quantity in a different, compatible unit, just call `.to()` with the target unit:

```python
from elevenone.basic_units import m, km, cm, s, h

# Convert distance to kilometers
dist = 1500 * m
print(dist.to(km))  # Output: 1.5 km

# Convert speed from m/s to km/h
speed_ms = 10 * (m / s)
speed_kmh = speed_ms.to(km / h)
print(speed_kmh)    # Output: 36.0 km·h⁻¹
```

---

## 4. Adding Measurement Errors (Uncertainty)

In real labs, every measurement has an error bound ($1\sigma$). You can define uncertainties using `Quantity(value, unit, error)` or by calling `.set_error()`:

```python
import elevenone as eo
from elevenone.basic_units import m, s

# 1. Directly when creating a quantity (value, unit, error)
t = eo.Quantity(10.0, s, 0.2)   # 10.0 ± 0.2 seconds
print(t)                        # Output: (10.0 ± 0.2) s

# 2. Assigning error to an existing variable
d = 50 * m
d.set_error(0.5)                # 50.0 ± 0.5 meters

# 3. Operations automatically propagate errors!
v = d / t
print(v)                        # Output: (5.0 ± 0.1118) m·s⁻¹
```

---

## 5. Quick tabular data workflow

Combine variables into a `Data` table to query, compute new columns, and plot in seconds:

```python
from elevenone import Data
from elevenone.basic_units import V, A

# Create a dataset table
lab_data = Data({
    "Voltage": [1.0, 2.0, 3.0, 4.0] * V,
    "Current": [0.10, 0.21, 0.29, 0.41] * A
})

# Add measurement errors to the columns
lab_data.set_error("Voltage", 0.05)
lab_data.set_error("Current", 0.01)

# Compute Resistance (Voltage / Current)
lab_data["Resistance"] = lab_data["Voltage"] / lab_data["Current"]

# Plot with error bars and automatic axis units!
lab_data.scatter(x="Current", y="Voltage", fit=True, title="Ohm's Law")
```

---

## Summary Cheat Sheet

| Task | Syntax Example |
| :--- | :--- |
| **Create quantity** | `x = 10 * m` |
| **Create array quantity** | `x = [1, 2, 3] * s` |
| **Convert unit** | `x.to(km)` |
| **Attach error** | `x = eo.Quantity(10, m, 0.1)` or `x.set_error(0.1)` |
| **Access raw number** | `x.value` |
| **Access unit object** | `x.unit` |
| **Access error array** | `x.error` |