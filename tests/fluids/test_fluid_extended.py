from typing import Optional

import CoolProp

from pyfluids import Fluid, FluidsList, Input


class FluidExtended(Fluid):
    """An example of how to add new properties to a Fluid."""

    def __init__(self, name: FluidsList, fraction: float = None):
        super().__init__(name, fraction)
        self.__molar_density: Optional[float] = None
        self.__ozone_depletion_potential: Optional[float] = None
        self.__specific_heat_const_volume: Optional[float] = None

    def factory(self) -> "FluidExtended":
        return FluidExtended(self.name, self.fraction)

    def reset(self):
        super().reset()
        self.__molar_density = None
        self.__ozone_depletion_potential = None
        self.__specific_heat_const_volume = None

    @property
    def specific_heat_const_volume(self) -> float:
        """Mass specific constant volume specific heat [J/kg/K]."""
        if self.__specific_heat_const_volume is None:
            self.__specific_heat_const_volume = self._keyed_output(CoolProp.iCvmass)
        return self.__specific_heat_const_volume

    @property
    def molar_density(self) -> Optional[float]:
        """Molar density [mol/m3]."""
        if self.__molar_density is None:
            self.__molar_density = self._nullable_keyed_output(CoolProp.iDmolar)
        return self.__molar_density

    @property
    def ozone_depletion_potential(self) -> Optional[float]:
        """Ozone depletion potential (ODP) [-]."""
        if self.__ozone_depletion_potential is None:
            self.__ozone_depletion_potential = self._nullable_keyed_output(
                CoolProp.iODP
            )
        return self.__ozone_depletion_potential


class TestFluidExtended:
    fluid = FluidExtended(FluidsList.Water).with_state(
        Input.pressure(101325), Input.temperature(150)
    )

    def test_specific_heat_const_volume(self):
        assert self.fluid.specific_heat_const_volume == 1496.5437531342086

    def test_molar_density(self):
        assert self.fluid.molar_density == 29.045175781507989

    def test_ozone_depletion_potential(self):
        assert self.fluid.ozone_depletion_potential is None
