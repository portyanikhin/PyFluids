from dataclasses import dataclass

from ..enums import UnitsSystem

__all__ = ["PyFluidsConfig"]


@dataclass
class PyFluidsConfig:
    """PyFluids configuration."""

    units_system: UnitsSystem = UnitsSystem.SIWithCelsiusAndPercents
