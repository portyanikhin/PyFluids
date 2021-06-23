#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict, field, make_dataclass
from math import isnan, isinf
from typing import Dict, Union

__all__ = ["FluidInterface"]


@dataclass
class FluidInterface(ABC):
    @abstractmethod
    def __post_init__(self):
        pass

    def __getattribute__(self, item):
        """Lazy class. Attributes are calculated only during access"""
        val = object.__getattribute__(self, item)
        if val is None and item != "fraction":
            try:
                val = self._attr_value(item)
            except ValueError:
                pass

        return (
            None
            if isinstance(val, (int, float)) and (isnan(val) or isinf(val))
            else val
        )

    @abstractmethod
    def update(self, *args):
        """Update fluid properties"""
        pass

    def add_props(self, new_props: Union[Dict[str, int], Dict[str, str]]):
        """Expand list of properties for calculation.

        Args:
            new_props (Union[Dict[str, int], Dict[str, str]]): dictionary with mapping
                of property names and CoolProp property keys
        """
        self._update_prop_names(new_props)
        self.__class__ = make_dataclass(
            self.__class__.__name__,
            fields=[(key, float, field(default=None)) for key in new_props],
            bases=(self.__class__,),
        )

    def to_dict(self) -> dict:
        """Convert object to dict.

        Returns:
            dict: dict based on the object
        """
        return asdict(self)

    def to_json(self, indent: int = None) -> str:
        """Convert object to JSON string.

        Args:
            indent (int, optional): number of margins during sterilization,
                default None

        Returns:
            str: JSON string based on the object
        """
        return json.dumps(self.to_dict(), default=repr, indent=indent)

    @staticmethod
    def _check_input_types(expected: type, *args):
        if not all(map(lambda x: isinstance(x.coolprop_key, expected), args)):
            raise TypeError("Wrong input type!")

    @abstractmethod
    def _attr_value(self, item: str):
        pass

    @abstractmethod
    def _update_prop_names(self, new_props: Union[Dict[str, int], Dict[str, str]]):
        pass
