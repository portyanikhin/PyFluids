import json
from typing import Optional

import pytest
from CoolProp.CoolProp import PropsSI

from pyfluids import Fluid, FluidsList, Phases, Input


class TestFluid:
    water: Fluid = Fluid(FluidsList.Water)
    fluid: Fluid = None
    fraction: float = None
    pressure: float = None
    temperature: float = None

    def test_factory(self):
        new_water = self.water.factory()
        assert new_water.name == self.water.name
        assert new_water.fraction == self.water.fraction
        assert new_water.phase == Phases.Unknown

    def test_with_state(self):
        assert (
            self.water.with_state(Input.pressure(101325), Input.temperature(20)).phase
            == Phases.Liquid
        )

    @pytest.mark.parametrize(
        "name, fraction, message",
        [
            (FluidsList.MPG, None, "Need to define fraction!"),
            (
                FluidsList.MPG,
                -200,
                "Invalid fraction value! It should be in [0;60] %. "
                "Entered value = -200 %.",
            ),
            (
                FluidsList.MPG,
                200,
                "Invalid fraction value! It should be in [0;60] %. "
                "Entered value = 200 %.",
            ),
        ],
    )
    def test_invalid_fraction(self, name: FluidsList, fraction: float, message: str):
        with pytest.raises(ValueError) as e:
            Fluid(name, fraction)
        assert message in str(e.value)

    @pytest.mark.parametrize("name", list(FluidsList))
    @pytest.mark.parametrize("pressure", [1e7, 1e8])
    def test_update(self, name: FluidsList, pressure: float):
        if name == FluidsList.AL or name == FluidsList.AN:
            return
        if name.coolprop_name.endswith(".mix"):
            return
        self.set_up(name, pressure)
        actual = (
            self.fluid.compressibility,
            self.fluid.conductivity,
            self.fluid.critical_pressure,
            self.fluid.critical_temperature,
            self.fluid.density,
            self.fluid.dynamic_viscosity,
            self.fluid.enthalpy,
            self.fluid.entropy,
            self.fluid.freezing_temperature,
            self.fluid.internal_energy,
            self.fluid.max_pressure,
            self.fluid.max_temperature,
            self.fluid.min_pressure,
            self.fluid.min_temperature,
            self.fluid.molar_mass,
            self.fluid.prandtl,
            self.fluid.pressure,
            self.fluid.quality,
            self.fluid.sound_speed,
            self.fluid.specific_heat,
            self.fluid.surface_tension,
            self.fluid.temperature,
            self.fluid.triple_pressure,
            self.fluid.triple_temperature,
        )
        keys = (
            "Z",
            "L",
            "p_critical",
            "T_critical",
            "D",
            "V",
            "H",
            "S",
            "T_freeze",
            "U",
            "P_max",
            "T_max",
            "P_min",
            "T_min",
            "M",
            "Prandtl",
            "P",
            "Q",
            "A",
            "C",
            "I",
            "T",
            "p_triple",
            "T_triple",
        )
        assert all(
            [
                True
                if (actual[i] is None and self.high_level_interface(keys[i]) is None)
                or (keys[i] == "P" or keys[i] == "T")
                else abs(actual[i] - self.high_level_interface(keys[i])) < 1e-9
                for i in range(len(actual))
            ]
        )
        assert (
            self.fluid.kinematic_viscosity
            == self.fluid.dynamic_viscosity / self.fluid.density
            if self.fluid.dynamic_viscosity is not None
            else True
        )

    def test_update_invalid_input(self):
        with pytest.raises(ValueError) as e:
            self.water.with_state(Input.pressure(1e5), Input.pressure(101325))
        assert "Need to define 2 unique inputs!" in str(e.value)

    def test_cached_inputs(self):
        water = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        assert water.pressure == 101325
        assert water.temperature == 20

    def test_equals(self):
        origin = self.water.with_state(Input.pressure(101325), Input.temperature(5))
        same = self.water.with_state(Input.pressure(101325), Input.temperature(5))
        other = self.water.with_state(Input.pressure(101325), Input.temperature(10))
        assert origin == same
        assert origin != other
        assert origin != object()

    def test_hash(self):
        origin = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        same = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        other = self.water.with_state(Input.pressure(101325), Input.temperature(30))
        assert hash(origin) == hash(same)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    def test_clone(self):
        origin = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        clone = origin.clone()
        assert origin == clone
        clone.update(Input.pressure(101325), Input.temperature(30))
        assert origin != clone

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json(self, indented: bool):
        water = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        assert water.as_json(indented) == json.dumps(
            water.as_dict(),
            indent=4 if indented else None,
            default=str,
            sort_keys=False,
        )

    def test_as_dict(self):
        water = self.water.with_state(Input.pressure(101325), Input.temperature(20))
        assert all(
            key
            in [
                k.split("__")[-1]
                for k in vars(water).keys()
                if not k.split("__")[-1].startswith("_")
            ]
            for key in list(water.as_dict().keys())
        )

    def set_up(self, name: FluidsList, pressure: float):
        self.fraction = (
            None if name.pure else 0.1 * name.fraction_min + 0.9 * name.fraction_max
        )
        self.fluid = Fluid(name, self.fraction)
        self.pressure = pressure
        self.temperature = (
            0.1 * self.fluid.min_temperature + 0.9 * self.fluid.max_temperature
        )
        self.fluid.update(
            Input.pressure(self.pressure), Input.temperature(self.temperature)
        )

    def high_level_interface(self, output_key: str) -> Optional[float]:
        try:
            value = PropsSI(
                output_key,
                "P",
                self.pressure,
                "T",
                self.temperature + 273.15,
                f"{self.fluid.name.coolprop_backend}::{self.fluid.name.coolprop_name}-"
                f"{self.fluid.fraction}%"
                if self.fluid.name.coolprop_backend == "INCOMP"
                else self.fluid.name.coolprop_name,
            )
            if value is not None and output_key.startswith("T"):
                value -= 273.15
            elif output_key == "Q" and (not 0 <= value <= 1):
                value = None
            return value
        except ValueError:
            return None
