from .dimension import *
from .unit import Unit
from .si_units import *

# ==============================================================================
# ASTROPHYSICS, ASTRONOMY & COSMOLOGY
# ==============================================================================

# Distance / Length
astronomical_unit       = Unit(LENGTH, "au", 1.495978707e11)
au                      = astronomical_unit
parsec                  = Unit(LENGTH, "pc", 3.08567758149137e16)
pc                      = parsec
kiloparsec              = Unit(LENGTH, "kpc", 3.08567758149137e19)
kpc                     = kiloparsec
megaparsec              = Unit(LENGTH, "Mpc", 3.08567758149137e22)
Mpc                     = megaparsec
gigaparsec              = Unit(LENGTH, "Gpc", 3.08567758149137e25)
Gpc                     = gigaparsec
light_year              = Unit(LENGTH, "ly", 9.4607304725808e15)
ly                      = light_year
lunar_distance          = Unit(LENGTH, "LD", 3.84402e8)
solar_radius            = Unit(LENGTH, "R_sun", 6.957e8)
jupiter_radius          = Unit(LENGTH, "R_jup", 7.1492e7)
earth_radius            = Unit(LENGTH, "R_earth", 6.371e6)

# Mass
solar_mass              = Unit(MASS, "M_sun", 1.98847e30)
M_sun                   = solar_mass
jupiter_mass            = Unit(MASS, "M_jup", 1.89813e27)
earth_mass              = Unit(MASS, "M_earth", 5.9722e24)

# Luminosity / Power
solar_luminosity        = Unit(POWER, "L_sun", 3.828e26)
L_sun                   = solar_luminosity

# Time / Epochs
julian_year             = Unit(TIME, "a", 31557600.0)
sideral_year            = Unit(TIME, "yr_sid", 31558149.7632)
hubble_time             = Unit(TIME, "t_H", 4.55e17)  # approx 1/H_0

# ==============================================================================
# ATOMIC, NUCLEAR & PARTICLE PHYSICS
# ==============================================================================

# Mass & Energy
atomic_mass_unit        = Unit(MASS, "u", 1.66053906660e-27)
u                       = atomic_mass_unit
dalton                  = atomic_mass_unit
Da                      = dalton
electron_mass           = Unit(MASS, "m_e", 9.1093837015e-31)
proton_mass             = Unit(MASS, "m_p", 1.67262192369e-27)
neutron_mass            = Unit(MASS, "m_n", 1.67492749804e-27)

# Length / Area / Cross-section
bohr_radius             = Unit(LENGTH, "a_0", 5.29177210903e-11)
classical_electron_radius = Unit(LENGTH, "r_e", 2.8179403262e-15)
angstrom                = Unit(LENGTH, "Å", 1e-10)
fermi                   = Unit(LENGTH, "fm", 1e-15)
barn                    = Unit(AREA, "b", 1e-28)
millibarn               = Unit(AREA, "mb", 1e-31)
microbarn               = Unit(AREA, "μb", 1e-34)
nanobarn                = Unit(AREA, "nb", 1e-37)
picobarn                = Unit(AREA, "pb", 1e-40)

# Charge & Electromagnetic Constants
elementary_charge       = Unit(CHARGE, "e", 1.602176634e-19)
statcoulomb             = Unit(CHARGE, "statC", 3.33564e-10)
esu                     = statcoulomb

# Energy units common in spectroscopy / particle physics
hartree                 = Unit(ENERGY, "E_h", 4.3597447222071e-18)
rydberg                 = Unit(ENERGY, "Ry", 2.1798723611035e-18)
kayser                  = Unit(WAVENUMBER, "cm⁻¹", 100.0)

# ==============================================================================
# CGS SYSTEM (GAUSSIAN / CENTIMETER-GRAM-SECOND)
# ==============================================================================

# Mechanics
dyne                    = Unit(FORCE, "dyn", 1e-5)
dyn                     = dyne
erg                     = Unit(ENERGY, "erg", 1e-7)
barye                   = Unit(PRESSURE, "Ba", 0.1)

# Viscosity
poise                   = Unit(DYNAMIC_VISCOSITY, "P", 0.1)
centipoise              = Unit(DYNAMIC_VISCOSITY, "cP", 1e-3)
stokes                  = Unit(KINEMATIC_VISCOSITY, "St", 1e-4)
centistokes             = Unit(KINEMATIC_VISCOSITY, "cSt", 1e-6)

# Magnetism & Electromagnetism (CGS / Gaussian)
gauss                   = Unit(MAGNETIC_FIELD, "G", 1e-4)
G                       = gauss
milligauss              = Unit(MAGNETIC_FIELD, "mG", 1e-7)
microgauss              = Unit(MAGNETIC_FIELD, "μG", 1e-10)
maxwell                 = Unit(MAGNETIC_FLUX, "Mx", 1e-8)
Mx                      = maxwell
oersted                 = Unit(MAGNETIC_FIELD_STRENGTH, "Oe", 79.57747154594767)
gamma_unit              = Unit(MAGNETIC_FIELD, "gamma", 1e-9)

# Photometry / Radiometry
phot                    = Unit(ILLUMINANCE, "ph", 1e4)
stilb                   = Unit(LUMINANCE, "sb", 1e4)

# ==============================================================================
# PLANCK UNITS (NATURAL UNITS: c = ħ = G = k_B = 1)
# ==============================================================================
planck_length           = Unit(LENGTH, "l_P", 1.616255e-35)
l_P                     = planck_length
planck_mass             = Unit(MASS, "m_P", 2.176434e-8)
m_P                     = planck_mass
planck_time             = Unit(TIME, "t_P", 5.391247e-44)
t_P                     = planck_time
planck_temperature      = Unit(TEMPERATURE, "T_P", 1.416784e32)
T_P                     = planck_temperature
planck_charge           = Unit(CHARGE, "q_P", 1.875545956e-18)
planck_energy           = Unit(ENERGY, "E_P", 1.9561e9)
planck_force            = Unit(FORCE, "F_P", 1.21027e44)
planck_power            = Unit(POWER, "P_P", 3.62831e52)
planck_density          = Unit(DENSITY, "rho_P", 5.155e96)
planck_pressure         = Unit(PRESSURE, "p_P", 4.63309e113)

# ==============================================================================
# PLASMA, FLUIDS, GEOPHYSICS & METEOROLOGY
# ==============================================================================
atmosphere              = Unit(PRESSURE, "atm", 101325.0)
atm                     = atmosphere
torr                    = Unit(PRESSURE, "Torr", 133.322368421)
mmHg                    = Unit(PRESSURE, "mmHg", 133.322368421)
technical_atmosphere    = Unit(PRESSURE, "at", 98066.5)

# ==============================================================================
# DOSIMETRY, NUCLEAR RADIATION & HEALTH PHYSICS
# ==============================================================================
curie                   = Unit(ACTIVITY, "Ci", 3.7e10)
Ci                      = curie
millicurie              = Unit(ACTIVITY, "mCi", 3.7e7)
microcurie              = Unit(ACTIVITY, "μCi", 3.7e4)
rutherford              = Unit(ACTIVITY, "Rd", 1e6)
roentgen                = Unit(EXPOSURE, "R", 2.58e-4)
rad_dose                = Unit(ABSORBED_DOSE, "rad", 0.01)
rem                     = Unit(DOSE_EQUIVALENT, "rem", 0.01)
millirem                = Unit(DOSE_EQUIVALENT, "mrem", 1e-5)