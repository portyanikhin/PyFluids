#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from pyfluids.interfaces.input_interfaces import *

__all__ = ["HAInput"]


class HAInput(InputInterface):
    """Thermophysical properties of humid air for inputs.

    Notes:
        Use `with_value` method when instantiate for setting value to the property.
        By default, the value is None. \n

        Density – mass density per humid air unit [kg/m3] \n
        DewTemperature – dew-point absolute temperature [K] \n
        Enthalpy – mass specific enthalpy per humid air [J/kg] \n
        Entropy – mass specific entropy per humid air [J/kg/K] \n
        Humidity – absolute humidity ratio [kg/kg d.a.] \n
        PartialPressure – partial pressure of water vapor [Pa] \n
        Pressure – absolute pressure [Pa] \n
        RelativeHumidity – relative humidity ratio (from 0 to 1) [-] \n
        Temperature – absolute dry-bulb temperature [K] \n
        WBTemperature – absolute wet-bulb temperature [K] \n

    Examples:
        >>> p = HAInput.Pressure
        >>> p.value
        ... None
        >>> p = HAInput.Pressure.with_value(101325)
        >>> p.value
        ... 101325
    """

    Density = "Vha"
    DewTemperature = "D"
    Enthalpy = "Hha"
    Entropy = "Sha"
    Humidity = "W"
    PartialPressure = "P_w"
    Pressure = "P"
    RelativeHumidity = "R"
    Temperature = "T"
    WBTemperature = "B"

    def with_value(self, value: float) -> ConcreteInput:
        """Set value for the property.

        Args:
            value (float): value of the property [SI units]

        Returns:
            ConcreteInput: new input instance with coolprop_key and value

        Examples:
            >>> p = HAInput.Pressure
            >>> p.value
            ... None
            >>> p = HAInput.Pressure.with_value(101325)
            >>> p.value
            ... 101325
        """
        return super().with_value(value)

    @property
    def coolprop_key(self) -> str:
        """CoolProp key for the property.

        Examples:
            >>> p = HAInput.Pressure.with_value(101325)
            >>> p.coolprop_key
            ... "P"
            >>> t = HAInput.Temperature.with_value(293.15)
            >>> t.coolprop_key
            ... "T"
            >>> phi = HAInput.RelativeHumidity.with_value(0.5)
            >>> phi.coolprop_key
            ... "R"
        """
        return super().coolprop_key

    @property
    def value(self) -> float:
        """Value of the property [SI units].

        Examples:
            >>> p = HAInput.Pressure
            >>> p.value
            ... None
            >>> p = HAInput.Pressure.with_value(101325)
            >>> p.value
            ... 101325
        """
        return super().value
