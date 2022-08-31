import CoolProp

from .abstract_input import AbstractInput

__all__ = ["Input"]


class Input(AbstractInput):
    """CoolProp keyed input for fluids and mixtures."""

    def __init__(self, coolprop_key: int, value: float):
        """
        CoolProp keyed input for fluids and mixtures.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def density(cls, value: float) -> "Input":
        """
        Mass density.

        :param value: The value of the input [kg/m3].
        :return: Mass density for the input.
        """
        return cls(CoolProp.iDmass, value)

    @classmethod
    def enthalpy(cls, value: float) -> "Input":
        """
        Mass specific enthalpy.

        :param value: The value of the input [J/kg].
        :return: Mass specific enthalpy for the input.
        """
        return cls(CoolProp.iHmass, value)

    @classmethod
    def entropy(cls, value: float) -> "Input":
        """
        Mass specific entropy.

        :param value: The value of the input [J/kg/K].
        :return: Mass specific entropy for the input.
        """
        return cls(CoolProp.iSmass, value)

    @classmethod
    def internal_energy(cls, value: float) -> "Input":
        """
        Mass specific internal energy.

        :param value: The value of the input [J/kg].
        :return: Mass specific internal energy for the input.
        """
        return cls(CoolProp.iUmass, value)

    @classmethod
    def pressure(cls, value: float) -> "Input":
        """
        Absolute pressure.

        :param value: The value of the input [Pa].
        :return: Absolute pressure for the input.
        """
        return cls(CoolProp.iP, value)

    @classmethod
    def quality(cls, value: float) -> "Input":
        """
        Mass vapor quality.

        :param value: The value of the input [%].
        :return: Mass vapor quality for the input.
        """
        return cls(CoolProp.iQ, value * 1e-2)

    @classmethod
    def temperature(cls, value: float) -> "Input":
        """
        Temperature.

        :param value: The value of the input [°C].
        :return: Temperature for the input.
        """
        return cls(CoolProp.iT, value + 273.15)
