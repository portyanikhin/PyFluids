#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from dataclasses import dataclass
from typing import Dict

from CoolProp.HumidAirProp import HAPropsSI

from pyfluids.humid_air_props.humid_air_inputs import HAInput
from pyfluids.interfaces import *

__all__ = ["HumidAir"]

# PyCoolProp and CoolProp parameters name mapping
prop_names = {
    "compressibility": "Z",
    "conductivity": "K",
    "density": "Vha",
    "dew_temperature": "D",
    "dynamic_viscosity": "M",
    "enthalpy": "Hha",
    "entropy": "Sha",
    "humidity": "W",
    "partial_pressure": "P_w",
    "pressure": "P",
    "relative_humidity": "R",
    "specific_heat": "Cha",
    "temperature": "T",
    "wb_temperature": "B",
}


@dataclass
class HumidAir(FluidInterface):
    # noinspection PyUnresolvedReferences
    """Humid air.

    Attributes:
        compressibility (float): compressibility factor [-]
        conductivity (float): thermal conductivity [W/m/K]
        density (float): mass density per humid air unit [kg/m3]
        dew_temperature (float): dew-point absolute temperature [K]
        dynamic_viscosity (float): dynamic viscosity [Pa*s]
        enthalpy (float): mass specific enthalpy per humid air [J/kg]
        entropy (float): mass specific entropy per humid air [J/kg/K]
        humidity (float): absolute humidity ratio [kg/kg d.a.]
        partial_pressure (float): partial pressure of water vapor [Pa]
        pressure (float): absolute pressure [Pa]
        relative_humidity (float): relative humidity ratio (from 0 to 1) [-]
        specific_heat (float): mass specific constant pressure specific heat
            per humid air [J/kg/K]
        temperature (float): absolute dry-bulb temperature [K]
        wb_temperature (float): absolute wet-bulb temperature [K]
    """

    compressibility: float = None
    conductivity: float = None
    density: float = None
    dew_temperature: float = None
    dynamic_viscosity: float = None
    enthalpy: float = None
    entropy: float = None
    humidity: float = None
    partial_pressure: float = None
    pressure: float = None
    relative_humidity: float = None
    specific_heat: float = None
    temperature: float = None
    wb_temperature: float = None

    def __post_init__(self):
        self.inputs = None

    def update(
        self, input1: ConcreteInput, input2: ConcreteInput, input3: ConcreteInput
    ):
        """Update humid air properties with three inputs.

        Args:
            input1 (ConcreteInput): first input property
            input2 (ConcreteInput): second input property
            input3 (ConcreteInput): third input property

        Examples:
            >>> humid_air = HumidAir()
            >>> humid_air.update(
            ...     HAInput.Pressure.with_value(101325),
            ...     HAInput.Temperature.with_value(293.15),
            ...     HAInput.RelativeHumidity.with_value(0.5),
            ... )
            >>> humid_air.humidity
            ... 0.007293697701992549
        """
        self._check_input_types(str, input1, input2, input3)
        # noinspection PyAttributeOutsideInit
        self.inputs = [input1, input2, input3]

    def add_props(self, new_props: Dict[str, str]):
        """Expand list of properties for calculation.

        Args:
            new_props (Dict[str, str]): dictionary with mapping of property names
                and CoolProp property keys

        Examples:
            >>> humid_air = HumidAir()
            >>> humid_air.update(
            ...     HAInput.Pressure.with_value(101325),
            ...     HAInput.Temperature.with_value(293.15),
            ...     HAInput.RelativeHumidity.with_value(0.5),
            ... )
            >>> humid_air.add_props(
            ...     {
            ...         "entropy_per_dry_air": "S",
            ...         "water_mole_fraction": "psi_w",
            ...     }
            ... )
            >>> humid_air.entropy_per_dry_air
            ... 139.97016819060187
            >>> humid_air.water_mole_fraction
            ... 0.011591305062179829
        """
        super().add_props(new_props)

    def _attr_value(self, item: str):
        val = HAPropsSI(
            prop_names[item],
            self.inputs[0].coolprop_key,
            self.inputs[0].value,
            self.inputs[1].coolprop_key,
            self.inputs[1].value,
            self.inputs[2].coolprop_key,
            self.inputs[2].value,
        )
        return 1 / val if (item == "density") else val

    def _update_prop_names(self, new_props: Dict[str, int]):
        prop_names.update(new_props)
