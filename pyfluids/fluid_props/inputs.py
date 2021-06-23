#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import CoolProp

from pyfluids.interfaces.input_interfaces import *

__all__ = ["Input"]


class Input(InputInterface):
    """Thermophysical properties for inputs.

    Notes:
        Use `with_value` method when instantiate for setting value to the property.
        By default, the value is None. \n

        Density – mass density [kg/m3] \n
        Enthalpy – mass specific enthalpy [J/kg] \n
        Entropy – mass specific entropy [J/kg/K] \n
        InternalEnergy – mass specific internal energy [J/kg] \n
        Pressure – absolute pressure [Pa] \n
        Quality – mass vapor quality [-] \n
        Temperature – absolute temperature [K] \n

    Examples:
        >>> p = Input.Pressure
        >>> p.value
        ... None
        >>> p = Input.Pressure.with_value(101325)
        >>> p.value
        ... 101325
    """

    Density = CoolProp.iDmass
    Enthalpy = CoolProp.iHmass
    Entropy = CoolProp.iSmass
    InternalEnergy = CoolProp.iUmass
    Pressure = CoolProp.iP
    Quality = CoolProp.iQ
    Temperature = CoolProp.iT

    def with_value(self, value: float) -> ConcreteInput:
        """Set value for the property.

        Args:
            value (float): value of the property [SI units]

        Returns:
            ConcreteInput: new input instance with coolprop_key and value

        Examples:
            >>> p = Input.Pressure
            >>> p.value
            ... None
            >>> p = Input.Pressure.with_value(101325)
            >>> p.value
            ... 101325
        """
        return super().with_value(value)

    @property
    def coolprop_key(self) -> int:
        """CoolProp key for the property.

        Examples:
            >>> p = Input.Pressure.with_value(101325)
            >>> p.coolprop_key
            ... 20
            >>> t = Input.Temperature.with_value(293.15)
            >>> t.coolprop_key
            ... 19
        """
        return super().coolprop_key

    @property
    def value(self) -> float:
        """Value of the property [SI units].

        Examples:
            >>> p = Input.Pressure
            >>> p.value
            ... None
            >>> p = Input.Pressure.with_value(101325)
            >>> p.value
            ... 101325
        """
        return super().value
