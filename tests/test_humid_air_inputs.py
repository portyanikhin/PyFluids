#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import pytest

from pyfluids import *


class TestHAInputs:
    @pytest.mark.parametrize("name", list(HAInput))
    def test_with_value(self, name):
        assert name.with_value(0).value == 0

    @pytest.mark.parametrize(
        "name, coolprop_key",
        [
            (HAInput.Density, "Vha"),
            (HAInput.DewTemperature, "D"),
            (HAInput.Enthalpy, "Hha"),
            (HAInput.Entropy, "Sha"),
            (HAInput.Humidity, "W"),
            (HAInput.PartialPressure, "P_w"),
            (HAInput.Pressure, "P"),
            (HAInput.RelativeHumidity, "R"),
            (HAInput.Temperature, "T"),
            (HAInput.WBTemperature, "B"),
        ],
    )
    def test_coolprop_key(self, name, coolprop_key):
        assert name.coolprop_key == coolprop_key

    @pytest.mark.parametrize("name", list(HAInput))
    def test_value(self, name):
        assert name.value is None
