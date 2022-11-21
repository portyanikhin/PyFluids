from .abstract_input import AbstractInput

__all__ = ["InputHumidAir"]


class InputHumidAir(AbstractInput):
    """CoolProp keyed input for humid air."""

    def __init__(self, coolprop_key: str, value: float):
        """
        CoolProp keyed input for humid air.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        super().__init__(coolprop_key, value)

    @classmethod
    def altitude(cls, value: float) -> "InputHumidAir":
        """
        Altitude above sea level.

        The pressure will be calculated by altitude above sea level according to
        ASHRAE Fundamentals Handbook.

        :param value: The value of the input [m].
        :return: Altitude above sea level for the input.
        :raises ValueError: If altitude above sea level is not between
            -5000 and 11000 meters.
        """
        if not -5000 <= value <= 11000:
            raise ValueError(
                "Altitude above sea level should be between -5000 and 11000 meters!"
            )
        return cls("P", 101325 * (1 - 2.25577e-5 * value) ** 5.2559)

    @classmethod
    def density(cls, value: float) -> "InputHumidAir":
        """
        Mass density per humid air unit.

        :param value: The value of the input [kg/m3].
        :return: Mass density per humid air unit for the input.
        """
        return cls("Vha", 1 / value)

    @classmethod
    def dew_temperature(cls, value: float) -> "InputHumidAir":
        """
        Dew-point temperature.

        :param value: The value of the input [°C].
        :return: Dew-point temperature for the input.
        """
        return cls("D", value + 273.15)

    @classmethod
    def enthalpy(cls, value: float) -> "InputHumidAir":
        """
        Mass specific enthalpy per humid air.

        :param value: The value of the input [J/kg].
        :return: Mass specific enthalpy per humid air for the input.
        """
        return cls("Hha", value)

    @classmethod
    def entropy(cls, value: float) -> "InputHumidAir":
        """
        Mass specific entropy per humid air.

        :param value: The value of the input [J/kg/K].
        :return: Mass specific entropy per humid air for the input.
        """
        return cls("Sha", value)

    @classmethod
    def humidity(cls, value: float) -> "InputHumidAir":
        """
        Absolute humidity ratio.

        :param value: The value of the input [kg/kg d.a.].
        :return: Absolute humidity ratio for the input.
        """
        return cls("W", value)

    @classmethod
    def partial_pressure(cls, value: float) -> "InputHumidAir":
        """
        Partial pressure of water vapor.

        :param value: The value of the input [Pa].
        :return: Partial pressure of water vapor for the input.
        """
        return cls("P_w", value)

    @classmethod
    def pressure(cls, value: float) -> "InputHumidAir":
        """
        Absolute pressure.

        :param value: The value of the input [Pa].
        :return: Absolute pressure for the input.
        """
        return cls("P", value)

    @classmethod
    def relative_humidity(cls, value: float) -> "InputHumidAir":
        """
        Relative humidity.

        :param value: The value of the input [%].
        :return: Relative humidity for the input.
        """
        return cls("R", value * 1e-2)

    @classmethod
    def temperature(cls, value: float) -> "InputHumidAir":
        """
        Temperature.

        :param value: The value of the input [°C].
        :return: Temperature for the input.
        """
        return cls("T", value + 273.15)

    @classmethod
    def wet_bulb_temperature(cls, value: float) -> "InputHumidAir":
        """
        Wet-bulb temperature.

        :param value: The value of the input [°C].
        :return: Wet-bulb temperature for the input.
        """
        return cls("B", value + 273.15)
