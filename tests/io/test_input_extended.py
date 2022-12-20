import CoolProp

from pyfluids import Input


class InputExtended(Input):
    """An example of how to extend the Input class."""

    def __init__(self, coolprop_key: int, value: float):
        """
        CoolProp keyed input for fluids and mixtures.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def molar_density(cls, value: float) -> "InputExtended":
        """
        Molar density.

        :param value: The value of the input [kg/mol].
        :return: Molar density for the input.
        """
        return cls(CoolProp.iDmolar, value)


class TestInputExtended:
    input_extended = InputExtended.molar_density(9e2)

    def test_coolprop_key_new_input_matches_with_coolprop(self):
        assert self.input_extended.coolprop_key == CoolProp.iDmolar

    def test_value_new_input_should_be_in_si_units(self):
        assert self.input_extended.value == 900
