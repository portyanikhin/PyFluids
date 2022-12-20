import CoolProp
import pytest

from pyfluids import Input


class TestInput:
    @pytest.mark.parametrize(
        "coolprop_input, coolprop_key",
        [
            (Input.density(999), CoolProp.iDmass),
            (Input.enthalpy(1e3), CoolProp.iHmass),
            (Input.entropy(5e3), CoolProp.iSmass),
            (Input.internal_energy(1e4), CoolProp.iUmass),
            (Input.pressure(101325), CoolProp.iP),
            (Input.quality(50), CoolProp.iQ),
            (Input.temperature(20), CoolProp.iT),
        ],
    )
    def test_coolprop_key_all_inputs_matches_with_coolprop(
        self, coolprop_input: Input, coolprop_key: int
    ):
        assert coolprop_input.coolprop_key == coolprop_key

    @pytest.mark.parametrize(
        "coolprop_input, value",
        [
            (Input.density(999), 999),
            (Input.enthalpy(1e3), 1e3),
            (Input.entropy(5e3), 5e3),
            (Input.internal_energy(1e4), 1e4),
            (Input.pressure(101325), 101325),
            (Input.quality(50), 0.5),
            (Input.temperature(20), 293.15),
        ],
    )
    def test_value_all_inputs_should_be_in_si_units(
        self, coolprop_input: Input, value: float
    ):
        assert coolprop_input.value == value

    def test_equals_same_returns_true(self):
        origin = Input.temperature(5)
        same = Input.temperature(5)
        assert origin == same

    def test_equals_other_returns_false(self):
        origin = Input.temperature(5)
        other = Input.temperature(10)
        assert origin != other
        assert origin != object()

    def test_hash_same_returns_same_hash_code(self):
        origin = Input.temperature(5)
        same = Input.temperature(5)
        assert hash(origin) == hash(same)

    def test_hash_other_returns_other_hash_code(self):
        origin = Input.temperature(5)
        other = Input.temperature(10)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())
