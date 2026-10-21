from .dimension import *
import numpy as np

_basic_symbols = ["m", "kg", "s", "A", "K", "mol", "cd"]

class Unit:

    __array_priority__ = 1000

    def __init__(self, dimension: Dimension, symbol: str, factor: float = 1.0, offset: float = 0.0, linear: bool = True):
       self.dimension = dimension
       self.symbol = symbol
       self.factor = factor  
       self.offset = offset  
       self.linear = linear

    def __str__(self):
        return self.symbol

    def __mul__(self, other):
        if isinstance(other, Unit):
            new_dim = self.dimension * other.dimension
            new_symbol = f"{self.symbol}·{other.symbol}"
            new_factor = self.factor * other.factor
            return Unit(new_dim, new_symbol, new_factor, 0, True)
        elif isinstance(other, (int, float, np.number, np.ndarray, list)):
            return Quantity(other, self)

    def __rmul__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list)):
            return Quantity(other, self)

    def __truediv__(self, other):
        if isinstance(other, Unit):
            new_dim = self.dimension / other.dimension
            new_symbol = f"{self.symbol}/{other.symbol}"
            new_factor = self.factor / other.factor
            return Unit(new_dim, new_symbol, new_factor, 0, True)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list)) and np.all(other == 1):
            new_dim = DIMENSIONLESS / self.dimension
            new_symbol = f"{self.symbol}⁻¹"
            new_factor = 1 / self.factor
            return Unit(new_dim, new_symbol, new_factor, 0, True)

    def __pow__(self, n):
        new_dim = self.dimension ** n
        superscripts = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")
        n_str = str(n).translate(superscripts)
        new_symbol = f"({self.symbol}){n_str}" if "/" in self.symbol or "·" in self.symbol else f"{self.symbol}{n_str}"
        new_factor = self.factor ** n
        return Unit(new_dim, new_symbol, new_factor, 0, True)

class Quantity:
    __array_priority__ = 1000 
    
    def __init__(self, value, unit: Unit):
        if isinstance(value, np.ndarray):
            self.value = value
        else:
            self.value = np.asarray(value)
        self.unit = unit

    @property
    def magnitude(self):
        """Devuelve el array o valor numérico interno."""
        return self.value

    @property
    def units(self):
        """Devuelve la unidad asociada."""
        return self.unit

    def __str__(self):
        return f"{self.value} {self.unit.symbol}"

    def __repr__(self):
        return f"Quantity({self.value}, {self.unit!r})"

    def __array__(self, dtype=None, copy=None):
        """Permite integración nativa con NumPy y Pandas."""
        return np.array(self.value, dtype=dtype, copy=copy)

    def __len__(self):
        return len(self.value)

    def __getitem__(self, key):
        return Quantity(self.value[key], self.unit)

    def __iter__(self):
        for val in self.value:
            yield Quantity(val, self.unit)

    def convert_to(self, target_unit: Unit):
        if self.unit.dimension != target_unit.dimension:
            raise ValueError("No se pueden convertir unidades de distinta dimensión.")
        
        base_value = (self.value * self.unit.factor) + self.unit.offset
        target_value = (base_value - target_unit.offset) / target_unit.factor
        return Quantity(target_value, target_unit)

    def __mul__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, self.unit * other.unit)
        elif isinstance(other, (int, float, np.number, np.ndarray, list)):
            return Quantity(self.value * other, self.unit)

    def __rmul__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list)):
            return Quantity(other * self.value, self.unit)
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, self.unit / other.unit)
        elif isinstance(other, (int, float, np.number, np.ndarray, list)):
            return Quantity(self.value / other, self.unit)

    def __rtruediv__(self, other):
        if isinstance(other, (int, float, np.number, np.ndarray, list)):
            inv_unit = 1 / self.unit
            return Quantity(other / self.value, inv_unit)

    def __pow__(self, n):
        return Quantity(self.value ** n, self.unit ** n)

    def __add__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("Solo se puede sumar una Quantity con otra Quantity.")
        other_converted = other.convert_to(self.unit)
        base_self = (self.value * self.unit.factor) + self.unit.offset
        base_other = (other_converted.value * self.unit.factor) + self.unit.offset
        base_sum = base_self + base_other
        return Quantity((base_sum - self.unit.offset) / self.unit.factor, self.unit)

    def __sub__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("Solo se puede restar una Quantity con otra Quantity.")
        other_converted = other.convert_to(self.unit)
        base_self = (self.value * self.unit.factor) + self.unit.offset
        base_other = (other_converted.value * self.unit.factor) + self.unit.offset
        base_sub = base_self - base_other
        return Quantity((base_sub - self.unit.offset) / self.unit.factor, self.unit)

    def sum(self, *args, **kwargs):
        return Quantity(np.sum(self.value, *args, **kwargs), self.unit)

    def mean(self, *args, **kwargs):
        return Quantity(np.mean(self.value, *args, **kwargs), self.unit)

    def min(self, *args, **kwargs):
        return Quantity(np.min(self.value, *args, **kwargs), self.unit)

    def max(self, *args, **kwargs):
        return Quantity(np.max(self.value, *args, **kwargs), self.unit)

    def std(self, *args, **kwargs):
        return Quantity(np.std(self.value, *args, **kwargs), self.unit)

    def var(self, *args, **kwargs):
        return Quantity(np.var(self.value, *args, **kwargs), self.unit ** 2)

    def __lt__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("La comparación requiere otra Quantity.")
        return self.value < other.convert_to(self.unit).value

    def __le__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("La comparación requiere otra Quantity.")
        return self.value <= other.convert_to(self.unit).value

    def __gt__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("La comparación requiere otra Quantity.")
        return self.value > other.convert_to(self.unit).value

    def __ge__(self, other):
        if not isinstance(other, Quantity):
            raise TypeError("La comparación requiere otra Quantity.")
        return self.value >= other.convert_to(self.unit).value

    def __eq__(self, other):
        if not isinstance(other, Quantity):
            return False
        try:
            return np.array_equal(self.value, other.convert_to(self.unit).value)
        except ValueError:
            return False