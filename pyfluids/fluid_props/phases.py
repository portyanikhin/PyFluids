#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from enum import Enum

import CoolProp

__all__ = ["Phase"]


class Phase(Enum):
    """Phases of fluids"""

    Liquid = CoolProp.iphase_liquid
    Gas = CoolProp.iphase_gas
    TwoPhase = CoolProp.iphase_twophase
    SupercriticalLiquid = CoolProp.iphase_supercritical_liquid
    SupercriticalGas = CoolProp.iphase_supercritical_gas
    Supercritical = CoolProp.iphase_supercritical

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name
