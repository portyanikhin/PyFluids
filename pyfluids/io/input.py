import CoolProp

from .abstract_input import AbstractInput

__all__ = ["Input"]


class Input(AbstractInput):
    """CoolProp keyed input for fluids and mixtures."""

    def __init__(self, coolprop_key: int, value: float):
        """
        CoolProp keyed input for fluids and mixtures.

        Args:
            coolprop_key (int): CoolProp internal key.
            value (float): Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def density(cls, value: float) -> "Input":
        """
        Mass density.

        Args:
            value (float): The value of the input [kg/m3].

        Returns:
            Input: Mass density for the input.
        """
        return cls(CoolProp.iDmass, value)

    @classmethod
    def enthalpy(cls, value: float) -> "Input":
        """
        Mass specific enthalpy.

        Args:
            value (float): The value of the input [J/kg].

        Returns:
            Input: Mass specific enthalpy for the input.
        """
        return cls(CoolProp.iHmass, value)

    @classmethod
    def entropy(cls, value: float) -> "Input":
        """
        Mass specific entropy.

        Args:
            value (float): The value of the input [J/kg/K].

        Returns:
            Input: Mass specific entropy for the input.
        """
        return cls(CoolProp.iSmass, value)

    @classmethod
    def internal_energy(cls, value: float) -> "Input":
        """
        Mass specific internal energy.

        Args:
            value (float): The value of the input [J/kg].

        Returns:
            Input: Mass specific internal energy for the input.
        """
        return cls(CoolProp.iUmass, value)

    @classmethod
    def pressure(cls, value: float) -> "Input":
        """
        Absolute pressure.

        Args:
            value (float): The value of the input [Pa].

        Returns:
            Input: Absolute pressure for the input.
        """
        return cls(CoolProp.iP, value)

    @classmethod
    def quality(cls, value: float) -> "Input":
        """
        Mass vapor quality.

        Args:
            value (float): The value of the input [-].

        Returns:
            Input: Mass vapor quality for the input.
        """
        return cls(CoolProp.iQ, value)

    @classmethod
    def temperature(cls, value: float) -> "Input":
        """
        Temperature.

        Args:
            value (float): The value of the input [°C].

        Returns:
            Input: Temperature for the input.
        """
        return cls(CoolProp.iT, value + 273.15)
