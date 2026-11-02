from .dimension import *
from .unit import Unit

# ==============================================================================
# IMPERIAL & US CUSTOMARY UNITS (UNIDADES IMPERIALES Y US CUSTOMARY)
# ==============================================================================

# --- Length (Longitud) ---
thou                    = Unit(LENGTH, "th", 0.0000254)  # 1 thou = 1 mil = 0.001 in
mil                     = thou
inch                    = Unit(LENGTH, "in", 0.0254)
foot                    = Unit(LENGTH, "ft", 0.3048)
ft                      = foot
yard                    = Unit(LENGTH, "yd", 0.9144)
yd                      = yard
fathom                  = Unit(LENGTH, "ftm", 1.8288)  # 6 ft
rod                     = Unit(LENGTH, "rd", 5.0292)  # pole / perch (16.5 ft)
pole                    = rod
perch                   = rod
chain                   = Unit(LENGTH, "ch", 20.1168)  # 66 ft / 4 rods
furlong                 = Unit(LENGTH, "fur", 201.168)  # 660 ft / 10 chains
mile                    = Unit(LENGTH, "mi", 1609.344)
mi                      = mile
statute_mile            = mile
nautical_mile           = Unit(LENGTH, "nmi", 1852.0)
nmi                     = nautical_mile
league                  = Unit(LENGTH, "lea", 4828.032)  # 3 miles

# --- Area (Área) ---
square_inch             = Unit(AREA, "in²", 0.00064516)
sq_in                   = square_inch
square_foot             = Unit(AREA, "ft²", 0.09290304)
sq_ft                   = square_foot
square_yard             = Unit(AREA, "yd²", 0.83612736)
sq_yd                   = square_yard
square_rod              = Unit(AREA, "rd²", 25.29285264)
rood                    = Unit(AREA, "rood", 1011.7141056)  # 1/4 acre
acre                    = Unit(AREA, "acre", 4046.8564224)
square_mile             = Unit(AREA, "mi²", 2589988.110336)
sq_mi                   = square_mile

# --- Volume & Capacity (Volumen y Capacidad Imperial UK) ---
fluid_ounce_imp         = Unit(VOLUME, "fl oz (imp)", 2.84130625e-5)
fl_oz                   = fluid_ounce_imp
gill_imp                = Unit(VOLUME, "gi (imp)", 0.0001420653125)  # 5 fl oz
pint_imp                = Unit(VOLUME, "pt (imp)", 0.00056826125)     # 20 fl oz
pt                      = pint_imp
quart_imp               = Unit(VOLUME, "qt (imp)", 0.0011365225)       # 2 pints
qt                      = quart_imp
gallon_imp              = Unit(VOLUME, "gal (imp)", 0.00454609)        # 4 quarts (Exact Imperial standard)
gal                     = gallon_imp
peck_imp                = Unit(VOLUME, "pk (imp)", 0.00909218)         # 2 gallons
bushel_imp              = Unit(VOLUME, "bu (imp)", 0.03636872)         # 8 gallons
cubic_inch              = Unit(VOLUME, "in³", 1.6387064e-5)
cu_in                   = cubic_inch
cubic_foot              = Unit(VOLUME, "ft³", 0.028316846592)
cu_ft                   = cubic_foot
cubic_yard              = Unit(VOLUME, "yd³", 0.764554857984)
cu_yd                   = cubic_yard

# --- Volume (US Customary Liquid / Dry comparison) ---
gallon_us               = Unit(VOLUME, "gal (US)", 0.003785411784)
fluid_ounce_us          = Unit(VOLUME, "fl oz (US)", 2.95735295625e-5)

# --- Mass & Weight (Masa Avoirdupois y Troy) ---
grain                   = Unit(MASS, "gr", 0.00006479891)  # Exact standard across systems
gr                      = grain
dram_avdp               = Unit(MASS, "dr", 0.0017718451953125)
ounce_avdp              = Unit(MASS, "oz", 0.028349523125)
oz                      = ounce_avdp
pound_avdp              = Unit(MASS, "lb", 0.45359237)
lb                      = pound_avdp
stone                   = Unit(MASS, "st", 6.35029318)      # 14 lb (UK Imperial)
st                      = stone
quarter_imp             = Unit(MASS, "qr", 12.70058636)      # 28 lb / 2 stone
hundredweight_uk        = Unit(MASS, "cwt (UK)", 50.80234544) # Imperial Long CWT (112 lb)
cwt                     = hundredweight_uk
hundredweight_us        = Unit(MASS, "cwt (US)", 45.359237)   # Short CWT (100 lb)
ton_imperial            = Unit(MASS, "ton (UK)", 1016.0469088) # Long ton (2240 lb)
long_ton                = ton_imperial
ton_us                  = Unit(MASS, "ton (US)", 907.18474)    # Short ton (2000 lb)
short_ton               = ton_us
slug                    = Unit(MASS, "slug", 14.5939029372)

# Troy Mass (Precious Metals)
pennyweight             = Unit(MASS, "dwt", 0.00155517384)
ounce_troy              = Unit(MASS, "oz t", 0.0311034768)
oz_t                    = ounce_troy
pound_troy              = Unit(MASS, "lb t", 0.3732417216)

# --- Force, Torque & Mechanical Units ---
pound_force             = Unit(FORCE, "lbf", 4.4482216152605)
lbf                     = pound_force
poundal                 = Unit(FORCE, "pdl", 0.138254954376)  # 1 lb·ft/s²
pdl                     = poundal
kip                     = Unit(FORCE, "kip", 4448.2216152605)
pound_foot              = Unit(TORQUE, "lb·ft", 1.3558179483314)
lb_ft                   = pound_foot
pound_inch              = Unit(TORQUE, "lb·in", 0.112984829027616)
lb_in                   = pound_inch

# --- Pressure & Stress ---
pound_force_per_sq_inch = Unit(PRESSURE, "psi", 6894.757293168)
psi                     = pound_force_per_sq_inch
kilopound_per_sq_inch   = Unit(PRESSURE, "ksi", 6.894757293168e6)
ksi                     = kilopound_per_sq_inch
pound_per_sq_foot       = Unit(PRESSURE, "psf", 47.8802589803)
psf                     = pound_per_sq_foot
inches_of_mercury       = Unit(PRESSURE, "inHg", 3386.38815789)
inHg                    = inches_of_mercury
inches_of_water         = Unit(PRESSURE, "inH2O", 249.088908601)
inH2O                   = inches_of_water

# --- Energy, Heat & Power ---
british_thermal_unit    = Unit(ENERGY, "BTU", 1055.05585262)
BTU                     = british_thermal_unit
foot_pound              = Unit(ENERGY, "ft·lbf", 1.3558179483314)
ft_lbf                  = foot_pound
horsepower              = Unit(POWER, "hp", 745.69987158227)
hp                      = horsepower
btu_per_hour            = Unit(POWER, "BTU/h", 0.29307107)
BTU_per_h               = btu_per_hour

# --- Temperature ---
degree_fahrenheit       = Unit(TEMPERATURE, "°F", 5/9, offset=255.3722222222222)
degF                    = degree_fahrenheit
degree_rankine          = Unit(TEMPERATURE, "°R", 5/9, offset=0.0)
degR                    = degree_rankine