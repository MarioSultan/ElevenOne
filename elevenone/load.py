import ast
import re
import pandas as pd
import numpy as np

from .data import Data
from .unit import Quantity, Unit
from . import basic_units


class Loader:
    """Carga CSV/Excel y asocia automáticamente columnas de incertidumbre."""

    def __init__(self):
        self.unit_registry = {}
        for attr_name in dir(basic_units):
            attr = getattr(basic_units, attr_name)
            if isinstance(attr, Unit):
                self.unit_registry[attr.symbol] = attr
                # También permite usar el nombre Python de la unidad.
                self.unit_registry.setdefault(attr_name, attr)

        self.sorted_symbols = sorted(self.unit_registry, key=len, reverse=True)

    def _parse_unit_expression(self, expression):
        """Evalúa expresiones de unidades sin ejecutar código arbitrario."""
        expr = expression.strip().replace("·", "*").replace("⋅", "*")
        expr = expr.replace("²", "**2").replace("³", "**3")
        expr = expr.replace("^", "**").replace(" ", "")
        if not expr:
            return None

        # AST restringido: nombres registrados, 1, multiplicación, división y potencias.
        try:
            tree = ast.parse(expr, mode="eval")
        except SyntaxError:
            return None

        def evaluate(node):
            if isinstance(node, ast.Expression):
                return evaluate(node.body)
            if isinstance(node, ast.Name):
                return self.unit_registry.get(node.id)
            if isinstance(node, ast.Constant) and node.value == 1:
                return 1
            if isinstance(node, ast.BinOp):
                left, right = evaluate(node.left), evaluate(node.right)
                if left is None or right is None:
                    return None
                if isinstance(node.op, ast.Mult):
                    return left * right
                if isinstance(node.op, ast.Div):
                    if left == 1:
                        return 1 / right if isinstance(right, Unit) else None
                    return left / right
                if isinstance(node.op, ast.Pow) and isinstance(right, (int, float)):
                    return left ** right
            if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
                value = evaluate(node.operand)
                return -value if isinstance(value, (int, float)) else None
            if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
                return node.value
            return None

        result = evaluate(tree)
        return result if isinstance(result, Unit) else None

    def _find_unit_in_string(self, text):
        """Extrae unidades de nombres/celdas: 'Tiempo (s)', 'Velocidad [m/s]', '2 m/s'."""
        if not isinstance(text, str):
            return None, text
        cleaned = text.strip()

        # Unidad entre delimitadores. Se intenta de derecha a izquierda para
        # permitir nombres que contengan paréntesis no relacionados con unidades.
        for match in reversed(list(re.finditer(r"[\(\[\{]([^\)\]\}]+)[\)\]\}]", cleaned))):
            unit = self._parse_unit_expression(match.group(1))
            if unit is not None:
                base = (cleaned[:match.start()] + cleaned[match.end():]).strip()
                return unit, base

        # Unidad al final separada por espacio: "velocidad m/s" o "12 kg·m/s²".
        # Los exponentes Unicode más habituales se traducen a potencias.
        normalized = cleaned.replace("²", "**2").replace("³", "**3")
        for split in range(len(normalized) - 1, 0, -1):
            if not normalized[split].isspace():
                continue
            candidate = normalized[split:].strip()
            unit = self._parse_unit_expression(candidate)
            if unit is not None:
                return unit, normalized[:split].strip()
        return None, cleaned

    def _parse_error_column_name(self, col_name):
        """Devuelve (nombre_base, unidad_error) si el nombre es una incertidumbre."""
        cleaned = str(col_name).strip()
        suffix = r"(?:err|error|unc|uncertainty|uncert|sigma)"

        # Caso habitual: tiempo_err (s), tiempo_error [ms], etc.
        match = re.match(
            rf"^(.*?)[\s_-]+{suffix}\s*(?:[\(\[\{{](.*?)[\)\]\}}])?$",
            cleaned, re.IGNORECASE
        )
        if match:
            base = match.group(1).strip()
            unit = self._parse_unit_expression(match.group(2)) if match.group(2) else None
            if unit is None:
                unit, base = self._find_unit_in_string(base)
            return base, unit

        # También admite tiempo (s)_err o tiempo [s]_err.
        match = re.match(rf"^(.*?)[\s_-]+{suffix}$", cleaned, re.IGNORECASE)
        if match:
            base_with_unit = match.group(1).strip()
            unit, base = self._find_unit_in_string(base_with_unit)
            return base, unit

        # Formas tiempo (err) y tiempo [err].
        unit, base = self._find_unit_in_string(cleaned)
        for pattern in (rf"^(.*?)\s*\({suffix}\)$", rf"^(.*?)\s*\[{suffix}\]$"):
            match = re.match(pattern, base, re.IGNORECASE)
            if match:
                return match.group(1).strip(), unit
        return None, None

    def parse_column(self, col_name, series):
        clean_name = str(col_name).strip()
        detected_unit, base_name = self._find_unit_in_string(clean_name)
        if detected_unit is not None:
            clean_name = base_name

        values = []
        unit_from_cells = None
        all_numeric = True

        for value in series:
            if pd.isna(value):
                values.append(np.nan)
                continue
            if isinstance(value, (int, float, np.number)):
                values.append(float(value))
                continue
            if isinstance(value, str):
                cell_unit, numeric_text = self._find_unit_in_string(value)
                try:
                    number = float(numeric_text)
                except (TypeError, ValueError):
                    all_numeric = False
                    break
                if cell_unit is not None:
                    if unit_from_cells is None:
                        unit_from_cells = cell_unit
                    elif cell_unit.dimension != unit_from_cells.dimension:
                        raise ValueError(f"Unidades incompatibles en la columna '{col_name}'.")
                    else:
                        number *= cell_unit.factor / unit_from_cells.factor
                values.append(number)
            else:
                all_numeric = False
                break

        if not all_numeric:
            return clean_name, series.to_numpy()

        unit = detected_unit or unit_from_cells
        arr = np.asarray(values, dtype=float)
        return clean_name, arr * unit if unit is not None else arr


def load_data(filepath, sheet_name=0, **kwargs):
    """Carga CSV/Excel, reconoce incertidumbres y devuelve un objeto Data."""
    loader = Loader()
    path = str(filepath).lower()

    if path.endswith(".csv"):
        df = pd.read_csv(filepath, **kwargs)
    elif path.endswith((".xls", ".xlsx", ".xlsm", ".xlsb")):
        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    else:
        try:
            df = pd.read_csv(filepath, **kwargs)
        except Exception:
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)

    parsed = {}
    errors = {}
    original_to_clean = {}

    for original_name in df.columns:
        original_name = str(original_name)
        clean_name, parsed_data = loader.parse_column(original_name, df[original_name])
        parsed[original_name] = (clean_name, parsed_data)
        original_to_clean[original_name] = clean_name

    # Primero se identifican todas las columnas de error.
    for original_name, (clean_name, values) in parsed.items():
        base_name, error_unit = loader._parse_error_column_name(original_name)
        if base_name is None:
            continue
        # El nombre de la magnitud puede llevar unidad en su propio encabezado.
        _, clean_base = loader._find_unit_in_string(base_name)
        if clean_base != base_name:
            base_name = clean_base
        errors[base_name] = (values, error_unit, original_name)

    data_dict = {}
    for original_name, (clean_name, values) in parsed.items():
        base_name, _ = loader._parse_error_column_name(original_name)
        if base_name is not None:
            continue

        error_entry = errors.get(clean_name)
        if error_entry is None:
            data_dict[clean_name] = values
            continue

        error_values, error_unit, error_col = error_entry
        if isinstance(error_values, Quantity):
            error_quantity = error_values
        elif error_unit is not None:
            error_quantity = Quantity(error_values, error_unit)
        else:
            error_quantity = None

        if isinstance(values, Quantity):
            if error_quantity is not None:
                converted_error = error_quantity.convert_to(values.unit)
                error_array = converted_error.value
            else:
                # Si no se especificó unidad en la columna _err, se entiende
                # que está expresada en la unidad de la magnitud.
                error_array = np.asarray(error_values, dtype=float)
            data_dict[clean_name] = Quantity(values.value, values.unit, error_array)
        else:
            # Si la columna principal no declara unidad pero _err sí, se
            # interpreta que ambas están expresadas en esa unidad.
            if error_quantity is not None:
                unit = error_quantity.unit
                error_array = error_quantity.value
            else:
                unit = getattr(basic_units, "counts", None)
                if unit is None:
                    raise ValueError(
                        f"La columna '{error_col}' tiene incertidumbre, pero "
                        f"'{clean_name}' no tiene unidad y basic_units.counts no existe."
                    )
                error_array = np.asarray(error_values, dtype=float)
            data_dict[clean_name] = Quantity(values, unit, error_array)

    return Data(data_dict)
