# Dataset Operations & Computations

This guide details all mathematical, structural, and query operations you can perform on ElevenOne `Data` objects. 

Every column manipulation automatically respects **physical units** and **propagates uncertainties ($1\sigma$)**.

---

## 1. Column Manipulation & Structure

### Adding & Updating Columns

Assigning a new column can be done via lists, NumPy arrays, or `Quantity` objects. Scalar values automatically broadcast across all rows.

```python
import elevenone as eo
from elevenone import Data
from elevenone.basic_units import m, s, kg, V, A

dataset = Data({
    "Distance": [10.0, 20.0, 30.0, 40.0] * m,
    "Time": [2.0, 4.0, 5.5, 8.0] * s
})

# Assigning a constant value (scalar broadcasting)
dataset["Trial_ID"] = 1

# Adding a new Quantity column with units and uncertainties
dataset["Mass"] = eo.Quantity([1.0, 1.0, 1.0, 1.0], kg, error=0.02)
```

### Renaming Columns (`.rename`)

Renaming columns returns a new `Data` instance with updated keys:

```python
# Rename specific columns
df_renamed = dataset.rename({
    "Distance": "Position",
    "Time": "Elapsed_Time"
})
```

### Removing Columns (`del`)

Delete columns directly using Python's `del` statement:

```python
del dataset["Trial_ID"]
```

---

## 2. Column Arithmetic & Automatic Propagation

When you perform mathematical operations between columns, ElevenOne automatically computes the resulting **units** and propagates standard **uncertainties ($1\sigma$)**.

### Division & Multiplication (Derived Units)

```python
# Speed (v = d / t) -> Unit automatically becomes 'm·s⁻¹'
dataset["Speed"] = dataset["Distance"] / dataset["Time"]

# Kinetic Energy (E = 0.5 * m * v^2) -> Unit becomes 'kg·m²·s⁻²' (Joules)
dataset["Kinetic_Energy"] = 0.5 * dataset["Mass"] * (dataset["Speed"] ** 2)
```

### Addition & Subtraction (Same Dimension Validation)

Adding or subtracting columns requires compatible physical dimensions. If units differ (e.g., meters and centimeters), values and errors are converted automatically.

```python
from elevenone.basic_units import cm

# Distance_2 in centimeters
dataset["Distance_2"] = [100.0, 200.0, 150.0, 50.0] * cm

# Adding meters and centimeters automatically converts units!
dataset["Total_Distance"] = dataset["Distance"] + dataset["Distance_2"]
```

> **Dimensional Error Guard:** Attempting to add columns with incompatible dimensions raises an error:
> ```python
> dataset["Invalid"] = dataset["Distance"] + dataset["Time"] # Raises ValueError!
> ```

---

## 3. Working with Column Uncertainties (`set_error`)

Uncertainty bounds ($1\sigma$) can be attached, updated, or modified for individual or multiple columns.

```python
# 1. Assign scalar uncertainty to a single column
dataset.set_error("Distance", 0.1)  # ±0.1 m for all rows

# 2. Assign individual uncertainties per row
dataset.set_error("Time", [0.05, 0.05, 0.10, 0.12])

# 3. Assign uncertainty using another unit (automatically converted)
dataset.set_error("Distance", 5 * cm)  # Converts 5 cm to 0.05 m automatically

# 4. Set errors for multiple columns simultaneously using a dictionary
dataset.set_error(
    columns=["Distance", "Time"],
    errors={
        "Distance": 0.05,
        "Time": 0.02
    }
)
```

---

## 4. In-Place Column Unit Conversions

Convert any column in your dataset to a different unit of the same dimension by reassigning `.to()`:

```python
from elevenone.basic_units import km, h, ms

# Convert Distance from meters to kilometers
dataset["Distance"] = dataset["Distance"].to(km)

# Convert Time from seconds to milliseconds
dataset["Time"] = dataset["Time"].to(ms)

# Convert Speed to km/h
dataset["Speed"] = dataset["Speed"].to(km / h)
```

---

## 5. Filtering & Querying Datasets

### String-Based Queries (`.query`)

Filter dataset rows dynamically using expressions:

```python
# Simple comparison
fast_runs = dataset.query("Speed > 5.0")

# Multiple conditions
filtered = dataset.query("Speed > 4.0 and Distance <= 0.03")
```

### Boolean Masking

You can filter datasets using boolean arrays or conditional masks created from `Quantity` comparisons:

```python
# Create mask where Distance is greater than 15 meters (0.015 km)
mask = dataset["Distance"] > (0.015 * km)

# Apply mask
high_dist_df = dataset[mask]
```

---

## 6. Sorting, Deduplication, & Random Sampling

### Sorting Rows (`.sort_values`)

Sort datasets based on one or more column values:

```python
# Sort ascending by Speed
df_sorted = dataset.sort_values(by="Speed", ascending=True)

# Sort descending by Distance
df_sorted_desc = dataset.sort_values(by="Distance", ascending=False)
```

### Removing Duplicates (`.drop_duplicates`)

```python
# Drop duplicates based on specific columns
clean_df = dataset.drop_duplicates(subset=["Mass"], keep="first")
```

### Random Sampling (`.sample`)

```python
# Sample 2 random rows
sample_df = dataset.sample(n=2, random_state=42)

# Sample 50% of rows
sample_frac = dataset.sample(frac=0.5)
```

---

## 7. Global Statistical Summaries

Compute statistical aggregations across all numeric columns in a single call:

```python
# Summary statistics table (count, mean, std, min, Q1, median, Q3, max)
print(dataset.describe())

# Aggregate operations (returns Quantity objects preserving units and propagated errors)
means   = dataset.mean()
medians = dataset.median()
stds    = dataset.std()
mins    = dataset.min()
maxs    = dataset.max()

# Pearson Correlation Matrix (returns a Pandas DataFrame)
correlation = dataset.corr()
```