"""
Modulo de integración para conectar la biblioteca de unidades (Unit/Quantity)
con Pandas y Matplotlib.
"""

from typing import Union, Sequence, Optional, Any
import numpy as np
import pandas as pd
from pandas.api.extensions import (
    ExtensionDtype,
    ExtensionArray,
    register_extension_dtype,
)
import matplotlib.units as munits
import matplotlib.ticker as mticker

from .unit import Unit, Quantity


# ==============================================================================
# 1. INTEGRACIÓN CON MATPLOTLIB (Custom ConversionInterface)
# ==============================================================================

class QuantityConverter(munits.ConversionInterface):
    """
    Permite que Matplotlib reconozca objetos Quantity automáticamente.
    Añade etiquetas de unidades en los ejes e interactúa limpiamente con los gráficos.
    """

    @staticmethod
    def axisinfo(unit: Optional[Unit], axis: Any) -> munits.AxisInfo:
        """Devuelve la información del eje (label, ticks) en función de la unidad."""
        if unit is None:
            return None
        symbol = getattr(unit, "symbol", str(unit))
        label = f"({symbol})" if symbol else ""
        return munits.AxisInfo(label=label)

    @staticmethod
    def default_units(x: Any, axis: Any) -> Optional[Unit]:
        """Extrae la unidad por defecto a partir de los datos pasados al eje."""
        if isinstance(x, Quantity):
            return x.unit
        elif isinstance(x, (list, tuple, np.ndarray)) and len(x) > 0:
            first = x[0]
            if isinstance(first, Quantity):
                return first.unit
        return None

    @staticmethod
    def convert(val: Any, unit: Optional[Unit], axis: Any) -> np.ndarray:
        """Convierte los valores a la unidad solicitada por la gráfica (o extraer magnitudes)."""
        if unit is None:
            if isinstance(val, Quantity):
                return val.magnitude
            return np.asarray(val)

        if isinstance(val, Quantity):
            return val.convert_to(unit).magnitude

        if isinstance(val, (list, tuple, np.ndarray)):
            if len(val) == 0:
                return np.array([])
            if isinstance(val[0], Quantity):
                # Convertir cada Quantity a la unidad objetivo
                converted = [q.convert_to(unit).magnitude for q in val]
                return np.asarray(converted)

        return np.asarray(val)


# ==============================================================================
# 2. INTEGRACIÓN CON PANDAS (ExtensionDtype & ExtensionArray)
# ==============================================================================

@register_extension_dtype
class QuantityDtype(ExtensionDtype):
    """
    Dtype personalizado de Pandas para manejar arreglos con unidades físicas.
    """

    name = "quantity"
    type = Quantity
    kind = "O"

    def __init__(self, unit: Optional[Unit] = None):
        self._unit = unit

    @property
    def unit(self) -> Optional[Unit]:
        return self._unit

    @property
    def name(self) -> str:
        if self._unit is not None:
            return f"quantity[{self._unit.symbol}]"
        return "quantity"

    @classmethod
    def construct_array_type(cls):
        return QuantityArray

    @classmethod
    def construct_from_string(cls, string: str):
        if string == "quantity":
            return cls(None)
        raise NotImplementedError(
            f"No se puede instanciar {cls.__name__} directamente desde el string '{string}'. "
            "Usa QuantityDtype(unit) especificando la unidad."
        )


class QuantityArray(ExtensionArray):
    """
    Arreglo de Pandas que encapsula un objeto Quantity vectorizado.
    """

    def __init__(self, values: Union[Quantity, np.ndarray, list], unit: Optional[Unit] = None):
        if isinstance(values, Quantity):
            self._quantity = values
            if unit is not None and values.unit != unit:
                self._quantity = values.convert_to(unit)
        elif isinstance(values, (np.ndarray, list)):
            if unit is None:
                raise ValueError("Se debe especificar una unidad cuando values es un ndarray o list.")
            self._quantity = Quantity(values, unit)
        else:
            raise TypeError("Tipo de datos no soportado para QuantityArray.")

    @property
    def dtype(self) -> QuantityDtype:
        return QuantityDtype(self._quantity.unit)

    @property
    def quantity(self) -> Quantity:
        return self._quantity

    def __len__(self) -> int:
        return len(self._quantity.value)

    def __getitem__(self, item):
        result = self._quantity[item]
        if isinstance(result.value, np.ndarray) and result.value.ndim > 0:
            return QuantityArray(result)
        return result

    def __setitem__(self, key, value):
        if isinstance(value, Quantity):
            val_converted = value.convert_to(self._quantity.unit).magnitude
            self._quantity.value[key] = val_converted
        else:
            self._quantity.value[key] = value

    @classmethod
    def _from_sequence(cls, scalars, dtype=None, copy=False):
        if isinstance(scalars, QuantityArray):
            return scalars
        if len(scalars) > 0 and isinstance(scalars[0], Quantity):
            target_unit = scalars[0].unit
            vals = [q.convert_to(target_unit).magnitude for q in scalars]
            return cls(Quantity(vals, target_unit))
        elif dtype is not None and dtype.unit is not None:
            return cls(Quantity(scalars, dtype.unit))
        raise ValueError("No se pudo inferir la unidad para crear el QuantityArray.")

    def isna(self):
        return np.isnan(self._quantity.value)

    def take(self, indices, allow_fill=False, fill_value=None):
        from pandas.core.algorithms import take

        vals = self._quantity.value
        if allow_fill:
            if fill_value is None or pd.isna(fill_value):
                fill_val = np.nan
            elif isinstance(fill_value, Quantity):
                fill_val = fill_value.convert_to(self._quantity.unit).magnitude
            else:
                fill_val = fill_value
            result_vals = take(vals, indices, fill_value=fill_val, allow_fill=True)
        else:
            result_vals = vals[indices]

        return QuantityArray(Quantity(result_vals, self._quantity.unit))

    def copy(self):
        return QuantityArray(Quantity(self._quantity.value.copy(), self._quantity.unit))

    @classmethod
    def _concat_same_type(cls, to_concat):
        if not to_concat:
            raise ValueError("No hay elementos para concatenar.")
        target_unit = to_concat[0]._quantity.unit
        concatenated_vals = np.concatenate([c._quantity.convert_to(target_unit).magnitude for c in to_concat])
        return cls(Quantity(concatenated_vals, target_unit))

    def __array__(self, dtype=None, copy=None):
        return np.array(self._quantity.value, dtype=dtype, copy=copy)

    # Operaciones Aritméticas Básicas
    def __add__(self, other):
        if isinstance(other, QuantityArray):
            return QuantityArray(self._quantity + other._quantity)
        elif isinstance(other, Quantity):
            return QuantityArray(self._quantity + other)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, QuantityArray):
            return QuantityArray(self._quantity - other._quantity)
        elif isinstance(other, Quantity):
            return QuantityArray(self._quantity - other)
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, QuantityArray):
            return QuantityArray(self._quantity * other._quantity)
        elif isinstance(other, (Quantity, int, float, np.ndarray)):
            return QuantityArray(self._quantity * other)
        return NotImplemented

    def __truediv__(self, other):
        if isinstance(other, QuantityArray):
            return QuantityArray(self._quantity / other._quantity)
        elif isinstance(other, (Quantity, int, float, np.ndarray)):
            return QuantityArray(self._quantity / other)
        return NotImplemented

    def __repr__(self):
        return f"<QuantityArray>\n{self._quantity.value}\nUnidad: {self._quantity.unit.symbol}"


# ==============================================================================
# 3. REGISTRO DE MATPLOTLIB Y EJEMPLO DE USO
# ==============================================================================

def register_matplotlib_support():
    """Registra la clase Quantity y objetos afines en el registro de unidades de Matplotlib."""
    munits.registry[Quantity] = QuantityConverter()
    munits.registry[QuantityArray] = QuantityConverter()

# Se ejecuta ahora que todas las clases (incluida QuantityArray) están definidas
register_matplotlib_support()
