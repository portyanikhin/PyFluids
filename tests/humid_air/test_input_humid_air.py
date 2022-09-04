import pytest

from pyfluids import InputHumidAir


class TestInputHumidAir:
    @pytest.mark.parametrize(
        "coolprop_input, coolprop_key, value",
        [
            (InputHumidAir.density(1.2), "Vha", 0.8333333333333334),
            (InputHumidAir.dew_temperature(10), "D", 283.15),
            (InputHumidAir.enthalpy(2e4), "Hha", 2e4),
            (InputHumidAir.entropy(1e4), "Sha", 1e4),
            (InputHumidAir.humidity(5e-3), "W", 5e-3),
            (InputHumidAir.partial_pressure(1e3), "P_w", 1e3),
            (InputHumidAir.pressure(101325), "P", 101325),
            (InputHumidAir.relative_humidity(50), "R", 0.5),
            (InputHumidAir.temperature(20), "T", 293.15),
            (InputHumidAir.wet_bulb_temperature(15), "B", 288.15),
        ],
    )
    def test_inputs(
        self, coolprop_input: InputHumidAir, coolprop_key: str, value: float
    ):
        assert coolprop_input.coolprop_key == coolprop_key
        assert coolprop_input.value == value

    def test_equals(self):
        origin = InputHumidAir.temperature(20)
        same = InputHumidAir.temperature(20)
        other = InputHumidAir.temperature(30)
        assert origin == same
        assert origin != other
        assert origin != object()

    def test_hash(self):
        origin = InputHumidAir.temperature(20)
        same = InputHumidAir.temperature(20)
        other = InputHumidAir.temperature(30)
        assert hash(origin) == hash(same)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())
