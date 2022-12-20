import asyncio
import json
from math import isinf, isnan
from typing import Optional, List

import pytest
from CoolProp.CoolProp import PropsSI

from pyfluids import Fluid, FluidsList, Phases, Input


class TestFluid:
    fluid: Fluid = Fluid(FluidsList.Water)
    fluid_names: List[FluidsList] = [
        name
        for name in list(FluidsList)
        if not (
            name is FluidsList.AL
            or name is FluidsList.AN
            or name.coolprop_name.endswith(".mix")
        )
    ]

    @pytest.mark.parametrize(
        "fraction, message",
        [
            (None, "Need to define fraction!"),
            (
                -200,
                "Invalid fraction value! It should be in [0;60] %. "
                "Entered value = -200 %.",
            ),
            (
                200,
                "Invalid fraction value! It should be in [0;60] %. "
                "Entered value = 200 %.",
            ),
        ],
    )
    def test_fluid_invalid_fraction_raises_value_error(
        self, fraction: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            Fluid(FluidsList.MPG, fraction)
        assert message in str(e.value)

    @pytest.mark.asyncio
    async def test_fluid_multi_threading_is_thread_safe(self):
        async def boiling_temperature_of_water_at_standard_pressure() -> float:
            return self.fluid.dew_point_at_pressure(101325).temperature

        tasks = [
            asyncio.create_task(boiling_temperature_of_water_at_standard_pressure())
            for _ in range(100)
        ]
        await asyncio.gather(*tasks)
        results = set(task.result() for task in tasks)
        assert len(results) == 1

    def test_factory_always_name_is_constant(self):
        assert self.fluid.factory().name == self.fluid.name

    def test_factory_always_fraction_is_constant(self):
        assert self.fluid.factory().fraction == self.fluid.fraction

    def test_factory_always_phase_is_unknown(self):
        assert self.fluid.factory().phase == Phases.Unknown

    def test_clone_always_returns_new_instance_with_same_state(self):
        origin = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        clone = origin.clone()
        assert origin == clone
        clone.update(Input.pressure(101325), Input.temperature(30))
        assert origin != clone

    def test_with_state_water_in_standard_conditions_phase_is_liquid(self):
        assert (
            self.fluid.with_state(Input.pressure(101325), Input.temperature(20)).phase
            == Phases.Liquid
        )

    def test_update_same_inputs_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.fluid.with_state(Input.pressure(101325), Input.pressure(1e5))
        assert "Need to define 2 unique inputs!" in str(e.value)

    def test_update_always_inputs_are_cached(self):
        self.fluid.update(Input.pressure(101325), Input.temperature(20))
        assert self.fluid.pressure == 101325
        assert self.fluid.temperature == 20

    @pytest.mark.parametrize("name", fluid_names)
    def test_update_various_fluids_matches_with_coolprop(self, name: FluidsList):
        self.setup_fluid(name)
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
        expected = list(
            map(
                self.coolprop_interface,
                (
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
                ),
            )
        )
        assert all(
            [
                True
                if actual[i] is None and expected[i] is None
                else abs(actual[i] - expected[i]) < 1e-9
                for i in range(len(actual))
            ]
        )
        assert (
            self.fluid.kinematic_viscosity
            == self.fluid.dynamic_viscosity / self.fluid.density
            if self.fluid.dynamic_viscosity is not None
            else True
        )

    def test_equals_same_returns_true(self):
        origin = self.fluid.with_state(Input.pressure(101325), Input.temperature(5))
        same = self.fluid.with_state(Input.pressure(101325), Input.temperature(5))
        assert origin == same

    def test_equals_other_returns_false(self):
        origin = self.fluid.with_state(Input.pressure(101325), Input.temperature(5))
        other = self.fluid.with_state(Input.pressure(101325), Input.temperature(10))
        assert origin != other
        assert origin != object()

    def test_hash_same_returns_same_hash_code(self):
        origin = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        same = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        assert hash(origin) == hash(same)

    def test_hash_other_returns_other_hash_code(self):
        origin = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        other = self.fluid.with_state(Input.pressure(101325), Input.temperature(30))
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json_indented_or_not_returns_properly_formatted_json(
        self, indented: bool
    ):
        fluid = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        assert fluid.as_json(indented) == json.dumps(
            fluid.as_dict(),
            indent=4 if indented else None,
            default=str,
            sort_keys=False,
        )

    def test_as_dict_always_returns_only_public_properties(self):
        fluid = self.fluid.with_state(Input.pressure(101325), Input.temperature(20))
        assert all(
            key
            in [
                k.split("__")[-1]
                for k in vars(fluid).keys()
                if not k.split("__")[-1].startswith("_")
            ]
            for key in list(fluid.as_dict().keys())
        )

    def setup_fluid(self, name: FluidsList):
        fraction = (
            None if name.pure else round(0.5 * (name.fraction_min + name.fraction_max))
        )
        self.fluid = Fluid(name, fraction)
        self.fluid.update(
            Input.pressure(
                10e6 if self.fluid.max_pressure is None else self.fluid.max_pressure
            ),
            Input.temperature(self.fluid.max_temperature),
        )

    def coolprop_interface(self, output_key: str) -> Optional[float]:
        if output_key == "P":
            return self.fluid.pressure
        if output_key == "T":
            return self.fluid.temperature
        try:
            value = PropsSI(
                output_key,
                "P",
                self.fluid.pressure,
                "T",
                self.fluid.temperature + 273.15,
                f"{self.fluid.name.coolprop_backend}::{self.fluid.name.coolprop_name}"
                + ("" if self.fluid.name.pure else f"-{self.fluid.fraction}%"),
            )
            return self.checked_value(value, output_key)
        except ValueError:
            return None

    @staticmethod
    def checked_value(value: float, output_key: str) -> Optional[float]:
        if isinf(value) or isnan(value) or (output_key == "Q" and not 0 <= value <= 1):
            return None
        if output_key.startswith("T"):
            return value - 273.15
        return value
