from .abstract_input import AbstractInput

__all__ = ["InputHumidAir"]


class InputHumidAir(AbstractInput):
    """CoolProp keyed input for humid air."""

    def __init__(self, coolprop_key: str, value: float):
        """
        CoolProp keyed input for humid air.

        Args:
            coolprop_key (str): CoolProp internal key.
            value (float): Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def density(cls, value: float) -> "InputHumidAir":
        """
        Mass density per humid air unit.

        Args:
            value (float): The value of the input [kg/m3].

        Returns:
            InputHumidAir: Mass density per humid air unit for the input.
        """
        return cls("Vha", 1 / value)

    @classmethod
    def dew_temperature(cls, value: float) -> "InputHumidAir":
        """
        Dew-point temperature.

        Args:
            value (float): The value of the input [°C].

        Returns:
            InputHumidAir: Dew-point temperature for the input.
        """
        return cls("D", value + 273.15)

    @classmethod
    def enthalpy(cls, value: float) -> "InputHumidAir":
        """
        Mass specific enthalpy per humid air.

        Args:
            value (float): The value of the input [J/kg].

        Returns:
            InputHumidAir: Mass specific enthalpy per humid air for the input.
        """
        return cls("Hha", value)

    @classmethod
    def entropy(cls, value: float) -> "InputHumidAir":
        """
        Mass specific entropy per humid air.

        Args:
            value (float): The value of the input [J/kg/K].

        Returns:
            InputHumidAir: Mass specific entropy per humid air for the input.
        """
        return cls("Sha", value)

    @classmethod
    def humidity(cls, value: float) -> "InputHumidAir":
        """
        Absolute humidity ratio.

        Args:
            value (float): The value of the input [kg/kg d.a.].

        Returns:
            InputHumidAir: Absolute humidity ratio for the input.
        """
        return cls("W", value)

    @classmethod
    def partial_pressure(cls, value: float) -> "InputHumidAir":
        """
        Partial pressure of water vapor.

        Args:
            value (float): The value of the input [Pa].

        Returns:
            InputHumidAir: Partial pressure of water vapor for the input.
        """
        return cls("P_w", value)

    @classmethod
    def pressure(cls, value: float) -> "InputHumidAir":
        """
        Absolute pressure.

        Args:
            value (float): The value of the input [Pa].

        Returns:
            InputHumidAir: Absolute pressure for the input.
        """
        return cls("P", value)

    @classmethod
    def relative_humidity(cls, value: float) -> "InputHumidAir":
        """
        Relative humidity.

        Args:
            value (float): The value of the input [%].

        Returns:
            InputHumidAir: Relative humidity for the input.
        """
        return cls("R", value * 1e-2)

    @classmethod
    def temperature(cls, value: float) -> "InputHumidAir":
        """
        Temperature.

        Args:
            value (float): The value of the input [°C].

        Returns:
            InputHumidAir: Temperature for the input.
        """
        return cls("T", value + 273.15)

    @classmethod
    def wet_bulb_temperature(cls, value: float) -> "InputHumidAir":
        """
        Wet-bulb temperature.

        Args:
            value (float): The value of the input [°C].

        Returns:
            InputHumidAir: Wet-bulb temperature for the input.
        """
        return cls("B", value + 273.15)
