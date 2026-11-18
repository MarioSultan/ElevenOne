from .dimension import *
from .unit import *
from .basic_units import *
from .load import *
from .data import *
from .report import *
import sys

__version__ = "0.7.0"

def _show_welcome():
    if hasattr(sys, "ps1"):
        print(f"""ElevenOne v{__version__} — Your perfect lab assistant
Documentation: https://elevenone.readthedocs.io/""")

_show_welcome()