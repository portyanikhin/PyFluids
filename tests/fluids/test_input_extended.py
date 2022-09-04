import CoolProp

from pyfluids import Input


class InputExtended(Input):
    """An example of how to extend Input."""

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
    input_extended = InputExtended.molar_density(900)

    def test_coolprop_key(self):
        assert self.input_extended.coolprop_key == CoolProp.iDmolar

    def test_value(self):
        assert self.input_extended.value == 900
