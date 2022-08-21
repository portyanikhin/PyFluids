from abc import ABC, abstractmethod
from typing import Union


class AbstractInput(ABC):
    """Abstract CoolProp keyed input."""

    @abstractmethod
    def __init__(self, coolprop_key: Union[int, str], value: float):
        """
        Abstract CoolProp keyed input.

        Args:
            coolprop_key (Union[int, str]): CoolProp internal key.
            value (float): Input value in SI units.
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
