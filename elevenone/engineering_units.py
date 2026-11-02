from .dimension import *
from .unit import Unit
from .si_units import *

# ==============================================================================
# MECHANICAL & STRUCTURAL ENGINEERING
# ==============================================================================

# Pressure & Stress
pound_force_per_square_inch = Unit(PRESSURE, "psi", 6894.757293168)
psi                         = pound_force_per_square_inch
kilopound_per_square_inch   = Unit(PRESSURE, "ksi", 6.894757293168e6)
ksi                         = kilopound_per_square_inch
megapascal                  = Unit(PRESSURE, "MPa", 1e6)
MPa                         = megapascal
gigapascal                  = Unit(PRESSURE, "GPa", 1e9)
GPa                         = gigapascal
bar                         = Unit(PRESSURE, "bar", 100000.0)

# Force
pound_force                 = Unit(FORCE, "lbf", 4.4482216152605)
lbf                         = pound_force
kip                         = Unit(FORCE, "kip", 4448.2216152605)  # 1000 lbf
kilogram_force              = Unit(FORCE, "kgf", 9.80665)
kgf                         = kilogram_force
kilonewton                  = Unit(FORCE, "kN", 1e3)
kN                          = kilonewton
meganewton                  = Unit(FORCE, "MN", 1e6)
MN                          = meganewton

# Torque & Moment
newton_meter                = Unit(TORQUE, "N·m", 1.0)
Nm                          = newton_meter
kilonewton_meter            = Unit(TORQUE, "kN·m", 1e3)
pound_foot                  = Unit(TORQUE, "lb·ft", 1.3558179483314)
lb_ft                       = pound_foot
pound_inch                  = Unit(TORQUE, "lb·in", 0.112984829027616)
lb_in                       = pound_inch

# Power
horsepower                  = Unit(POWER, "hp", 745.69987158227)
hp                          = horsepower
metric_horsepower           = Unit(POWER, "PS", 735.49875)
PS                          = metric_horsepower
kilowatt                    = Unit(POWER, "kW", 1e3)
kW                          = kilowatt
megawatt                    = Unit(POWER, "MW", 1e6)
MW                          = megawatt

# Mass & Weight
slug                        = Unit(MASS, "slug", 14.5939029372)
pound                       = Unit(MASS, "lb", 0.45359237)
lb                          = pound
ounce                       = Unit(MASS, "oz", 0.028349523125)
metric_ton                  = Unit(MASS, "t", 1000.0)
tonne                       = metric_ton

# ==============================================================================
# ELECTRICAL & ELECTRONICS ENGINEERING
# ==============================================================================

# Voltage & Potential
volt                        = Unit(VOLTAGE, "V", 1.0)
V                           = volt
kilovolt                    = Unit(VOLTAGE, "kV", 1e3)
kV                          = kilovolt
megavolt                    = Unit(VOLTAGE, "MV", 1e6)
millivolt                   = Unit(VOLTAGE, "mV", 1e-3)
mV                          = millivolt
microvolt                   = Unit(VOLTAGE, "μV", 1e-6)

# Current
ampere                      = Unit(CURRENT, "A", 1.0)
A                           = ampere
milliampere                 = Unit(CURRENT, "mA", 1e-3)
mA                          = milliampere
microampere                 = Unit(CURRENT, "μA", 1e-6)
uA                          = microampere
kiloampere                  = Unit(CURRENT, "kA", 1e3)

# Resistance & Conductance
ohm                         = Unit(RESISTANCE, "Ω", 1.0)
Ohm                         = ohm
kiloohm                     = Unit(RESISTANCE, "kΩ", 1e3)
kOhm                        = kiloohm
megaohm                     = Unit(RESISTANCE, "MΩ", 1e6)
MOhm                        = megaohm
gigaohm                     = Unit(RESISTANCE, "GΩ", 1e9)
milliohm                    = Unit(RESISTANCE, "mΩ", 1e-3)

siemens                     = Unit(CONDUCTANCE, "S", 1.0)
S                           = siemens
millisiemens                = Unit(CONDUCTANCE, "mS", 1e-3)
microsiemens                = Unit(CONDUCTANCE, "μS", 1e-6)

# Capacitance & Inductance
farad                       = Unit(CAPACITANCE, "F", 1.0)
F                           = farad
microfarad                  = Unit(CAPACITANCE, "μF", 1e-6)
uF                          = microfarad
nanofarad                   = Unit(CAPACITANCE, "nF", 1e-9)
nF                          = nanofarad
picofarad                   = Unit(CAPACITANCE, "pF", 1e-12)
pF                          = picofarad

henry                       = Unit(INDUCTANCE, "H", 1.0)
H                           = henry
millihenry                  = Unit(INDUCTANCE, "mH", 1e-3)
mH                          = millihenry
microhenry                  = Unit(INDUCTANCE, "μH", 1e-6)
uH                          = microhenry

# Frequency & Energy / Work
hertz                       = Unit(FREQUENCY, "Hz", 1.0)
Hz                          = hertz
kilohertz                   = Unit(FREQUENCY, "kHz", 1e3)
kHz                         = kilohertz
megahertz                   = Unit(FREQUENCY, "MHz", 1e6)
MHz                         = megahertz
gigahertz                   = Unit(FREQUENCY, "GHz", 1e9)
GHz                         = gigahertz

kilowatt_hour               = Unit(ENERGY, "kWh", 3.6e6)
kWh                         = kilowatt_hour
megawatt_hour               = Unit(ENERGY, "MWh", 3.6e9)
MWh                         = megawatt_hour

# Apparent & Reactive Power (Power Systems)
volt_ampere                 = Unit(POWER, "VA", 1.0)
VA                          = volt_ampere
kilovolt_ampere             = Unit(POWER, "kVA", 1e3)
kVA                         = kilovolt_ampere
megavolt_ampere             = Unit(POWER, "MVA", 1e6)
MVA                         = megavolt_ampere

volt_ampere_reactive        = Unit(POWER, "var", 1.0)
var                         = volt_ampere_reactive
kilovolt_ampere_reactive   = Unit(POWER, "kvar", 1e3)
kvar                        = kilovolt_ampere_reactive
megavolt_ampere_reactive   = Unit(POWER, "Mvar", 1e6)
Mvar                        = megavolt_ampere_reactive

# ==============================================================================
# FLUID MECHANICS, HVAC & THERMODYNAMICS
# ==============================================================================

# Volumetric & Mass Flow
cubic_meter_per_second      = Unit(VOLUMETRIC_FLOW_RATE, "m³/s", 1.0)
m3_per_s                    = cubic_meter_per_second
cubic_meter_per_hour        = Unit(VOLUMETRIC_FLOW_RATE, "m³/h", 1/3600.0)
m3_per_h                    = cubic_meter_per_hour
cubic_feet_per_minute       = Unit(VOLUMETRIC_FLOW_RATE, "cfm", 0.0004719474432)
cfm                         = cubic_feet_per_minute
gallon_per_minute           = Unit(VOLUMETRIC_FLOW_RATE, "gpm", 6.30901964e-5)
gpm                         = gallon_per_minute
liter_per_second            = Unit(VOLUMETRIC_FLOW_RATE, "L/s", 0.001)
L_per_s                     = liter_per_second

kilogram_per_second         = Unit(MASS_FLOW_RATE, "kg/s", 1.0)
kg_per_s                    = kilogram_per_second
ton_per_hour                = Unit(MASS_FLOW_RATE, "t/h", 1000.0 / 3600.0)

# Viscosity
pascal_second               = Unit(DYNAMIC_VISCOSITY, "Pa·s", 1.0)
poise                       = Unit(DYNAMIC_VISCOSITY, "P", 0.1)
centipoise                  = Unit(DYNAMIC_VISCOSITY, "cP", 1e-3)
cP                          = centipoise
stokes                      = Unit(KINEMATIC_VISCOSITY, "St", 1e-4)
centistokes                 = Unit(KINEMATIC_VISCOSITY, "cSt", 1e-6)
cSt                         = centistokes

# HVAC & Thermal Units
british_thermal_unit        = Unit(ENERGY, "BTU", 1055.05585262)
BTU                         = british_thermal_unit
btu_per_hour                = Unit(POWER, "BTU/h", 0.29307107)
BTU_per_h                   = btu_per_hour
ton_of_refrigeration        = Unit(POWER, "TR", 3516.852842)
TR                          = ton_of_refrigeration
therm                       = Unit(ENERGY, "thm", 1.05505585262e8)

# ==============================================================================
# CIVIL, GEOTECHNICAL & SURVEYING ENGINEERING
# ==============================================================================

# Distance & Area
inch                        = Unit(LENGTH, "in", 0.0254)
foot                        = Unit(LENGTH, "ft", 0.3048)
ft                          = foot
yard                        = Unit(LENGTH, "yd", 0.9144)
yd                          = yard
mile                        = Unit(LENGTH, "mi", 1609.344)
mi                          = mile
nautical_mile               = Unit(LENGTH, "nmi", 1852.0)

acre                        = Unit(AREA, "acre", 4046.8564224)
square_foot                 = Unit(AREA, "ft²", 0.09290304)
sq_ft                       = square_foot
hectare                     = Unit(AREA, "ha", 10000.0)

# Volume & Soil / Material Density
cubic_yard                  = Unit(VOLUME, "yd³", 0.764554857984)
yd3                         = cubic_yard
pound_per_cubic_foot        = Unit(DENSITY, "lb/ft³", 16.01846337396)
pcf                         = pound_per_cubic_foot
kilonewton_per_cubic_meter  = Unit(SPECIFIC_WEIGHT, "kN/m³", 1000.0)

# Geotechnical Permeability
centimeter_per_second       = Unit(VELOCITY, "cm/s", 0.01)
darcy                       = Unit(DIMENSIONLESS, "Darcy", 9.869233e-13)
millidarcy                  = Unit(DIMENSIONLESS, "mD", 9.869233e-16)
mD                          = millidarcy