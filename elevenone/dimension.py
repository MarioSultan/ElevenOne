class Dimension:

    def __init__(self, dimension: list):
        dimensions = [
            "Longitud",
            "Masa",
            "Tiempo",
            "Corriente",
            "Temperatura",
            "Cantidad de sustancia",
            "Intensidad luminosa"
        ]

        # Asegurar que la lista de dimensiones tenga la longitud correcta (7 magnitudes fundamentales)
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
# DIMENSIONES FUNDAMENTALES (SI)
# ==============================================================================
DIMENSIONLESS       = Dimension([])
LENGTH              = Dimension([1])
MASS                = Dimension([0, 1])     
TIME                = Dimension([0, 0, 1])
CURRENT             = Dimension([0, 0, 0, 1])
TEMPERATURE         = Dimension([0, 0, 0, 0, 1])
AMOUNT              = Dimension([0, 0, 0, 0, 0, 1])
LUMINOUS            = Dimension([0, 0, 0, 0, 0, 0, 1])

# ==============================================================================
# DIMENSIONES DERIVADAS (MECÁNICA Y CINEMÁTICA)
# ==============================================================================
AREA                = LENGTH**2
VOLUME              = LENGTH**3
VELOCITY            = LENGTH / TIME
SPEED               = VELOCITY
ACCELERATION        = VELOCITY / TIME
JERK                = ACCELERATION / TIME

DENSITY             = MASS / VOLUME
SPECIFIC_VOLUME     = VOLUME / MASS
MOMENTUM            = MASS * VELOCITY
ANGULAR_MOMENTUM    = MASS * (LENGTH**2) / TIME
MOMENT_OF_INERTIA   = MASS * (LENGTH**2)

FORCE               = MASS * LENGTH / (TIME**2)
TORQUE              = FORCE * LENGTH
PRESSURE            = FORCE / (LENGTH**2)
STRESS              = PRESSURE
DYNAMIC_VISCOSITY   = PRESSURE * TIME
KINEMATIC_VISCOSITY = (LENGTH**2) / TIME
SURFACE_TENSION     = FORCE / LENGTH

ENERGY              = FORCE * LENGTH
WORK                = ENERGY
POWER               = ENERGY / TIME
ACTION              = ENERGY * TIME

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
INDUCTANCE          = MAGNETIC_FLUX / CURRENT

ELECTRIC_FIELD      = VOLTAGE / LENGTH
ELECTRIC_DISPLACEMENT = CHARGE / AREA
PERMITTIVITY        = CAPACITANCE / LENGTH
PERMEABILITY        = INDUCTANCE / LENGTH
CHARGE_DENSITY      = CHARGE / VOLUME
CURRENT_DENSITY     = CURRENT / AREA

# ==============================================================================
# DIMENSIONES DERIVADAS (TERMODINÁMICA Y OTRAS)
# ==============================================================================
ENTROPY             = ENERGY / TEMPERATURE
HEAT_CAPACITY       = ENTROPY
SPECIFIC_HEAT       = HEAT_CAPACITY / MASS
THERMAL_CONDUCTIVITY= POWER / (LENGTH * TEMPERATURE)

FREQUENCY           = 1 / TIME
ACTIVITY            = FREQUENCY             # Becquerel (radiactividad)
LUMINOUS_FLUX       = LUMINOUS              # Lumen
ILLUMINANCE         = LUMINOUS_FLUX / AREA  # Lux
MOLAR_CONCENTRATION = AMOUNT / VOLUME
MOLAR_MASS          = MASS / AMOUNT
MOLAR_ENERGY        = ENERGY / AMOUNT