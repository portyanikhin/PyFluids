from pyfluids import InputHumidAir


class InputHumidAirExtended(InputHumidAir):
    """An example of how to extend the InputHumidAir class."""

    def __init__(self, coolprop_key: str, value: float):
        """
        CoolProp keyed input for humid air.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def water_mole_fraction(cls, value: float) -> "InputHumidAirExtended":
        """
        Water mole fraction.

        :param value: The value of the input [mol/mol].
        :return: Water mole fraction for the input.
        """
        return cls("psi_w", value)


class TestInputHumidAirExtended:
    input_extended = InputHumidAirExtended.water_mole_fraction(5e-3)

    def test_coolprop_key_new_input_matches_with_coolprop(self):
        assert self.input_extended.coolprop_key == "psi_w"

    def test_value_new_input_should_be_in_si_units(self):
        assert self.input_extended.value == 5e-3
