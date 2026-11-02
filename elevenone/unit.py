from .dimension import *
import numpy as np

_basic_symbols = ["m", "kg", "s", "A", "K", "mol", "cd", "rad"]


def _format_dimension_symbol(dim_list):
    superscripts = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
    pos_parts = []
    neg_parts = []
    for sym, exp in zip(_basic_symbols, dim_list):
        if exp == 0:
            continue
        if exp == 1:
            part = sym
        elif exp == -1:
            part = f"{sym}⁻¹"
        else:
            exp_str = str(exp).translate(superscripts)
            part = f"{sym}{exp_str}"
        
        if exp > 0:
            pos_parts.append(part)
        else:
            neg_parts.append(part)
            
    all_parts = pos_parts + neg_parts
    if not all_parts:
        return "1"
    return "·".join(all_parts)


class Unit:
    __array_priority__ = 1000

    def __init__(self, dimension: Dimension, symbol: str = None, factor: float = 1.0,
                 offset: float = 0.0, linear: bool = True):
        self.dimension = dimension
        if symbol is None:
            self.symbol = _format_dimension_symbol(dimension.dimension)
        else:
            self.symbol = symbol
        self.factor = factor
        self.offset = offset
        self.linear = linear

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return f"Unit({self.symbol!r})"

    def __mul__(self, other):
        if isinstance(other, Unit):
            new_dim = self.dimension * other.dimension
            return Unit(new_dim,
                        _format_dimension_symbol(new_dim.dimension),
                        self.factor * other.factor)
        if isinstance(other, (int, float, np.number, np.ndarray, list, tuple)):
            return Quantity(other, self)

    def __rmul__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list, tuple)):
            return Quantity(other, self)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            new_dim = self.dimension / other.dimension
            return Unit(new_dim,
                        _format_dimension_symbol(new_dim.dimension),
                        self.factor / other.factor)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list, tuple)) and np.all(np.asarray(other) == 1):
            new_dim = DIMENSIONLESS / self.dimension
            return Unit(new_dim,
                        _format_dimension_symbol(new_dim.dimension), 1 / self.factor)

    def __pow__(self, n):
        new_dim = self.dimension ** n
        return Unit(new_dim,
                    _format_dimension_symbol(new_dim.dimension), self.factor ** n)


# Standard predefined units for mathematical operations
RADIAN = Unit(ANGULAR, "rad", 1.0)
DIMENSIONLESS_UNIT = Unit(DIMENSIONLESS, "1", 1.0)


class Quantity:
    """Physical quantity with standard uncertainty (1 sigma)."""
    __array_priority__ = 1000

    def __init__(self, value, unit: Unit, error=None):
        self.value = np.asarray(value)
        self.unit = unit

        if isinstance(error, Quantity):
            error = error.convert_to(unit).value
        if error is None:
            self.error = np.zeros_like(self.value, dtype=float)
        else:
            self.error = np.broadcast_to(np.asarray(error, dtype=float), self.value.shape).copy()

    @property
    def magnitude(self):
        return self.value

    @property
    def units(self):
        return self.unit

    def set_error(self, error):
        """Easily modifies the quantity's error."""
        if isinstance(error, Quantity):
            error = error.convert_to(self.unit).value
        if error is None:
            self.error = np.zeros_like(self.value, dtype=float)
        else:
            self.error = np.broadcast_to(np.asarray(error, dtype=float), self.value.shape).copy()
        return self

    def __str__(self):
        if np.any(self.error != 0):
            return f"({self.value} ± {self.error}) {self.unit.symbol}"
        return f"{self.value} {self.unit.symbol}"

    def __repr__(self):
        return f"Quantity({self.value!r}, {self.unit!r}, error={self.error!r})"

    def __array__(self, dtype=None, copy=None):
        arr = np.asarray(self.value, dtype=dtype)
        return arr.copy() if copy else arr

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return Quantity(self.value[key], self.unit, self.error[key])

    def __iter__(self):
        for i in range(len(self.value)):
            yield Quantity(self.value[i], self.unit, self.error[i])

    @staticmethod
    def _as_array(value):
        return np.asarray(value)

    def convert_to(self, target_unit: Unit):
        if self.unit.dimension != target_unit.dimension:
            raise ValueError(f"Cannot convert units of different dimensions: {self.unit.dimension} vs {target_unit.dimension}.")
        base_value = self.value * self.unit.factor + self.unit.offset
        target_value = (base_value - target_unit.offset) / target_unit.factor
        target_error = self.error * abs(self.unit.factor / target_unit.factor)
        return Quantity(target_value, target_unit, target_error)

    to = convert_to

    def _coerce_additive(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("Addition and subtraction require another Quantity with compatible units.")
        return other.convert_to(self.unit)

    def __add__(self, other):
        other = self._coerce_additive(other)
        return Quantity(self.value + other.value, self.unit,
                        np.sqrt(self.error**2 + other.error**2))

    def __radd__(self, other):
        if np.isscalar(other) and other == 0:
            return self
        return self.__add__(other)

    def __sub__(self, other):
        other = self._coerce_additive(other)
        return Quantity(self.value - other.value, self.unit,
                        np.sqrt(self.error**2 + other.error**2))

    def __rsub__(self, other):
        if isinstance(other, Quantity):
            return other.__sub__(self)
        raise TypeError("Subtraction requires quantities with compatible units.")

    def __neg__(self):
        return Quantity(-self.value, self.unit, self.error)

    def __pos__(self):
        return self

    def __abs__(self):
        return Quantity(np.abs(self.value), self.unit, self.error)

    def __mul__(self, other):
        if isinstance(other, Quantity):
            val = self.value * other.value
            err = np.sqrt((other.value * self.error)**2 + (self.value * other.error)**2)
            return Quantity(val, self.unit * other.unit, err)
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit * other, self.error)
        arr = np.asarray(other)
        return Quantity(self.value * arr, self.unit, np.abs(arr) * self.error)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            val = self.value / other.value
            with np.errstate(divide="ignore", invalid="ignore"):
                err = np.sqrt((self.error / other.value)**2 +
                              (self.value * other.error / other.value**2)**2)
            return Quantity(val, self.unit / other.unit, err)
        if isinstance(other, Unit):
            return Quantity(self.value, self.unit / other, self.error)
        arr = np.asarray(other)
        return Quantity(self.value / arr, self.unit, self.error / np.abs(arr))

    def __rtruediv__(self, other):
        if isinstance(other, Quantity):
            return other.__truediv__(self)
        if isinstance(other, Unit):
            val = 1 / self.value
            with np.errstate(divide="ignore", invalid="ignore"):
                err = np.abs(1 / self.value**2) * self.error
            return Quantity(val, other / self.unit, err)
        arr = np.asarray(other)
        val = arr / self.value
        with np.errstate(divide="ignore", invalid="ignore"):
            err = np.abs(arr / self.value**2) * self.error
        inv_dim = DIMENSIONLESS / self.unit.dimension
        inv_unit = Unit(inv_dim, None, 1 / self.unit.factor)
        return Quantity(val, inv_unit, err)

    def __pow__(self, n):
        val = self.value ** n
        with np.errstate(divide="ignore", invalid="ignore"):
            err = np.abs(n * self.value ** (n - 1)) * self.error
        return Quantity(val, self.unit ** n, np.nan_to_num(err, nan=0.0, posinf=0.0))

    def sum(self, *args, **kwargs):
        err = np.sqrt(np.sum(self.error**2, *args, **kwargs))
        return Quantity(np.sum(self.value, *args, **kwargs), self.unit, err)

    def mean(self, *args, **kwargs):
        axis = kwargs.get("axis", args[0] if args else None)
        count = self.value.size if axis is None else self.value.shape[axis]
        err = np.sqrt(np.sum(self.error**2, axis=axis, **{k: v for k, v in kwargs.items() if k != "axis"})) / max(count, 1)
        return Quantity(np.mean(self.value, *args, **kwargs), self.unit, err)

    def min(self, *args, **kwargs):
        idx = np.argmin(self.value, axis=kwargs.get("axis", None))
        return Quantity(np.min(self.value, *args, **kwargs), self.unit,
                        np.take_along_axis(self.error, np.expand_dims(idx, kwargs.get("axis", 0)),
                                           axis=kwargs.get("axis", 0)).squeeze() if kwargs.get("axis", None) is not None else self.error.flat[idx])

    def max(self, *args, **kwargs):
        idx = np.argmax(self.value, axis=kwargs.get("axis", None))
        return Quantity(np.max(self.value, *args, **kwargs), self.unit,
                        np.take_along_axis(self.error, np.expand_dims(idx, kwargs.get("axis", 0)),
                                           axis=kwargs.get("axis", 0)).squeeze() if kwargs.get("axis", None) is not None else self.error.flat[idx])

    def std(self, *args, **kwargs):
        axis = kwargs.get("axis", args[0] if args else None)
        mean = np.mean(self.value, axis=axis, keepdims=True)
        std = np.std(self.value, *args, **kwargs)
        n = self.value.size if axis is None else self.value.shape[axis]
        denom = np.maximum(np.abs(std) * max(n, 1), np.finfo(float).eps)
        err = np.sqrt(np.sum(((self.value - mean) * self.error)**2, axis=axis)) / denom
        return Quantity(std, self.unit, err)

    def var(self, *args, **kwargs):
        axis = kwargs.get("axis", args[0] if args else None)
        mean = np.mean(self.value, axis=axis, keepdims=True)
        n = self.value.size if axis is None else self.value.shape[axis]
        denom = max(n, 1)
        err = np.sqrt(np.sum((2 * (self.value - mean) * self.error)**2, axis=axis)) / denom
        return Quantity(np.var(self.value, *args, **kwargs), self.unit ** 2, err)

    def __lt__(self, other):
        return self.value < self._coerce_additive(other).value

    def __le__(self, other):
        return self.value <= self._coerce_additive(other).value

    def __gt__(self, other):
        return self.value > self._coerce_additive(other).value

    def __ge__(self, other):
        return self.value >= self._coerce_additive(other).value

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return False
        try:
            return np.array_equal(self.value, other.convert_to(self.unit).value)
        except (ValueError, TypeError):
            return False


# ==============================================================================
# MATHEMATICAL FUNCTIONS WITH DIMENSION VALIDATION AND ERROR PROPAGATION
# ==============================================================================

def _ensure_angular(x: Quantity) -> Quantity:
    """Validates that input x has ANGULAR dimension and converts to radians."""
    if not isinstance(x, Quantity):
        raise TypeError("Argument must be a Quantity.")
    if x.unit.dimension != ANGULAR:
        raise ValueError(f"Argument must have ANGULAR dimension, got {x.unit.dimension}.")
    return x.convert_to(RADIAN)


def _ensure_dimensionless(x: Quantity) -> Quantity:
    """Validates that input x is DIMENSIONLESS."""
    if not isinstance(x, Quantity):
        raise TypeError("Argument must be a Quantity.")
    if x.unit.dimension != DIMENSIONLESS:
        raise ValueError(f"Argument must be DIMENSIONLESS, got {x.unit.dimension}.")
    return x.convert_to(DIMENSIONLESS_UNIT)


# ------------------------------------------------------------------------------
# Trigonometric Functions (Require ANGULAR dimension, return DIMENSIONLESS)
# ------------------------------------------------------------------------------

def sin(x: Quantity) -> Quantity:
    rad = _ensure_angular(x)
    val = np.sin(rad.value)
    err = np.abs(np.cos(rad.value)) * rad.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


def cos(x: Quantity) -> Quantity:
    rad = _ensure_angular(x)
    val = np.cos(rad.value)
    err = np.abs(np.sin(rad.value)) * rad.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


def tan(x: Quantity) -> Quantity:
    rad = _ensure_angular(x)
    val = np.tan(rad.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = np.abs(1.0 / np.cos(rad.value)**2) * rad.error
    return Quantity(val, DIMENSIONLESS_UNIT, np.nan_to_num(err, nan=0.0, posinf=0.0))


# ------------------------------------------------------------------------------
# Inverse Trigonometric Functions (Require DIMENSIONLESS, return ANGULAR in radians)
# ------------------------------------------------------------------------------

def asin(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.arcsin(q.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / np.sqrt(1.0 - q.value**2)) * q.error
    return Quantity(val, RADIAN, np.nan_to_num(err, nan=0.0, posinf=0.0))


def acos(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.arccos(q.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / np.sqrt(1.0 - q.value**2)) * q.error
    return Quantity(val, RADIAN, np.nan_to_num(err, nan=0.0, posinf=0.0))


def atan(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.arctan(q.value)
    err = (1.0 / (1.0 + q.value**2)) * q.error
    return Quantity(val, RADIAN, err)


def atan2(y: Quantity, x: Quantity) -> Quantity:
    if not isinstance(y, Quantity) or not isinstance(x, Quantity):
        raise TypeError("Both arguments for atan2 must be Quantity objects.")
    if y.unit.dimension != x.unit.dimension:
        raise ValueError("Arguments for atan2 must have matching dimensions.")
    x_conv = x.convert_to(y.unit)
    val = np.arctan2(y.value, x_conv.value)
    denom = y.value**2 + x_conv.value**2
    with np.errstate(divide="ignore", invalid="ignore"):
        err = np.sqrt((x_conv.value * y.error)**2 + (y.value * x_conv.error)**2) / denom
    return Quantity(val, RADIAN, np.nan_to_num(err, nan=0.0, posinf=0.0))


# ------------------------------------------------------------------------------
# Hyperbolic Functions (Require DIMENSIONLESS or ANGULAR, return DIMENSIONLESS)
# ------------------------------------------------------------------------------

def sinh(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x) if x.unit.dimension == DIMENSIONLESS else _ensure_angular(x)
    val = np.sinh(q.value)
    err = np.abs(np.cosh(q.value)) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


def cosh(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x) if x.unit.dimension == DIMENSIONLESS else _ensure_angular(x)
    val = np.cosh(q.value)
    err = np.abs(np.sinh(q.value)) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


def tanh(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x) if x.unit.dimension == DIMENSIONLESS else _ensure_angular(x)
    val = np.tanh(q.value)
    err = (1.0 / np.cosh(q.value)**2) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


# ------------------------------------------------------------------------------
# Exponential and Logarithmic Functions (Require DIMENSIONLESS, return DIMENSIONLESS)
# ------------------------------------------------------------------------------

def exp(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.exp(q.value)
    err = val * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, err)


def log(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.log(q.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / np.abs(q.value)) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, np.nan_to_num(err, nan=0.0, posinf=0.0))


def log10(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.log10(q.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / (np.abs(q.value) * np.log(10))) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, np.nan_to_num(err, nan=0.0, posinf=0.0))


def log2(x: Quantity) -> Quantity:
    q = _ensure_dimensionless(x)
    val = np.log2(q.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / (np.abs(q.value) * np.log(2))) * q.error
    return Quantity(val, DIMENSIONLESS_UNIT, np.nan_to_num(err, nan=0.0, posinf=0.0))


# ------------------------------------------------------------------------------
# Roots and Power Functions (Accept any dimension)
# ------------------------------------------------------------------------------

def sqrt(x: Quantity) -> Quantity:
    if not isinstance(x, Quantity):
        raise TypeError("Argument must be a Quantity.")
    val = np.sqrt(x.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (0.5 / np.sqrt(x.value)) * x.error
    return Quantity(val, x.unit ** 0.5, np.nan_to_num(err, nan=0.0, posinf=0.0))


def cbrt(x: Quantity) -> Quantity:
    if not isinstance(x, Quantity):
        raise TypeError("Argument must be a Quantity.")
    val = np.cbrt(x.value)
    with np.errstate(divide="ignore", invalid="ignore"):
        err = (1.0 / (3.0 * np.cbrt(x.value)**2)) * x.error
    return Quantity(val, x.unit ** (1.0 / 3.0), np.nan_to_num(err, nan=0.0, posinf=0.0))