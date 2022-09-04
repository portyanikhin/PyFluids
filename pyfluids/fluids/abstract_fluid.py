import json
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union

import CoolProp
from CoolProp import AbstractState
from CoolProp.CoolProp import generate_update_pair

from ..enums import Phases
from ..io import Input, OutputsValidator


class AbstractFluid(ABC):
    """Fluids base class."""

    @abstractmethod
    def __init__(self):
        """Fluids base class."""
        self._backend: Optional[AbstractState] = None
        self._inputs: List[Input] = []
        self.__compressibility: Optional[float] = None
        self.__conductivity: Optional[float] = None
        self.__critical_pressure: Optional[float] = None
        self.__critical_temperature: Optional[float] = None
        self.__density: Optional[float] = None
        self.__dynamic_viscosity: Optional[float] = None
        self.__enthalpy: Optional[float] = None
        self.__entropy: Optional[float] = None
        self.__freezing_temperature: Optional[float] = None
        self.__internal_energy: Optional[float] = None
        self.__max_pressure: Optional[float] = None
        self.__max_temperature: Optional[float] = None
        self.__min_pressure: Optional[float] = None
        self.__min_temperature: Optional[float] = None
        self.__molar_mass: Optional[float] = None
        self.__phase: Optional[Phases] = None
        self.__prandtl: Optional[float] = None
        self.__pressure: Optional[float] = None
        self.__quality: Optional[float] = None
        self.__sound_speed: Optional[float] = None
        self.__specific_heat: Optional[float] = None
        self.__surface_tension: Optional[float] = None
        self.__temperature: Optional[float] = None
        self.__triple_pressure: Optional[float] = None
        self.__triple_temperature: Optional[float] = None

    @property
    def compressibility(self) -> Optional[float]:
        """Compressibility factor [-]."""
        if self.__compressibility is None:
            self.__compressibility = self._nullable_keyed_output(CoolProp.iZ)
        return self.__compressibility

    @property
    def conductivity(self) -> Optional[float]:
        """Thermal conductivity [W/m/K]."""
        if self.__conductivity is None:
            self.__conductivity = self._nullable_keyed_output(CoolProp.iconductivity)
        return self.__conductivity

    @property
    def critical_pressure(self) -> Optional[float]:
        """Absolute pressure at the critical point [Pa]."""
        if self.__critical_pressure is None:
            self.__critical_pressure = self._nullable_keyed_output(CoolProp.iP_critical)
        return self.__critical_pressure

    @property
    def critical_temperature(self) -> Optional[float]:
        """Temperature at the critical point [°C]."""
        if self.__critical_temperature is None:
            value = self._nullable_keyed_output(CoolProp.iT_critical)
            self.__critical_temperature = value - 273.15 if value is not None else None
        return self.__critical_temperature

    @property
    def density(self) -> float:
        """Mass density [kg/m3]."""
        if self.__density is None:
            self.__density = self._keyed_output(CoolProp.iDmass)
        return self.__density

    @property
    def dynamic_viscosity(self) -> Optional[float]:
        """Dynamic viscosity [Pa*s]."""
        if self.__dynamic_viscosity is None:
            self.__dynamic_viscosity = self._nullable_keyed_output(CoolProp.iviscosity)
        return self.__dynamic_viscosity

    @property
    def enthalpy(self) -> float:
        """Mass specific enthalpy [J/kg]."""
        if self.__enthalpy is None:
            self.__enthalpy = self._keyed_output(CoolProp.iHmass)
        return self.__enthalpy

    @property
    def entropy(self) -> float:
        """Mass specific entropy [J/kg/K]."""
        if self.__entropy is None:
            self.__entropy = self._keyed_output(CoolProp.iSmass)
        return self.__entropy

    @property
    def freezing_temperature(self) -> Optional[float]:
        """Temperature at freezing point (for incompressible fluids) [°C]."""
        if self.__freezing_temperature is None:
            value = self._nullable_keyed_output(CoolProp.iT_freeze)
            self.__freezing_temperature = value - 273.15 if value is not None else None
        return self.__freezing_temperature

    @property
    def internal_energy(self) -> float:
        """Mass specific internal energy [J/kg]."""
        if self.__internal_energy is None:
            self.__internal_energy = self._keyed_output(CoolProp.iUmass)
        return self.__internal_energy

    @property
    def kinematic_viscosity(self) -> Optional[float]:
        """Kinematic viscosity [m2/s]."""
        return (
            None
            if self.dynamic_viscosity is None
            else self.dynamic_viscosity / self.density
        )

    @property
    def max_pressure(self) -> Optional[float]:
        """Maximum pressure limit [Pa]."""
        if self.__max_pressure is None:
            self.__max_pressure = self._nullable_keyed_output(CoolProp.iP_max)
        return self.__max_pressure

    @property
    def max_temperature(self) -> float:
        """Maximum temperature limit [°C]."""
        if self.__max_temperature is None:
            value = self._keyed_output(CoolProp.iT_max)
            self.__max_temperature = value - 273.15 if value is not None else None
        return self.__max_temperature

    @property
    def min_pressure(self) -> Optional[float]:
        """Minimum pressure limit [Pa]."""
        if self.__min_pressure is None:
            self.__min_pressure = self._nullable_keyed_output(CoolProp.iP_min)
        return self.__min_pressure

    @property
    def min_temperature(self) -> float:
        """Minimum temperature limit [°C]."""
        if self.__min_temperature is None:
            value = self._keyed_output(CoolProp.iT_min)
            self.__min_temperature = value - 273.15 if value is not None else None
        return self.__min_temperature

    @property
    def molar_mass(self) -> Optional[float]:
        """Molar mass [kg/mol]."""
        if self.__molar_mass is None:
            self.__molar_mass = self._nullable_keyed_output(CoolProp.imolar_mass)
        return self.__molar_mass

    @property
    def phase(self) -> Phases:
        """Phase state."""
        if self.__phase is None:
            self.__phase = Phases(self._keyed_output(CoolProp.iPhase))
        return self.__phase

    @property
    def prandtl(self) -> Optional[float]:
        """Prandtl number [-]."""
        if self.__prandtl is None:
            self.__prandtl = self._nullable_keyed_output(CoolProp.iPrandtl)
        return self.__prandtl

    @property
    def pressure(self) -> float:
        """Absolute pressure [Pa]."""
        if self.__pressure is None:
            self.__pressure = self._keyed_output(CoolProp.iP)
        return self.__pressure

    @property
    def quality(self) -> Optional[float]:
        """Mass vapor quality [%]."""
        if self.__quality is None:
            value = self._nullable_keyed_output(CoolProp.iQ)
            self.__quality = value * 1e2 if value is not None else None
        return self.__quality

    @property
    def sound_speed(self) -> Optional[float]:
        """Sound speed [m/s]."""
        if self.__sound_speed is None:
            self.__sound_speed = self._nullable_keyed_output(CoolProp.ispeed_sound)
        return self.__sound_speed

    @property
    def specific_heat(self) -> float:
        """Mass specific constant pressure specific heat [J/kg/K]."""
        if self.__specific_heat is None:
            self.__specific_heat = self._keyed_output(CoolProp.iCpmass)
        return self.__specific_heat

    @property
    def surface_tension(self) -> Optional[float]:
        """Surface tension [N/m]."""
        if self.__surface_tension is None:
            self.__surface_tension = self._nullable_keyed_output(
                CoolProp.isurface_tension
            )
        return self.__surface_tension

    @property
    def temperature(self) -> float:
        """Temperature [°C]."""
        if self.__temperature is None:
            value = self._keyed_output(CoolProp.iT)
            self.__temperature = value - 273.15 if value is not None else None
        return self.__temperature

    @property
    def triple_pressure(self) -> Optional[float]:
        """Absolute pressure at the triple point [Pa]."""
        if self.__triple_pressure is None:
            self.__triple_pressure = self._nullable_keyed_output(CoolProp.iP_triple)
        return self.__triple_pressure

    @property
    def triple_temperature(self) -> Optional[float]:
        """Temperature at the triple point [°C]."""
        if self.__triple_temperature is None:
            value = self._nullable_keyed_output(CoolProp.iT_triple)
            self.__triple_temperature = value - 273.15 if value is not None else None
        return self.__triple_temperature

    @abstractmethod
    def factory(self) -> "AbstractFluid":
        """Returns a new fluid object with no defined state."""
        raise NotImplementedError  # pragma: no cover

    def clone(self) -> "AbstractFluid":
        """Performs deep (full) copy of the fluid instance."""
        return self.with_state(*self._inputs)

    def with_state(self, first_input: Input, second_input: Input) -> "AbstractFluid":
        """
        Returns a new fluid object with defined state.

        :param first_input: First input property.
        :param second_input: Second input property.
        :return: A new fluid object with defined state.
        :raises ValueError: If input is invalid.
        """
        fluid = self.factory()
        fluid.update(first_input, second_input)
        return fluid

    def update(self, first_input: Input, second_input: Input):
        """
        Update fluid state.

        :param first_input: First input property.
        :param second_input: Second input property.
        :raises ValueError: If input is invalid.
        """
        if first_input.coolprop_key == second_input.coolprop_key:
            raise ValueError("Need to define 2 unique inputs!")
        self.reset()
        self._backend.update(
            *generate_update_pair(
                first_input.coolprop_key,
                first_input.value,
                second_input.coolprop_key,
                second_input.value,
            )
        )
        self._inputs = [first_input, second_input]

    # noinspection DuplicatedCode
    def reset(self):
        """Reset all non-trivial properties."""
        self.__compressibility = None
        self.__conductivity = None
        self.__density = None
        self.__dynamic_viscosity = None
        self.__enthalpy = None
        self.__entropy = None
        self.__internal_energy = None
        self.__phase = None
        self.__prandtl = None
        self.__pressure = None
        self.__quality = None
        self.__sound_speed = None
        self.__specific_heat = None
        self.__surface_tension = None
        self.__temperature = None

    def isentropic_compression_to_pressure(self, pressure: float) -> "AbstractFluid":
        """
        The process of isentropic compression to a given pressure.

        :param pressure: Absolute pressure [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If pressure is invalid.
        """
        if not pressure > self.pressure:
            raise ValueError(
                "Compressor outlet pressure should be higher than inlet pressure!"
            )
        return self.with_state(Input.pressure(pressure), Input.entropy(self.entropy))

    def compression_to_pressure(
        self, pressure: float, isentropic_efficiency: float
    ) -> "AbstractFluid":
        """
        The process of compression to a given pressure.

        :param pressure: Absolute pressure [Pa].
        :param isentropic_efficiency: Compressor isentropic efficiency [%].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If pressure or isentropic efficiency is invalid.
        """
        if not 0 < isentropic_efficiency < 100:
            raise ValueError("Invalid compressor isentropic efficiency!")
        return self.with_state(
            Input.pressure(pressure),
            Input.enthalpy(
                self.enthalpy
                + (
                    self.isentropic_compression_to_pressure(pressure).enthalpy
                    - self.enthalpy
                )
                / (isentropic_efficiency * 1e-2)
            ),
        )

    def isenthalpic_expansion_to_pressure(self, pressure: float) -> "AbstractFluid":
        """
        The process of isenthalpic expansion to a given pressure.

        :param pressure: Absolute pressure [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If pressure is invalid.
        """
        if not pressure < self.pressure:
            raise ValueError(
                "Expansion valve outlet pressure should be lower than inlet pressure!"
            )
        return self.with_state(Input.pressure(pressure), Input.enthalpy(self.enthalpy))

    def isentropic_expansion_to_pressure(self, pressure: float) -> "AbstractFluid":
        """
        The process of isentropic expansion to a given pressure.

        :param pressure: Absolute pressure [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If pressure is invalid.
        """
        if not pressure < self.pressure:
            raise ValueError(
                "Expander outlet pressure should be lower than inlet pressure!"
            )
        return self.with_state(Input.pressure(pressure), Input.entropy(self.entropy))

    def expansion_to_pressure(
        self, pressure: float, isentropic_efficiency: float
    ) -> "AbstractFluid":
        """
        The process of expansion to a given pressure.

        :param pressure: Absolute pressure [Pa].
        :param isentropic_efficiency: Expander isentropic efficiency [%].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If pressure or isentropic efficiency is invalid.
        """
        if not 0 < isentropic_efficiency < 100:
            raise ValueError("Invalid expander isentropic efficiency!")
        return self.with_state(
            Input.pressure(pressure),
            Input.enthalpy(
                self.enthalpy
                - (
                    self.enthalpy
                    - self.isentropic_expansion_to_pressure(pressure).enthalpy
                )
                * (isentropic_efficiency * 1e-2)
            ),
        )

    def cooling_to_temperature(
        self, temperature: float, pressure_drop: float = 0
    ) -> "AbstractFluid":
        """
        The process of cooling to a given temperature.

        :param temperature: Temperature [°C].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If temperature or pressure drop is invalid.
        """
        if not temperature < self.temperature:
            raise ValueError(
                "During the cooling process, the temperature should decrease!"
            )
        return self.__heat_transfer_to_temperature(temperature, pressure_drop)

    def cooling_to_enthalpy(
        self, enthalpy: float, pressure_drop: float = 0
    ) -> "AbstractFluid":
        """
        The process of cooling to a given enthalpy.

        :param enthalpy: Enthalpy [J/kg].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If enthalpy or pressure drop is invalid.
        """
        if not enthalpy < self.enthalpy:
            raise ValueError(
                "During the cooling process, the enthalpy should decrease!"
            )
        return self.__heat_transfer_to_enthalpy(enthalpy, pressure_drop)

    def heating_to_temperature(
        self, temperature: float, pressure_drop: float = 0
    ) -> "AbstractFluid":
        """
        The process of heating to a given temperature.

        :param temperature: Temperature [°C].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If temperature or pressure drop is invalid.
        """
        if not temperature > self.temperature:
            raise ValueError(
                "During the heating process, the temperature should increase!"
            )
        return self.__heat_transfer_to_temperature(temperature, pressure_drop)

    def heating_to_enthalpy(
        self, enthalpy: float, pressure_drop: float = 0
    ) -> "AbstractFluid":
        """
        The process of heating to a given enthalpy.

        :param enthalpy: Enthalpy [J/kg].
        :param pressure_drop: Pressure drop in the heat exchanger (optional) [Pa].
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If enthalpy or pressure drop is invalid.
        """
        if not enthalpy > self.enthalpy:
            raise ValueError(
                "During the heating process, the enthalpy should increase!"
            )
        return self.__heat_transfer_to_enthalpy(enthalpy, pressure_drop)

    def bubble_point_at_pressure(self, pressure: float) -> "AbstractFluid":
        """
        Bubble point at a given pressure.

        :param pressure: Absolute pressure [Pa].
        :return: Bubble point at a given pressure.
        """
        return self.with_state(Input.pressure(pressure), Input.quality(0))

    def bubble_point_at_temperature(self, temperature: float) -> "AbstractFluid":
        """
        Bubble point at a given temperature.

        :param temperature: Temperature [°C].
        :return: TBubble point at a given temperature.
        """
        return self.with_state(Input.temperature(temperature), Input.quality(0))

    def dew_point_at_pressure(self, pressure: float) -> "AbstractFluid":
        """
        Dew point at a given pressure.

        :param pressure: Absolute pressure [Pa].
        :return: Dew point at a given pressure.
        """
        return self.with_state(Input.pressure(pressure), Input.quality(100))

    def dew_point_at_temperature(self, temperature: float) -> "AbstractFluid":
        """
        Dew point at a given temperature.

        :param temperature: Temperature [°C].
        :return: Dew point at a given temperature.
        """
        return self.with_state(Input.temperature(temperature), Input.quality(100))

    def two_phase_point_at_pressure(
        self, pressure: float, quality: float
    ) -> "AbstractFluid":
        """
        Two phase point at a given pressure.

        :param pressure: Absolute pressure [Pa].
        :param quality: Vapor quality [%].
        :return: Two phase point at a given pressure.
        """
        return self.with_state(Input.pressure(pressure), Input.quality(quality))

    def mixing(
        self,
        first_specific_mass_flow: float,
        first: "AbstractFluid",
        second_specific_mass_flow: float,
        second: "AbstractFluid",
    ) -> "AbstractFluid":
        """
        The mixing process.

        :param first_specific_mass_flow: Specific mass flow rate of the fluid
            at the first state [-].
        :param first: Fluid at the first state.
        :param second_specific_mass_flow: Specific mass flow rate of the fluid
            at the second state [-].
        :param second: Fluid at the second state.
        :return: The state of the fluid at the end of the process.
        :raises ValueError: If the mixing process is not possible.
        """
        if not self._is_valid_fluids_for_mixing(first, second):
            raise ValueError("The mixing process is possible only for the same fluids!")
        if first.pressure != second.pressure:
            raise ValueError(
                "The mixing process is possible only for flows with the same pressure!"
            )
        return self.with_state(
            Input.pressure(first.pressure),
            Input.enthalpy(
                (
                    first_specific_mass_flow * first.enthalpy
                    + second_specific_mass_flow * second.enthalpy
                )
                / (first_specific_mass_flow + second_specific_mass_flow)
            ),
        )

    def as_json(self, indented: bool = True) -> str:
        """
        Converts the fluid instance to a JSON string.

        :param indented: True if indented.
        :return: The fluid instance as a JSON string.
        """
        return json.dumps(
            self.as_dict(), indent=4 if indented else None, default=str, sort_keys=False
        )

    def as_dict(self) -> Dict[str, Union[str, float, None]]:
        """Converts the fluid instance to a dict."""
        dictionary = {
            self.__select(key): getattr(self, self.__select(key))
            for key, value in vars(self).items()
            if not self.__select(key).startswith("_")
        }
        return {
            key: dictionary[key]
            for key in list(dictionary.keys())[-2:] + list(dictionary.keys())[:-2]
        }

    def _nullable_keyed_output(self, coolprop_key: int) -> Optional[float]:
        try:
            value = self._keyed_output(coolprop_key)
            return (
                None if coolprop_key == CoolProp.iQ and (not 0 <= value <= 1) else value
            )
        except ValueError:
            return None

    def _keyed_output(self, coolprop_key: int) -> float:
        cached_input = next(
            (i for i in self._inputs if i.coolprop_key == coolprop_key), None
        )
        value = (
            cached_input.value
            if cached_input is not None
            else self._backend.keyed_output(coolprop_key)
        )
        OutputsValidator(value).validate()
        return value

    @abstractmethod
    def _is_valid_fluids_for_mixing(
        self, first: "AbstractFluid", second: "AbstractFluid"
    ) -> bool:
        """Returns True if the fluids can be mixed."""
        raise NotImplementedError  # pragma: no cover

    def __hash__(self) -> int:
        return hash(
            (
                self.compressibility,
                self.conductivity,
                self.critical_pressure,
                self.critical_temperature,
                self.density,
                self.dynamic_viscosity,
                self.enthalpy,
                self.entropy,
                self.freezing_temperature,
                self.internal_energy,
                self.max_pressure,
                self.max_temperature,
                self.min_pressure,
                self.min_temperature,
                self.molar_mass,
                self.phase,
                self.prandtl,
                self.pressure,
                self.quality,
                self.sound_speed,
                self.specific_heat,
                self.surface_tension,
                self.temperature,
                self.triple_pressure,
                self.triple_temperature,
            )
        )

    def __heat_transfer_to_temperature(
        self, temperature: float, pressure_drop: float
    ) -> "AbstractFluid":
        self.__check_pressure_drop(pressure_drop)
        return self.with_state(
            Input.pressure(self.pressure - pressure_drop),
            Input.temperature(temperature),
        )

    def __heat_transfer_to_enthalpy(
        self, enthalpy: float, pressure_drop: float
    ) -> "AbstractFluid":
        self.__check_pressure_drop(pressure_drop)
        return self.with_state(
            Input.pressure(self.pressure - pressure_drop),
            Input.enthalpy(enthalpy),
        )

    @staticmethod
    def __check_pressure_drop(pressure_drop: float):
        if pressure_drop < 0:
            raise ValueError("Invalid pressure drop in the heat exchanger!")

    @staticmethod
    def __select(key: str) -> str:
        return key.split("__")[-1]
