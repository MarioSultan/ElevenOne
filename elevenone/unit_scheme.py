"""
unit_scheme.py
==============

Global unit schemes for ElevenOne.

A *unit scheme* tells the module which unit to use to **present** every physical
quantity: tables, printed results, statistics, plots and reports.

    >>> from elevenone.unit_scheme import set_scheme
    >>> set_scheme("SI")            # everything is shown in m, kg, s, N, Pa, J, ...
    >>> set_scheme("CGS")           # everything is shown in cm, g, s, dyn, erg, ...
    >>> set_scheme(None)            # back to the default: no scheme at all

Design rules
------------
* **Opt-in.** With no scheme selected (the default) nothing changes: every
  quantity keeps showing the unit it carries, exactly as before.
* **Presentation only.** A scheme never alters arithmetic. ``Quantity.value``,
  ``Quantity.unit`` and all operations keep working with the units the user
  chose; the scheme only decides how results are *displayed* (``str``/``repr``
  of a ``Quantity``, ``Data`` tables, statistics, plot labels, reports).
* **Dimension based.** A scheme maps each physical dimension to one unit:
    1. an explicit *named* unit if the scheme defines one (N, Pa, J, dyn, erg, ...);
    2. otherwise a *coherent* unit composed from the scheme's 8 base units
       (e.g. ``cm·s⁻¹`` in CGS, ``AU·yr⁻¹`` in astronomy);
    3. dimensionless quantities are never touched.
* **Customisable.** Schemes can be copied, modified and registered.

Built-in schemes
----------------
    SI           m, kg, s, A, K, mol, cd, rad + N, Pa, J, W, C, V, F, Ω, S, Wb, T, H, Hz
    CGS          Gaussian CGS: cm, g, s + dyn, erg, Ba, P, St, Gal, statC, statV, G, Mx, Oe, ...
    astronomy    AU, M☉, yr, arcsec + km/s, erg, L☉, dyn, Ba, Gal, g/cm³, G, Hz
    galactic     kpc, M☉, Myr, deg + km/s, erg, L☉, dyn, Ba, μG, Hz
    engineering  mm, t, s + N, MPa, mJ, mW (the usual mm-t-s FEM system)
    imperial     ft, lb, s, °F + lbf, psi, ft·lbf, HP
    atomic       Hartree atomic units (a0, m_e, ħ/Eh, e, Eh, ...)

Custom scheme example
---------------------
    >>> from elevenone.unit_scheme import UnitScheme, register_scheme, set_scheme
    >>> from elevenone import si_units as si
    >>> lab = UnitScheme("lab", length=si.millimeter, time=si.millisecond,
    ...                  units=[si.kPa, si.millijoule])
    >>> register_scheme(lab)
    >>> set_scheme("lab")

Or start from a built-in one:

    >>> from elevenone.unit_scheme import get_scheme
    >>> mine = get_scheme("SI").copy("SI-km")
    >>> mine.set_unit(si.kilometer)
    >>> set_scheme(mine)
"""

import math
from contextlib import contextmanager

from . import unit as _unit_module
from . import si_units as _si
from . import cgs_units as _cgs
from . import basic_units as _basic
from .dimension import *
from .unit import Unit, Quantity

__all__ = [
    "UnitScheme",
    "register_scheme",
    "list_schemes",
    "get_scheme",
    "set_scheme",
    "set_unit_scheme",
    "reset_scheme",
    "use_scheme",
    "convert_to_scheme",
]


# ==============================================================================
# HELPERS
# ==============================================================================

# Order of the 8 fundamental dimensions (must match dimension.py)
_BASIS = (
    ("length", LENGTH),
    ("mass", MASS),
    ("time", TIME),
    ("current", CURRENT),
    ("temperature", TEMPERATURE),
    ("amount", AMOUNT),
    ("luminous", LUMINOUS),
    ("angle", ANGULAR),
)
_N_BASIS = len(_BASIS)

_SUPERSCRIPTS = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def _key(dimension):
    """Hashable key of a Dimension (Dimension itself defines __eq__ but not __hash__)."""
    exps = [float(e) + 0.0 for e in dimension.dimension]   # + 0.0 turns -0.0 into 0.0
    exps += [0.0] * (_N_BASIS - len(exps))
    return tuple(exps)


_TEMPERATURE_KEY = _key(TEMPERATURE)


def _format_symbol(base_symbols, exponents):
    """Builds a symbol such as 'cm·s⁻¹' from the scheme's base symbols and the exponents."""
    positive, negative = [], []
    for symbol, e in zip(base_symbols, exponents):
        if e == 0:
            continue
        if float(e).is_integer():
            n = int(e)
            part = symbol if n == 1 else f"{symbol}{str(n).translate(_SUPERSCRIPTS)}"
        else:
            part = f"{symbol}^{e:g}"
        (positive if e > 0 else negative).append(part)
    parts = positive + negative
    return "·".join(parts) if parts else "1"


# ==============================================================================
# UNIT SCHEME
# ==============================================================================

class UnitScheme:
    """Maps every physical dimension to the unit used to present it.

    Parameters
    ----------
    name : str
        Name of the scheme (case-insensitive when registered).
    length, mass, time, current, temperature, amount, luminous, angle : Unit, optional
        Base unit of each fundamental dimension. Anything omitted defaults to SI.
        They are used to compose a coherent unit for every dimension that has no
        named unit (velocity, density, electric field, ...).
    units : iterable of Unit, optional
        Named units to prefer for their dimension (e.g. ``N`` for FORCE). When two
        units share a dimension, the last one wins.
    description : str, optional
        One-line description (shown by ``repr``/``describe``).
    convert_temperature : bool
        If False, plain temperatures are left in the unit they carry. Useful because
        ``Quantity`` has no notion of temperature *difference*: ``T2 - T1`` with
        both in °C is stored as e.g. ``10 °C`` and would be shown as ``283.15 K``.
    """

    _SI_BASE = (_si.m, _si.kg, _si.s, _si.A, _si.K, _si.mol, _si.cd, _si.rad)

    def __init__(self, name, *, length=None, mass=None, time=None, current=None,
                 temperature=None, amount=None, luminous=None, angle=None,
                 units=(), description="", convert_temperature=True):
        self.name = str(name)
        self.description = description
        self.convert_temperature = convert_temperature

        given = dict(length=length, mass=mass, time=time, current=current,
                     temperature=temperature, amount=amount, luminous=luminous, angle=angle)
        bases = []
        for (label, dim), default in zip(_BASIS, self._SI_BASE):
            unit = given[label] if given[label] is not None else default
            if not isinstance(unit, Unit):
                raise TypeError(f"Base '{label}' must be a Unit, got {type(unit).__name__}.")
            if unit.dimension != dim:
                raise ValueError(f"Base '{label}' must have dimension {dim}, "
                                 f"but '{unit.symbol}' has {unit.dimension}.")
            bases.append(unit)
        self._bases = tuple(bases)

        self._named = {}
        self._cache = {}
        for unit in self._bases:
            self._named[_key(unit.dimension)] = unit
        for unit in units:
            self.set_unit(unit)

    # ------------------------------------------------------------------ info
    @property
    def base_units(self):
        """The 8 base units (length, mass, time, current, temperature, amount, luminous, angle)."""
        return self._bases

    @property
    def named_units(self):
        """Named units explicitly defined by the scheme (includes the base units)."""
        return list(self._named.values())

    def describe(self):
        """Human readable summary of the scheme."""
        lines = [f"UnitScheme '{self.name}'" + (f" - {self.description}" if self.description else "")]
        lines.append("  base : " + ", ".join(f"{lbl}={u.symbol}" for (lbl, _), u in zip(_BASIS, self._bases)))
        base_keys = {_key(u.dimension) for u in self._bases}
        extra = [u.symbol for k, u in self._named.items() if k not in base_keys]
        if extra:
            lines.append("  named: " + ", ".join(extra))
        return "\n".join(lines)

    def __repr__(self):
        return f"UnitScheme({self.name!r}: " + ", ".join(u.symbol for u in self._bases) + ")"

    # -------------------------------------------------------------- editing
    def set_unit(self, unit):
        """Uses ``unit`` to present every quantity of its dimension. Returns self."""
        if not isinstance(unit, Unit):
            raise TypeError(f"set_unit expects a Unit, got {type(unit).__name__}.")
        self._named[_key(unit.dimension)] = unit
        self._cache.clear()
        return self

    def remove_unit(self, unit_or_dimension):
        """Removes the named unit of a dimension (it falls back to the composed unit). Returns self."""
        dim = unit_or_dimension.dimension if isinstance(unit_or_dimension, Unit) else unit_or_dimension
        self._named.pop(_key(dim), None)
        self._cache.clear()
        return self

    def copy(self, name=None):
        """Independent copy of the scheme (handy to customise a built-in one)."""
        labels = [label for label, _ in _BASIS]
        new = UnitScheme(name or self.name, description=self.description,
                         convert_temperature=self.convert_temperature,
                         **dict(zip(labels, self._bases)))
        new._named = dict(self._named)
        return new

    # ----------------------------------------------------------- resolution
    def unit_for(self, dimension):
        """Unit the scheme uses for ``dimension``, or None if it must be left untouched."""
        key = _key(dimension)
        try:
            return self._cache[key]
        except KeyError:
            unit = self._resolve(dimension, key)
            self._cache[key] = unit
            return unit

    def _resolve(self, dimension, key):
        if key == _TEMPERATURE_KEY and not self.convert_temperature:
            return None
        unit = self._named.get(key)
        if unit is not None:
            return unit
        if not any(key):                       # dimensionless: leave as is
            return None
        return self._compose(dimension, key)

    def _compose(self, dimension, key):
        """Coherent unit built from the base units (offsets are irrelevant for derived units)."""
        factor = 1.0
        for base, e in zip(self._bases, key):
            if e:
                factor *= base.factor ** e
        symbol = _format_symbol([b.symbol for b in self._bases], key)
        return Unit(Dimension(list(dimension.dimension)), symbol, factor)

    # ----------------------------------------------------------- conversion
    def convert(self, obj):
        """Expresses a Quantity (or Unit) in this scheme. Anything else is returned untouched."""
        if isinstance(obj, Quantity):
            target = self.unit_for(obj.unit.dimension)
            if target is None:
                return obj
            current = obj.unit
            if current is target or (current.factor == target.factor and current.offset == target.offset):
                return obj                      # already expressed in the scheme's unit
            return obj.convert_to(target)
        if isinstance(obj, Unit):
            target = self.unit_for(obj.dimension)
            return obj if target is None else target
        return obj


# ==============================================================================
# CONSTANTS AND EXTRA UNITS USED BY THE BUILT-IN SCHEMES
# ==============================================================================

# Astronomy (IAU)
_AU_M = 1.495978707e11                 # astronomical unit, exact (IAU 2012)
_PC_M = 648000.0 / math.pi * _AU_M     # parsec
_MSUN_KG = 1.98841e30                  # solar mass
_LSUN_W = 3.828e26                     # nominal solar luminosity (IAU 2015)
_YR_S = _basic.year.factor             # Julian year, same as basic_units

_au = Unit(LENGTH, "AU", _AU_M)
_kpc = Unit(LENGTH, "kpc", 1e3 * _PC_M)
_Msun = Unit(MASS, "M☉", _MSUN_KG)
_Myr = Unit(TIME, "Myr", 1e6 * _YR_S)
_arcsec = Unit(ANGULAR, "″", math.pi / 648000.0)
_degree = Unit(ANGULAR, "°", math.pi / 180.0)
_Lsun = Unit(POWER, "L☉", _LSUN_W)
_km_per_s = Unit(VELOCITY, "km/s", 1e3)

# Mechanics / CGS / imperial
_erg_per_s = Unit(POWER, "erg/s", 1e-7)
_statV_per_cm = Unit(ELECTRIC_FIELD, "statV/cm", _cgs.statvolt.factor / _cgs.centimeter.factor)
_ft_lbf = Unit(ENERGY, "ft·lbf", 1.3558179483314004)

# Hartree atomic units (CODATA 2018)
_A0 = 5.29177210903e-11                # Bohr radius [m]
_ME = 9.1093837015e-31                 # electron mass [kg]
_E = 1.602176634e-19                   # elementary charge [C]
_EH = 4.3597447222071e-18              # Hartree energy [J]
_HBAR = 1.054571817e-34                # reduced Planck constant [J s]
_KB = 1.380649e-23                     # Boltzmann constant [J/K]
_T_AU = _HBAR / _EH                    # atomic unit of time [s]

_au_length = Unit(LENGTH, "a0", _A0)
_au_mass = Unit(MASS, "m_e", _ME)
_au_time = Unit(TIME, "t_au", _T_AU)
_au_current = Unit(CURRENT, "I_au", _E / _T_AU)
_au_temperature = Unit(TEMPERATURE, "T_au", _EH / _KB, offset=0.0)

# Electrical units with special names (shared by the schemes whose base is not SI)
_SI_NAMED_ELECTRICAL = [_si.C, _si.V, _si.F, _si.Ohm, _si.S, _si.Wb, _si.T, _si.H]


# ==============================================================================
# BUILT-IN SCHEMES
# ==============================================================================

def _builtin_schemes():
    si = UnitScheme(
        "SI",
        description="International System of Units",
        units=[_si.N, _si.Pa, _si.J, _si.W, _si.Hz] + _SI_NAMED_ELECTRICAL,
    )

    cgs = UnitScheme(
        "CGS",
        description="Gaussian CGS (cm, g, s; electromagnetic quantities in statC/statV/G/Oe/Mx)",
        length=_cgs.centimeter, mass=_cgs.gram, time=_cgs.second, current=_cgs.statampere,
        units=[
            _cgs.dyne, _cgs.erg, _erg_per_s, _cgs.barye, _cgs.poise, _cgs.stokes,
            _cgs.galileo_acceleration,
            _cgs.statcoulomb, _cgs.statvolt, _cgs.statohm, _cgs.statfarad, _cgs.stathanry,
            _statV_per_cm,
            _cgs.gauss, _cgs.maxwell, _cgs.oersted, _cgs.erg_per_gauss,
            _si.Hz,
        ],
    )

    astronomy = UnitScheme(
        "astronomy",
        description="AU, solar mass, year, arcsec; km/s, erg, L☉, cgs pressure/force/field",
        length=_au, mass=_Msun, time=_basic.year, angle=_arcsec,
        units=[
            _km_per_s, _cgs.erg, _Lsun, _cgs.dyne, _cgs.barye, _cgs.galileo_acceleration,
            _si.gram_per_cubic_centimeter, _cgs.gauss, _si.Hz,
        ],
    )

    galactic = UnitScheme(
        "galactic",
        description="kpc, solar mass, Myr, degrees; km/s, erg, L☉, μG",
        length=_kpc, mass=_Msun, time=_Myr, angle=_degree,
        units=[
            _km_per_s, _cgs.erg, _Lsun, _cgs.dyne, _cgs.barye, _cgs.microgauss, _si.Hz,
        ],
    )

    engineering = UnitScheme(
        "engineering",
        description="mm, tonne, s (coherent with N and MPa; the usual FEM system)",
        length=_si.millimeter, mass=_si.tonne, time=_si.s,
        units=[_si.N, _si.MPa, _si.millijoule, _si.milliwatt, _si.Hz] + _SI_NAMED_ELECTRICAL,
    )

    imperial = UnitScheme(
        "imperial",
        description="US customary / foot-pound-second with Fahrenheit",
        length=_basic.ft, mass=_basic.lb, time=_basic.s, temperature=_basic.degF,
        units=[_basic.lbf, _basic.psi, _ft_lbf, _basic.HP, _si.Hz] + _SI_NAMED_ELECTRICAL,
    )

    atomic = UnitScheme(
        "atomic",
        description="Hartree atomic units (a0, m_e, ħ/Eh, e)",
        length=_au_length, mass=_au_mass, time=_au_time, current=_au_current,
        temperature=_au_temperature,
        units=[
            Unit(ENERGY, "Eh", _EH),
            Unit(CHARGE, "e", _E),
            Unit(FORCE, "Eh/a0", _EH / _A0),
            Unit(PRESSURE, "Eh/a0³", _EH / _A0 ** 3),
            Unit(VOLTAGE, "Eh/e", _EH / _E),
            Unit(ELECTRIC_FIELD, "Eh/(e·a0)", _EH / (_E * _A0)),
            Unit(MAGNETIC_FIELD, "ħ/(e·a0²)", _HBAR / (_E * _A0 ** 2)),
        ],
    )

    return [
        (si, ()),
        (cgs, ("gaussian",)),
        (astronomy, ("astro",)),
        (galactic, ()),
        (engineering, ("eng",)),
        (imperial, ("us", "fps", "us-customary")),
        (atomic, ("hartree",)),
    ]


# ==============================================================================
# REGISTRY AND GLOBAL STATE
# ==============================================================================

_REGISTRY = {}        # lower-case name or alias -> UnitScheme
_CANONICAL = []       # registered scheme names, in registration order
_active = None        # currently active scheme (None = no scheme)

_NO_SCHEME_NAMES = {"none", "default", "off", "no", ""}


def _norm(name):
    return str(name).strip().lower()


def register_scheme(scheme, *aliases, overwrite=False):
    """Registers a scheme so it can be selected by name with ``set_scheme``."""
    if not isinstance(scheme, UnitScheme):
        raise TypeError(f"register_scheme expects a UnitScheme, got {type(scheme).__name__}.")
    names = [_norm(n) for n in (scheme.name, *aliases)]
    for n in names:
        if n in _NO_SCHEME_NAMES:
            raise ValueError(f"'{n}' is reserved and cannot be used as a scheme name.")
        if n in _REGISTRY and not overwrite:
            raise ValueError(f"A scheme named '{n}' already exists (use overwrite=True to replace it).")
    for n in names:
        _REGISTRY[n] = scheme
    if scheme.name not in _CANONICAL:
        _CANONICAL.append(scheme.name)
    return scheme


def list_schemes():
    """Names of the registered schemes."""
    return list(_CANONICAL)


def _resolve_scheme(scheme):
    if scheme is None:
        return None
    if isinstance(scheme, UnitScheme):
        return scheme
    if isinstance(scheme, str):
        key = _norm(scheme)
        if key in _NO_SCHEME_NAMES:
            return None
        if key not in _REGISTRY:
            raise ValueError(f"Unknown unit scheme '{scheme}'. Available schemes: {list_schemes()}")
        return _REGISTRY[key]
    raise TypeError("A scheme must be a name, a UnitScheme or None.")


def get_scheme(name=None):
    """Returns the active scheme (None if there is none), or the registered scheme called ``name``."""
    if name is None:
        return _active
    return _resolve_scheme(name)


def set_scheme(scheme=None):
    """Selects the global unit scheme.

    Parameters
    ----------
    scheme : str, UnitScheme or None
        A registered name ('SI', 'CGS', 'astronomy', ...), a UnitScheme instance, or
        None / 'none' to disable schemes (default behaviour of the module).

    Returns
    -------
    The active UnitScheme, or None.

    Examples
    --------
    >>> set_scheme("SI")
    >>> set_scheme("cgs")
    >>> set_scheme(None)
    """
    global _active
    _active = _resolve_scheme(scheme)
    _unit_module._scheme_hook = None if _active is None else _active.convert
    return _active


set_unit_scheme = set_scheme


def reset_scheme():
    """Disables the global scheme (same as ``set_scheme(None)``)."""
    return set_scheme(None)


@contextmanager
def use_scheme(scheme):
    """Temporarily selects a scheme::

        with use_scheme("CGS"):
            print(result)
    """
    previous = _active
    set_scheme(scheme)
    try:
        yield _active
    finally:
        set_scheme(previous)


def convert_to_scheme(obj, scheme=None):
    """Expresses a Quantity in ``scheme`` (default: the active scheme).

    Without any scheme the object is returned untouched; objects that are not
    quantities are always returned untouched.
    """
    target = _active if scheme is None else _resolve_scheme(scheme)
    if target is None:
        return obj
    return target.convert(obj)


# Built-ins are registered at import time but NOT activated: the default is "no scheme".
for _scheme, _aliases in _builtin_schemes():
    register_scheme(_scheme, *_aliases)
del _scheme, _aliases