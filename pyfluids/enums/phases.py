from enum import Enum


class Phases(Enum):
    """Fluids and mixtures phase states."""

    Liquid = "Liquid"
    Supercritical = "Supercritical"
    SupercriticalGas = "Supercritical gas"
    SupercriticalLiquid = "Supercritical liquid"
    CriticalPoint = "Critical point"
    Gas = "Gas"
    TwoPhase = "Two phase"
    Unknown = "Unknown"
    NotImposed = "Not imposed"

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
