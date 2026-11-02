from .dimension import *
from .unit import Unit
from .si_units import *

# ==============================================================================
# AMOUNT OF SUBSTANCE & CONCENTRATION
# ==============================================================================

# Amount of Substance
mole                    = Unit(AMOUNT, "mol", 1.0)
mol                     = mole
micromole               = Unit(AMOUNT, "μmol", 1e-6)
millimole               = Unit(AMOUNT, "mmol", 1e-3)
kilomole                = Unit(AMOUNT, "kmol", 1e3)
pound_mole              = Unit(AMOUNT, "lb-mol", 453.59237)

# Molar Concentration (Molarity)
molar                   = Unit(MOLAR_CONCENTRATION, "M", 1000.0)
M                       = molar
millimolar              = Unit(MOLAR_CONCENTRATION, "mM", 1.0)
mM                      = millimolar
micromolar              = Unit(MOLAR_CONCENTRATION, "μM", 1e-3)
uM                      = micromolar
nanomolar               = Unit(MOLAR_CONCENTRATION, "nM", 1e-6)
picomolar               = Unit(MOLAR_CONCENTRATION, "pM", 1e-9)
femtomolar              = Unit(MOLAR_CONCENTRATION, "fM", 1e-12)
attomolar               = Unit(MOLAR_CONCENTRATION, "aM", 1e-15)

mole_per_liter          = molar
mol_per_L               = molar
mole_per_cubic_meter    = Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0)

# Molality (mol/kg)
molal                   = Unit(DIMENSIONLESS / MASS, "m_molal", 1.0)
mol_per_kg              = molal

# Mass Concentration & Density
gram_per_liter          = Unit(DENSITY, "g/L", 1.0)
g_per_L                 = gram_per_liter
milligram_per_liter     = Unit(DENSITY, "mg/L", 1e-3)
mg_per_L                = milligram_per_liter
microgram_per_liter     = Unit(DENSITY, "μg/L", 1e-6)
ug_per_L                = microgram_per_liter
gram_per_milliliter     = Unit(DENSITY, "g/mL", 1000.0)
g_per_mL                = gram_per_milliliter
gram_per_cubic_centimeter = Unit(DENSITY, "g/cm³", 1000.0)
g_per_cm3               = gram_per_cubic_centimeter

# Dimensionless Parts-Per Ratios
parts_per_hundred       = Unit(DIMENSIONLESS, "%", 0.01)
percent                 = parts_per_hundred
parts_per_thousand      = Unit(DIMENSIONLESS, "‰", 1e-3)
permille                = parts_per_thousand
parts_per_million       = Unit(DIMENSIONLESS, "ppm", 1e-6)
ppm                     = parts_per_million
parts_per_billion       = Unit(DIMENSIONLESS, "ppb", 1e-9)
ppb                     = parts_per_billion
parts_per_trillion      = Unit(DIMENSIONLESS, "ppt", 1e-12)
ppt                     = parts_per_trillion

# ==============================================================================
# ATOMIC & MOLECULAR UNITS
# ==============================================================================

# Atomic Mass & Mass Units
atomic_mass_unit        = Unit(MASS, "amu", 1.66053906660e-27)
amu                     = atomic_mass_unit
dalton                  = Unit(MASS, "Da", 1.66053906660e-27)
Da                      = dalton
kilodalton              = Unit(MASS, "kDa", 1.66053906660e-24)
kDa                     = kilodalton
megadalton              = Unit(MASS, "MDa", 1.66053906660e-21)
MDa                     = megadalton

# Length & Molecular Geometry
angstrom                = Unit(LENGTH, "Å", 1e-10)
picometer               = Unit(LENGTH, "pm", 1e-12)
bohr_radius             = Unit(LENGTH, "a_0", 5.29177210903e-11)

# Dipole Moment
debye                   = Unit(ELECTRIC_DIPOLE_MOMENT, "D", 3.33564e-30)

# Spectroscopy & Energy
wave_number             = Unit(WAVENUMBER, "cm⁻¹", 100.0)
kayser                  = wave_number
hartree                 = Unit(ENERGY, "E_h", 4.3597447222071e-18)
rydberg                 = Unit(ENERGY, "Ry", 2.1798723611035e-18)
electronvolt            = Unit(ENERGY, "eV", 1.602176634e-19)
eV                      = electronvolt

# ==============================================================================
# THERMOCHEMISTRY & CALORIMETRY
# ==============================================================================

# Energy & Heat
calorie                 = Unit(ENERGY, "cal", 4.184)
cal                     = calorie
kilocalorie             = Unit(ENERGY, "kcal", 4184.0)
kcal                    = kilocalorie
joule                   = Unit(ENERGY, "J", 1.0)
J                       = joule
kilojoule               = Unit(ENERGY, "kJ", 1000.0)
kJ                      = kilojoule
british_thermal_unit    = Unit(ENERGY, "BTU", 1055.05585)
BTU                     = british_thermal_unit

# Molar Energy & Enthalpy
joule_per_mole          = Unit(MOLAR_ENERGY, "J/mol", 1.0)
J_per_mol               = joule_per_mole
kilojoule_per_mole      = Unit(MOLAR_ENERGY, "kJ/mol", 1000.0)
kJ_per_mol              = kilojoule_per_mole
calorie_per_mole        = Unit(MOLAR_ENERGY, "cal/mol", 4.184)
cal_per_mol             = calorie_per_mole
kilocalorie_per_mole    = Unit(MOLAR_ENERGY, "kcal/mol", 4184.0)
kcal_per_mol            = kilocalorie_per_mole

# Entropy & Heat Capacity
joule_per_kelvin        = Unit(HEAT_CAPACITY, "J/K", 1.0)
joule_per_mole_kelvin   = Unit(MOLAR_HEAT_CAPACITY, "J/(mol·K)", 1.0)
J_per_mol_K             = joule_per_mole_kelvin
calorie_per_mole_kelvin = Unit(MOLAR_HEAT_CAPACITY, "cal/(mol·K)", 4.184)
cal_per_mol_K           = calorie_per_mole_kelvin
entropy_unit            = Unit(MOLAR_HEAT_CAPACITY, "e.u.", 4.184)
eu                      = entropy_unit

# ==============================================================================
# PRESSURE & GAS LAWS
# ==============================================================================

atmosphere              = Unit(PRESSURE, "atm", 101325.0)
atm                     = atmosphere
bar                     = Unit(PRESSURE, "bar", 100000.0)
millibar                = Unit(PRESSURE, "mbar", 100.0)
mbar                    = millibar
torr                    = Unit(PRESSURE, "Torr", 133.322368421)
Torr                    = torr
millimeter_of_mercury   = Unit(PRESSURE, "mmHg", 133.322368421)
mmHg                    = millimeter_of_mercury
pascal                  = Unit(PRESSURE, "Pa", 1.0)
Pa                      = pascal
kilopascal              = Unit(PRESSURE, "kPa", 1000.0)
kPa                     = kilopascal
megapascal              = Unit(PRESSURE, "MPa", 1e6)
MPa                     = megapascal
psi                     = Unit(PRESSURE, "psi", 6894.757293168)

# ==============================================================================
# VOLUMETRIC & LABORATORY UNITS
# ==============================================================================

cubic_meter             = Unit(VOLUME, "m³", 1.0)
m3                      = cubic_meter
liter                   = Unit(VOLUME, "L", 1e-3)
L                       = liter
deciliter               = Unit(VOLUME, "dL", 1e-4)
dL                      = deciliter
centiliter              = Unit(VOLUME, "cL", 1e-5)
cL                      = centiliter
milliliter              = Unit(VOLUME, "mL", 1e-6)
mL                      = milliliter
microliter              = Unit(VOLUME, "μL", 1e-9)
uL                      = microliter
nanoliter               = Unit(VOLUME, "nL", 1e-12)
nL                      = nanoliter
picoliter               = Unit(VOLUME, "pL", 1e-15)
pL                      = picoliter
femtoliter              = Unit(VOLUME, "fL", 1e-18)
fL                      = femtoliter
cubic_centimeter        = Unit(VOLUME, "cm³", 1e-6)
cc                      = cubic_centimeter
cubic_decimeter         = Unit(VOLUME, "dm³", 1e-3)

# ==============================================================================
# VISCOSITY, TRANSPORT & ELECTROCHEMISTRY
# ==============================================================================

# Dynamic Viscosity
poise                   = Unit(DYNAMIC_VISCOSITY, "P", 0.1)
centipoise              = Unit(DYNAMIC_VISCOSITY, "cP", 1e-3)
cP                      = centipoise
pascal_second           = Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0)
millipascal_second      = Unit(DYNAMIC_VISCOSITY, "mPa·s", 1e-3)

# Kinematic Viscosity
stokes                  = Unit(KINEMATIC_VISCOSITY, "St", 1e-4)
centistokes             = Unit(KINEMATIC_VISCOSITY, "cSt", 1e-6)
cSt                     = centistokes

# Catalytic Activity & Reaction Kinetics
katal                   = Unit(CATALYTIC_ACTIVITY, "kat", 1.0)
kat                     = katal
microkatal              = Unit(CATALYTIC_ACTIVITY, "μkat", 1e-6)
nanokatal               = Unit(CATALYTIC_ACTIVITY, "nkat", 1e-9)
enzyme_unit             = Unit(CATALYTIC_ACTIVITY, "U", 1.6666666666666667e-8)
U                       = enzyme_unit

# Electrochemistry & Conductance
faraday                 = Unit(CHARGE, "F_const", 96485.33212)
siemens                 = Unit(CONDUCTANCE, "S", 1.0)
S                       = siemens
millisiemens            = Unit(CONDUCTANCE, "mS", 1e-3)
microsiemens            = Unit(CONDUCTANCE, "μS", 1e-6)
siemens_per_meter       = Unit(CONDUCTIVITY, "S/m", 1.0)
siemens_cm2_per_mole    = Unit(MOLAR_CONDUCTIVITY, "S·cm²/mol", 1e-4)

# Radiochemistry
curie                   = Unit(ACTIVITY, "Ci", 3.7e10)
Ci                      = curie
becquerel               = Unit(ACTIVITY, "Bq", 1.0)
Bq                      = becquerel