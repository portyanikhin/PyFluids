import pytest

from pyfluids import InputHumidAir


class TestInputHumidAir:
    @pytest.mark.parametrize(
        "coolprop_input, coolprop_key",
        [
            (InputHumidAir.altitude(300), "P"),
            (InputHumidAir.density(1.2), "Vha"),
            (InputHumidAir.dew_temperature(10), "D"),
            (InputHumidAir.enthalpy(2e4), "Hha"),
            (InputHumidAir.entropy(1e4), "Sha"),
            (InputHumidAir.humidity(5e-3), "W"),
            (InputHumidAir.partial_pressure(1e3), "P_w"),
            (InputHumidAir.pressure(101325), "P"),
            (InputHumidAir.relative_humidity(50), "R"),
            (InputHumidAir.temperature(20), "T"),
            (InputHumidAir.wet_bulb_temperature(15), "B"),
        ],
    )
    def test_coolprop_key_all_inputs_matches_with_coolprop(
        self, coolprop_input: InputHumidAir, coolprop_key: str
    ):
        assert coolprop_input.coolprop_key == coolprop_key

    @pytest.mark.parametrize(
        "coolprop_input, value",
        [
            (InputHumidAir.altitude(300), 97772.56060611102),
            (InputHumidAir.density(1.2), 0.8333333333333334),
            (InputHumidAir.dew_temperature(10), 283.15),
            (InputHumidAir.enthalpy(2e4), 2e4),
            (InputHumidAir.entropy(1e4), 1e4),
            (InputHumidAir.humidity(5e-3), 5e-3),
            (InputHumidAir.partial_pressure(1e3), 1e3),
            (InputHumidAir.pressure(101325), 101325),
            (InputHumidAir.relative_humidity(50), 0.5),
            (InputHumidAir.temperature(20), 293.15),
            (InputHumidAir.wet_bulb_temperature(15), 288.15),
        ],
    )
    def test_value_all_inputs_should_be_in_si_units(
        self, coolprop_input: InputHumidAir, value: float
    ):
        assert coolprop_input.value == value

    def test_equals_same_returns_true(self):
        origin = InputHumidAir.altitude(0)
        same = InputHumidAir.pressure(101325)
        assert origin == same

    def test_equals_other_returns_false(self):
        origin = InputHumidAir.altitude(0)
        other = InputHumidAir.pressure(1e5)
        assert origin != other
        assert origin != object()

    def test_hash_same_returns_same_hash_code(self):
        origin = InputHumidAir.altitude(0)
        same = InputHumidAir.pressure(101325)
        assert hash(origin) == hash(same)

    def test_hash_other_returns_other_hash_code(self):
        origin = InputHumidAir.altitude(0)
        other = InputHumidAir.pressure(1e5)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    @pytest.mark.parametrize("altitude", [-5000.1, 11000.1])
    def test_altitude_wrong_value_raises_value_error(self, altitude):
        with pytest.raises(ValueError) as e:
            InputHumidAir.altitude(altitude)
        assert (
            "Altitude above sea level should be between -5000 and 11000 meters!"
            in str(e.value)
        )
