import asyncio
import json

import pytest
from CoolProp.HumidAirProp import HAPropsSI

from pyfluids import HumidAir, InputHumidAir


class TestHumidAir:
    humid_air: HumidAir = HumidAir()

    @pytest.mark.asyncio
    async def test_humid_air_multi_threading_is_thread_safe(self):
        async def dew_temperature_of_humid_air_at_standard_conditions() -> float:
            return self.humid_air.with_state(
                InputHumidAir.pressure(101325),
                InputHumidAir.temperature(20),
                InputHumidAir.relative_humidity(50),
            ).dew_temperature

        tasks = [
            asyncio.create_task(dew_temperature_of_humid_air_at_standard_conditions())
            for _ in range(100)
        ]
        await asyncio.gather(*tasks)
        results = set(task.result() for task in tasks)
        assert len(results) == 1

    def test_factory_always_returns_new_instance_with_no_defined_state(self):
        assert self.humid_air.factory() == HumidAir()

    def test_clone_always_returns_new_instance_with_same_state(self):
        origin = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        clone = origin.clone()
        assert origin == clone
        clone.update(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(60),
        )
        assert origin != clone

    def test_with_state_always_returns_new_instance_with_defined_state(self):
        assert (
            self.humid_air.with_state(
                InputHumidAir.pressure(101325),
                InputHumidAir.temperature(20),
                InputHumidAir.relative_humidity(50),
            )
            != HumidAir()
        )

    def test_update_same_inputs_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.humid_air.update(
                InputHumidAir.pressure(101325),
                InputHumidAir.temperature(20),
                InputHumidAir.temperature(30),
            )
        assert "Need to define 3 unique inputs!" in str(e.value)

    def test_update_always_inputs_are_cached(self):
        self.humid_air.update(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        assert self.humid_air.pressure == 101325
        assert self.humid_air.temperature == 20
        assert self.humid_air.relative_humidity == 50

    @pytest.mark.parametrize("pressure", [1e5, 2e5, 5e5])
    @pytest.mark.parametrize("temperature", range(-20, 50, 10))
    @pytest.mark.parametrize("relative_humidity", range(0, 100, 10))
    def test_update_various_conditions_matches_with_coolprop(
        self, pressure: float, temperature: float, relative_humidity: float
    ):
        self.humid_air.update(
            InputHumidAir.pressure(pressure),
            InputHumidAir.temperature(temperature),
            InputHumidAir.relative_humidity(relative_humidity),
        )
        actual = (
            self.humid_air.compressibility,
            self.humid_air.conductivity,
            self.humid_air.density,
            self.humid_air.dew_temperature,
            self.humid_air.dynamic_viscosity,
            self.humid_air.enthalpy,
            self.humid_air.entropy,
            self.humid_air.humidity,
            self.humid_air.partial_pressure,
            self.humid_air.pressure,
            self.humid_air.relative_humidity,
            self.humid_air.specific_heat,
            self.humid_air.temperature,
            self.humid_air.wet_bulb_temperature,
        )
        expected = list(
            map(
                self.coolprop_interface,
                (
                    "Z",
                    "K",
                    "Vha",
                    "D",
                    "M",
                    "Hha",
                    "Sha",
                    "W",
                    "P_w",
                    "P",
                    "R",
                    "Cha",
                    "T",
                    "B",
                ),
            )
        )
        assert all([abs(actual[i] - expected[i]) < 1e-9 for i in range(len(actual))])
        assert (
            self.humid_air.kinematic_viscosity
            == self.humid_air.dynamic_viscosity / self.humid_air.density
        )
        assert (
            self.humid_air.prandtl
            == self.humid_air.dynamic_viscosity
            * self.humid_air.specific_heat
            / self.humid_air.conductivity
        )

    def test_equals_same_returns_true(self):
        origin = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        same = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        assert origin == same

    def test_equals_other_returns_false(self):
        origin = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        other = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(60),
        )
        assert origin != other
        assert origin != object()

    def test_hash_same_returns_same_hash_code(self):
        origin = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(50),
        )
        same = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(50),
        )
        assert hash(origin) == hash(same)

    def test_hash_other_returns_other_hash_code(self):
        origin = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(50),
        )
        other = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(60),
        )
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json_indented_or_not_returns_properly_formatted_json(
        self, indented: bool
    ):
        humid_air = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        assert humid_air.as_json(indented) == json.dumps(
            humid_air.as_dict(),
            indent=4 if indented else None,
            default=str,
            sort_keys=False,
        )

    def test_as_dict_always_returns_only_public_properties(self):
        humid_air = self.humid_air.with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(40),
        )
        assert all(
            key
            in [
                k.split("__")[-1]
                for k in vars(humid_air).keys()
                if not k.split("__")[-1].startswith("_")
            ]
            for key in list(humid_air.as_dict().keys())
        )

    def coolprop_interface(self, output_key: str) -> float:
        value = HAPropsSI(
            output_key,
            "P",
            self.humid_air.pressure,
            "T",
            self.humid_air.temperature + 273.15,
            "R",
            self.humid_air.relative_humidity * 1e-2,
        )
        if output_key == "Vha":
            return 1 / value
        if output_key in ("D", "T", "B"):
            return value - 273.15
        if output_key == "R":
            return value * 1e2
        return value
