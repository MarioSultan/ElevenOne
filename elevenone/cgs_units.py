from .dimension import *
from .unit import Unit

# ==============================================================================
# CGS SYSTEM (CENTIMETER-GRAM-SECOND) UNITS
# ==============================================================================

# --- Base Units (CGS) ---
centimeter              = Unit(LENGTH, "cm", 0.01)
cm                      = centimeter
gram                    = Unit(MASS, "g", 0.001)
g                       = gram
second                  = Unit(TIME, "s", 1.0)
s                       = second

# --- Mechanical Units (CGS) ---
square_centimeter       = Unit(AREA, "cm²", 1e-4)
cubic_centimeter        = Unit(VOLUME, "cm³", 1e-6)
cc                      = cubic_centimeter
gal                     = Unit(VELOCITY, "cm/s", 0.01)
galileo_acceleration    = Unit(ACCELERATION, "Gal", 0.01)
Gal                     = galileo_acceleration
dyne                    = Unit(FORCE, "dyn", 1e-5)
dyn                     = dyne
erg                     = Unit(ENERGY, "erg", 1e-7)
barye                   = Unit(PRESSURE, "Ba", 0.1)
Ba                      = barye
poise                   = Unit(DYNAMIC_VISCOSITY, "P", 0.1)
P                       = poise
centipoise              = Unit(DYNAMIC_VISCOSITY, "cP", 1e-3)
cP                      = centipoise
stokes                  = Unit(KINEMATIC_VISCOSITY, "St", 1e-4)
St                      = stokes
centistokes             = Unit(KINEMATIC_VISCOSITY, "cSt", 1e-6)
cSt                     = centistokes

# --- Electromagnetic Units (CGS-Gaussian / EMU / ESU) ---
statcoulomb             = Unit(CHARGE, "statC", 3.33564095e-10)
statC                   = statcoulomb
esu_charge              = statcoulomb
franklin                = statcoulomb

statampere              = Unit(CURRENT, "statA", 3.33564095e-10)
statA                   = statampere

statvolt                = Unit(VOLTAGE, "statV", 299.792458)
statV                   = statvolt

statohm                 = Unit(RESISTANCE, "statΩ", 8.987551787e11)
statOhm                 = statohm

statfarad               = Unit(CAPACITANCE, "statF", 1.112650056e-12)
statF                   = statfarad

stathanry               = Unit(INDUCTANCE, "statH", 8.987551787e11)

gauss                   = Unit(MAGNETIC_FIELD, "G", 1e-4)
G                       = gauss
milligauss              = Unit(MAGNETIC_FIELD, "mG", 1e-7)
microgauss              = Unit(MAGNETIC_FIELD, "μG", 1e-10)
gamma_field             = Unit(MAGNETIC_FIELD, "gamma", 1e-9)

maxwell                 = Unit(MAGNETIC_FLUX, "Mx", 1e-8)
Mx                      = maxwell

oersted                 = Unit(MAGNETIC_FIELD_STRENGTH, "Oe", 79.57747154594767)
Oe                      = oersted

erg_per_gauss           = Unit(MAGNETIC_MOMENT, "erg/G", 1e-3)
emu_magnetic_moment     = Unit(MAGNETIC_MOMENT, "emu", 1e-3)

# --- Photometry (CGS Photometric Units) ---
phot                    = Unit(ILLUMINANCE, "ph", 1e4)
stilb                   = Unit(LUMINANCE, "sb", 1e4)
sb                      = stilb
lambda_luminance        = Unit(LUMINANCE, "lambert", 3183.0988618)