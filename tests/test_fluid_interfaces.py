#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import json

import pytest

from pyfluids import *


class TestFluidInterface:
    def setup(self):
        self.fluid = Fluid(PureFluids.Water)
        self.fluid.update(
            Input.Pressure.with_value(101325), Input.Temperature.with_value(293.15)
        )

    def test_post_init(self):
        FluidInterface.__post_init__(self.fluid)

    def test_update(self):
        FluidInterface.update(self.fluid)

    def test_to_json(self):
        actual = json.loads(self.fluid.to_json())
        expected = self.fluid.to_dict()
        for key in ("name", "phase"):
            expected[key] = str(expected[key])
        assert actual == expected

    def test_check_input_types(self):
        with pytest.raises(TypeError):
            self.fluid.update(
                HAInput.Pressure.with_value(101325),
                HAInput.Temperature.with_value(293.15),
            )

    def test_attr_value(self):
        FluidInterface._attr_value(self.fluid, "name")

    def test_update_prop_names(self):
        FluidInterface._update_prop_names(self.fluid, {"attr_name": "coolprop_key"})
