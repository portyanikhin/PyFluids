from __future__ import annotations

import json

from CoolProp.HumidAirProp import HAPropsSI

from ..config import UnitConverter, UnitsSystem
from ..io import InputHumidAir, OutputsValidator

__all__ = ["HumidAir"]


class HumidAir:
    """Real humid air (see ASHRAE RP-1485)."""

    def __init__(self):
        """Real humid air (see ASHRAE RP-1485)."""
        self._inputs: list[InputHumidAir] = []
        self.__compressibility: float | None = None
        self.__conductivity: float | None = None
        self.__dew_temperature: float | None = None
        self.__dynamic_viscosity: float | None = None
        self.__enthalpy: float | None = None
        self.__entropy: float | None = None
        self.__humidity: float | None = None
        self.__partial_pressure: float | None = None
        self.__pressure: float | None = None
        self.__relative_humidity: float | None = None
        self.__specific_heat: float | None = None
        self.__specific_volume: float | None = None
        self.__temperature: float | None = None
        self.__wet_bulb_temperature: float | None = None
        self._unit_converter: UnitConverter = UnitConverter()

    @property
    def units_system(self) -> UnitsSystem:
        """Configured units system."""
        return self._unit_converter.units_system

    @property
    def compressibility(self) -> float:
        """Compressibility factor [-]."""
        if self.__compressibility is None:
            self.__compressibility = self._keyed_output("Z")
        return self.__compressibility

    @property
    def conductivity(self) -> float:
        """Thermal conductivity [W/m/K]."""
        if self.__conductivity is None:
            self.__conductivity = self._keyed_output("K")
        return self.__conductivity

    @property
    def density(self) -> float:
        """Mass density per humid air unit [kg/m3]."""
        return 1 / self.specific_volume

    @property
    def dew_temperature(self) -> float:
        """
        Dew-point temperature
        [by default, °C; you can change this using the configuration file].
        """
        if self.__dew_temperature is None:
            self.__dew_temperature = self._unit_converter.convert_temperature_from_si(
                self._keyed_output("D")
            )
        return self.__dew_temperature

    @property
    def dynamic_viscosity(self) -> float:
        """Dynamic viscosity [Pa*s]."""
        if self.__dynamic_viscosity is None:
            self.__dynamic_viscosity = self._keyed_output("M")
        return self.__dynamic_viscosity

    @property
    def enthalpy(self) -> float:
        """Mass specific enthalpy per humid air [J/kg]."""
        if self.__enthalpy is None:
            self.__enthalpy = self._keyed_output("Hha")
        return self.__enthalpy

    @property
    def entropy(self) -> float:
        """Mass specific entropy per humid air [J/kg/K]."""
        if self.__entropy is None:
            self.__entropy = self._keyed_output("Sha")
        return self.__entropy

    @property
    def humidity(self) -> float:
        """Absolute humidity ratio [kg/kg d.a.]."""
        if self.__humidity is None:
            self.__humidity = self._keyed_output("W")
        return self.__humidity

    @property
    def kinematic_viscosity(self) -> float:
        """Kinematic viscosity [m2/s]."""
        return self.dynamic_viscosity / self.density

    @property
    def partial_pressure(self) -> float:
        """Partial pressure of water vapor [Pa]."""
        if self.__partial_pressure is None:
            self.__partial_pressure = self._keyed_output("P_w")
        return self.__partial_pressure

    @property
    def prandtl(self) -> float:
        """Prandtl number [-]."""
        return self.dynamic_viscosity * self.specific_heat / self.conductivity

    @property
    def pressure(self) -> float:
        """Absolute pressure [Pa]."""
        if self.__pressure is None:
            self.__pressure = self._keyed_output("P")
        return self.__pressure

    @property
    def relative_humidity(self) -> float:
        """
        Relative humidity ratio
        [by default, %; you can change this using the configuration file].
        """
        if self.__relative_humidity is None:
            self.__relative_humidity = (
                self._unit_converter.convert_decimal_fraction_from_si(
                    self._keyed_output("R")
                )
            )
        return self.__relative_humidity

    @property
    def specific_heat(self) -> float:
        """Mass specific constant pressure specific heat per humid air [J/kg/K]."""
        if self.__specific_heat is None:
            self.__specific_heat = self._keyed_output("Cha")
        return self.__specific_heat

    @property
    def specific_volume(self) -> float:
        """Mass specific volume per humid air unit [m3/kg]."""
        if self.__specific_volume is None:
            self.__specific_volume = self._keyed_output("Vha")
        return self.__specific_volume

    @property
    def temperature(self) -> float:
        """
        Dry-bulb temperature
        [by default, °C; you can change this using the configuration file].
        """
        if self.__temperature is None:
            self.__temperature = self._unit_converter.convert_temperature_from_si(
                self._keyed_output("T")
            )
        return self.__temperature

    @property
    def wet_bulb_temperature(self) -> float:
        """
        Wet-bulb temperature
        [by default, °C; you can change this using the configuration file].
        """
        if self.__wet_bulb_temperature is None:
            self.__wet_bulb_temperature = (
                self._unit_converter.convert_temperature_from_si(
                    self._keyed_output("B")
                )
            )
        return self.__wet_bulb_temperature

    def factory(self) -> HumidAir:
        """Returns a new humid air instance with no defined state."""
        return HumidAir()

    def clone(self) -> HumidAir:
        """Performs deep (full) copy of the humid air instance."""
        return self.with_state(*self._inputs)

    def with_state(
        self,
        first_input: InputHumidAir,
        second_input: InputHumidAir,
        third_input: InputHumidAir,
    ) -> HumidAir:
        """
        Returns a new humid air instance with a defined state.

        :param first_input: First input property.
        :param second_input: Second input property.
        :param third_input: Third input property.
        :return: A new humid air instance with a defined state.
        :raises ValueError: If input is invalid.
        """
        humid_air = self.factory()
        humid_air.update(first_input, second_input, third_input)
        return humid_air

    def update(
        self,
        first_input: InputHumidAir,
        second_input: InputHumidAir,
        third_input: InputHumidAir,
    ):
        """
        Updates the state of the humid air.

        :param first_input: First input property.
        :param second_input: Second input property.
        :param third_input: Third input property.
        :raises ValueError: If input is invalid.
        """
        self.reset()
        self._inputs = [first_input, second_input, third_input]
        self.__check_inputs()

    # noinspection DuplicatedCode
    def reset(self):
        """Resets all properties."""
        self._inputs.clear()
        self.__compressibility = None
        self.__conductivity = None
        self.__dew_temperature = None
        self.__dynamic_viscosity = None
        self.__enthalpy = None
        self.__entropy = None
        self.__humidity = None
        self.__partial_pressure = None
        self.__pressure = None
        self.__relative_humidity = None
        self.__specific_heat = None
        self.__specific_volume = None
        self.__temperature = None
        self.__wet_bulb_temperature = None

    def dry_cooling_to_temperature(
        self, temperature: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling without dehumidification to given temperature.

        :param temperature: Temperature
            [by default, °C; you can change this using the configuration file].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If temperature or pressure drop is invalid.
        """
        return self.__dry_heat_transfer_to_temperature(temperature, True, pressure_drop)

    def dry_cooling_to_enthalpy(
        self, enthalpy: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling without dehumidification to given enthalpy.

        :param enthalpy: Enthalpy [J/kg].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If enthalpy or pressure drop is invalid.
        """
        return self.__dry_heat_transfer_to_enthalpy(enthalpy, True, pressure_drop)

    def wet_cooling_to_temperature_and_relative_humidity(
        self, temperature: float, relative_humidity: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling with dehumidification
        to given temperature and relative humidity ratio.

        :param temperature: Temperature
            [by default, °C; you can change this using the configuration file].
        :param relative_humidity: Relative humidity ratio
            [by default, %; you can change this using the configuration file].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If temperature, relative humidity ratio or
            pressure drop is invalid.
        """
        return self.__wet_cooling_to(
            InputHumidAir.temperature(temperature),
            InputHumidAir.relative_humidity(relative_humidity),
            pressure_drop,
        )

    def wet_cooling_to_temperature_and_absolute_humidity(
        self, temperature: float, humidity: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling with dehumidification
        to given temperature and absolute humidity ratio.

        :param temperature: Temperature
            [by default, °C; you can change this using the configuration file].
        :param humidity: Absolute humidity ratio [kg/kg d.a.].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If temperature, absolute humidity ratio or
            pressure drop is invalid.
        """
        return self.__wet_cooling_to(
            InputHumidAir.temperature(temperature),
            InputHumidAir.humidity(humidity),
            pressure_drop,
        )

    def wet_cooling_to_enthalpy_and_relative_humidity(
        self, enthalpy: float, relative_humidity: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling with dehumidification
        to given enthalpy and relative humidity ratio.

        :param enthalpy: Enthalpy [J/kg].
        :param relative_humidity: Relative humidity ratio
            [by default, %; you can change this using the configuration file].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If enthalpy, relative humidity ratio or
            pressure drop is invalid.
        """
        return self.__wet_cooling_to(
            InputHumidAir.enthalpy(enthalpy),
            InputHumidAir.relative_humidity(relative_humidity),
            pressure_drop,
        )

    def wet_cooling_to_enthalpy_and_absolute_humidity(
        self, enthalpy: float, humidity: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of cooling with dehumidification
        to given enthalpy and absolute humidity ratio.

        :param enthalpy: Enthalpy [J/kg].
        :param humidity: Absolute humidity ratio [kg/kg d.a.].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If enthalpy, absolute humidity ratio or
            pressure drop is invalid.
        """
        return self.__wet_cooling_to(
            InputHumidAir.enthalpy(enthalpy),
            InputHumidAir.humidity(humidity),
            pressure_drop,
        )

    def heating_to_temperature(
        self, temperature: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of heating to given temperature.

        :param temperature: Temperature
            [by default, °C; you can change this using the configuration file].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If temperature or pressure drop is invalid.
        """
        return self.__dry_heat_transfer_to_temperature(
            temperature, False, pressure_drop
        )

    def heating_to_enthalpy(
        self, enthalpy: float, pressure_drop: float = 0
    ) -> HumidAir:
        """
        The process of heating to given enthalpy.

        :param enthalpy: Enthalpy [J/kg].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If enthalpy or pressure drop is invalid.
        """
        return self.__dry_heat_transfer_to_enthalpy(enthalpy, False, pressure_drop)

    def humidification_by_water_to_relative_humidity(
        self, relative_humidity: float
    ) -> HumidAir:
        """
        The process of humidification by water (isenthalpic)
        to given relative humidity ratio.

        :param relative_humidity: Relative humidity ratio
            [by default, %; you can change this using the configuration file].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If relative humidity ratio is invalid.
        """
        return self.__humidification_to(
            InputHumidAir.enthalpy(self.enthalpy),
            InputHumidAir.relative_humidity(relative_humidity),
        )

    def humidification_by_water_to_absolute_humidity(self, humidity: float) -> HumidAir:
        """
        The process of humidification by water (isenthalpic)
        to given absolute humidity ratio.

        :param humidity: Absolute humidity ratio [kg/kg d.a.].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If absolute humidity ratio is invalid.
        """
        return self.__humidification_to(
            InputHumidAir.enthalpy(self.enthalpy),
            InputHumidAir.humidity(humidity),
        )

    def humidification_by_steam_to_relative_humidity(
        self, relative_humidity: float
    ) -> HumidAir:
        """
        The process of humidification by steam (isothermal)
        to given relative humidity ratio.

        :param relative_humidity: Relative humidity ratio
            [by default, %; you can change this using the configuration file].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If relative humidity ratio is invalid.
        """
        return self.__humidification_to(
            InputHumidAir.temperature(self.temperature),
            InputHumidAir.relative_humidity(relative_humidity),
        )

    def humidification_by_steam_to_absolute_humidity(self, humidity: float) -> HumidAir:
        """
        The process of humidification by steam (isothermal)
        to given absolute humidity ratio.

        :param humidity: Absolute humidity ratio [kg/kg d.a.].
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If absolute humidity ratio is invalid.
        """
        return self.__humidification_to(
            InputHumidAir.temperature(self.temperature),
            InputHumidAir.humidity(humidity),
        )

    def mixing(
        self,
        first_specific_mass_flow: float,
        first: HumidAir,
        second_specific_mass_flow: float,
        second: HumidAir,
    ) -> HumidAir:
        """
        The mixing process.

        :param first_specific_mass_flow: Specific mass flow rate of the humid air
            at the first state [-].
        :param first: Humid air at the first state.
        :param second_specific_mass_flow: Specific mass flow rate of the humid air
            the second state [-].
        :param second: Humid air at the second state.
        :return: The state of the humid air at the end of the process.
        :raises ValueError: If the mixing process is not possible.
        """
        if first.pressure != second.pressure:
            raise ValueError(
                "The mixing process is possible only for flows with the same pressure!"
            )
        return self.with_state(
            InputHumidAir.pressure(first.pressure),
            InputHumidAir.enthalpy(
                (
                    first_specific_mass_flow * first.enthalpy
                    + second_specific_mass_flow * second.enthalpy
                )
                / (first_specific_mass_flow + second_specific_mass_flow)
            ),
            InputHumidAir.humidity(
                (
                    first_specific_mass_flow * first.humidity * (1 + second.humidity)
                    + second_specific_mass_flow * second.humidity * (1 + first.humidity)
                )
                / (
                    first_specific_mass_flow * (1 + second.humidity)
                    + second_specific_mass_flow * (1 + first.humidity)
                )
            ),
        )

    def as_json(self, indented: bool = True) -> str:
        """
        Converts the humid air instance to a JSON string.

        :param indented: True if indented.
        :return: The humid air instance as a JSON string.
        """
        return json.dumps(
            self.as_dict(), indent=4 if indented else None, default=str, sort_keys=False
        )

    def as_dict(self) -> dict[str, float]:
        """Converts the humid air to a dict."""
        keys = [
            key
            for key in dir(self.__class__)
            if isinstance(getattr(self.__class__, key), property)
        ]
        values = [getattr(self, key) for key in keys]
        return {key: value for key, value in zip(keys, values)}

    def _keyed_output(self, coolprop_key: str) -> float:
        self.__check_inputs()
        cached_input = next(
            (i for i in self._inputs if i.coolprop_key == coolprop_key), None
        )
        value = (
            cached_input.value
            if cached_input is not None
            else HAPropsSI(
                coolprop_key,
                self._inputs[0].coolprop_key,
                self._inputs[0].value,
                self._inputs[1].coolprop_key,
                self._inputs[1].value,
                self._inputs[2].coolprop_key,
                self._inputs[2].value,
            )
        )
        OutputsValidator(value).validate()
        return value

    def __eq__(self, other: HumidAir) -> bool:
        return isinstance(other, HumidAir) and hash(self) == hash(other)

    def __ne__(self, other: HumidAir) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(
            (
                "&".join(str(i.value) for i in self._inputs),
                "&".join(str(i.coolprop_key) for i in self._inputs),
            )
        )

    def __check_inputs(self):
        unique_keys = set([i.coolprop_key for i in self._inputs])
        if len(self._inputs) != 3 or len(unique_keys) != 3:
            raise ValueError("Need to define 3 unique inputs!")

    def __dry_heat_transfer_to_temperature(
        self, temperature: float, cooling: bool, pressure_drop: float = 0
    ) -> HumidAir:
        self.__check_temperature(temperature, cooling)
        self.__check_dew_temperature(temperature)
        self.__check_pressure_drop(pressure_drop)
        return self.with_state(
            InputHumidAir.pressure(self.pressure - pressure_drop),
            InputHumidAir.temperature(temperature),
            InputHumidAir.humidity(self.humidity),
        )

    def __dry_heat_transfer_to_enthalpy(
        self, enthalpy: float, cooling: bool, pressure_drop: float = 0
    ) -> HumidAir:
        self.__check_enthalpy(enthalpy, cooling)
        self.__check_dew_enthalpy(enthalpy)
        self.__check_pressure_drop(pressure_drop)
        return self.with_state(
            InputHumidAir.pressure(self.pressure - pressure_drop),
            InputHumidAir.enthalpy(enthalpy),
            InputHumidAir.humidity(self.humidity),
        )

    def __wet_cooling_to(
        self,
        first_input: InputHumidAir,
        second_input: InputHumidAir,
        pressure_drop: float = 0,
    ):
        if first_input.coolprop_key == "T":
            self.__check_temperature(
                self._unit_converter.convert_temperature_from_si(first_input.value),
                True,
            )
        if first_input.coolprop_key == "Hha":
            self.__check_enthalpy(first_input.value, True)
        self.__check_pressure_drop(pressure_drop)
        result = self.with_state(
            InputHumidAir.pressure(self.pressure - pressure_drop),
            first_input,
            second_input,
        )
        if not result.humidity < self.humidity:
            raise ValueError(
                "During the wet cooling process, "
                "the absolute humidity ratio should decrease!"
            )
        return result

    def __humidification_to(
        self, first_input: InputHumidAir, second_input: InputHumidAir
    ) -> HumidAir:
        result = self.with_state(
            InputHumidAir.pressure(self.pressure), first_input, second_input
        )
        if not result.humidity > self.humidity:
            raise ValueError(
                "During the humidification process, "
                "the absolute humidity ratio should increase!"
            )
        return result

    def __check_temperature(self, temperature: float, cooling: bool):
        if cooling and temperature >= self.temperature:
            raise ValueError(
                "During the cooling process, the temperature should decrease!"
            )
        if not cooling and temperature <= self.temperature:
            raise ValueError(
                "During the heating process, the temperature should increase!"
            )

    def __check_enthalpy(self, enthalpy: float, cooling: bool):
        if cooling and enthalpy >= self.enthalpy:
            raise ValueError(
                "During the cooling process, the enthalpy should decrease!"
            )
        if not cooling and enthalpy <= self.enthalpy:
            raise ValueError(
                "During the heating process, the enthalpy should increase!"
            )

    def __check_dew_temperature(self, temperature: float):
        if temperature < self.dew_temperature:
            raise ValueError(
                "The outlet temperature after dry heat transfer "
                "should be greater than the dew point temperature!"
            )

    def __check_dew_enthalpy(self, enthalpy: float):
        if (
            enthalpy
            < self.with_state(
                InputHumidAir.pressure(self.pressure),
                InputHumidAir.temperature(self.dew_temperature),
                InputHumidAir.relative_humidity(
                    100
                    if self.units_system == UnitsSystem.SIWithCelsiusAndPercents
                    else 1
                ),
            ).enthalpy
        ):
            raise ValueError(
                "The outlet enthalpy after dry heat transfer "
                "should be greater than the dew point enthalpy!"
            )

    @staticmethod
    def __check_pressure_drop(pressure_drop: float):
        if pressure_drop < 0:
            raise ValueError("Invalid pressure drop in the heat exchanger!")
