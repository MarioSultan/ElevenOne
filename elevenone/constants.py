import numpy as np
from .dimension import *
from .unit import Unit, Quantity, DIMENSIONLESS_UNIT

# ==============================================================================
# ELEVENONE LABORATORY & SCIENTIFIC CONSTANTS LIBRARY
# ==============================================================================
# All constants are defined as Quantity objects with exact or CODATA 2022 /
# standard reference values, complete dimensional tracking, and 1-sigma
# standard uncertainties where experimentally determined.
# ==============================================================================


# ------------------------------------------------------------------------------
# 1. MATHEMATICAL & DIMENSIONLESS CONSTANTS
# ------------------------------------------------------------------------------
PI = Quantity(np.pi, DIMENSIONLESS_UNIT)
TAU = Quantity(2.0 * np.pi, DIMENSIONLESS_UNIT)
EULER_E = Quantity(np.e, DIMENSIONLESS_UNIT)
GOLDEN_RATIO = Quantity((1.0 + np.sqrt(5.0)) / 2.0, DIMENSIONLESS_UNIT)
EULER_MASCHERONI = Quantity(0.57721566490153286060651209008240243, DIMENSIONLESS_UNIT)
SQRT2 = Quantity(np.sqrt(2.0), DIMENSIONLESS_UNIT)
SQRT3 = Quantity(np.sqrt(3.0), DIMENSIONLESS_UNIT)
LN2 = Quantity(np.log(2.0), DIMENSIONLESS_UNIT)
LN10 = Quantity(np.log(10.0), DIMENSIONLESS_UNIT)


# ------------------------------------------------------------------------------
# 2. FUNDAMENTAL UNIVERSAL & QUANTUM CONSTANTS (CODATA 2022 / SI)
# ------------------------------------------------------------------------------
# Exact SI defining constants
SPEED_OF_LIGHT = Quantity(299792458.0, Unit(VELOCITY, "m/s", 1.0))
c = SPEED_OF_LIGHT

PLANCK_CONSTANT = Quantity(6.62607015e-34, Unit(ACTION, "J·s", 1.0))
h = PLANCK_CONSTANT

REDUCED_PLANCK_CONSTANT = Quantity(6.62607015e-34 / (2.0 * np.pi), Unit(ACTION, "J·s", 1.0))
hbar = REDUCED_PLANCK_CONSTANT

ELEMENTARY_CHARGE = Quantity(1.602176634e-19, Unit(CHARGE, "C", 1.0))
e_charge = ELEMENTARY_CHARGE

BOLTZMANN_CONSTANT = Quantity(1.380649e-23, Unit(ENTROPY, "J/K", 1.0))
k_B = BOLTZMANN_CONSTANT

AVOGADRO_CONSTANT = Quantity(6.02214076e23, Unit(1 / AMOUNT, "mol⁻¹", 1.0))
N_A = AVOGADRO_CONSTANT

LUMINOUS_EFFICACY_540THZ = Quantity(683.0, Unit(LUMINOUS_EFFICACY, "lm/W", 1.0))
K_cd = LUMINOUS_EFFICACY_540THZ

HYPERFINE_TRANSITION_CS133 = Quantity(9192631770.0, Unit(FREQUENCY, "Hz", 1.0))

# Measured universal & electromagnetic constants (with 1-sigma uncertainty)
GRAVITATIONAL_CONSTANT = Quantity(
    6.67430e-11, Unit(GRAVITATIONAL_CONSTANT, "m³·kg⁻¹·s⁻²", 1.0), error=1.5e-15
)
G = GRAVITATIONAL_CONSTANT

VACUUM_ELECTRIC_PERMITTIVITY = Quantity(
    8.8541878188e-12, Unit(PERMITTIVITY, "F/m", 1.0), error=1.4e-21
)
epsilon_0 = VACUUM_ELECTRIC_PERMITTIVITY

VACUUM_MAGNETIC_PERMEABILITY = Quantity(
    1.25663706127e-6, Unit(PERMEABILITY, "N/A²", 1.0), error=2.0e-16
)
mu_0 = VACUUM_MAGNETIC_PERMEABILITY

COULOMB_CONSTANT = Quantity(
    8.9875517862e9, Unit(FORCE * AREA / (CHARGE**2), "N·m²/C²", 1.0), error=1.4e0
)
k_e = COULOMB_CONSTANT

IMPEDANCE_OF_FREE_SPACE = Quantity(
    376.730313412, Unit(RESISTANCE, "Ω", 1.0), error=5.9e-8
)
Z_0 = IMPEDANCE_OF_FREE_SPACE

FINE_STRUCTURE_CONSTANT = Quantity(
    7.2973525643e-3, DIMENSIONLESS_UNIT, error=1.1e-12
)
alpha = FINE_STRUCTURE_CONSTANT

INVERSE_FINE_STRUCTURE_CONSTANT = Quantity(
    137.035999177, DIMENSIONLESS_UNIT, error=2.1e-8
)


# ------------------------------------------------------------------------------
# 3. ATOMIC, SUBATOMIC & NUCLEAR PHYSICS CONSTANTS
# ------------------------------------------------------------------------------
# Particle masses
ELECTRON_MASS = Quantity(9.1093837139e-31, Unit(MASS, "kg", 1.0), error=2.8e-40)
m_e = ELECTRON_MASS

PROTON_MASS = Quantity(1.67262192595e-27, Unit(MASS, "kg", 1.0), error=5.2e-37)
m_p = PROTON_MASS

NEUTRON_MASS = Quantity(1.67492750056e-27, Unit(MASS, "kg", 1.0), error=8.5e-37)
m_n = NEUTRON_MASS

MUON_MASS = Quantity(1.883531627e-28, Unit(MASS, "kg", 1.0), error=4.2e-36)
m_mu = MUON_MASS

TAU_MASS = Quantity(3.16754e-27, Unit(MASS, "kg", 1.0), error=2.1e-31)
m_tau = TAU_MASS

DEUTERON_MASS = Quantity(3.3435837768e-27, Unit(MASS, "kg", 1.0), error=1.0e-36)
m_d = DEUTERON_MASS

HELION_MASS = Quantity(5.0064127862e-27, Unit(MASS, "kg", 1.0), error=1.6e-36)
m_h = HELION_MASS

ALPHA_PARTICLE_MASS = Quantity(6.6446573450e-27, Unit(MASS, "kg", 1.0), error=2.1e-36)
m_alpha = ALPHA_PARTICLE_MASS

ATOMIC_MASS_CONSTANT = Quantity(1.66053906892e-27, Unit(MASS, "kg", 1.0), error=5.2e-37)
u_mass = ATOMIC_MASS_CONSTANT

# Atomic scales & electromagnetic quanta
BOHR_RADIUS = Quantity(5.29177210544e-11, Unit(LENGTH, "m", 1.0), error=8.2e-21)
a_0 = BOHR_RADIUS

CLASSICAL_ELECTRON_RADIUS = Quantity(2.8179403205e-15, Unit(LENGTH, "m", 1.0), error=1.3e-24)
r_e = CLASSICAL_ELECTRON_RADIUS

COMPTON_WAVELENGTH = Quantity(2.42631023538e-12, Unit(LENGTH, "m", 1.0), error=7.6e-22)
lambda_C = COMPTON_WAVELENGTH

RYDBERG_CONSTANT = Quantity(10973731.568157, Unit(WAVENUMBER, "m⁻¹", 1.0), error=1.2e-5)
R_inf = RYDBERG_CONSTANT

HARTREE_ENERGY = Quantity(4.3597447222060e-18, Unit(ENERGY, "J", 1.0), error=4.8e-30)
E_h = HARTREE_ENERGY

BOHR_MAGNETON = Quantity(9.2740100657e-24, Unit(MAGNETIC_MOMENT, "J/T", 1.0), error=2.9e-33)
mu_B = BOHR_MAGNETON

NUCLEAR_MAGNETON = Quantity(5.0507837393e-27, Unit(MAGNETIC_MOMENT, "J/T", 1.0), error=1.6e-36)
mu_N = NUCLEAR_MAGNETON

ELECTRON_MAGNETIC_MOMENT = Quantity(-9.2847646917e-24, Unit(MAGNETIC_MOMENT, "J/T", 1.0), error=2.9e-33)
PROTON_MAGNETIC_MOMENT = Quantity(1.41060679545e-26, Unit(MAGNETIC_MOMENT, "J/T", 1.0), error=6.0e-36)
NEUTRON_MAGNETIC_MOMENT = Quantity(-9.6623653e-27, Unit(MAGNETIC_MOMENT, "J/T", 1.0), error=2.3e-33)

ELECTRON_G_FACTOR = Quantity(-2.00231930436092, DIMENSIONLESS_UNIT, error=3.6e-13)
PROTON_G_FACTOR = Quantity(5.5856946893, DIMENSIONLESS_UNIT, error=1.6e-9)

GYROMAGNETIC_RATIO_PROTON = Quantity(2.6752218708e8, Unit(ANGULAR / (MAGNETIC_FIELD * TIME), "rad·s⁻¹·T⁻¹", 1.0), error=1.1e-1)
gamma_p = GYROMAGNETIC_RATIO_PROTON

MAGNETIC_FLUX_QUANTUM = Quantity(2.067833848e-15, Unit(MAGNETIC_FLUX, "Wb", 1.0))
Phi_0 = MAGNETIC_FLUX_QUANTUM

CONDUCTANCE_QUANTUM = Quantity(7.748091729e-5, Unit(CONDUCTANCE, "S", 1.0))
G_0 = CONDUCTANCE_QUANTUM

JOSEPHSON_CONSTANT = Quantity(483597.8484e9, Unit(FREQUENCY / VOLTAGE, "Hz/V", 1.0))
K_J = JOSEPHSON_CONSTANT

VON_KLITZING_CONSTANT = Quantity(25812.80745, Unit(RESISTANCE, "Ω", 1.0))
R_K = VON_KLITZING_CONSTANT

THOMSON_CROSS_SECTION = Quantity(6.6524587051e-29, Unit(AREA, "m²", 1.0), error=6.2e-38)
sigma_e = THOMSON_CROSS_SECTION

FERMI_COUPLING_CONSTANT = Quantity(1.1663787e-5, Unit(1 / (ENERGY**2), "GeV⁻²", 1.0 / (1e9 * 1.602176634e-19)**2), error=6.0e-12)
WEAK_MIXING_ANGLE = Quantity(0.22305, DIMENSIONLESS_UNIT, error=0.00023)


# ------------------------------------------------------------------------------
# 4. THERMODYNAMICS, RADIATION & STATISTICAL MECHANICS
# ------------------------------------------------------------------------------
MOLAR_GAS_CONSTANT = Quantity(8.314462618, Unit(MOLAR_HEAT_CAPACITY, "J·mol⁻¹·K⁻¹", 1.0))
R_gas = MOLAR_GAS_CONSTANT

FARADAY_CONSTANT = Quantity(96485.33212, Unit(CHARGE / AMOUNT, "C/mol", 1.0))
F_const = FARADAY_CONSTANT

STEFAN_BOLTZMANN_CONSTANT = Quantity(5.670374419e-8, Unit(IRRADIANCE / (TEMPERATURE**4), "W·m⁻²·K⁻⁴", 1.0))
sigma_SB = STEFAN_BOLTZMANN_CONSTANT

FIRST_RADIATION_CONSTANT = Quantity(3.741771852e-16, Unit(POWER * AREA, "W·m²", 1.0))
c_1 = FIRST_RADIATION_CONSTANT

FIRST_RADIATION_CONSTANT_SPECTRAL = Quantity(1.191042972e-16, Unit(POWER * AREA / ANGULAR, "W·m²·sr⁻¹", 1.0))
c_1L = FIRST_RADIATION_CONSTANT_SPECTRAL

SECOND_RADIATION_CONSTANT = Quantity(1.438776877e-2, Unit(LENGTH * TEMPERATURE, "m·K", 1.0))
c_2 = SECOND_RADIATION_CONSTANT

WIEN_WAVELENGTH_DISPLACEMENT = Quantity(2.897771955e-3, Unit(LENGTH * TEMPERATURE, "m·K", 1.0))
b_wien = WIEN_WAVELENGTH_DISPLACEMENT

WIEN_FREQUENCY_DISPLACEMENT = Quantity(5.878925757e10, Unit(FREQUENCY / TEMPERATURE, "Hz/K", 1.0))

WIEN_ENTROPY_DISPLACEMENT = Quantity(3.002916077e-3, Unit(LENGTH * TEMPERATURE, "m·K", 1.0))

LOSCHMIDT_CONSTANT_STP = Quantity(2.686780111e25, Unit(1 / VOLUME, "m⁻³", 1.0))
n_0 = LOSCHMIDT_CONSTANT_STP

SACKUR_TETRODE_CONSTANT_1BAR = Quantity(-1.15170753496, DIMENSIONLESS_UNIT, error=4.7e-10)
SACKUR_TETRODE_CONSTANT_1ATM = Quantity(-1.16487052149, DIMENSIONLESS_UNIT, error=4.7e-10)

# Standard Reference States
STANDARD_ATMOSPHERE = Quantity(101325.0, Unit(PRESSURE, "Pa", 1.0))
P_atm = STANDARD_ATMOSPHERE

STANDARD_STATE_PRESSURE = Quantity(100000.0, Unit(PRESSURE, "Pa", 1.0))
P_std = STANDARD_STATE_PRESSURE

STANDARD_TEMPERATURE_STP = Quantity(273.15, Unit(TEMPERATURE, "K", 1.0))
T_stp = STANDARD_TEMPERATURE_STP

STANDARD_AMBIENT_TEMPERATURE = Quantity(298.15, Unit(TEMPERATURE, "K", 1.0))
T_satp = STANDARD_AMBIENT_TEMPERATURE

ABSOLUTE_ZERO_CELSIUS = Quantity(-273.15, Unit(TEMPERATURE, "°C", 1.0, offset=273.15))

WATER_TRIPLE_POINT_TEMP = Quantity(273.16, Unit(TEMPERATURE, "K", 1.0))
WATER_TRIPLE_POINT_PRESSURE = Quantity(611.657, Unit(PRESSURE, "Pa", 1.0))

MOLAR_VOLUME_IDEAL_GAS_STP = Quantity(0.02271095464, Unit(MOLAR_VOLUME, "m³/mol", 1.0))       # At 273.15 K, 1 bar
MOLAR_VOLUME_IDEAL_GAS_1ATM = Quantity(0.02241396954, Unit(MOLAR_VOLUME, "m³/mol", 1.0))      # At 273.15 K, 1 atm


# ------------------------------------------------------------------------------
# 5. CHEMISTRY, ELECTROCHEMISTRY & LABORATORY REAGENTS
# ------------------------------------------------------------------------------
# Common Molar Masses
MOLAR_MASS_H2O = Quantity(0.01801528, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_D2O = Quantity(0.0200276, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_CO2 = Quantity(0.0440095, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_O2 = Quantity(0.0319988, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_N2 = Quantity(0.0280134, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_H2 = Quantity(0.00201588, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_HE = Quantity(0.004002602, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_AR = Quantity(0.039948, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_DRY_AIR = Quantity(0.0289647, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_NACL = Quantity(0.058443, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_HCL = Quantity(0.0364609, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_H2SO4 = Quantity(0.098079, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_NAOH = Quantity(0.039997, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_ETHANOL = Quantity(0.0460684, Unit(MOLAR_MASS, "kg/mol", 1.0))
MOLAR_MASS_GLUCOSE = Quantity(0.180156, Unit(MOLAR_MASS, "kg/mol", 1.0))

# Water physical-chemical properties (at 25 °C / 298.15 K, 1 atm unless noted)
WATER_DENSITY_4C = Quantity(999.972, Unit(DENSITY, "kg/m³", 1.0))
WATER_DENSITY_20C = Quantity(998.2071, Unit(DENSITY, "kg/m³", 1.0))
WATER_DENSITY_25C = Quantity(997.0479, Unit(DENSITY, "kg/m³", 1.0))
WATER_SPECIFIC_HEAT_25C = Quantity(4181.3, Unit(SPECIFIC_HEAT, "J·kg⁻¹·K⁻¹", 1.0))
WATER_HEAT_OF_FUSION = Quantity(333550.0, Unit(SPECIFIC_ENERGY, "J/kg", 1.0))
WATER_HEAT_OF_VAPORIZATION_100C = Quantity(2256400.0, Unit(SPECIFIC_ENERGY, "J/kg", 1.0))
WATER_DYNAMIC_VISCOSITY_20C = Quantity(1.0016e-3, Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0))
WATER_DYNAMIC_VISCOSITY_25C = Quantity(8.900e-4, Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0))
WATER_SURFACE_TENSION_20C = Quantity(0.07286, Unit(SURFACE_TENSION, "N/m", 1.0))
WATER_THERMAL_CONDUCTIVITY_25C = Quantity(0.6065, Unit(THERMAL_CONDUCTIVITY, "W·m⁻¹·K⁻¹", 1.0))
WATER_REFRACTIVE_INDEX_20C = Quantity(1.332986, DIMENSIONLESS_UNIT)
WATER_DIELECTRIC_CONSTANT_25C = Quantity(78.36, DIMENSIONLESS_UNIT)
WATER_ION_PRODUCT_KW_25C = Quantity(1.008e-14, Unit(MOLAR_CONCENTRATION**2, "mol²/m⁶", 1000.0**2))
WATER_EBULLIOSCOPIC_CONSTANT = Quantity(0.512, Unit(TEMPERATURE * MASS / AMOUNT, "K·kg·mol⁻¹", 1.0))
WATER_CRYOSCOPIC_CONSTANT = Quantity(1.86, Unit(TEMPERATURE * MASS / AMOUNT, "K·kg·mol⁻¹", 1.0))

# Electrochemistry & Physical Chemistry
NERNST_SLOPE_25C = Quantity(0.059159, Unit(VOLTAGE, "V", 1.0))  # (RT/F) * ln(10) at 298.15 K
THERMAL_VOLTAGE_25C = Quantity(0.0256926, Unit(VOLTAGE, "V", 1.0))  # k_B * T / e at 298.15 K
DEBYE_LENGTH_WATER_1M_25C = Quantity(3.04e-10, Unit(LENGTH, "m", 1.0))
CARBON_12_MOLAR_MASS = Quantity(0.012, Unit(MOLAR_MASS, "kg/mol", 1.0))


# ------------------------------------------------------------------------------
# 6. ENGINEERING, MATERIALS SCIENCE & FLUID MECHANICS
# ------------------------------------------------------------------------------
STANDARD_GRAVITY = Quantity(9.80665, Unit(ACCELERATION, "m/s²", 1.0))
g_0 = STANDARD_GRAVITY

# Dry Air Properties (at 20 °C, 1 atm)
AIR_DENSITY_20C = Quantity(1.2041, Unit(DENSITY, "kg/m³", 1.0))
AIR_DENSITY_0C = Quantity(1.2922, Unit(DENSITY, "kg/m³", 1.0))
AIR_SPECIFIC_HEAT_CP_20C = Quantity(1005.0, Unit(SPECIFIC_HEAT, "J·kg⁻¹·K⁻¹", 1.0))
AIR_SPECIFIC_HEAT_CV_20C = Quantity(718.0, Unit(SPECIFIC_HEAT, "J·kg⁻¹·K⁻¹", 1.0))
AIR_ADIABATIC_INDEX = Quantity(1.40, DIMENSIONLESS_UNIT)
AIR_DYNAMIC_VISCOSITY_20C = Quantity(1.825e-5, Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0))
AIR_KINEMATIC_VISCOSITY_20C = Quantity(1.516e-5, Unit(KINEMATIC_VISCOSITY, "m²/s", 1.0))
AIR_THERMAL_CONDUCTIVITY_20C = Quantity(0.02587, Unit(THERMAL_CONDUCTIVITY, "W·m⁻¹·K⁻¹", 1.0))
SPEED_OF_SOUND_AIR_20C = Quantity(343.21, Unit(VELOCITY, "m/s", 1.0))
SPEED_OF_SOUND_AIR_0C = Quantity(331.3, Unit(VELOCITY, "m/s", 1.0))
SPEED_OF_SOUND_WATER_25C = Quantity(1497.0, Unit(VELOCITY, "m/s", 1.0))
AIR_REFRACTIVE_INDEX_STP = Quantity(1.000293, DIMENSIONLESS_UNIT)

# Reference Solid & Liquid Properties (Room Temp ~20 °C)
MERCURY_DENSITY_20C = Quantity(13545.8, Unit(DENSITY, "kg/m³", 1.0))
ETHANOL_DENSITY_20C = Quantity(789.3, Unit(DENSITY, "kg/m³", 1.0))
GLYCEROL_DENSITY_20C = Quantity(1261.3, Unit(DENSITY, "kg/m³", 1.0))
GLYCEROL_DYNAMIC_VISCOSITY_20C = Quantity(1.412, Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0))

STEEL_DENSITY = Quantity(7850.0, Unit(DENSITY, "kg/m³", 1.0))
STEEL_YOUNGS_MODULUS = Quantity(200.0e9, Unit(PRESSURE, "Pa", 1.0))
STEEL_POISSON_RATIO = Quantity(0.30, DIMENSIONLESS_UNIT)

ALUMINUM_DENSITY = Quantity(2700.0, Unit(DENSITY, "kg/m³", 1.0))
ALUMINUM_YOUNGS_MODULUS = Quantity(69.0e9, Unit(PRESSURE, "Pa", 1.0))
ALUMINUM_THERMAL_CONDUCTIVITY = Quantity(237.0, Unit(THERMAL_CONDUCTIVITY, "W·m⁻¹·K⁻¹", 1.0))

COPPER_DENSITY = Quantity(8960.0, Unit(DENSITY, "kg/m³", 1.0))
COPPER_YOUNGS_MODULUS = Quantity(117.0e9, Unit(PRESSURE, "Pa", 1.0))
COPPER_THERMAL_CONDUCTIVITY = Quantity(401.0, Unit(THERMAL_CONDUCTIVITY, "W·m⁻¹·K⁻¹", 1.0))
COPPER_RESISTIVITY_20C = Quantity(1.68e-8, Unit(RESISTIVITY, "Ω·m", 1.0))
ANNEALED_COPPER_CONDUCTIVITY_IACS = Quantity(5.80e7, Unit(CONDUCTIVITY, "S/m", 1.0))

SILICON_DENSITY = Quantity(2329.0, Unit(DENSITY, "kg/m³", 1.0))
SILICON_BANDGAP_300K = Quantity(1.12 * 1.602176634e-19, Unit(ENERGY, "J", 1.0))
FUSED_SILICA_REFRACTIVE_INDEX_589NM = Quantity(1.4584, DIMENSIONLESS_UNIT)
BOROSILICATE_GLASS_DENSITY = Quantity(2230.0, Unit(DENSITY, "kg/m³", 1.0))


# ------------------------------------------------------------------------------
# 7. GEOLOGY, GEOPHYSICS & EARTH SCIENCES
# ------------------------------------------------------------------------------
# Earth Geodetic & Orbital Parameters
EARTH_MASS = Quantity(5.97217e24, Unit(MASS, "kg", 1.0), error=1.4e19)
M_earth = EARTH_MASS

EARTH_GM = Quantity(3.986004418e14, Unit((LENGTH**3) / (TIME**2), "m³/s²", 1.0), error=8.0e5)
GM_earth = EARTH_GM

EARTH_EQUATORIAL_RADIUS = Quantity(6378137.0, Unit(LENGTH, "m", 1.0))
R_earth_eq = EARTH_EQUATORIAL_RADIUS

EARTH_POLAR_RADIUS = Quantity(6356752.3142, Unit(LENGTH, "m", 1.0))
R_earth_pol = EARTH_POLAR_RADIUS

EARTH_MEAN_RADIUS = Quantity(6371008.8, Unit(LENGTH, "m", 1.0))
R_earth = EARTH_MEAN_RADIUS

EARTH_FLATTENING = Quantity(1.0 / 298.257223563, DIMENSIONLESS_UNIT)  # WGS84
EARTH_ANGULAR_VELOCITY = Quantity(7.2921150e-5, Unit(ANGULAR_VELOCITY, "rad/s", 1.0))
omega_earth = EARTH_ANGULAR_VELOCITY

EARTH_ESCAPE_VELOCITY = Quantity(11186.0, Unit(VELOCITY, "m/s", 1.0))
EARTH_MEAN_DENSITY = Quantity(5514.0, Unit(DENSITY, "kg/m³", 1.0))
EARTH_SURFACE_AREA = Quantity(5.100656e14, Unit(AREA, "m²", 1.0))
EARTH_ALBEDO_BOND = Quantity(0.306, DIMENSIONLESS_UNIT)

# Solar, Lunar & Astronomical References
SOLAR_CONSTANT = Quantity(1361.0, Unit(IRRADIANCE, "W/m²", 1.0), error=1.0)
S_0 = SOLAR_CONSTANT

SOLAR_MASS = Quantity(1.98841e30, Unit(MASS, "kg", 1.0), error=4.0e25)
M_sun = SOLAR_MASS

SOLAR_GM = Quantity(1.32712440041e20, Unit((LENGTH**3) / (TIME**2), "m³/s²", 1.0))
SOLAR_RADIUS = Quantity(6.957e8, Unit(LENGTH, "m", 1.0))
R_sun = SOLAR_RADIUS

SOLAR_LUMINOSITY = Quantity(3.828e26, Unit(POWER, "W", 1.0))
L_sun = SOLAR_LUMINOSITY

ASTRONOMICAL_UNIT = Quantity(149597870700.0, Unit(LENGTH, "m", 1.0))
AU = ASTRONOMICAL_UNIT

PARSEC = Quantity(3.0856775814913673e16, Unit(LENGTH, "m", 1.0))
pc = PARSEC

LIGHT_YEAR = Quantity(9.4607304725808e15, Unit(LENGTH, "m", 1.0))
ly_const = LIGHT_YEAR

LUNAR_MASS = Quantity(7.346e22, Unit(MASS, "kg", 1.0))
LUNAR_MEAN_RADIUS = Quantity(1737400.0, Unit(LENGTH, "m", 1.0))
LUNAR_MEAN_DISTANCE = Quantity(384400000.0, Unit(LENGTH, "m", 1.0))

# Geophysics, Seismology, Geochronology & Rock Mechanics
EARTH_MAGNETIC_DIPOLE_MOMENT = Quantity(7.72e22, Unit(MAGNETIC_MOMENT, "A·m²", 1.0))
EARTH_SURFACE_MAGNETIC_FIELD_MEAN = Quantity(4.5e-5, Unit(MAGNETIC_FIELD, "T", 1.0))
GEOTHERMAL_HEAT_FLUX_MEAN = Quantity(0.087, Unit(IRRADIANCE, "W/m²", 1.0))
GEOTHERMAL_GRADIENT_CONTINENTAL = Quantity(0.025, Unit(TEMPERATURE / LENGTH, "K/m", 1.0))

SEAWATER_MEAN_DENSITY = Quantity(1025.0, Unit(DENSITY, "kg/m³", 1.0))
SEAWATER_SALINITY_MEAN = Quantity(0.035, DIMENSIONLESS_UNIT)  # 35 PSU / kg/kg
CONTINENTAL_CRUST_DENSITY = Quantity(2700.0, Unit(DENSITY, "kg/m³", 1.0))
OCEANIC_CRUST_DENSITY = Quantity(2900.0, Unit(DENSITY, "kg/m³", 1.0))
UPPER_MANTLE_DENSITY = Quantity(3350.0, Unit(DENSITY, "kg/m³", 1.0))
GRANITE_P_WAVE_VELOCITY = Quantity(5800.0, Unit(VELOCITY, "m/s", 1.0))
BASALT_P_WAVE_VELOCITY = Quantity(6500.0, Unit(VELOCITY, "m/s", 1.0))
QUARTZ_DENSITY = Quantity(2648.0, Unit(DENSITY, "kg/m³", 1.0))
CALCITE_DENSITY = Quantity(2710.0, Unit(DENSITY, "kg/m³", 1.0))

# Radiometric Decay Constants (Geochronology)
YEAR_JULIAN = Quantity(31557600.0, Unit(TIME, "s", 1.0))
YEAR_TROPICAL = Quantity(31556925.2, Unit(TIME, "s", 1.0))
SIDEREAL_DAY = Quantity(86164.0905, Unit(TIME, "s", 1.0))

HALF_LIFE_C14 = Quantity(5730.0 * 31557600.0, Unit(TIME, "s", 1.0), error=40.0 * 31557600.0)
DECAY_CONSTANT_C14 = Quantity(np.log(2.0) / (5730.0 * 31557600.0), Unit(FREQUENCY, "s⁻¹", 1.0))

HALF_LIFE_U238 = Quantity(4.468e9 * 31557600.0, Unit(TIME, "s", 1.0))
DECAY_CONSTANT_U238 = Quantity(1.55125e-10 / 31557600.0, Unit(FREQUENCY, "s⁻¹", 1.0))

HALF_LIFE_U235 = Quantity(7.038e8 * 31557600.0, Unit(TIME, "s", 1.0))
DECAY_CONSTANT_U235 = Quantity(9.8485e-10 / 31557600.0, Unit(FREQUENCY, "s⁻¹", 1.0))

HALF_LIFE_TH232 = Quantity(1.405e10 * 31557600.0, Unit(TIME, "s", 1.0))
DECAY_CONSTANT_TH232 = Quantity(4.9475e-11 / 31557600.0, Unit(FREQUENCY, "s⁻¹", 1.0))

HALF_LIFE_K40 = Quantity(1.248e9 * 31557600.0, Unit(TIME, "s", 1.0))
DECAY_CONSTANT_K40 = Quantity(5.543e-10 / 31557600.0, Unit(FREQUENCY, "s⁻¹", 1.0))

HALF_LIFE_RB87 = Quantity(4.961e10 * 31557600.0, Unit(TIME, "s", 1.0))
DECAY_CONSTANT_RB87 = Quantity(1.3972e-11 / 31557600.0, Unit(FREQUENCY, "s⁻¹", 1.0))


# ------------------------------------------------------------------------------
# 8. BIOLOGY, BIOCHEMISTRY & MOLECULAR BIOLOGY
# ------------------------------------------------------------------------------
# Nucleic Acids & Proteins
DNA_BP_RISE_B_FORM = Quantity(3.4e-10, Unit(LENGTH, "m", 1.0))
DNA_HELIX_PITCH_B_FORM = Quantity(3.4e-9, Unit(LENGTH, "m", 1.0))
DNA_BP_PER_TURN_B_FORM = Quantity(10.5, DIMENSIONLESS_UNIT)
DNA_DIAMETER_B_FORM = Quantity(2.0e-9, Unit(LENGTH, "m", 1.0))

MOLAR_MASS_DNA_BP_AVERAGE = Quantity(0.61796, Unit(MOLAR_MASS, "kg/mol", 1.0))      # ~617.96 g/mol per dsDNA bp (sodium salt ~660)
MOLAR_MASS_DNA_NT_AVERAGE = Quantity(0.30897, Unit(MOLAR_MASS, "kg/mol", 1.0))      # ~308.97 g/mol per ssDNA nt
MOLAR_MASS_RNA_NT_AVERAGE = Quantity(0.32047, Unit(MOLAR_MASS, "kg/mol", 1.0))      # ~320.47 g/mol per ssRNA nt
MOLAR_MASS_AMINO_ACID_AVERAGE = Quantity(0.110, Unit(MOLAR_MASS, "kg/mol", 1.0))    # ~110 Da per residue in polypeptide

# Spectrophotometric Conversion Factors (A260 = 1.0, 1 cm pathlength)
DSDNA_A260_CONCENTRATION = Quantity(0.050, Unit(DENSITY, "kg/m³", 1.0))             # 50 µg/mL = 0.050 kg/m³
SSDNA_A260_CONCENTRATION = Quantity(0.033, Unit(DENSITY, "kg/m³", 1.0))             # 33 µg/mL = 0.033 kg/m³
SSRNA_A260_CONCENTRATION = Quantity(0.040, Unit(DENSITY, "kg/m³", 1.0))             # 40 µg/mL = 0.040 kg/m³

# Cellular Bioenergetics & Membrane Biophysics
ATP_HYDROLYSIS_DG0 = Quantity(-30500.0, Unit(MOLAR_ENERGY, "J/mol", 1.0))            # Standard ΔG°' at pH 7
ATP_HYDROLYSIS_DG_CELLULAR = Quantity(-54000.0, Unit(MOLAR_ENERGY, "J/mol", 1.0))    # Typical in vivo ΔG
LIPID_BILAYER_SPECIFIC_CAPACITANCE = Quantity(0.01, Unit(CAPACITANCE / AREA, "F/m²", 1.0))  # ~1 µF/cm²
CELL_MEMBRANE_THICKNESS = Quantity(5.0e-9, Unit(LENGTH, "m", 1.0))
NEURON_RESTING_POTENTIAL = Quantity(-0.070, Unit(VOLTAGE, "V", 1.0))
PROTON_MOTIVE_FORCE_MITOCHONDRIA = Quantity(0.170, Unit(VOLTAGE, "V", 1.0))
CYTOPLASM_DENSITY = Quantity(1030.0, Unit(DENSITY, "kg/m³", 1.0))
PROTEIN_PARTIAL_SPECIFIC_VOLUME = Quantity(7.35e-4, Unit(SPECIFIC_VOLUME, "m³/kg", 1.0))  # ~0.735 mL/g
PROTEIN_DENSITY_AVERAGE = Quantity(1360.0, Unit(DENSITY, "kg/m³", 1.0))

# Standard Buffer pKa values (at 25 °C)
PKA_ACETIC_ACID = Quantity(4.76, DIMENSIONLESS_UNIT)
PKA_MES = Quantity(6.15, DIMENSIONLESS_UNIT)
PKA_PHOSPHATE_2 = Quantity(7.20, DIMENSIONLESS_UNIT)
PKA_MOPS = Quantity(7.20, DIMENSIONLESS_UNIT)
PKA_HEPES = Quantity(7.48, DIMENSIONLESS_UNIT)
PKA_TRIS = Quantity(8.06, DIMENSIONLESS_UNIT)
PKA_BORATE = Quantity(9.24, DIMENSIONLESS_UNIT)
PKA_GLYCINE_2 = Quantity(9.78, DIMENSIONLESS_UNIT)
PKA_CARBONIC_ACID_1 = Quantity(6.35, DIMENSIONLESS_UNIT)


# ------------------------------------------------------------------------------
# 9. MEDICINE, CLINICAL LABORATORY & HUMAN PHYSIOLOGY
# ------------------------------------------------------------------------------
# Reference Physiological & Anthropometric Values (70 kg Reference Adult)
HUMAN_BODY_TEMP_NORMAL = Quantity(310.15, Unit(TEMPERATURE, "K", 1.0))              # 37.0 °C
HUMAN_REFERENCE_MASS = Quantity(70.0, Unit(MASS, "kg", 1.0))
HUMAN_REFERENCE_BSA = Quantity(1.73, Unit(AREA, "m²", 1.0))                         # Standard Body Surface Area for eGFR

# Blood & Cardiovascular Constants
BLOOD_DENSITY = Quantity(1060.0, Unit(DENSITY, "kg/m³", 1.0))
BLOOD_PLASMA_DENSITY = Quantity(1025.0, Unit(DENSITY, "kg/m³", 1.0))
BLOOD_VISCOSITY_37C = Quantity(3.5e-3, Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0))
BLOOD_PH_ARTERIAL = Quantity(7.40, DIMENSIONLESS_UNIT)
BLOOD_PH_VENOUS = Quantity(7.35, DIMENSIONLESS_UNIT)
BLOOD_OSMOLARITY_NORMAL = Quantity(290.0, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0)) # 290 mOsm/L = 290 mol/m³
BLOOD_VOLUME_PER_KG = Quantity(7.0e-5, Unit(SPECIFIC_VOLUME, "m³/kg", 1.0))         # ~70 mL/kg
CARDIAC_OUTPUT_RESTING = Quantity(8.3333333e-5, Unit(VOLUMETRIC_FLOW_RATE, "m³/s", 1.0))  # 5.0 L/min
SYSTOLIC_BP_NORMAL = Quantity(15998.68, Unit(PRESSURE, "Pa", 1.0))                  # 120 mmHg
DIASTOLIC_BP_NORMAL = Quantity(10665.79, Unit(PRESSURE, "Pa", 1.0))                 # 80 mmHg
MAP_NORMAL = Quantity(12443.42, Unit(PRESSURE, "Pa", 1.0))                          # 93.3 mmHg

# Clinical Chemistry & Hematology Reference Midpoints (in SI base units)
SERUM_SODIUM_NORMAL = Quantity(140.0, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0))     # 140 mmol/L
SERUM_POTASSIUM_NORMAL = Quantity(4.2, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0))    # 4.2 mmol/L
SERUM_CHLORIDE_NORMAL = Quantity(102.0, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0))   # 102 mmol/L
SERUM_BICARBONATE_NORMAL = Quantity(24.0, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0)) # 24 mmol/L
SERUM_CALCIUM_TOTAL_NORMAL = Quantity(2.35, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0))  # 2.35 mmol/L
FASTING_GLUCOSE_NORMAL = Quantity(5.0, Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0))    # 5.0 mmol/L (~90 mg/dL)
HEMOGLOBIN_MOLAR_MASS = Quantity(64.458, Unit(MOLAR_MASS, "kg/mol", 1.0))           # ~64,458 g/mol (tetramer)
HEMOGLOBIN_CONCENTRATION_NORMAL = Quantity(145.0, Unit(DENSITY, "kg/m³", 1.0))      # 14.5 g/dL = 145 kg/m³
HUFNER_CONSTANT = Quantity(1.34e-3, Unit(VOLUME / MASS, "m³/kg", 1.0))              # 1.34 mL O2 / g Hb
HEMATOCRIT_NORMAL = Quantity(0.43, DIMENSIONLESS_UNIT)

# Respiratory & Renal Physiology
TIDAL_VOLUME_NORMAL = Quantity(5.0e-4, Unit(VOLUME, "m³", 1.0))                     # 500 mL
ALVEOLAR_PO2_NORMAL = Quantity(13332.24, Unit(PRESSURE, "Pa", 1.0))                 # 100 mmHg
ALVEOLAR_PCO2_NORMAL = Quantity(5332.89, Unit(PRESSURE, "Pa", 1.0))                 # 40 mmHg
GFR_NORMAL = Quantity(2.0e-6, Unit(VOLUMETRIC_FLOW_RATE, "m³/s", 1.0))              # 120 mL/min
CSF_DENSITY = Quantity(1007.0, Unit(DENSITY, "kg/m³", 1.0))
INTRACRANIAL_PRESSURE_NORMAL = Quantity(1333.22, Unit(PRESSURE, "Pa", 1.0))         # 10 mmHg

# Medical Imaging, Dosimetry & Radiation Protection
TC99M_HALF_LIFE = Quantity(6.0067 * 3600.0, Unit(TIME, "s", 1.0))
TC99M_GAMMA_ENERGY = Quantity(140.511e3 * 1.602176634e-19, Unit(ENERGY, "J", 1.0))
FDG_F18_HALF_LIFE = Quantity(109.77 * 60.0, Unit(TIME, "s", 1.0))
ANNIHILATION_PHOTON_ENERGY = Quantity(510.99895069e3 * 1.602176634e-19, Unit(ENERGY, "J", 1.0))
I131_HALF_LIFE = Quantity(8.0252 * 86400.0, Unit(TIME, "s", 1.0))
CO60_HALF_LIFE = Quantity(5.2713 * 31557600.0, Unit(TIME, "s", 1.0))
AIR_W_VALUE_IONIZATION = Quantity(33.97 * 1.602176634e-19, Unit(ENERGY, "J", 1.0))  # Mean energy per ion pair in dry air
SOFT_TISSUE_DENSITY_ICRU = Quantity(1060.0, Unit(DENSITY, "kg/m³", 1.0))
BONE_CORTICAL_DENSITY_ICRU = Quantity(1920.0, Unit(DENSITY, "kg/m³", 1.0))
ULTRASOUND_SPEED_SOFT_TISSUE = Quantity(1540.0, Unit(VELOCITY, "m/s", 1.0))
PROTON_GYROMAGNETIC_FREQUENCY_PER_TESLA = Quantity(42.577478461e6, Unit(FREQUENCY / MAGNETIC_FIELD, "Hz/T", 1.0))  # MRI Larmor freq
