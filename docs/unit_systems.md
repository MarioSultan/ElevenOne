# ElevenOne Unit Systems Guide

The `ElevenOne` library offers modular unit conversion and physical dimension management. Importing the main package automatically includes the basic, everyday unit system. Additional specialized unit packages can be loaded as needed.

```python
# Automatically loaded:
from elevenone import *  # Loads basic_units.py

# Optional specialized modules:
from elevenone.si_units import *
from elevenone.engineering_units import *
from elevenone.imperial_units import *
from elevenone.physics_units import *
from elevenone.chemistry_units import *
from elevenone.geology_units import *
from elevenone.cgs_units import *
from elevenone.medical_units import *
```

---

## Unit Systems Breakdown

The table below lists all supported unit modules, ordered from **most general-purpose** to **highly specialized domain-specific** systems. Within each system, units are grouped by physical dimension and ordered into **Simple (Base/Fundamental)**, **Derived (Combined/Compound)**, and **Specialized (Domain/Named)** units.

| Module System | Included Units (Simple $\rightarrow$ Combined $\rightarrow$ Specialized) |
| :--- | :--- |
| **Basic Units**<br>`basic_units.py`<br>*(Default / Always Loaded)* | **Simple / Base:**<br>• *Length:* `m`, `km`, `cm`, `mm`, `um` ($\mu\text{m}$), `nm`, `inch`, `ft`, `yd`, `mi`, `nmi`, `angstrom` ($\text{\AA}$), `ly`<br>• *Mass:* `kg`, `g`, `mg`, `ug` ($\mu\text{g}$), `ton` ($\text{t}$), `lb`, `oz`, `st`, `cwt`<br>• *Time:* `s`, `ms`, `us` ($\mu\text{s}$), `ns`, `min_unit`, `h`, `day`, `week`, `year`<br>• *Temperature:* `K`, `degC` ($^\circ\text{C}$), `degF` ($^\circ\text{F}$), `R` ($^\circ\text{R}$)<br>• *Current & Charge:* `A`, `mA`, `uA` ($\mu\text{A}$), `C`, `Ah`, `mAh`<br>• *Angle / Freq:* `rad`, `deg`, `Hz`<br><br>**Derived & Combined:**<br>• *Voltage & Resistance:* `V`, `mV`, `kV`, `Ohm` ($\Omega$), `kOhm`, `MOhm`<br>• *Force & Pressure:* `N`, `kN`, `MN`, `lbf`, `dyn`, `Pa`, `kPa`, `MPa`, `bar`, `mbar`, `psi`, `atm`, `mmHg`<br>• *Energy & Power:* `J`, `kJ`, `MJ`, `cal`, `kcal`, `kWh`, `eV`, `BTU`, `W`, `kW`, `MW`, `HP`<br>• *Volume:* `L`, `mL`, `m3` ($\text{m}^3$), `gal`<br>• *Dimensionless:* `counts` |
| **SI Comprehensive**<br>`si_units.py` | **Simple / Base:**<br>• *Metric Standard:* Full SI prefixes (`y`, `z`, `a`, `f`, `p`, `n`, `u`, `m`, `c`, `d`, `da`, `h`, `k`, `M`, `G`, `T`, `P`, `E`, `Z`, `Y`) for `m`, `g`/`kg`, `s`, `A`, `K`, `mol`, `cd`, `rad`, `sr`<br><br>**Derived & Combined:**<br>• *Standard SI Derived:* `Hz`, `N`, `Pa`, `J`, `W`, `C`, `V`, `F`, `Ohm` ($\Omega$), `S`, `Wb`, `T`, `H`, `lm`, `lx`, `Bq`, `Gy`, `Sv`, `kat`<br>• *Kinematics & Dynamics:* `m/s`, `km/h`, `m/s²`, `kg/m³`, `g/cm³`, `g/mL`<br>• *Transport & Thermal:* `Pa·s`, `mPa·s`, `m²/s`, `J/K`, `J/(kg·K)`, `W/(m·K)`<br>• *Molarity & Area/Vol:* `m²`, `cm²`, `mm²`, `km²`, `ha`, `m³`, `L`, `mL`, `μL`, `cL`, `dL`, `cm³`, `mol/m³`, `M`, `mM` |
| **Engineering**<br>`engineering_units.py` | **Simple / Base:**<br>• *Imperial/Customary:* `in`, `ft`, `yd`, `mi`, `nmi`, `lb`, `oz`, `slug`<br><br>**Derived & Combined:**<br>• *Mechanical / Civil:* `psi`, `ksi`, `MPa`, `GPa`, `bar`, `lbf`, `kip`, `kgf`, `kN`, `MN`, `N·m`, `kN·m`, `lb·ft`, `lb·in`, `pcf` ($\text{lb/ft}^3$), `kN/m³`<br>• *Electrical & Power:* `hp`, `PS`, `kW`, `MW`, `VA`, `kVA`, `MVA`, `var`, `kvar`, `Mvar`, `GΩ`, `mΩ`, `S`, `mS`, `μS`, `μF`, `nF`, `pF`, `mH`, `μH`, `kHz`, `MHz`, `GHz`, `MWh`<br>• *Fluids & HVAC:* `m³/s`, `m³/h`, `cfm`, `gpm`, `L/s`, `kg/s`, `t/h`, `BTU/h`, `TR` (ton of refrigeration), `thm` (therm)<br>• *Surveying & Permeability:* `acre`, `sq_ft`, `ha`, `yd³`, `cm/s`, `Darcy`, `mD` |
| **Imperial & US Customary**<br>`imperial_units.py` | **Simple / Base:**<br>• *Length:* `thou`/`mil`, `in`, `ft`, `yd`, `fathom`, `rod`/`pole`/`perch`, `chain`, `furlong`, `mi`, `nmi`, `league`<br>• *Mass:* `grain` (`gr`), `dram`, `oz`, `lb`, `stone`, `quarter` (`qr`), `cwt` (UK/US), `ton` (UK long / US short), `slug`, `pennyweight` (`dwt`), `oz_t` (troy), `lb t` (troy)<br>• *Temperature:* `°F`, `°R`<br><br>**Derived & Combined:**<br>• *Area:* `in²`, `ft²`, `yd²`, `rd²`, `rood`, `acre`, `mi²`<br>• *Volume:* `fl oz` (imp/US), `gill`, `pt`, `qt`, `gal` (imp/US), `peck`, `bushel`, `in³`, `ft³`, `yd³`<br>• *Force, Torque & Stress:* `lbf`, `poundal` (`pdl`), `kip`, `lb·ft`, `lb·in`, `psi`, `ksi`, `psf`, `inHg`, `inH2O`<br>• *Energy & Power:* `BTU`, `ft·lbf`, `hp`, `BTU/h` |
| **Physics**<br>`physics_units.py` | **Simple / Base:**<br>• *Particle/Atomic Mass:* `u`/`Da`, `m_e`, `m_p`, `m_n`<br>• *Astrophysics Mass/Radius:* `M_sun`, `M_jup`, `M_earth`, `R_sun`, `R_jup`, `R_earth`<br><br>**Derived & Combined:**<br>• *Astrophysics & Cosmology:* `au`, `pc`, `kpc`, `Mpc`, `Gpc`, `ly`, `LD`, `L_sun`, `a` (julian year), `yr_sid`, `t_H` (Hubble time)<br>• *Atomic & Cross-Section:* `a_0`, `r_e`, `Å`, `fm`, `barn` (`b`, `mb`, `μb`, `nb`, `pb`), `e`, `statC`/`esu`, `E_h` (Hartree), `Ry`, `cm⁻¹` (kayser)<br>• *Natural / Planck Units:* `l_P`, `m_P`, `t_P`, `T_P`, `q_P`, `E_P`, `F_P`, `P_P`, `rho_P`, `p_P`<br>• *Radiology & Dosimetry:* `Ci`, `mCi`, `μCi`, `Rd`, `R`, `rad`, `rem`, `mrem` |
| **Chemistry**<br>`chemistry_units.py` | **Simple / Base:**<br>• *Amount:* `mol`, `μmol`, `mmol`, `kmol`, `lb-mol`<br>• *Atomic Mass:* `amu`, `Da`, `kDa`, `MDa`<br><br>**Derived & Combined:**<br>• *Concentration & Molarity:* `M`, `mM`, `μM`, `nM`, `pM`, `fM`, `aM`, `mol/m³`, `molal` ($\text{mol/kg}$)<br>• *Mass Conc & Density:* `g/L`, `mg/L`, `μg/L`, `g/mL`, `g/cm³`<br>• *Dimensionless Ratios:* `%`, `‰`, `ppm`, `ppb`, `ppt`<br>• *Thermochemistry & Enthalpy:* `cal`, `kcal`, `J`, `kJ`, `BTU`, `J/mol`, `kJ/mol`, `cal/mol`, `kcal/mol`, `J/K`, `J/(mol·K)`, `cal/(mol·K)`, `e.u.`<br>• *Viscosity & Electrochemistry:* `P`, `cP`, `St`, `cSt`, `kat`, `U` (enzyme unit), `F_const` (Faraday), `S`, `mS`, `μS`, `S/m`, `S·cm²/mol`, `Ci`, `Bq` |
| **Geology**<br>`geology_units.py` | **Simple / Base:**<br>• *Deep Time:* `ka`, `Ma`, `Ga`, `yr`<br>• *Geophysical Length:* `km`, `m`, `cm`, `mm`, `μm`, `Å`<br>• *Earth Metrics:* `M_earth`, `R_earth`<br><br>**Derived & Combined:**<br>• *Petroleum & Permeability:* `bbl` (barrel), `ft³`, `acft` (acre-foot), `gal`, `Darcy`, `mD`<br>• *Density & Pressure:* `g/cm³`, `kg/m³`, `GPa`, `MPa`, `bar`, `kbar`, `Mbar`, `atm`<br>• *Geothermal & Geophysics:* `HFU` (heat flow unit), `mW/m²`, `T`, `nT`, `gamma`, `G`, `Gal` ($\text{cm/s}^2$), `mGal`, `μGal`, `phi` (grain size scale) |
| **CGS System**<br>`cgs_units.py` | **Simple / Base:**<br>• *Base CGS:* `cm`, `g`, `s`<br><br>**Derived & Combined:**<br>• *Mechanical CGS:* `cm²`, `cm³`/`cc`, `Gal` ($\text{cm/s}^2$), `dyn`, `erg`, `Ba` (barye), `P`, `cP`, `St`, `cSt`<br>• *Gaussian Electromagnetism:* `statC`/`esu`/`franklin`, `statA`, `statV`, `statΩ`, `statF`, `statH`, `G` (gauss), `mG`, `μG`, `gamma`, `Mx` (maxwell), `Oe` (oersted), `erg/G`, `emu`<br>• *Photometry:* `ph` (phot), `sb` (stilb), `lambert` |
| **Medical**<br>`medical_units.py` | **Simple / Base:**<br>• *Substance & Equivalents:* `Eq`, `mEq`, `osm`, `mOsm`, `IU`, `U`, `mU`, `μU`<br>• *Clinical Weight & Vol:* `kg`, `g`, `mg`, `mcg`/`μg`, `dL`, `mL`, `μL`, `cc`, `gtt` (drops), `mcgtt`<br><br>**Derived & Combined:**<br>• *Clinical Biochemistry:* `mg/dL`, `μg/dL`, `ng/dL`, `pg/mL`, `ng/mL`, `μg/mL`, `mg/L`, `g/dL`, `mM`, `μM`, `nM`, `pM`, `fM`, `mEq/L`, `mOsm/kg`, `mOsm/L`, `mg/kg`, `μg/kg`<br>• *Infusion & Flow:* `mL/h`, `gtt/min`, `L/min`, `L/(min·m²)` (cardiac index)<br>• *Hemodynamics & Vitals:* `mmHg`, `cmH2O`, `Torr`, `WU` (Wood units), `dyn·s/cm⁵`, `bpm`, `brpm`, `MET`<br>• *Radiotherapy & Dosimetry:* `Gy`, `mGy`, `μGy`, `cGy`, `Sv`, `mSv`, `μSv`, `R`, `mR`, `Ci`, `mCi`, `μCi`, `Bq`, `MBq`, `GBq` |

---

## Quick Example Usage

```python
from elevenone import *            # Basic units loaded by default
from elevenone.medical_units import mmHg, mL_per_h
from elevenone.physics_units import M_sun, parsec

# Convert basic units
speed = 100 * (km / h)
print(speed.to(m / s))

# Medical dosage/hemodynamic rate
blood_pressure = 120 * mmHg
infusion = 50 * mL_per_h

# Astrophysics calculations
stellar_mass = 2.5 * M_sun
distance = 10 * parsec
```