from .pyfluids_config import PyFluidsConfig
from .pyfluids_config_builder import PyFluidsConfigBuilder
from .units_system import UnitsSystem

__all__ = ["UnitConverter"]


class UnitConverter:
    """Unit converter."""

    def __init__(self):
        """Unit converter."""
        self.__config: PyFluidsConfig = PyFluidsConfigBuilder().build()

    @property
    def units_system(self) -> UnitsSystem:
        """Configured units system."""
        return self.__config.units_system

    def convert_temperature_from_si(self, value: float) -> float:
        """
        Convert temperature from SI to configured units system.

        :param value: Temperature value.
        :return: Converted value.
        """
        if self.units_system == UnitsSystem.SI:
            return value
        return value - 273.15

    def convert_temperature_to_si(self, value: float) -> float:
        """
        Convert temperature from configured units system to SI.

        :param value: Temperature value.
        :return: Converted value.
        """
        if self.units_system == UnitsSystem.SI:
            return value
        return value + 273.15

    def convert_decimal_fraction_from_si(self, value: float) -> float:
        """
        Convert decimal fraction from SI to configured units system.

        :param value: Decimal fraction value.
        :return: Converted value.
        """
        if self.units_system == UnitsSystem.SIWithCelsiusAndPercents:
            return value * 1e2
        return value

    def convert_decimal_fraction_to_si(self, value: float) -> float:
        """
        Convert decimal fraction from configured units system to SI.

        :param value: Decimal fraction value.
        :return: Converted value.
        """
        if self.units_system == UnitsSystem.SIWithCelsiusAndPercents:
            return value * 1e-2
        return value
