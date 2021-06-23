#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import CoolProp
import pytest

from pyfluids import *


class TestPhase:
    @pytest.mark.parametrize(
        "name, coolprop_key",
        [
            (Phase.Liquid, CoolProp.iphase_liquid),
            (Phase.Gas, CoolProp.iphase_gas),
            (Phase.TwoPhase, CoolProp.iphase_twophase),
            (Phase.SupercriticalLiquid, CoolProp.iphase_supercritical_liquid),
            (Phase.SupercriticalGas, CoolProp.iphase_supercritical_gas),
            (Phase.Supercritical, CoolProp.iphase_supercritical),
        ],
    )
    def test_value(self, name, coolprop_key):
        assert name.value == coolprop_key

    @pytest.mark.parametrize("name", list(Phase))
    def test_repr(self, name):
        assert repr(name) == name.name

    @pytest.mark.parametrize("name", list(Phase))
    def test_str(self, name):
        assert str(name) == name.name
