import CoolProp

from enum import Enum

__all__ = ["Phases"]


class Phases(Enum):
    """Fluids and mixtures phase states."""

    Liquid = CoolProp.iphase_liquid
    Supercritical = CoolProp.iphase_supercritical
    SupercriticalGas = CoolProp.iphase_supercritical_gas
    SupercriticalLiquid = CoolProp.iphase_supercritical_liquid
    CriticalPoint = CoolProp.iphase_critical_point
    Gas = CoolProp.iphase_gas
    TwoPhase = CoolProp.iphase_twophase
    Unknown = CoolProp.iphase_unknown
    NotImposed = CoolProp.iphase_not_imposed

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
