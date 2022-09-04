from abc import ABC, abstractmethod
from typing import Union


class AbstractInput(ABC):
    """Abstract CoolProp keyed input."""

    @abstractmethod
    def __init__(self, coolprop_key: Union[int, str], value: float):
        """
        Abstract CoolProp keyed input.

        :param coolprop_key: CoolProp internal key.
        :param value: Input value in SI units.
        """
        self.__coolprop_key, self.__value = coolprop_key, value

    @property
    def coolprop_key(self) -> Union[int, str]:
        """CoolProp internal key."""
        return self.__coolprop_key

    @property
    def value(self) -> float:
        """Input value in SI units."""
        return self.__value

    def __eq__(self, other: "AbstractInput") -> bool:
        return isinstance(other, AbstractInput) and hash(self) == hash(other)

    def __ne__(self, other: "AbstractInput") -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((self.coolprop_key, self.value))
