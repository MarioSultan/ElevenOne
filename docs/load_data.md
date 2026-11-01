# Loading Data (`load_data`)

The `load_data` function automatically reads tabular datasets (CSV and Excel spreadsheets), detects physical units in column headers or cell strings, and pairs measurement columns with their corresponding uncertainty ($1\sigma$) columns.

---

## 1. Quick Example

Loading a file returns a fully populated `Data` container with units and uncertainties attached:

```python
import elevenone as eo

# Load a CSV file
df = eo.load_data("experiment_data.csv")

# Load a specific sheet from an Excel workbook
df_excel = eo.load_data("experiment_data.xlsx", sheet_name="Trial_1")
```

---

## 2. Header Naming Conventions

ElevenOne automatically parses unit symbols and uncertainty indicators embedded in column headers.

### A. Specifying Units in Column Headers

You can place unit symbols inside parentheses `()`, square brackets `[]`, or curly braces `{}`. Units can also be appended at the end after a space.

| Header Format | Recognized Base Name | Detected Unit |
| :--- | :--- | :--- |
| `Time (s)` | `Time` | `s` (Seconds) |
| `Velocity [m/s]` | `Velocity` | `m/s` (Meters per second) |
| `Mass {kg}` | `Mass` | `kg` (Kilograms) |
| `Force N` | `Force` | `N` (Newtons) |
| `Pressure (kPa)` | `Pressure` | `kPa` (Kilopascals) |
| `Energy (kg·m²/s²)` | `Energy` | `kg·m²/s²` (Derived unit expression) |

### B. Uncertainty Column Pairing

Columns representing standard measurement errors ($1\sigma$) are identified by recognized suffixes or keywords: `err`, `error`, `unc`, `uncertainty`, `uncert`, or `sigma`.

The loader pairs an uncertainty column with its base measurement variable using any of the following structures:

| Main Variable Header | Uncertainty Header | Notes |
| :--- | :--- | :--- |
| `Time (s)` | `Time_err (s)` | Same unit explicitly declared in both. |
| `Voltage [V]` | `Voltage_err` | Uncertainty inherits the unit (`V`) from the main column. |
| `Distance (m)` | `Distance_unc (cm)` | Unit mismatch handled automatically (`cm` converted to `m`). |
| `Current` | `Current (err)` | Keyword in parentheses pairing with `Current`. |

---

## 3. Recommended CSV / Excel Table Structure

Below are two sample table structures demonstrating how to prepare your raw files for zero-configuration ingestion.

### Example 1: Standard Laboratory Layout (Header-Defined Units & Errors)

**File:** `ohmlaw_experiment.csv`

| Voltage (V) | Voltage_err (V) | Current (mA) | Current_err (mA) | Notes |
| :--- | :--- | :--- | :--- | :--- |
| 1.0 | 0.02 | 10.2 | 0.1 | initial reading |
| 2.0 | 0.02 | 20.5 | 0.1 | steady state |
| 3.0 | 0.05 | 31.1 | 0.2 | high temperature |
| 4.0 | 0.05 | 40.8 | 0.2 | peak load |

When loaded with `df = eo.load_data("ohmlaw_experiment.csv")`:
* `df["Voltage"]` becomes a `Quantity` in Volts (`V`) with standard error $\pm 0.02, 0.05\text{ V}$.
* `df["Current"]` becomes a `Quantity` in Milliamperes (`mA`) with standard error $\pm 0.1, 0.2\text{ mA}$.
* `Notes` is loaded as a standard string array.
* `Voltage_err` and `Current_err` are consumed during pairing and hidden from the primary dataset columns.

---

### Example 2: In-Cell Units Layout

If units are written inside cell values, ElevenOne extracts the numerical magnitude, validates unit dimensional compatibility across rows, and scales values to a common unit automatically.

**File:** `pendulum_trials.csv`

| Trial | Length | Time (s) | Time_error |
| :--- | :--- | :--- | :--- |
| 1 | 50 cm | 1.42 | 0.02 |
| 2 | 1.0 m | 2.01 | 0.03 |
| 3 | 1500 mm | 2.46 | 0.04 |

When loaded with `df = eo.load_data("pendulum_trials.csv")`:
* `df["Length"]` automatically unifies values to meters (`m`): `[0.5, 1.0, 1.5] m`.
* `df["Time"]` pairs with `Time_error` in seconds (`s`).

---

## 4. Function Reference & Options

```python
eo.load_data(filepath, sheet_name=0, **kwargs)
```

### Parameters

* **`filepath`** *(str or Path)*: Path to the `.csv`, `.xls`, `.xlsx`, `.xlsm`, or `.xlsb` file.
* **`sheet_name`** *(int or str, default 0)*: Sheet name or index when loading Excel files.
* **`**kwargs`**: Additional keyword arguments passed directly to `pandas.read_csv()` or `pandas.read_excel()` (e.g., `delimiter=";"`, `skiprows=2`).

### Return Value

Returns a fully initialized `Data` object ready for analysis and visualization.