import re
import pandas as pd
import numpy as np
from .data import Data
from . import basic_units

class Loader:
    """Utility class to dynamically extract units from column names and cell data, 
    returning a fully-functional Data object."""

    def __init__(self):
        # Build a dynamic registry of available units from basic_units module, 
        # sorted by symbol length descending to match longer units first (e.g., 'mbar' before 'm')
        self.unit_registry = {}
        for attr_name in dir(basic_units):
            attr = getattr(basic_units, attr_name)
            if hasattr(attr, 'symbol'):
                self.unit_registry[attr.symbol] = attr
        
        # Sort symbols by length (descending) to avoid partial replacements (e.g. 'm' inside 'mm')
        self.sorted_symbols = sorted(self.unit_registry.keys(), key=len, reverse=True)

    def _find_unit_in_string(self, text: str):
        """Searches for a known unit symbol inside a string (e.g. 'Tiempo (s)' or '20 kPa')."""
        if not isinstance(text, str):
            return None, text

        cleaned_text = text.strip()
        
        # 1. Look inside parentheses or brackets first (e.g., "Velocity (m/s)" -> "m/s")
        match_brackets = re.search(r'[\(\[\{](.*?)[\)\]\}]', cleaned_text)
        if match_brackets:
            inner_content = match_brackets.group(1).strip()
            if inner_content in self.unit_registry:
                # Remove the bracketed unit part from the original name
                base_name = re.sub(r'[\(\[\{].*?[\)\]\}]', '', cleaned_text).strip()
                return self.unit_registry[inner_content], base_name

        # 2. Look for space-separated unit at the end or standalone (e.g., "20 kPa")
        for sym in self.sorted_symbols:
            # Match symbol as a distinct token or ending pattern
            pattern = rf'(.*?)\s+({re.escape(sym)})$'
            match = re.match(pattern, cleaned_text, re.IGNORECASE)
            if match:
                base_val_str = match.group(1).strip()
                unit_obj = self.unit_registry[sym]
                return unit_obj, base_val_str

        return None, cleaned_text

    def parse_column(self, col_name: str, series: pd.Series):
        """Analyzes a pandas Series and its column name to extract units and convert to Quantity or appropriate array."""
        clean_col_name = col_name
        detected_unit, base_name = self._find_unit_in_string(col_name)
        if detected_unit is not None:
            clean_col_name = base_name

        # Check if data values themselves contain units as strings (e.g., ["10 m", "20 m"])
        numeric_vals = []
        data_unit = detected_unit
        has_string_units = False

        if series.dtype == object or pd.api.types.is_string_dtype(series):
            parsed_nums = []
            unit_found_in_data = None
            success = True

            for val in series:
                if pd.isna(val):
                    parsed_nums.append(np.nan)
                    continue
                
                if isinstance(val, (int, float, np.number)):
                    parsed_nums.append(float(val))
                    continue

                if isinstance(val, str):
                    u_obj, clean_val_str = self._find_unit_in_string(val)
                    if u_obj is not None:
                        if unit_found_in_data is None:
                            unit_found_in_data = u_obj
                        elif unit_found_in_data.symbol != u_obj.symbol:
                            success = False # Mixed units inside column
                            break
                    
                    try:
                        parsed_nums.append(float(clean_val_str))
                    except ValueError:
                        success = False
                        break
                else:
                    success = False
                    break

            if success and len(parsed_nums) > 0:
                numeric_vals = np.asarray(parsed_nums)
                if unit_found_in_data is not None:
                    data_unit = unit_found_in_data
                has_string_units = True

        # If values are natively numeric
        if not has_string_units:
            try:
                numeric_vals = pd.to_numeric(series).to_numpy()
            except (ValueError, TypeError):
                # If conversion fails completely, treat as plain object/string array (e.g., text columns)
                return clean_col_name, series.to_numpy()

        # If we successfully parsed numbers and identified a unit, return a Quantity
        if data_unit is not None and len(numeric_vals) > 0:
            return clean_col_name, numeric_vals * data_unit
        
        # Otherwise return standard numeric or text array
        return clean_col_name, numeric_vals


def load_data(filepath: str, sheet_name=0, **kwargs) -> Data:
    """
    Loads a CSV or Excel file and returns a Data object with automatic unit detection.
    
    Parameters:
    -----------
    filepath : str
        Path to the .csv, .xls, or .xlsx file.
    sheet_name : str or int, optional
        Sheet name or index if loading an Excel file.
    **kwargs : dict
        Additional arguments passed to pd.read_csv or pd.read_excel.
    """
    loader = Loader()

    # Determine file format based on extension
    if filepath.endswith('.csv'):
        df = pd.read_csv(filepath, **kwargs)
    elif filepath.endswith(('.xls', '.xlsx', '.xlsm')):
        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
    else:
        # Fallback trying CSV first
        try:
            df = pd.read_csv(filepath, **kwargs)
        except Exception:
            df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)

    data_dict = {}
    for col in df.columns:
        clean_name, parsed_data = loader.parse_column(str(col), df[col])
        data_dict[clean_name] = parsed_data

    return Data(data_dict)