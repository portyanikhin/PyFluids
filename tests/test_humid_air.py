#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import pytest
from CoolProp.HumidAirProp import HAPropsSI

from pyfluids import *

# noinspection PyProtectedMember
from pyfluids.humid_air_props.humid_air import prop_names


class TestHumidAir:
    def setup(self):
        self.air = HumidAir()

    @pytest.mark.parametrize("pressure", [1e5, 1e6, 1e7])
    @pytest.mark.parametrize("temperature", list(range(253, 333, 10)))
    @pytest.mark.parametrize(
        "relative_humidity", [i * 1e-2 for i in list(range(0, 120, 20))]
    )
    def test_update(self, pressure, temperature, relative_humidity):
        self.air.update(
            HAInput.Pressure.with_value(pressure),
            HAInput.Temperature.with_value(temperature),
            HAInput.RelativeHumidity.with_value(relative_humidity),
        )
        actual = self.air.to_dict()
        for key, value in prop_names.items():
            try:
                expected = HAPropsSI(
                    value, "P", pressure, "T", temperature, "R", relative_humidity
                )
                expected = 1 / expected if (key == "density") else expected
            except ValueError:
                expected = None
            assert actual[key] == expected

    @pytest.mark.parametrize("pressure", [1e5, 1e6, 1e7])
    @pytest.mark.parametrize("temperature", list(range(253, 333, 10)))
    @pytest.mark.parametrize(
        "relative_humidity", [i * 1e-2 for i in list(range(0, 120, 20))]
    )
    def test_add_props(self, pressure, temperature, relative_humidity):
        new_props = {
            "entropy_per_dry_air": "S",
            "water_mole_fraction": "psi_w",
        }
        self.air.add_props(new_props)
        self.air.update(
            HAInput.Pressure.with_value(pressure),
            HAInput.Temperature.with_value(temperature),
            HAInput.RelativeHumidity.with_value(relative_humidity),
        )
        actual = self.air.to_dict()
        for key, value in new_props.items():
            expected = HAPropsSI(
                value, "P", pressure, "T", temperature, "R", relative_humidity
            )
            assert actual[key] == expected
