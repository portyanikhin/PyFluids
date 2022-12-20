from CoolProp import AbstractState

from .abstract_fluid import AbstractFluid
from ..enums import FluidsList, Mix

__all__ = ["Fluid"]


class Fluid(AbstractFluid):
    """Pure/pseudo-pure fluid or binary mixture."""

    def __init__(self, name: FluidsList, fraction: float = None):
        """
        Pure/pseudo-pure fluid or binary mixture.

        :param name: Selected fluid name.
        :param fraction: Mass-based or volume-based fraction for binary mixtures [%].
        :raises ValueError: If fraction is invalid.
        """
        if fraction is not None and (
            not name.fraction_min <= fraction <= name.fraction_max
        ):
            raise ValueError(
                f"Invalid fraction value! It should be in "
                f"[{'{0:g}'.format(name.fraction_min)};"
                f"{'{0:g}'.format(name.fraction_max)}] %. "
                f"Entered value = {'{0:g}'.format(fraction)} %."
            )
        if fraction is None and not name.pure:
            raise ValueError("Need to define fraction!")
        super().__init__()
        self.__name = name
        self.__fraction = 100 if self.__name.pure else fraction
        self._backend = AbstractState(
            self.__name.coolprop_backend, self.__name.coolprop_name
        )
        if not self.__name.pure:
            self.__set_fraction()

    def factory(self) -> "Fluid":
        return Fluid(self.__name, self.__fraction)

    @property
    def name(self) -> FluidsList:
        """Selected fluid name."""
        return self.__name

    @property
    def fraction(self) -> float:
        """Mass-based or volume-based fraction for binary mixtures [%]."""
        return self.__fraction

    def mixing(
        self,
        first_specific_mass_flow: float,
        first: AbstractFluid,
        second_specific_mass_flow: float,
        second: AbstractFluid,
    ) -> AbstractFluid:
        if not self.__is_valid_fluids_for_mixing(first, second):
            raise ValueError("The mixing process is possible only for the same fluids!")
        return super().mixing(
            first_specific_mass_flow, first, second_specific_mass_flow, second
        )

    def __set_fraction(self):
        if self.__name.mix_type == Mix.Mass:
            self._backend.set_mass_fractions([self.__fraction * 1e-2])
        else:
            self._backend.set_volu_fractions([self.__fraction * 1e-2])

    def __is_valid_fluids_for_mixing(
        self, first: AbstractFluid, second: AbstractFluid
    ) -> bool:
        return (
            isinstance(first, Fluid)
            and isinstance(second, Fluid)
            and first.name == self.__name
            and first.name == second.name
            and first.fraction == self.__fraction
            and first.fraction == second.fraction
        )

    def __eq__(self, other: "Fluid") -> bool:
        return isinstance(other, Fluid) and hash(self) == hash(other)

    def __ne__(self, other: "Fluid") -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((super().__hash__(), self.__name, self.__fraction))
