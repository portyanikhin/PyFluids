import CoolProp
import pytest

from pyfluids import Input


class TestInput:
    @pytest.mark.parametrize(
        "coolprop_input, coolprop_key, value",
        [
            (Input.density(999), CoolProp.iDmass, 999),
            (Input.enthalpy(1e3), CoolProp.iHmass, 1e3),
            (Input.entropy(5e3), CoolProp.iSmass, 5e3),
            (Input.internal_energy(1e4), CoolProp.iUmass, 1e4),
            (Input.pressure(101325), CoolProp.iP, 101325),
            (Input.quality(0.5), CoolProp.iQ, 0.5),
            (Input.temperature(20), CoolProp.iT, 293.15),
        ],
    )
    def test_inputs(self, coolprop_input: Input, coolprop_key: int, value: float):
        assert coolprop_input.coolprop_key == coolprop_key
        assert coolprop_input.value == value
