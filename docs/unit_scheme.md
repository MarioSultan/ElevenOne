# Unit Schemes (`unit_scheme`)

A **Unit Scheme** configures how ElevenOne **presents** physical quantities across the entire session—including printed outputs, `Data` tables, summary statistics, plot axis labels, and generated reports—without altering underlying calculations or stored values.

---

## 1. Core Design Rules

* **Opt-In by Default:** When no scheme is active (`None`), ElevenOne behaves normally and displays every `Quantity` in the exact unit it carries.
* **Presentation Only:** A unit scheme never mutates `Quantity.value`, `Quantity.unit`, or arithmetic operations. All calculations continue using the original units; the scheme only transforms how results are rendered.
* **Dimension-Based Resolution:** For any physical dimension, a scheme resolves the target unit in the following order:
  1. An explicit **named unit** defined in the scheme (e.g., $\text{N}$, $\text{Pa}$, $\text{J}$, $\text{dyn}$, $\text{erg}$).
  2. A **coherent derived unit** automatically composed from the scheme's 8 base units (e.g., $\text{cm}\cdot\text{s}^{-1}$ in CGS, or $\text{AU}\cdot\text{yr}^{-1}$ in astronomy).
  3. **Dimensionless** quantities are left untouched.

---

## 2. Built-in Unit Schemes

ElevenOne provides 7 pre-registered schemes ready to use:

| Scheme Name | Aliases | Base Units | Notable Named Units |
| :--- | :--- | :--- | :--- |
| **`"SI"`** | — | $\text{m}, \text{kg}, \text{s}, \text{A}, \text{K}, \text{mol}, \text{cd}, \text{rad}$ | $\text{N}, \text{Pa}, \text{J}, \text{W}, \text{C}, \text{V}, \text{F}, \Omega, \text{S}, \text{Wb}, \text{T}, \text{H}, \text{Hz}$ |
| **`"CGS"`** | `"gaussian"` | $\text{cm}, \text{g}, \text{s}, \text{statA}$ | $\text{dyn}, \text{erg}, \text{Ba}, \text{P}, \text{St}, \text{Gal}, \text{statC}, \text{statV}, \text{G}, \text{Mx}, \text{Oe}$ |
| **`"astronomy"`** | `"astro"` | $\text{AU}, M_\odot, \text{yr}, \text{arcsec}$ | $\text{km/s}, \text{erg}, L_\odot, \text{dyn}, \text{Ba}, \text{Gal}, \text{g/cm}^3, \text{G}, \text{Hz}$ |
| **`"galactic"`** | — | $\text{kpc}, M_\odot, \text{Myr}, \text{deg}$ | $\text{km/s}, \text{erg}, L_\odot, \text{dyn}, \text{Ba}, \mu\text{G}, \text{Hz}$ |
| **`"engineering"`** | `"eng"` | $\text{mm}, \text{t}, \text{s}$ | $\text{N}, \text{MPa}, \text{mJ}, \text{mW}, \text{Hz}$ (+ SI electrical) |
| **`"imperial"`** | `"us"`, `"fps"`, `"us-customary"` | $\text{ft}, \text{lb}, \text{s}, ^\circ\text{F}$ | $\text{lbf}, \text{psi}, \text{ft}\cdot\text{lbf}, \text{HP}, \text{Hz}$ (+ SI electrical) |
| **`"atomic"`** | `"hartree"` | $a_0, m_e, t_{\text{au}}, I_{\text{au}}, T_{\text{au}}$ | $E_h, e, E_h/a_0, E_h/a_0^3, E_h/e, \hbar/(e\cdot a_0^2)$ |

---

## 3. Function Signatures & Class Reference

### Global Management Functions

```python
set_scheme(scheme: Optional[Union[str, UnitScheme]] = None) -> Optional[UnitScheme]
get_scheme(name: Optional[str] = None) -> Optional[UnitScheme]
reset_scheme() -> None
list_schemes() -> List[str]
register_scheme(scheme: UnitScheme, *aliases: str, overwrite: bool = False) -> UnitScheme
use_scheme(scheme: Optional[Union[str, UnitScheme]]) -> ContextManager[Optional[UnitScheme]]
convert_to_scheme(obj: Any, scheme: Optional[Union[str, UnitScheme]] = None) -> Any
```

* `set_scheme` (also aliased as `set_unit_scheme`): Activates a scheme globally by registered name (case-insensitive) or `UnitScheme` instance. Pass `None` or `"none"` to disable.
* `get_scheme`: Returns the currently active `UnitScheme` (or `None`), or retrieves a registered scheme by `name`.
* `use_scheme`: Context manager to temporarily apply a scheme within a `with` block.
* `convert_to_scheme`: Explicitly converts a `Quantity` (or `Unit`) to the target scheme (defaults to the active scheme).

### `UnitScheme` Class

```python
UnitScheme(
    name: str,
    *,
    length: Optional[Unit] = None,
    mass: Optional[Unit] = None,
    time: Optional[Unit] = None,
    current: Optional[Unit] = None,
    temperature: Optional[Unit] = None,
    amount: Optional[Unit] = None,
    luminous: Optional[Unit] = None,
    angle: Optional[Unit] = None,
    units: Iterable[Unit] = (),
    description: str = "",
    convert_temperature: bool = True
)
```

**Key Methods:**
* `.set_unit(unit: Unit) -> UnitScheme`: Assigns a named unit for its dimension within the scheme.
* `.remove_unit(unit_or_dimension: Union[Unit, Dimension]) -> UnitScheme`: Removes a named unit so the dimension falls back to its coherent base composition.
* `.copy(name: Optional[str] = None) -> UnitScheme`: Creates an independent copy of an existing scheme for customization.
* `.unit_for(dimension: Dimension) -> Optional[Unit]`: Resolves the target `Unit` for a given `Dimension`.
* `.convert(obj: Any) -> Any`: Expresses a `Quantity` or `Unit` in the scheme.
* `.describe() -> str`: Returns a human-readable summary of base and named units.

### Explicit Conversion Methods on `Quantity` and `Data`

```python
Quantity.to_scheme(scheme: Optional[Union[str, UnitScheme]] = None) -> Quantity
Data.to_scheme(scheme: Optional[Union[str, UnitScheme]] = None) -> Data
```

Returns a converted copy of the `Quantity` or `Data` object expressed in the given scheme (or the active scheme if `scheme=None`), useful for exporting data or working without an active global scheme.

---

## 4. Usage Examples

### Basic Usage & Temporary Contexts

```python
from elevenone import *
from elevenone.unit_scheme import set_scheme, use_scheme, reset_scheme

# Define quantities in mixed units
F = 500 * N
d = 20 * cm
W = F * d

print(W)  # Output: 10000.0 N·cm

# Activate SI globally
set_scheme("SI")
print(W)  # Output: 100.0 J (displayed in J, underlying value remains 10000.0 N·cm)

# Temporarily switch to CGS for a specific block
with use_scheme("CGS"):
    print(W)  # Output: 1000000000.0 erg

# Returns automatically to SI
print(W)  # Output: 100.0 J

# Disable schemes
reset_scheme()
```

### Integration with `Data` and Plotting

```python
import numpy as np
from elevenone import *
from elevenone.unit_scheme import set_scheme, use_scheme

df = Data({
    "Distance": np.array([1.0, 2.0, 3.0]) * km,
    "Energy": np.array([1.0, 4.0, 9.0]) * kWh
})

set_scheme("SI")
print(df)  # Columns automatically display as 'Distance [m]' and 'Energy [J]'

# Plot using imperial units without modifying the underlying Data object
with use_scheme("imperial"):
    fig, ax = df.plot(x="Distance", y="Energy", title="Energy vs Distance")
    # Axis labels automatically render as 'Distance [ft]' and 'Energy [ft·lbf]'

# Export a permanently converted copy of the dataset
df_cgs = df.to_scheme("CGS")
```

### Creating & Customizing Schemes

```python
from elevenone import *
from elevenone.unit_scheme import UnitScheme, register_scheme, get_scheme, set_scheme

# Option A: Build a custom scheme from scratch
lab_scheme = UnitScheme(
    name="lab",
    length=mm,
    time=ms,
    units=[kPa, mA, mV],
    description="Benchtop microfluidics and sensor scheme"
)
register_scheme(lab_scheme)
set_scheme("lab")

# Option B: Clone and modify a built-in scheme
si_km = get_scheme("SI").copy("SI-km")
si_km.set_unit(km)
register_scheme(si_km)
set_scheme("SI-km")
```
