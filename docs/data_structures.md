# Data Structures & Dataset Manipulation (`Data`)

The `Data` class is ElevenOne's core data container, acting similarly to a Pandas DataFrame or a dictionary of NumPy arrays, but fully integrated with **units** and **uncertainties ($1\sigma$)**. 

It ensures that tabular data maintains physical consistency during filtering, column transformations, indexing, and statistical summaries.

---

## 1. Creating a `Data` Container

To build a `Data` object manually, pass a dictionary mapping column names to lists, NumPy arrays, or ElevenOne `Quantity` objects. All columns must have equal length.

```python
import elevenone as eo
from elevenone import Data
from elevenone.basic_units import V, A, s

# Creating Data with quantities and standard arrays
dataset = Data({
    "Time": [0.0, 1.0, 2.0, 3.0, 4.0] * s,
    "Voltage": [1.2, 2.5, 3.7, 5.1, 6.2] * V,
    "Current": [0.10, 0.22, 0.31, 0.42, 0.51] * A,
    "Status": ["ok", "ok", "ok", "warn", "ok"]  # Categorical/string columns allowed
})

# Display shape and dimensions
print(dataset.shape)  # Output: (5, 4) -> 5 rows, 4 columns
```

---

## 2. Basic Indexing, Selection, and Slicing

### Selecting Columns

Accessing a column by name returns the underlying array or `Quantity`:

```python
# Returns a Quantity object (values, units, and errors)
voltage_qty = dataset["Voltage"]

# Select multiple columns -> Returns a sub-Data container
subset = dataset[["Time", "Voltage"]]
```

### Slicing and Row Indexing

You can slice rows using integers or slice notation:

```python
# First row
first_row = dataset[0]

# Slice rows 1 to 3
sub_rows = dataset[1:4]

# Quick head and tail methods
top_three = dataset.head(3)
bottom_two = dataset.tail(2)
```

---

## 3. Modifying & Assigning Columns

You can assign new columns or update existing ones using scalar broadcasting or array operations.

### Adding New Columns & Automatic Unit Propagation

When deriving columns from existing ones, physical units and uncertainties are computed automatically:

```python
# Deriving Resistance (R = V / I)
# Units will automatically become 'V·A⁻¹' (Ohms)
dataset["Resistance"] = dataset["Voltage"] / dataset["Current"]

# Scalar broadcasting (e.g., adding a constant offset)
dataset["Time_Offset"] = dataset["Time"] + (0.5 * s)
```

### Renaming and Deleting Columns

```python
# Rename columns (returns a new Data object)
dataset = dataset.rename({"Voltage": "V_in", "Current": "I_measured"})

# Delete a column
del dataset["Time_Offset"]
```

---

## 4. Managing Uncertainties (`set_error`)

You can set or update uncertainties ($1\sigma$) across columns easily using `.set_error()`.

```python
from elevenone.basic_units import mV

# Set a uniform error for a single column
dataset.set_error("V_in", 0.05)  # Sets 0.05 V for all rows

# Set error using a Quantity (automatically converted to matching column units)
dataset.set_error("V_in", 50 * mV)  # Converts 50 mV -> 0.05 V automatically

# Set individual errors per row via a list or array
dataset.set_error("I_measured", [0.01, 0.01, 0.02, 0.02, 0.01])

# Set errors for multiple columns using a dictionary
dataset.set_error(
    columns=["V_in", "I_measured"],
    errors={"V_in": 0.05, "I_measured": 0.01}
)
```

---

## 5. Converting Column Units

To change the displayed or calculated unit of a column in a `Data` table, assign a converted `Quantity` back to the table:

```python
from elevenone.basic_units import mV, mA

# Convert V_in from Volts (V) to Millivolts (mV)
dataset["V_in"] = dataset["V_in"].to(mV)

# Convert I_measured from Amperes (A) to Milliamperes (mA)
dataset["I_measured"] = dataset["I_measured"].to(mA)
```

The values, uncertainties, and internal scale factors are automatically recalculated to reflect the target unit.

---

## 6. Querying and Data Filtering

### Query Expressions (`.query()`)

Filter rows dynamically using string-based logical expressions:

```python
# Query based on values (ignoring units during string evaluation)
high_v = dataset.query("V_in > 3.0")

# Complex logical query
filtered = dataset.query("V_in > 2.0 and Status == 'ok'")
```

### Boolean Masking

Filter directly using boolean arrays or conditions on quantities:

```python
# Boolean mask from a Quantity comparison
mask = dataset["V_in"] >= (3.0 * V)

# Apply mask to dataset
subset = dataset[mask]
```

---

## 7. Sorting, Random Sampling, & Deduplication

```python
# Sort values by one or more columns
sorted_df = dataset.sort_values(by="V_in", ascending=False)

# Randomly sample rows
sampled_df = dataset.sample(n=3, random_state=42)

# Drop duplicate rows based on subset
clean_df = dataset.drop_duplicates(subset=["Status"], keep="first")
```

---

## 8. Summary Statistics & Aggregation

`Data` objects provide built-in methods to compute statistics across all numerical columns simultaneously, properly keeping track of physical units and combined errors.

```python
# Full statistical summary table (count, mean, std, min, Q1, median, Q3, max)
summary = dataset.describe()

# Aggregation functions (return stats preserving units and propagated errors)
mean_vals   = dataset.mean()
std_vals    = dataset.std()
min_vals    = dataset.min()
max_vals    = dataset.max()
median_vals = dataset.median()

# Pearson correlation matrix (returns a Pandas DataFrame)
corr_matrix = dataset.corr()
```

---

## 9. Copying and Memory Integrity

To clone a `Data` instance and ensure underlying NumPy arrays and Quantities are detached from original references, use `.copy()`:

```python
dataset_copy = dataset.copy()
```