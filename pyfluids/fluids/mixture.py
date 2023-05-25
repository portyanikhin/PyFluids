from __future__ import annotations

from CoolProp import AbstractState

from .abstract_fluid import AbstractFluid
from ..config import UnitsSystem
from ..enums import FluidsList

__all__ = ["Mixture"]


class Mixture(AbstractFluid):
    """Mass-based mixture of pure fluids."""

    __AVAILABLE_BACKEND = "HEOS"

    def __init__(self, fluids: list[FluidsList], fractions: list[float]):
        """
        Mass-based mixture of pure fluids.

        :param fluids: List of selected names of pure fluids.
        :param fractions: List of mass-based fractions
            [by default, %; you can change this using the configuration file].
        :raises ValueError: If fluids or fractions are invalid.
        """
        super().__init__()
        if len(fluids) != len(fractions):
            raise ValueError(
                "Invalid input! Fluids and fractions should be of the same length."
            )
        if not all(
            fluid.pure and fluid.coolprop_backend == self.__AVAILABLE_BACKEND
            for fluid in fluids
        ):
            raise ValueError(
                "Invalid components! All of them should be "
                f"a pure fluid with {self.__AVAILABLE_BACKEND} backend."
            )
        if not all(
            0 < self._unit_converter.convert_decimal_fraction_to_si(fraction) < 1
            for fraction in fractions
        ):
            fraction_range = (
                "(0;100) %"
                if self.units_system == UnitsSystem.SIWithCelsiusAndPercents
                else "(0;1)"
            )
            raise ValueError(
                "Invalid components mass fractions! "
                f"All of them should be in {fraction_range}."
            )
        fractions_sum = (
            100 if self.units_system == UnitsSystem.SIWithCelsiusAndPercents else 1
        )
        if abs(sum(fractions) - fractions_sum) > 1e-6:
            raise ValueError(
                "Invalid components mass fractions! "
                f"Their sum should be equal to {fractions_sum}{self._fraction_unit}."
            )
        self.__fluids, self.__fractions = fluids, fractions
        self._backend = AbstractState(
            self.__AVAILABLE_BACKEND,
            "&".join(fluid.coolprop_name for fluid in self.__fluids),
        )
        self._backend.set_mass_fractions(
            [
                self._unit_converter.convert_decimal_fraction_to_si(fraction)
                for fraction in self.__fractions
            ]
        )

    def factory(self) -> Mixture:
        return Mixture(self.__fluids, self.__fractions)

    @property
    def fluids(self) -> list[FluidsList]:
        """List of selected names of pure fluids."""
        return self.__fluids

    @property
    def fractions(self) -> list[float]:
        """
        List of mass-based fractions
        [by default, %; you can change this using the configuration file].
        """
        return self.__fractions

    def __eq__(self, other: Mixture) -> bool:
        return isinstance(other, Mixture) and hash(self) == hash(other)

    def __ne__(self, other: Mixture) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash(
            (
                "&".join(str(i.coolprop_name) for i in self.__fluids),
                "&".join(str(i) for i in self.__fractions),
                super().__hash__(),
            )
        )
