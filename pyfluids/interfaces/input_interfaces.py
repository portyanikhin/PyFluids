#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from dataclasses import dataclass
from enum import Enum
from typing import Union

__all__ = ["ConcreteInput", "InputInterface"]


@dataclass
class ConcreteInput:
    coolprop_key: Union[int, str]
    value: float


class InputInterface(Enum):
    def __init__(self, coolprop_key: Union[int, str]):
        self.__coolprop_key = coolprop_key
        self.__value = None

    def with_value(self, value: float) -> ConcreteInput:
        """Set value for the property.

        Args:
            value (float): value of the property [SI units]

        Returns:
            ConcreteInput: new input instance with coolprop_key and value
        """
        return ConcreteInput(self.__coolprop_key, value)

    @property
    def coolprop_key(self) -> Union[int, str]:
        """CoolProp key for the property"""
        return self.__coolprop_key

    @property
    def value(self) -> float:
        """Value of the property [SI units]"""
        return self.__value
