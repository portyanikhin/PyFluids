#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from abc import abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Union

import CoolProp
from CoolProp.CoolProp import AbstractState
from CoolProp.CoolProp import generate_update_pair

from pyfluids.fluid_props.fluid_lists import *
from pyfluids.fluid_props.inputs import *
from pyfluids.fluid_props.phases import *
from pyfluids.interfaces import *

__all__ = ["Fluid", "Mixture"]

# PyCoolProp and CoolProp parameters name mapping
prop_names = {
    "compressibility": CoolProp.iZ,
    "conductivity": CoolProp.iconductivity,
    "critical_pressure": CoolProp.iP_critical,
    "critical_temperature": CoolProp.iT_critical,
    "density": CoolProp.iDmass,
    "dynamic_viscosity": CoolProp.iviscosity,
    "enthalpy": CoolProp.iHmass,
    "entropy": CoolProp.iSmass,
    "freezing_temperature": CoolProp.iT_freeze,
    "internal_energy": CoolProp.iUmass,
    "max_pressure": CoolProp.iP_max,
    "max_temperature": CoolProp.iT_max,
    "min_pressure": CoolProp.iP_min,
    "min_temperature": CoolProp.iT_min,
    "molar_mass": CoolProp.imolar_mass,
    "phase": CoolProp.iPhase,
    "prandtl": CoolProp.iPrandtl,
    "pressure": CoolProp.iP,
    "quality": CoolProp.iQ,
    "sound_speed": CoolProp.ispeed_sound,
    "specific_heat": CoolProp.iCpmass,
    "surface_tension": CoolProp.isurface_tension,
    "temperature": CoolProp.iT,
    "triple_pressure": CoolProp.iP_triple,
    "triple_temperature": CoolProp.iT_triple,
}


@dataclass
class SingleComponent:
    name: Union[PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF]
    fraction: float = None


@dataclass
class MultiComponent:
    components: List[PureFluids]
    fractions: List[float]


@dataclass
class AbstractFluid(FluidInterface):
    compressibility: float = None
    conductivity: float = None
    critical_pressure: float = None
    critical_temperature: float = None
    density: float = None
    dynamic_viscosity: float = None
    enthalpy: float = None
    entropy: float = None
    freezing_temperature: float = None
    internal_energy: float = None
    max_pressure: float = None
    max_temperature: float = None
    min_pressure: float = None
    min_temperature: float = None
    molar_mass: float = None
    phase: Phase = None
    prandtl: float = None
    pressure: float = None
    quality: float = None
    sound_speed: float = None
    specific_heat: float = None
    surface_tension: float = None
    temperature: float = None
    triple_pressure: float = None
    triple_temperature: float = None

    @abstractmethod
    def __post_init__(self):
        self._backend = None

    def update(self, input1: ConcreteInput, input2: ConcreteInput):
        """Update fluid properties with two inputs.

        Args:
            input1 (ConcreteInput): first input property
            input2 (ConcreteInput): second input property

        Examples:
            >>> water = Fluid(PureFluids.Water)
            >>> water.update(
            ...     Input.Pressure.with_value(101325),
            ...     Input.Temperature.with_value(293.15),
            ... )
            >>> water.specific_heat
            ... 4184.050924523541
        """
        self._check_input_types(int, input1, input2)
        self._backend.update(
            *generate_update_pair(
                input1.coolprop_key, input1.value, input2.coolprop_key, input2.value
            )
        )

    def add_props(self, new_props: Dict[str, int]):
        """Expand list of properties for calculation.

        Args:
            new_props (Dict[str, int]): dictionary with mapping of property names
                and CoolProp property keys

        Examples:
            >>> refrigerant = Fluid(PureFluids.R32)
            >>> refrigerant.add_props(
            ...     {
            ...         "gwp20": CoolProp.iGWP20,
            ...         "gwp100": CoolProp.iGWP100,
            ...         "gwp500": CoolProp.iGWP500,
            ...     }
            ... )
            >>> refrigerant.gwp20
            ... 2330.0
            >>> refrigerant.gwp100
            ... 675.0
            >>> refrigerant.gwp500
            ... 205.0
        """
        super().add_props(new_props)

    def _attr_value(self, item: str):
        val = self._backend.keyed_output(prop_names[item])
        val = None if (item == "quality") and (not 0 <= val <= 1) else val
        return Phase(val) if item == "phase" else val

    def _update_prop_names(self, new_props: Dict[str, int]):
        prop_names.update(new_props)


@dataclass
class Fluid(AbstractFluid, SingleComponent):
    # noinspection PyUnresolvedReferences
    """Thermophysical properties of pure and pseudo pure fluids,
    incompressible pure fluids and incompressible mixtures.

    Args:
        name (Union[
            PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF
        ]): substance from fluids list
        fraction (float, optional): mass or volume (if name is IncompMixturesVF)
            fraction (from 0 to 1) [-],
            by default None

    Attributes:
        name (Union[
            PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF
        ]): substance from fluids list
        fraction (float): mass or volume (if name is IncompMixturesVF)
            fraction (from 0 to 1) [-]
        compressibility (float): compressibility factor [-]
        conductivity (float): thermal conductivity [W/m/K]
        critical_pressure (float): absolute pressure at the critical point [Pa]
        critical_temperature (float): absolute temperature at the critical point [K]
        density (float): mass density [kg/m3]
        dynamic_viscosity (float): dynamic viscosity [Pa*s]
        enthalpy (float): mass specific enthalpy [J/kg]
        entropy (float): mass specific entropy [J/kg/K]
        freezing_temperature (float): temperature at freezing point
            (for incompressible fluids) [K]
        internal_energy (float): mass specific internal energy [J/kg]
        max_pressure (float): maximum pressure limit [Pa]
        max_temperature (float): maximum temperature limit [K]
        min_pressure (float): minimum pressure limit [Pa]
        min_temperature (float): minimum temperature limit [K]
        molar_mass (float): molar mass [kg/mol]
        phase (Phase): phase
        prandtl (float): Prandtl number [-]
        pressure (float): absolute pressure [Pa]
        quality (float): mass vapor quality [-]
        sound_speed (float): sound speed [m/s]
        specific_heat (float): mass specific constant pressure specific heat [J/kg/K]
        surface_tension (float): surface tension [N/m]
        temperature (float): absolute temperature [K]
        triple_pressure (float): absolute pressure at the triple point [Pa]
        triple_temperature (float): absolute temperature at the triple point [K]

    Examples:
        >>> pure_fluid = Fluid(PureFluids.Water)
        >>> incomp_pure_fluid = Fluid(IncompPureFluids.AS10)
        >>> incomp_mixture_mf = Fluid(IncompMixturesMF.MPG, 0.4)
        >>> incomp_mixture_vf = Fluid(IncompMixturesVF.APG, 0.4)
    """

    def __post_init__(self):
        backend_name = "HEOS" if isinstance(self.name, PureFluids) else "INCOMP"
        self._backend = AbstractState(backend_name, self.name.coolprop_name)
        if isinstance(self.name, (PureFluids, IncompPureFluids)):
            self.fraction = 1
        elif self.fraction is None:
            raise ValueError("Need to define fraction!")
        elif not 0 <= self.fraction <= 1:
            raise ValueError(
                "Invalid fraction value! It should be in [0;1]. "
                f"Entered value = {self.fraction}"
            )
        elif isinstance(self.name, IncompMixturesMF):
            self._backend.set_mass_fractions([self.fraction])
        elif isinstance(self.name, IncompMixturesVF):
            self._backend.set_volu_fractions([self.fraction])


@dataclass
class Mixture(AbstractFluid, MultiComponent):
    # noinspection PyUnresolvedReferences
    """Thermophysical properties of mixtures.

    Args:
        components (List[PureFluids]): pure or pseudo pure substances
        fractions (List[float]): mass fractions of the components [-]

    Attributes:
        components (List[PureFluids]): pure or pseudo pure substances
        fractions (List[float]): mass fractions of the components [-]
        compressibility (float): compressibility factor [-]
        conductivity (float): thermal conductivity [W/m/K]
        critical_pressure (float): absolute pressure at the critical point [Pa]
        critical_temperature (float): absolute temperature at the critical point [K]
        density (float): mass density [kg/m3]
        dynamic_viscosity (float): dynamic viscosity [Pa*s]
        enthalpy (float): mass specific enthalpy [J/kg]
        entropy (float): mass specific entropy [J/kg/K]
        freezing_temperature (float): temperature at freezing point
            (for incompressible fluids) [K]
        internal_energy (float): mass specific internal energy [J/kg]
        max_pressure (float): maximum pressure limit [Pa]
        max_temperature (float): maximum temperature limit [K]
        min_pressure (float): minimum pressure limit [Pa]
        min_temperature (float): minimum temperature limit [K]
        molar_mass (float): molar mass [kg/mol]
        phase (Phase): phase
        prandtl (float): Prandtl number [-]
        pressure (float): absolute pressure [Pa]
        quality (float): mass vapor quality [-]
        sound_speed (float): sound speed [m/s]
        specific_heat (float): mass specific constant pressure specific heat [J/kg/K]
        surface_tension (float): surface tension [N/m]
        temperature (float): absolute temperature [K]
        triple_pressure (float): absolute pressure at the triple point [Pa]
        triple_temperature (float): absolute temperature at the triple point [K]

    Examples:
        >>> mixture = Mixture([PureFluids.Water, PureFluids.Ethanol], [0.6, 0.4])
    """

    def __post_init__(self):
        if len(self.components) != len(self.fractions):
            raise ValueError("Invalid input!")
        if not all(map(lambda x: x > 0, self.fractions)):
            raise ValueError(
                "Invalid component mass fractions! All of them should be > 0."
            )
        if sum(self.fractions) != 1:
            raise ValueError(
                "Invalid component mass fractions! Their sum should be equal to 1."
            )
        mixture_name = "&".join(name.coolprop_name for name in self.components)
        self._backend = AbstractState("HEOS", mixture_name)
        self._backend.set_mass_fractions(self.fractions)
