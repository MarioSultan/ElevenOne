# Scientific & Laboratory Constants (`constants`)

The `constants` module provides a comprehensive library of mathematical, physical, chemical, astronomical, geological, biological, and clinical constants. Every constant is implemented as an ElevenOne `Quantity` object with full dimensional tracking and $1\sigma$ standard uncertainties (CODATA 2022 / SI reference values) where experimentally determined.

---

## 1. Core Design Features

* **Full Dimensional Tracking:** All constants carry their exact physical `Dimension` and SI units, preventing dimensional mismatches in calculations.
* **Built-in Experimental Uncertainties ($1\sigma$):** Measured physical constants (such as $G$, $\varepsilon_0$, $m_e$, or $t_{1/2}$ of $^{14}\text{C}$) include their standard $1\sigma$ uncertainty, which automatically propagates through arithmetic operations.
* **Exact SI Defining Constants:** Fundamental constants fixed by the 2019 SI revision ($c$, $h$, $e$, $k_B$, $N_A$, $K_{\text{cd}}$, $\Delta\nu_{\text{Cs}}$) are stored with zero uncertainty.
* **Descriptive Names & Standard Symbols:** Most fundamental constants can be accessed both by their full uppercase name (e.g., `SPEED_OF_LIGHT`, `PLANCK_CONSTANT`) and their standard scientific symbol alias (e.g., `c`, `h`, `hbar`, `k_B`, `N_A`).

---

## 2. Constant Categories

The library is organized into 9 scientific domains:

### 2.1 Mathematical & Dimensionless Constants
Pure mathematical constants stored with `DIMENSIONLESS_UNIT`:
* `PI` ($\pi$), `TAU` ($2\pi$), `EULER_E` ($e$), `GOLDEN_RATIO` ($\varphi$), `EULER_MASCHERONI` ($\gamma$), `SQRT2` ($\sqrt{2}$), `SQRT3` ($\sqrt{3}$), `LN2` ($\ln 2$), `LN10` ($\ln 10$).

### 2.2 Fundamental Universal & Quantum Constants (CODATA 2022)
| Constant Name | Symbol Alias | Value & Unit | $1\sigma$ Uncertainty |
| :--- | :--- | :--- | :--- |
| `SPEED_OF_LIGHT` | `c` | $299\,792\,458\ \text{m/s}$ | Exact |
| `PLANCK_CONSTANT` | `h` | $6.62607015 \times 10^{-34}\ \text{J}\cdot\text{s}$ | Exact |
| `REDUCED_PLANCK_CONSTANT` | `hbar` | $1.054571817\dots \times 10^{-34}\ \text{J}\cdot\text{s}$ | Exact |
| `ELEMENTARY_CHARGE` | `e_charge` | $1.602176634 \times 10^{-19}\ \text{C}$ | Exact |
| `BOLTZMANN_CONSTANT` | `k_B` | $1.380649 \times 10^{-23}\ \text{J/K}$ | Exact |
| `AVOGADRO_CONSTANT` | `N_A` | $6.02214076 \times 10^{23}\ \text{mol}^{-1}$ | Exact |
| `GRAVITATIONAL_CONSTANT` | `G` | $6.67430 \times 10^{-11}\ \text{m}^3\cdot\text{kg}^{-1}\cdot\text{s}^{-2}$ | $1.5 \times 10^{-15}$ |
| `VACUUM_ELECTRIC_PERMITTIVITY` | `epsilon_0` | $8.8541878188 \times 10^{-12}\ \text{F/m}$ | $1.4 \times 10^{-21}$ |
| `VACUUM_MAGNETIC_PERMEABILITY` | `mu_0` | $1.25663706127 \times 10^{-6}\ \text{N/A}^2$ | $2.0 \times 10^{-16}$ |
| `COULOMB_CONSTANT` | `k_e` | $8.9875517862 \times 10^{9}\ \text{N}\cdot\text{m}^2/\text{C}^2$ | $1.4$ |
| `IMPEDANCE_OF_FREE_SPACE` | `Z_0` | $376.730313412\ \Omega$ | $5.9 \times 10^{-8}$ |
| `FINE_STRUCTURE_CONSTANT` | `alpha` | $7.2973525643 \times 10^{-3}$ | $1.1 \times 10^{-12}$ |

### 2.3 Atomic, Subatomic & Nuclear Physics
* **Particle Masses:** `ELECTRON_MASS` (`m_e`), `PROTON_MASS` (`m_p`), `NEUTRON_MASS` (`m_n`), `MUON_MASS` (`m_mu`), `TAU_MASS` (`m_tau`), `DEUTERON_MASS` (`m_d`), `HELION_MASS` (`m_h`), `ALPHA_PARTICLE_MASS` (`m_alpha`), `ATOMIC_MASS_CONSTANT` (`u_mass`).
* **Atomic & Quantum Scales:** `BOHR_RADIUS` (`a_0`), `CLASSICAL_ELECTRON_RADIUS` (`r_e`), `COMPTON_WAVELENGTH` (`lambda_C`), `RYDBERG_CONSTANT` (`R_inf`), `HARTREE_ENERGY` (`E_h`), `THOMSON_CROSS_SECTION` (`sigma_e`).
* **Magnetic & Quantum Electrical Standards:** `BOHR_MAGNETON` (`mu_B`), `NUCLEAR_MAGNETON` (`mu_N`), `MAGNETIC_FLUX_QUANTUM` (`Phi_0`), `CONDUCTANCE_QUANTUM` (`G_0`), `JOSEPHSON_CONSTANT` (`K_J`), `VON_KLITZING_CONSTANT` (`R_K`), `GYROMAGNETIC_RATIO_PROTON` (`gamma_p`), `FERMI_COUPLING_CONSTANT`, `WEAK_MIXING_ANGLE`.

### 2.4 Thermodynamics, Radiation & Statistical Mechanics
* **Gas & Radiation Laws:** `MOLAR_GAS_CONSTANT` (`R_gas`), `FARADAY_CONSTANT` (`F_const`), `STEFAN_BOLTZMANN_CONSTANT` (`sigma_SB`), `FIRST_RADIATION_CONSTANT` (`c_1`), `SECOND_RADIATION_CONSTANT` (`c_2`), `WIEN_WAVELENGTH_DISPLACEMENT` (`b_wien`), `LOSCHMIDT_CONSTANT_STP` (`n_0`).
* **Standard Reference States:** `STANDARD_ATMOSPHERE` (`P_atm`), `STANDARD_STATE_PRESSURE` (`P_std`), `STANDARD_TEMPERATURE_STP` (`T_stp`), `STANDARD_AMBIENT_TEMPERATURE` (`T_satp`), `WATER_TRIPLE_POINT_TEMP`, `MOLAR_VOLUME_IDEAL_GAS_STP`.

### 2.5 Chemistry, Electrochemistry & Laboratory Reagents
* **Molar Masses:** `MOLAR_MASS_H2O`, `MOLAR_MASS_D2O`, `MOLAR_MASS_CO2`, `MOLAR_MASS_O2`, `MOLAR_MASS_N2`, `MOLAR_MASS_H2`, `MOLAR_MASS_DRY_AIR`, `MOLAR_MASS_NACL`, `MOLAR_MASS_HCL`, `MOLAR_MASS_H2SO4`, `MOLAR_MASS_NAOH`, `MOLAR_MASS_ETHANOL`, `MOLAR_MASS_GLUCOSE`.
* **Water Properties:** `WATER_DENSITY_4C`, `WATER_DENSITY_20C`, `WATER_DENSITY_25C`, `WATER_SPECIFIC_HEAT_25C`, `WATER_HEAT_OF_FUSION`, `WATER_HEAT_OF_VAPORIZATION_100C`, `WATER_DYNAMIC_VISCOSITY_20C`, `WATER_SURFACE_TENSION_20C`, `WATER_REFRACTIVE_INDEX_20C`, `WATER_ION_PRODUCT_KW_25C`.
* **Electrochemistry:** `NERNST_SLOPE_25C` ($0.059159\ \text{V}$), `THERMAL_VOLTAGE_25C` ($0.0256926\ \text{V}$), `DEBYE_LENGTH_WATER_1M_25C`.

### 2.6 Engineering, Materials Science & Fluid Mechanics
* **Gravity & Acoustics:** `STANDARD_GRAVITY` (`g_0`), `SPEED_OF_SOUND_AIR_20C`, `SPEED_OF_SOUND_AIR_0C`, `SPEED_OF_SOUND_WATER_25C`.
* **Dry Air Properties:** `AIR_DENSITY_20C`, `AIR_SPECIFIC_HEAT_CP_20C`, `AIR_ADIABATIC_INDEX`, `AIR_DYNAMIC_VISCOSITY_20C`, `AIR_THERMAL_CONDUCTIVITY_20C`.
* **Structural & Electronic Materials:** Densities, Young's moduli, thermal conductivities, and electrical resistivities for `STEEL_*`, `ALUMINUM_*`, `COPPER_*`, `SILICON_*`, `MERCURY_DENSITY_20C`, `GLYCEROL_*`, `FUSED_SILICA_REFRACTIVE_INDEX_589NM`.

### 2.7 Geology, Geophysics & Astrophysics
* **Earth & Solar System:** `EARTH_MASS` (`M_earth`), `EARTH_GM` (`GM_earth`), `EARTH_MEAN_RADIUS` (`R_earth`), `EARTH_ANGULAR_VELOCITY` (`omega_earth`), `SOLAR_CONSTANT` (`S_0`), `SOLAR_MASS` (`M_sun`), `SOLAR_RADIUS` (`R_sun`), `SOLAR_LUMINOSITY` (`L_sun`), `ASTRONOMICAL_UNIT` (`AU`), `PARSEC` (`pc`), `LIGHT_YEAR` (`ly_const`), `LUNAR_MASS`, `LUNAR_MEAN_DISTANCE`.
* **Geophysics & Geochronology:** `EARTH_SURFACE_MAGNETIC_FIELD_MEAN`, `GEOTHERMAL_HEAT_FLUX_MEAN`, `SEAWATER_MEAN_DENSITY`, `CONTINENTAL_CRUST_DENSITY`, `GRANITE_P_WAVE_VELOCITY`, and half-lives / decay constants for $^{14}\text{C}$, $^{238}\text{U}$, $^{235}\text{U}$, $^{232}\text{Th}$, $^{40}\text{K}$, and $^{87}\text{Rb}$.

### 2.8 Biology, Biochemistry & Molecular Biology
* **Nucleic Acids & Proteins:** B-form DNA structural constants (`DNA_BP_RISE_B_FORM`, `DNA_HELIX_PITCH_B_FORM`), average residue molar masses (`MOLAR_MASS_DNA_BP_AVERAGE`, `MOLAR_MASS_AMINO_ACID_AVERAGE`), and $A_{260}$ spectrophotometric factors (`DSDNA_A260_CONCENTRATION`, `SSRNA_A260_CONCENTRATION`).
* **Membrane Biophysics & Buffers:** `ATP_HYDROLYSIS_DG0`, `LIPID_BILAYER_SPECIFIC_CAPACITANCE`, `NEURON_RESTING_POTENTIAL`, and standard buffer $\text{p}K_a$ values (`PKA_HEPES`, `PKA_TRIS`, `PKA_MES`, `PKA_PHOSPHATE_2`, etc.).

### 2.9 Medicine, Clinical Laboratory & Human Physiology
* **Cardiovascular & Anthropometric:** `HUMAN_BODY_TEMP_NORMAL` ($310.15\ \text{K}$), `HUMAN_REFERENCE_BSA` ($1.73\ \text{m}^2$), `BLOOD_DENSITY`, `BLOOD_VISCOSITY_37C`, `BLOOD_PH_ARTERIAL`, `CARDIAC_OUTPUT_RESTING`, `SYSTOLIC_BP_NORMAL`, `DIASTOLIC_BP_NORMAL`.
* **Clinical Chemistry & Hematology:** `SERUM_SODIUM_NORMAL`, `SERUM_POTASSIUM_NORMAL`, `FASTING_GLUCOSE_NORMAL`, `HEMOGLOBIN_MOLAR_MASS`, `HUFNER_CONSTANT`, `GFR_NORMAL`, `TIDAL_VOLUME_NORMAL`.
* **Medical Imaging & Dosimetry:** Radioisotope half-lives and photon energies (`TC99M_HALF_LIFE`, `TC99M_GAMMA_ENERGY`, `FDG_F18_HALF_LIFE`, `ANNIHILATION_PHOTON_ENERGY`, `I131_HALF_LIFE`, `CO60_HALF_LIFE`), `ULTRASOUND_SPEED_SOFT_TISSUE`, and MRI Larmor frequency (`PROTON_GYROMAGNETIC_FREQUENCY_PER_TESLA`).

---

## 3. Usage Examples

### Basic Calculations & Automatic Error Propagation

```python
from elevenone import *
from elevenone.constants import G, M_earth, R_earth, h, c

# 1. Gravitational acceleration at Earth's surface (propagates uncertainties from G and M_earth)
g_surface = (G * M_earth) / (R_earth ** 2)
print(g_surface)
# Output: (9.79828... ± 2.3e-05) m/s²

# 2. Photon energy at 532 nm
wavelength = 532 * nm
E_photon = (h * c) / wavelength
print(E_photon.convert_to(eV))
# Output: 2.33053... eV
```

### Working with Unit Schemes & Chemistry / Clinical Constants

```python
from elevenone import *
from elevenone.constants import R_gas, T_satp, F_const, BLOOD_OSMOLARITY_NORMAL
from elevenone.unit_scheme import use_scheme

# Compute Nernst potential at 25 °C (298.15 K)
E_nernst = (R_gas * T_satp) / F_const
print(E_nernst)  # Output: 0.0256926... V

# Display physiological constants in CGS or custom units
with use_scheme("CGS"):
    print(BLOOD_OSMOLARITY_NORMAL)
```