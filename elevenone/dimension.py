class Dimension:

    def __init__(self, dimension: list):
        dimensions = [
            "Longitud",
            "Masa",
            "Tiempo",
            "Corriente",
            "Temperatura",
            "Cantidad de sustancia",
            "Intensidad luminosa",
            "Angulo"
        ]

        # Asegurar que la lista de dimensiones tenga la longitud correcta (8 magnitudes)
        dimension = list(dimension)
        while len(dimension) < len(dimensions):
            dimension.append(0)

        self.dimension = dimension

    def __str__(self):
        return str(f"(Dimension: {self.dimension})")

    def __repr__(self):
        return f"Dimension({self.dimension})"

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self
        return Dimension([a + b for a, b in zip(self.dimension, other.dimension)])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __pow__(self, n):
        return Dimension([n * a for a in self.dimension])

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self
        return Dimension([a - b for a, b in zip(self.dimension, other.dimension)])

    def __rtruediv__(self, other):
        # 1 / Dimension -> Inverso de la dimensión
        return Dimension([-a for a in self.dimension])

    def __eq__(self, other):
        if not isinstance(other, Dimension):
            return False
        return self.dimension == other.dimension

    def __ne__(self, other):
        return not self.__eq__(other)


# ==============================================================================
# DIMENSIONES FUNDAMENTALES (SI + ÁNGULO)
# ==============================================================================
DIMENSIONLESS       = Dimension([])
LENGTH              = Dimension([1])
MASS                = Dimension([0, 1])     
TIME                = Dimension([0, 0, 1])
CURRENT             = Dimension([0, 0, 0, 1])
TEMPERATURE         = Dimension([0, 0, 0, 0, 1])
AMOUNT              = Dimension([0, 0, 0, 0, 0, 1])
LUMINOUS            = Dimension([0, 0, 0, 0, 0, 0, 1])
ANGULAR             = Dimension([0, 0, 0, 0, 0, 0, 0, 1])

# ==============================================================================
# DIMENSIONES DERIVADAS (MECÁNICA Y CINEMÁTICA)
# ==============================================================================
AREA                = LENGTH**2
VOLUME              = LENGTH**3
VELOCITY            = LENGTH / TIME
SPEED               = VELOCITY
ACCELERATION        = VELOCITY / TIME
JERK                = ACCELERATION / TIME
SNAP                = JERK / TIME
CRACKLE             = SNAP / TIME
POP                 = CRACKLE / TIME

ANGULAR_VELOCITY    = ANGULAR / TIME
ANGULAR_ACCELERATION= ANGULAR_VELOCITY / TIME
ANGULAR_JERK        = ANGULAR_ACCELERATION / TIME

VOLUMETRIC_FLOW_RATE= VOLUME / TIME
MASS_FLOW_RATE      = MASS / TIME

FORCE               = MASS * LENGTH / (TIME**2)
TORQUE              = FORCE * LENGTH
PRESSURE            = FORCE / (LENGTH**2)
STRESS              = PRESSURE
DYNAMIC_VISCOSITY   = PRESSURE * TIME
KINEMATIC_VISCOSITY = (LENGTH**2) / TIME
SURFACE_TENSION     = FORCE / LENGTH
COMPRESSIBILITY     = 1 / PRESSURE
BULK_MODULUS        = PRESSURE

DENSITY             = MASS / VOLUME
SPECIFIC_VOLUME     = VOLUME / MASS
SPECIFIC_WEIGHT     = FORCE / VOLUME
MOMENTUM            = MASS * VELOCITY
IMPULSE             = MOMENTUM
ANGULAR_MOMENTUM    = MASS * (LENGTH**2) / TIME
MOMENT_OF_INERTIA   = MASS * (LENGTH**2)

ENERGY              = FORCE * LENGTH
WORK                = ENERGY
POWER               = ENERGY / TIME
ACTION              = ENERGY * TIME
ENERGY_DENSITY      = ENERGY / VOLUME
SPECIFIC_ENERGY     = ENERGY / MASS

# ==============================================================================
# DIMENSIONES DERIVADAS (ELECTROMAGNETISMO)
# ==============================================================================
CHARGE              = CURRENT * TIME
VOLTAGE             = ENERGY / CHARGE
ELECTRIC_POTENTIAL  = VOLTAGE
RESISTANCE          = VOLTAGE / CURRENT
CONDUCTANCE         = 1 / RESISTANCE
CAPACITANCE         = CHARGE / VOLTAGE

MAGNETIC_FLUX       = ENERGY / CURRENT
MAGNETIC_FIELD      = MAGNETIC_FLUX / AREA  # Tesla (B)
MAGNETIC_FIELD_STRENGTH = CURRENT / LENGTH  # Ampere/meter (H)
INDUCTANCE          = MAGNETIC_FLUX / CURRENT
MAGNETIC_MOMENT     = CURRENT * AREA
MAGNETIC_VECTOR_POTENTIAL = MAGNETIC_FLUX / LENGTH

ELECTRIC_FIELD      = VOLTAGE / LENGTH
ELECTRIC_DISPLACEMENT = CHARGE / AREA
PERMITTIVITY        = CAPACITANCE / LENGTH
PERMEABILITY        = INDUCTANCE / LENGTH
CHARGE_DENSITY      = CHARGE / VOLUME
SURFACE_CHARGE_DENSITY = CHARGE / AREA
LINEAR_CHARGE_DENSITY  = CHARGE / LENGTH
CURRENT_DENSITY     = CURRENT / AREA
RESISTIVITY         = RESISTANCE * LENGTH
CONDUCTIVITY        = 1 / RESISTIVITY
ELECTRIC_DIPOLE_MOMENT = CHARGE * LENGTH
RELUCTANCE          = 1 / INDUCTANCE

# ==============================================================================
# DIMENSIONES DERIVADAS (TERMODINÁMICA Y FISICOQUÍMICA)
# ==============================================================================
ENTROPY             = ENERGY / TEMPERATURE
HEAT_CAPACITY       = ENTROPY
SPECIFIC_HEAT       = HEAT_CAPACITY / MASS
SPECIFIC_ENTROPY    = SPECIFIC_HEAT
MOLAR_HEAT_CAPACITY = HEAT_CAPACITY / AMOUNT
MOLAR_ENTROPY       = MOLAR_HEAT_CAPACITY

THERMAL_CONDUCTIVITY= POWER / (LENGTH * TEMPERATURE)
THERMAL_RESISTANCE  = TEMPERATURE / POWER
THERMAL_DIFFUSIVITY = KINEMATIC_VISCOSITY  # L^2 / T
HEAT_TRANSFER_COEFFICIENT = POWER / (AREA * TEMPERATURE)

MOLAR_CONCENTRATION = AMOUNT / VOLUME
MOLAR_MASS          = MASS / AMOUNT
MOLAR_ENERGY        = ENERGY / AMOUNT
MOLAR_VOLUME        = VOLUME / AMOUNT
CATALYTIC_ACTIVITY  = AMOUNT / TIME         # Katal (kat)
MOLAR_CONDUCTIVITY  = CONDUCTIVITY / MOLAR_CONCENTRATION

# ==============================================================================
# DIMENSIONES DERIVADAS (ONDAS, RADIACIÓN Y DOSIMETRÍA)
# ==============================================================================
FREQUENCY           = 1 / TIME
WAVENUMBER          = 1 / LENGTH
IRRADIANCE          = POWER / AREA          # W / m^2
RADIANT_INTENSITY   = POWER                 # W / sr
SPECTRAL_POWER      = POWER / LENGTH

ACTIVITY            = FREQUENCY             # Becquerel (radiactividad)
ABSORBED_DOSE       = ENERGY / MASS         # Gray (Gy)
DOSE_EQUIVALENT     = ABSORBED_DOSE         # Sievert (Sv)
EXPOSURE            = CHARGE / MASS         # Roentgen / (C/kg)

LUMINOUS_FLUX       = LUMINOUS              # Lumen
ILLUMINANCE         = LUMINOUS_FLUX / AREA  # Lux
LUMINANCE           = LUMINOUS / AREA       # Candela / m^2
LUMINOUS_EFFICACY   = LUMINOUS_FLUX / POWER # lm / W

# ==============================================================================
# DIMENSIONES DERIVADAS (ASTROFÍSICA, MECÁNICA DE FLUIDOS Y GEOFÍSICA)
# ==============================================================================
GRAVITATIONAL_POTENTIAL = (LENGTH**2) / (TIME**2)
GRAVITATIONAL_CONSTANT  = (LENGTH**3) / (MASS * (TIME**2))
HUBBLE_CONSTANT         = 1 / TIME
CIRCULATION             = (LENGTH**2) / TIME
MASS_FLUX               = MASS / (AREA * TIME)
POWER_DENSITY           = POWER / VOLUME