from .dimension import *
from .unit import Unit

# ==============================================================================
# SI BASE UNITS (7 Base Units + Radian/Steradian)
# ==============================================================================

# 1. Length (meter)
meter           = Unit(LENGTH, "m", 1.0)
m               = meter
yoctometer      = Unit(LENGTH, "ym", 1e-24)
zeptometer      = Unit(LENGTH, "zm", 1e-21)
attometer       = Unit(LENGTH, "am", 1e-18)
femtometer      = Unit(LENGTH, "fm", 1e-15)
picometer       = Unit(LENGTH, "pm", 1e-12)
nanometer       = Unit(LENGTH, "nm", 1e-9)
micrometer      = Unit(LENGTH, "μm", 1e-6)
millimeter      = Unit(LENGTH, "mm", 1e-3)
centimeter      = Unit(LENGTH, "cm", 1e-2)
decimeter       = Unit(LENGTH, "dm", 1e-1)
decameter       = Unit(LENGTH, "dam", 10.0)
hectometer      = Unit(LENGTH, "hm", 100.0)
kilometer       = Unit(LENGTH, "km", 1e3)
megameter       = Unit(LENGTH, "Mm", 1e6)
gigameter       = Unit(LENGTH, "Gm", 1e9)
terameter       = Unit(LENGTH, "Tm", 1e12)
petameter       = Unit(LENGTH, "Pm", 1e15)
exameter        = Unit(LENGTH, "Em", 1e18)
zettameter      = Unit(LENGTH, "Zm", 1e21)
yottameter      = Unit(LENGTH, "Ym", 1e24)

# 2. Mass (kilogram is base SI)
kilogram        = Unit(MASS, "kg", 1.0)
kg              = kilogram
gram            = Unit(MASS, "g", 1e-3)
g               = gram
yoctogram       = Unit(MASS, "yg", 1e-27)
zeptogram       = Unit(MASS, "zg", 1e-24)
attogram        = Unit(MASS, "ag", 1e-21)
femtogram       = Unit(MASS, "fg", 1e-18)
picogram        = Unit(MASS, "pg", 1e-15)
nanogram        = Unit(MASS, "ng", 1e-12)
microgram       = Unit(MASS, "μg", 1e-9)
ug              = microgram
milligram       = Unit(MASS, "mg", 1e-6)
mg              = milligram
centigram       = Unit(MASS, "cg", 1e-5)
decigram        = Unit(MASS, "dg", 1e-4)
tonne           = Unit(MASS, "t", 1000.0)
metric_ton      = tonne
megagram        = Unit(MASS, "Mg", 1000.0)
gigagram        = Unit(MASS, "Gg", 1e6)

# 3. Time (second)
second          = Unit(TIME, "s", 1.0)
s               = second
yoctosecond     = Unit(TIME, "ys", 1e-24)
zeptosecond     = Unit(TIME, "zs", 1e-21)
attosecond      = Unit(TIME, "as", 1e-18)
femtosecond     = Unit(TIME, "fs", 1e-15)
picosecond      = Unit(TIME, "ps", 1e-12)
nanosecond      = Unit(TIME, "ns", 1e-9)
ns              = nanosecond
microsecond     = Unit(TIME, "μs", 1e-6)
us              = microsecond
millisecond     = Unit(TIME, "ms", 1e-3)
ms              = millisecond
minute          = Unit(TIME, "min", 60.0)
hour            = Unit(TIME, "h", 3600.0)
day             = Unit(TIME, "d", 86400.0)

# 4. Electric Current (ampere)
ampere          = Unit(CURRENT, "A", 1.0)
A               = ampere
yoctoampere     = Unit(CURRENT, "yA", 1e-24)
zeptoampere     = Unit(CURRENT, "zA", 1e-21)
attoampere      = Unit(CURRENT, "aA", 1e-18)
femtoampere     = Unit(CURRENT, "fA", 1e-15)
picoampere      = Unit(CURRENT, "pA", 1e-12)
nanoampere      = Unit(CURRENT, "nA", 1e-9)
microampere     = Unit(CURRENT, "μA", 1e-6)
uA              = microampere
milliampere     = Unit(CURRENT, "mA", 1e-3)
mA              = milliampere
kiloampere      = Unit(CURRENT, "kA", 1e3)
megaampere      = Unit(CURRENT, "MA", 1e6)

# 5. Thermodynamic Temperature (kelvin)
kelvin          = Unit(TEMPERATURE, "K", 1.0, offset=0.0)
K               = kelvin
millikelvin     = Unit(TEMPERATURE, "mK", 1e-3, offset=0.0)
microkelvin     = Unit(TEMPERATURE, "μK", 1e-6, offset=0.0)
nanokelvin      = Unit(TEMPERATURE, "nK", 1e-9, offset=0.0)
degree_celsius  = Unit(TEMPERATURE, "°C", 1.0, offset=273.15)
degC            = degree_celsius

# 6. Amount of Substance (mole)
mole            = Unit(AMOUNT, "mol", 1.0)
mol             = mole
micromole       = Unit(AMOUNT, "μmol", 1e-6)
millimole       = Unit(AMOUNT, "mmol", 1e-3)
kilomole        = Unit(AMOUNT, "kmol", 1e3)

# 7. Luminous Intensity (candela)
candela         = Unit(LUMINOUS, "cd", 1.0)
cd              = candela
millicandela    = Unit(LUMINOUS, "mcd", 1e-3)

# 8. Angles (radian & steradian)
radian          = Unit(ANGULAR, "rad", 1.0)
rad             = radian
milliradian     = Unit(ANGULAR, "mrad", 1e-3)
microradian     = Unit(ANGULAR, "μrad", 1e-6)
steradian       = Unit(DIMENSIONLESS, "sr", 1.0)
sr              = steradian

# ==============================================================================
# SI DERIVED UNITS WITH SPECIAL NAMES
# ==============================================================================

# Frequency (hertz)
hertz           = Unit(FREQUENCY, "Hz", 1.0)
Hz              = hertz
millihertz      = Unit(FREQUENCY, "mHz", 1e-3)
kilohertz       = Unit(FREQUENCY, "kHz", 1e3)
megahertz       = Unit(FREQUENCY, "MHz", 1e6)
gigahertz       = Unit(FREQUENCY, "GHz", 1e9)
terahertz       = Unit(FREQUENCY, "THz", 1e12)

# Force (newton)
newton          = Unit(FORCE, "N", 1.0)
N               = newton
micronewton     = Unit(FORCE, "μN", 1e-6)
millinewton     = Unit(FORCE, "mN", 1e-3)
kilonewton      = Unit(FORCE, "kN", 1e3)
kN              = kilonewton
meganewton      = Unit(FORCE, "MN", 1e6)
MN              = meganewton

# Pressure / Stress (pascal)
pascal          = Unit(PRESSURE, "Pa", 1.0)
Pa              = pascal
hectopascal     = Unit(PRESSURE, "hPa", 100.0)
kilopascal      = Unit(PRESSURE, "kPa", 1e3)
kPa             = kilopascal
megapascal      = Unit(PRESSURE, "MPa", 1e6)
MPa             = megapascal
gigapascal      = Unit(PRESSURE, "GPa", 1e9)
bar             = Unit(PRESSURE, "bar", 100000.0)
millibar        = Unit(PRESSURE, "mbar", 100.0)

# Energy / Work / Heat (joule)
joule           = Unit(ENERGY, "J", 1.0)
J               = joule
attojoule       = Unit(ENERGY, "aJ", 1e-18)
nanojoule       = Unit(ENERGY, "nJ", 1e-9)
microjoule      = Unit(ENERGY, "μJ", 1e-6)
millijoule      = Unit(ENERGY, "mJ", 1e-3)
kilojoule       = Unit(ENERGY, "kJ", 1e3)
kJ              = kilojoule
megajoule       = Unit(ENERGY, "MJ", 1e6)
MJ              = megajoule
gigajoule       = Unit(ENERGY, "GJ", 1e9)
electronvolt    = Unit(ENERGY, "eV", 1.602176634e-19)
eV              = electronvolt
kiloelectronvolt= Unit(ENERGY, "keV", 1.602176634e-16)
megaelectronvolt= Unit(ENERGY, "MeV", 1.602176634e-13)
gigaelectronvolt= Unit(ENERGY, "GeV", 1.602176634e-10)

# Power / Radiant Flux (watt)
watt            = Unit(POWER, "W", 1.0)
W               = watt
picowatt        = Unit(POWER, "pW", 1e-12)
nanowatt        = Unit(POWER, "nW", 1e-9)
microwatt       = Unit(POWER, "μW", 1e-6)
milliwatt       = Unit(POWER, "mW", 1e-3)
kilowatt        = Unit(POWER, "kW", 1e3)
kW              = kilowatt
megawatt        = Unit(POWER, "MW", 1e6)
MW              = megawatt
gigawatt        = Unit(POWER, "GW", 1e9)

# Electric Charge (coulomb)
coulomb         = Unit(CHARGE, "C", 1.0)
C               = coulomb
picocoulomb     = Unit(CHARGE, "pC", 1e-12)
nanocoulomb     = Unit(CHARGE, "nC", 1e-9)
microcoulomb    = Unit(CHARGE, "μC", 1e-6)
millicoulomb    = Unit(CHARGE, "mC", 1e-3)
kilocoulomb     = Unit(CHARGE, "kC", 1e3)

# Voltage / Electric Potential (volt)
volt            = Unit(VOLTAGE, "V", 1.0)
V               = volt
microvolt       = Unit(VOLTAGE, "μV", 1e-6)
millivolt       = Unit(VOLTAGE, "mV", 1e-3)
mV              = millivolt
kilovolt        = Unit(VOLTAGE, "kV", 1e3)
kV              = kilovolt
megavolt        = Unit(VOLTAGE, "MV", 1e6)

# Electrical Capacitance (farad)
farad           = Unit(CAPACITANCE, "F", 1.0)
F               = farad
picofarad       = Unit(CAPACITANCE, "pF", 1e-12)
nanofarad       = Unit(CAPACITANCE, "nF", 1e-9)
microfarad      = Unit(CAPACITANCE, "μF", 1e-6)
millifarad      = Unit(CAPACITANCE, "mF", 1e-3)

# Electrical Resistance (ohm)
ohm             = Unit(RESISTANCE, "Ω", 1.0)
Ohm             = ohm
milliohm        = Unit(RESISTANCE, "mΩ", 1e-3)
kiloohm         = Unit(RESISTANCE, "kΩ", 1e3)
kOhm            = kiloohm
megaohm         = Unit(RESISTANCE, "MΩ", 1e6)
MOhm            = megaohm
gigaohm         = Unit(RESISTANCE, "GΩ", 1e9)

# Electrical Conductance (siemens)
siemens         = Unit(CONDUCTANCE, "S", 1.0)
S               = siemens
microsiemens    = Unit(CONDUCTANCE, "μS", 1e-6)
millisiemens    = Unit(CONDUCTANCE, "mS", 1e-3)

# Magnetic Flux (weber)
weber           = Unit(MAGNETIC_FLUX, "Wb", 1.0)
Wb              = weber
milliweber      = Unit(MAGNETIC_FLUX, "mWb", 1e-3)

# Magnetic Flux Density / Field (tesla)
tesla           = Unit(MAGNETIC_FIELD, "T", 1.0)
T               = tesla
microtesla      = Unit(MAGNETIC_FIELD, "μT", 1e-6)
millitesla      = Unit(MAGNETIC_FIELD, "mT", 1e-3)

# Inductance (henry)
henry           = Unit(INDUCTANCE, "H", 1.0)
H               = henry
microhenry      = Unit(INDUCTANCE, "μH", 1e-6)
millihenry      = Unit(INDUCTANCE, "mH", 1e-3)

# Luminous Flux (lumen)
lumen           = Unit(LUMINOUS_FLUX, "lm", 1.0)
lm              = lumen

# Illuminance (lux)
lux             = Unit(ILLUMINANCE, "lx", 1.0)
lx              = lux

# Radioactivity (becquerel)
becquerel       = Unit(ACTIVITY, "Bq", 1.0)
Bq              = becquerel
kilobecquerel   = Unit(ACTIVITY, "kBq", 1e3)
megabecquerel   = Unit(ACTIVITY, "MBq", 1e6)
gigabecquerel   = Unit(ACTIVITY, "GBq", 1e9)

# Absorbed Dose (gray)
gray            = Unit(ABSORBED_DOSE, "Gy", 1.0)
Gy              = gray
milligray       = Unit(ABSORBED_DOSE, "mGy", 1e-3)
microgray       = Unit(ABSORBED_DOSE, "μGy", 1e-6)

# Equivalent Dose (sievert)
sievert         = Unit(DOSE_EQUIVALENT, "Sv", 1.0)
Sv              = sievert
millisievert    = Unit(DOSE_EQUIVALENT, "mSv", 1e-3)
microsievert    = Unit(DOSE_EQUIVALENT, "μSv", 1e-6)

# Catalytic Activity (katal)
katal           = Unit(CATALYTIC_ACTIVITY, "kat", 1.0)
kat             = katal
microkatal      = Unit(CATALYTIC_ACTIVITY, "μkat", 1e-6)

# ==============================================================================
# DERIVED COMBINED UNITS (Volume, Area, Velocity, Density, Viscosity, etc.)
# ==============================================================================

# Area
square_meter        = Unit(AREA, "m²", 1.0)
sq_m                = square_meter
square_centimeter   = Unit(AREA, "cm²", 1e-4)
square_millimeter   = Unit(AREA, "mm²", 1e-6)
square_kilometer    = Unit(AREA, "km²", 1e6)
hectare             = Unit(AREA, "ha", 1e4)

# Volume
cubic_meter         = Unit(VOLUME, "m³", 1.0)
m3                  = cubic_meter
liter               = Unit(VOLUME, "L", 1e-3)
L                   = liter
milliliter          = Unit(VOLUME, "mL", 1e-6)
mL                  = milliliter
microliter          = Unit(VOLUME, "μL", 1e-9)
ul                  = microliter
centiliter          = Unit(VOLUME, "cL", 1e-5)
deciliter           = Unit(VOLUME, "dL", 1e-4)
cubic_centimeter    = Unit(VOLUME, "cm³", 1e-6)
cc                  = cubic_centimeter

# Velocity / Speed
meter_per_second    = Unit(VELOCITY, "m/s", 1.0)
mps                 = meter_per_second
kilometer_per_hour  = Unit(VELOCITY, "km/h", 1/3.6)
kmh                 = kilometer_per_hour

# Acceleration
meter_per_second_sq = Unit(ACCELERATION, "m/s²", 1.0)

# Density
kilogram_per_cubic_meter  = Unit(DENSITY, "kg/m³", 1.0)
gram_per_cubic_centimeter = Unit(DENSITY, "g/cm³", 1000.0)
gram_per_milliliter       = Unit(DENSITY, "g/mL", 1000.0)

# Viscosity
pascal_second       = Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0)
millipascal_second  = Unit(DYNAMIC_VISCOSITY, "mPa·s", 1e-3)
square_meter_per_second = Unit(KINEMATIC_VISCOSITY, "m²/s", 1.0)

# Concentration / Molarity
mole_per_cubic_meter = Unit(MOLAR_CONCENTRATION, "mol/m³", 1.0)
molar                = Unit(MOLAR_CONCENTRATION, "M", 1000.0)
M                    = molar
millimolar           = Unit(MOLAR_CONCENTRATION, "mM", 1.0)
mM                   = millimolar

# Thermal
joule_per_kelvin          = Unit(HEAT_CAPACITY, "J/K", 1.0)
joule_per_kilogram_kelvin = Unit(SPECIFIC_HEAT, "J/(kg·K)", 1.0)
watt_per_meter_kelvin     = Unit(THERMAL_CONDUCTIVITY, "W/(m·K)", 1.0)