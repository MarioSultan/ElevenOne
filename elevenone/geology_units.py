from .dimension import *
from .unit import Unit
from .si_units import *

# ==============================================================================
# GEOLOGY, EARTH SCIENCES & GEOPHYSICS
# ==============================================================================

# Time (Geological Epochs & Deep Time)
megaannum               = Unit(TIME, "Ma", 31557600.0 * 1e6)  # Million years
Ma                      = megaannum
gigaannum               = Unit(TIME, "Ga", 31557600.0 * 1e9)  # Billion years
Ga                      = gigaannum
kiloannum               = Unit(TIME, "ka", 31557600.0 * 1e3)  # Thousand years
ka                      = kiloannum
year                    = Unit(TIME, "yr", 31557600.0)
yr                      = year

# Length / Depth / Stratigraphy
kilometer               = Unit(LENGTH, "km", 1e3)
km                      = kilometer
meter                   = Unit(LENGTH, "m", 1.0)
m                       = meter
centimeter              = Unit(LENGTH, "cm", 0.01)
cm                      = centimeter
millimeter              = Unit(LENGTH, "mm", 0.001)
mm                      = millimeter
micron                  = Unit(LENGTH, "μm", 1e-6)
angstrom                = Unit(LENGTH, "Å", 1e-10)

# Petroleum & Mining Units (Volume and Flow)
barrel_oil              = Unit(VOLUME, "bbl", 0.158987294928)  # Petroleum barrel
bbl                     = barrel_oil
cubic_foot              = Unit(VOLUME, "ft³", 0.028316846592)
ft3                     = cubic_foot
acre_foot               = Unit(VOLUME, "acft", 1233.4818375)
acft                    = acre_foot
gallon                  = Unit(VOLUME, "gal", 0.003785411784)

darcy                   = Unit(DIMENSIONLESS, "Darcy", 9.869233e-13)  # Permeability unit
millidarcy              = Unit(DIMENSIONLESS, "mD", 9.869233e-16)
mD                      = millidarcy

# Mass, Density & Earth Metrics
earth_mass              = Unit(MASS, "M_earth", 5.9722e24)
M_earth                 = earth_mass
earth_radius            = Unit(LENGTH, "R_earth", 6.371e6)
R_earth                 = earth_radius
gram_per_cubic_centimeter = Unit(DENSITY, "g/cm³", 1000.0)
g_cm3                   = gram_per_cubic_centimeter
kilogram_per_cubic_meter = Unit(DENSITY, "kg/m³", 1.0)

# Pressure, Stress & Seismology (Tectonics)
gigapascal              = Unit(PRESSURE, "GPa", 1e9)
GPa                     = gigapascal
megapascal              = Unit(PRESSURE, "MPa", 1e6)
MPa                     = megapascal
bar                     = Unit(PRESSURE, "bar", 1e5)
kilobar                 = Unit(PRESSURE, "kbar", 1e8)
kbar                    = kilobar
megabar                 = Unit(PRESSURE, "Mbar", 1e11)
Mbar                    = megabar
atmosphere              = Unit(PRESSURE, "atm", 101325.0)

# Geothermal & Heat Flow
heat_flow_unit          = Unit(POWER / AREA, "HFU", 41.84)  # 1 HFU = 1 µcal/(cm²·s)
HFU                     = heat_flow_unit
mW_per_m2               = Unit(POWER / AREA, "mW/m²", 0.001)

# Magnetism & Gravity (Geophysics)
tesla                   = Unit(MAGNETIC_FIELD, "T", 1.0)
nanotesla               = Unit(MAGNETIC_FIELD, "nT", 1e-9)
nT                      = nanotesla
gamma_magnetic          = Unit(MAGNETIC_FIELD, "gamma", 1e-9)
gauss                   = Unit(MAGNETIC_FIELD, "G", 1e-4)

galileo_gravity         = Unit(ACCELERATION, "Gal", 0.01)  # 1 Gal = 1 cm/s²
Gal                     = galileo_gravity
milligal                = Unit(ACCELERATION, "mGal", 1e-5)
mGal                    = milligal
microgal                = Unit(ACCELERATION, "μGal", 1e-8)
uGal                    = microgal

# Sedimentology & Particle Size
phi_unit                = Unit(DIMENSIONLESS, "phi", 1.0)