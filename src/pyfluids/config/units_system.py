from enum import Enum

__all__ = ["UnitsSystem"]


class UnitsSystem(Enum):
    """List of available units systems."""

    SI = "SI"
    SIWithCelsius = "SIWithCelsius"
    SIWithCelsiusAndPercents = "SIWithCelsiusAndPercents"

    def __repr__(self) -> str:
        return self.name

    def __str__(self) -> str:
        return self.name
