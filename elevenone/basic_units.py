from .unit import *

# ==============================================================================
# BIBLIOTECA DE UNIDADES PREDEFINIDAS
# (Base de Masa = kilogramos 'kg', Longitud = metros 'm', Tiempo = segundos 's')
# ==============================================================================

# --- Longitud ---
m    = Unit(LENGTH, "m", 1.0)
km   = Unit(LENGTH, "km", 1000.0)
cm   = Unit(LENGTH, "cm", 0.01)
mm   = Unit(LENGTH, "mm", 0.001)
um   = Unit(LENGTH, "μm", 1e-6)
nm   = Unit(LENGTH, "nm", 1e-9)

inch = Unit(LENGTH, "in", 0.0254)
ft   = Unit(LENGTH, "ft", 0.3048)
yd   = Unit(LENGTH, "yd", 0.9144)
mi   = Unit(LENGTH, "mi", 1609.344)
nmi  = Unit(LENGTH, "nmi", 1852.0)
angstrom = Unit(LENGTH, "Å", 1e-10)
ly   = Unit(LENGTH, "ly", 9.4607e15)

# --- Masa (Base SI: kilogramos 'kg') ---
kg   = Unit(MASS, "kg", 1.0)
g    = Unit(MASS, "g", 0.001)
mg   = Unit(MASS, "mg", 1e-6)
ug   = Unit(MASS, "μg", 1e-9)
ton  = Unit(MASS, "t", 1000.0)

lb   = Unit(MASS, "lb", 0.45359237)
oz   = Unit(MASS, "oz", 0.028349523125)
st   = Unit(MASS, "st", 6.35029318)      # stone
cwt  = Unit(MASS, "cwt", 50.80234544)    # hundredweight (UK)

# --- Tiempo ---
s    = Unit(TIME, "s", 1.0)
ms   = Unit(TIME, "ms", 0.001)
us   = Unit(TIME, "μs", 1e-6)
ns   = Unit(TIME, "ns", 1e-9)
min_unit = Unit(TIME, "min", 60.0)
h    = Unit(TIME, "h", 3600.0)
day  = Unit(TIME, "d", 86400.0)
week = Unit(TIME, "wk", 604800.0)
year = Unit(TIME, "yr", 31557600.0)

# --- Temperatura (Usando Offset respecto a Kelvin) ---
K    = Unit(TEMPERATURE, "K", 1.0, offset=0.0)
degC = Unit(TEMPERATURE, "°C", 1.0, offset=273.15)
degF = Unit(TEMPERATURE, "°F", 5/9, offset=255.3722222222222)
R    = Unit(TEMPERATURE, "°R", 5/9, offset=0.0)

# --- Corriente y Carga ---
A    = Unit(CURRENT, "A", 1.0)
mA   = Unit(CURRENT, "mA", 0.001)
uA   = Unit(CURRENT, "μA", 1e-6)
C    = Unit(CHARGE, "C", 1.0)   # 1 C = 1 A·s
Ah   = Unit(CHARGE, "Ah", 3600.0)
mAh  = Unit(CHARGE, "mAh", 3.6)

# --- Tensión y Resistencia Eléctrica ---
V    = Unit(VOLTAGE, "V", 1.0)
mV   = Unit(VOLTAGE, "mV", 0.001)
kV   = Unit(VOLTAGE, "kV", 1000.0)
Ohm  = Unit(RESISTANCE, "Ω", 1.0)
kOhm = Unit(RESISTANCE, "kΩ", 1000.0)
MOhm = Unit(RESISTANCE, "MΩ", 1e6)

# --- Fuerza (1 N = 1 kg·m/s²) ---
N    = Unit(FORCE, "N", 1.0)
kN   = Unit(FORCE, "kN", 1000.0)
MN   = Unit(FORCE, "MN", 1e6)
lbf  = Unit(FORCE, "lbf", 4.4482216)
dyn  = Unit(FORCE, "dyn", 1e-5)

# --- Presión (1 Pa = 1 N/m² = 1 kg/(m·s²)) ---
Pa   = Unit(PRESSURE, "Pa", 1.0)
kPa  = Unit(PRESSURE, "kPa", 1000.0)
MPa  = Unit(PRESSURE, "MPa", 1e6)
bar  = Unit(PRESSURE, "bar", 100000.0)
mbar = Unit(PRESSURE, "mbar", 100.0)
psi  = Unit(PRESSURE, "psi", 6894.757)
atm  = Unit(PRESSURE, "atm", 101325.0)
mmHg = Unit(PRESSURE, "mmHg", 133.322368)

# --- Energía y Potencia (1 J = 1 kg·m²/s², 1 W = 1 J/s) ---
J    = Unit(ENERGY, "J", 1.0)
kJ   = Unit(ENERGY, "kJ", 1000.0)
MJ   = Unit(ENERGY, "MJ", 1e6)
cal  = Unit(ENERGY, "cal", 4.184)
kcal = Unit(ENERGY, "kcal", 4184.0)
kWh  = Unit(ENERGY, "kWh", 3.6e6)
eV   = Unit(ENERGY, "eV", 1.602176634e-19)
BTU  = Unit(ENERGY, "BTU", 1055.05585)

W    = Unit(POWER, "W", 1.0)
kW   = Unit(POWER, "kW", 1000.0)
MW   = Unit(POWER, "MW", 1e6)
HP   = Unit(POWER, "HP", 745.69987)

# --- Volumen ---
L    = Unit(VOLUME, "L", 0.001)
mL   = Unit(VOLUME, "mL", 1e-6)
m3   = Unit(VOLUME, "m³", 1.0)
gal  = Unit(VOLUME, "gal", 0.003785411784)