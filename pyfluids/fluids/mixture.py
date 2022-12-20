from typing import List

from CoolProp import AbstractState

from .abstract_fluid import AbstractFluid
from ..enums import FluidsList

__all__ = ["Mixture"]


class Mixture(AbstractFluid):
    """Mass-based mixture of pure fluids."""

    def __init__(self, fluids: List[FluidsList], fractions: List[float]):
        """
        Mass-based mixture of pure fluids.

        :param fluids: List of selected names of pure fluids.
        :param fractions: List of mass-based fractions [%].
        :raises ValueError: If fluids or fractions are invalid.
        """
        if len(fluids) != len(fractions):
            raise ValueError(
                "Invalid input! Fluids and fractions should be of the same length."
            )
        if not all(fluid.pure and fluid.coolprop_backend == "HEOS" for fluid in fluids):
            raise ValueError(
                "Invalid components! All of them should be "
                "a pure fluid with HEOS backend."
            )
        if not all(0 < fraction < 100 for fraction in fractions):
            raise ValueError(
                "Invalid component mass fractions! All of them should be in (0;100) %."
            )
        if abs(sum(fractions) - 100) > 1e-6:
            raise ValueError(
                "Invalid component mass fractions! Their sum should be equal to 100 %."
            )
        super().__init__()
        self.__fluids, self.__fractions = fluids, fractions
        self._backend = AbstractState(
            "HEOS", "&".join(fluid.coolprop_name for fluid in self.__fluids)
        )
        self._backend.set_mass_fractions(self.__fractions)

    def factory(self) -> "Mixture":
        return Mixture(self.__fluids, self.__fractions)

    @property
    def fluids(self) -> List[FluidsList]:
        """List of selected pure fluids."""
        return self.__fluids

    @property
    def fractions(self) -> List[float]:
        """List of mass-based fractions [%]."""
        return self.__fractions

    def __eq__(self, other: "Mixture") -> bool:
        return isinstance(other, Mixture) and hash(self) == hash(other)

    def __ne__(self, other: "Mixture") -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((super().__hash__(), *self.__fluids, *self.__fractions))
