#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import CoolProp
import pytest

from pyfluids import *


class TestInputs:
    @pytest.mark.parametrize("name", list(Input))
    def test_with_value(self, name):
        assert name.with_value(0).value == 0

    @pytest.mark.parametrize(
        "name, coolprop_key",
        [
            (Input.Density, CoolProp.iDmass),
            (Input.Enthalpy, CoolProp.iHmass),
            (Input.Entropy, CoolProp.iSmass),
            (Input.InternalEnergy, CoolProp.iUmass),
            (Input.Pressure, CoolProp.iP),
            (Input.Quality, CoolProp.iQ),
            (Input.Temperature, CoolProp.iT),
        ],
    )
    def test_coolprop_key(self, name, coolprop_key):
        assert name.coolprop_key == coolprop_key

    @pytest.mark.parametrize("name", list(Input))
    def test_value(self, name):
        assert name.value is None
