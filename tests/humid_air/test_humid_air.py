import json

import pytest
from CoolProp.HumidAirProp import HAPropsSI

from pyfluids import HumidAir, InputHumidAir


class TestHumidAir:
    def test_factory(self):
        assert HumidAir().factory() == HumidAir()

    def test_with_state(self):
        assert hash(
            HumidAir().with_state(
                InputHumidAir.pressure(101325),
                InputHumidAir.temperature(20),
                InputHumidAir.humidity(50),
            )
        ) != hash(HumidAir())

    def test_invalid_input(self):
        with pytest.raises(ValueError) as e:
            HumidAir().with_state(
                InputHumidAir.pressure(101325),
                InputHumidAir.temperature(20),
                InputHumidAir.temperature(30),
            )
        assert "Need to define 3 unique inputs!" in str(e.value)

    @pytest.mark.parametrize("pressure", [0.5e5, 1e5, 2e5, 5e5])
    @pytest.mark.parametrize("temperature", range(-20, 50, 10))
    @pytest.mark.parametrize("relative_humidity", range(0, 100, 10))
    def test_update(
        self, pressure: float, temperature: float, relative_humidity: float
    ):
        humid_air = HumidAir().with_state(
            InputHumidAir.pressure(pressure),
            InputHumidAir.temperature(temperature),
            InputHumidAir.relative_humidity(relative_humidity),
        )
        actual = (
            humid_air.compressibility,
            humid_air.conductivity,
            humid_air.density,
            humid_air.dew_temperature,
            humid_air.dynamic_viscosity,
            humid_air.enthalpy,
            humid_air.entropy,
            humid_air.humidity,
            humid_air.partial_pressure,
            humid_air.pressure,
            humid_air.relative_humidity,
            humid_air.specific_heat,
            humid_air.temperature,
            humid_air.wet_bulb_temperature,
        )
        keys = (
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
        )
        assert all(
            [
                abs(
                    actual[i]
                    - self.high_level_interface(
                        keys[i], pressure, temperature, relative_humidity
                    )
                )
                < 1e-6
                for i in range(len(actual))
            ]
        )
        assert (
            humid_air.kinematic_viscosity
            == humid_air.dynamic_viscosity / humid_air.density
        )
        assert (
            humid_air.prandtl
            == humid_air.dynamic_viscosity
            * humid_air.specific_heat
            / humid_air.conductivity
        )

    def test_cached_inputs(self):
        humid_air = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        assert humid_air.pressure == 101325
        assert humid_air.temperature == 20
        assert humid_air.relative_humidity == 50

    def test_equals(self):
        origin = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        same = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
        )
        other = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(60),
        )
        assert origin == same
        assert origin != other
        assert origin != object()

    def test_hash(self):
        origin = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(50),
        )
        same = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(50),
        )
        other = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(30),
            InputHumidAir.relative_humidity(60),
        )
        assert hash(origin) == hash(same)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    def test_clone(self):
        origin = HumidAir().with_state(
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

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json(self, indented: bool):
        humid_air = HumidAir().with_state(
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

    def test_as_dict(self):
        humid_air = HumidAir().with_state(
            InputHumidAir.pressure(101325),
            InputHumidAir.temperature(20),
            InputHumidAir.relative_humidity(50),
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

    @staticmethod
    def high_level_interface(
        key: str, pressure: float, temperature: float, relative_humidity: float
    ) -> float:
        value = HAPropsSI(
            key, "P", pressure, "T", temperature + 273.15, "R", relative_humidity * 1e-2
        )
        if key == "Vha":
            value = 1 / value
        if key in ("D", "T", "B"):
            value -= 273.15
        if key == "R":
            value *= 1e2
        return value
