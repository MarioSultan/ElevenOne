from .dimension import *
from .unit import Unit
from .si_units import *

# ==============================================================================
# PHARMACOLOGY, CONCENTRATION & DOSAGE
# ==============================================================================

# Mass-based Concentration (Blood & Lab Values)
milligram_per_deciliter = Unit(DENSITY, "mg/dL", 0.01)
mg_per_dL               = milligram_per_deciliter
microgram_per_deciliter = Unit(DENSITY, "μg/dL", 1e-5)
ug_per_dL               = microgram_per_deciliter
nanogram_per_deciliter  = Unit(DENSITY, "ng/dL", 1e-8)
ng_per_dL               = nanogram_per_deciliter
picogram_per_milliliter = Unit(DENSITY, "pg/mL", 1e-7)
pg_per_mL               = picogram_per_milliliter
nanogram_per_milliliter = Unit(DENSITY, "ng/mL", 1e-4)
ng_per_mL               = nanogram_per_milliliter
microgram_per_milliliter= Unit(DENSITY, "μg/mL", 1e-3)
ug_per_mL               = microgram_per_milliliter
milligram_per_liter     = Unit(DENSITY, "mg/L", 1e-3)
mg_per_L                = milligram_per_liter
gram_per_deciliter      = Unit(DENSITY, "g/dL", 10.0)
g_per_dL                = gram_per_deciliter

# Molar Concentration (Clinical Biochemistry)
millimolar              = Unit(MOLAR_CONCENTRATION, "mM", 1.0)
mM                      = millimolar
micromolar              = Unit(MOLAR_CONCENTRATION, "μM", 1e-3)
uM                      = micromolar
nanomolar               = Unit(MOLAR_CONCENTRATION, "nM", 1e-6)
nM                      = nanomolar
picomolar               = Unit(MOLAR_CONCENTRATION, "pM", 1e-9)
pM                      = picomolar
femtomolar              = Unit(MOLAR_CONCENTRATION, "fM", 1e-12)

# Electrolytes & Equivalents
equivalent              = Unit(AMOUNT, "Eq", 1.0)
Eq                      = equivalent
milliequivalent         = Unit(AMOUNT, "mEq", 1e-3)
mEq                     = milliequivalent
milliequivalent_per_liter = Unit(MOLAR_CONCENTRATION, "mEq/L", 1.0)
mEq_per_L               = milliequivalent_per_liter

# Osmolality & Osmolarity
osmole                  = Unit(AMOUNT, "osm", 1.0)
osm                     = osmole
milliosmole             = Unit(AMOUNT, "mOsm", 1e-3)
mOsm                    = milliosmole
milliosmole_per_kilogram= Unit(DIMENSIONLESS / MASS, "mOsm/kg", 1e-3)
mOsm_per_kg             = milliosmole_per_kilogram
milliosmole_per_liter   = Unit(MOLAR_CONCENTRATION, "mOsm/L", 1.0)
mOsm_per_L              = milliosmole_per_liter

# Dosage & Administration Rates
drop                    = Unit(VOLUME, "gtt", 5e-8)  # 1 mL ≈ 20 drops (gtt)
gtt                     = drop
microdrop               = Unit(VOLUME, "mcgtt", 1.6666666666666667e-8)  # 1 mL ≈ 60 microdrops
mcgtt                   = microdrop
milligram_per_kilogram  = Unit(DIMENSIONLESS, "mg/kg", 1e-6)
mg_per_kg               = milligram_per_kilogram
microgram_per_kilogram  = Unit(DIMENSIONLESS, "μg/kg", 1e-9)
ug_per_kg               = microgram_per_kilogram

# Infusion Rates
milliliter_per_hour     = Unit(VOLUMETRIC_FLOW_RATE, "mL/h", 2.777777777777778e-10)
mL_per_h                = milliliter_per_hour
drop_per_minute         = Unit(VOLUMETRIC_FLOW_RATE, "gtt/min", 8.333333333333333e-10)
gtt_per_min             = drop_per_minute

# International Units (Biologics, Insulin, Vitamins)
international_unit      = Unit(DIMENSIONLESS, "IU", 1.0)
IU                      = international_unit
unit_u                  = Unit(DIMENSIONLESS, "U", 1.0)
milliunit               = Unit(DIMENSIONLESS, "mU", 1e-3)
mU                      = milliunit
microunit               = Unit(DIMENSIONLESS, "μU", 1e-6)
uU                      = microunit

# ==============================================================================
# CARDIOVASCULAR, RESPIRATORY & CLINICAL HEMODYNAMICS
# ==============================================================================

# Hemodynamic Pressure
millimeter_of_mercury   = Unit(PRESSURE, "mmHg", 133.322368421)
mmHg                    = millimeter_of_mercury
centimeter_of_water     = Unit(PRESSURE, "cmH2O", 98.0665)
cmH2O                   = centimeter_of_water
torr                    = Unit(PRESSURE, "Torr", 133.322368421)

# Cardiac Output & Flow
liter_per_minute        = Unit(VOLUMETRIC_FLOW_RATE, "L/min", 1.6666666666666667e-5)
L_per_min               = liter_per_minute
cardiac_index           = Unit(VOLUMETRIC_FLOW_RATE / AREA, "L/(min·m²)", 1.6666666666666667e-5)

# Vascular Resistance
wood_unit               = Unit(PRESSURE * TIME / VOLUME, "WU", 7999342.1)  # mmHg·min/L
dyn_sec_cm5             = Unit(PRESSURE * TIME / VOLUME, "dyn·s/cm⁵", 1e5)  # 1 WU = 80 dyn·s/cm⁵

# Heart Rate & Frequency
beats_per_minute        = Unit(FREQUENCY, "bpm", 1 / 60.0)
bpm                     = beats_per_minute
breaths_per_minute      = Unit(FREQUENCY, "brpm", 1 / 60.0)
brpm                    = breaths_per_minute

# ==============================================================================
# CLINICAL RADIOLOGY, DOSIMETRY & RADIATION ONCOLOGY
# ==============================================================================

gray                    = Unit(ABSORBED_DOSE, "Gy", 1.0)
Gy                      = gray
milligray               = Unit(ABSORBED_DOSE, "mGy", 1e-3)
mGy                     = milligray
microgray               = Unit(ABSORBED_DOSE, "μGy", 1e-6)
uGy                     = microgray
centigray               = Unit(ABSORBED_DOSE, "cGy", 0.01)  # Common in radiotherapy
cGy                     = centigray

sievert                 = Unit(DOSE_EQUIVALENT, "Sv", 1.0)
Sv                      = sievert
millisievert            = Unit(DOSE_EQUIVALENT, "mSv", 1e-3)
mSv                     = millisievert
microsievert            = Unit(DOSE_EQUIVALENT, "μSv", 1e-6)
uSv                     = microsievert

roentgen                = Unit(EXPOSURE, "R", 2.58e-4)  # C/kg
milliroentgen           = Unit(EXPOSURE, "mR", 2.58e-7)

curie                   = Unit(ACTIVITY, "Ci", 3.7e10)
Ci                      = curie
millicurie              = Unit(ACTIVITY, "mCi", 3.7e7)
mCi                     = millicurie
microcurie              = Unit(ACTIVITY, "μCi", 3.7e4)
uCi                     = microcurie
becquerel               = Unit(ACTIVITY, "Bq", 1.0)
Bq                      = becquerel
megabecquerel           = Unit(ACTIVITY, "MBq", 1e6)
MBq                     = megabecquerel
gigabecquerel           = Unit(ACTIVITY, "GBq", 1e9)
GBq                     = gigabecquerel

# ==============================================================================
# ANTHROPOMETRY, PHYSIOLOGY & CLINICAL METRICS
# ==============================================================================

# Body Surface Area & Metabolic Rate
square_meter            = Unit(AREA, "m²", 1.0)
m2                      = square_meter
metabolic_equivalent    = Unit(POWER / AREA, "MET", 58.2)  # 1 MET ≈ 58.2 W/m² (or 3.5 mL O2/kg/min)
MET                     = metabolic_equivalent

# Clinical Temperature
degree_celsius          = Unit(TEMPERATURE, "°C", 1.0, offset=273.15)
degC                    = degree_celsius
degree_fahrenheit       = Unit(TEMPERATURE, "°F", 5/9, offset=255.3722222222222)
degF                    = degree_fahrenheit

# Clinical Mass & Weight
kilogram                = Unit(MASS, "kg", 1.0)
kg                      = kilogram
gram                    = Unit(MASS, "g", 1e-3)
g                       = gram
milligram               = Unit(MASS, "mg", 1e-6)
mg                      = milligram
microgram               = Unit(MASS, "μg", 1e-9)
mcg                     = microgram  # Medical standard abbreviation for microgram
ug                      = microgram

# Clinical Volume & Fluid Balance
deciliter               = Unit(VOLUME, "dL", 1e-4)
dL                      = deciliter
milliliter              = Unit(VOLUME, "mL", 1e-6)
mL                      = milliliter
microliter              = Unit(VOLUME, "μL", 1e-9)
uL                      = microliter
cc                      = milliliter  # Cubic centimeter (commonly used in clinical settings)