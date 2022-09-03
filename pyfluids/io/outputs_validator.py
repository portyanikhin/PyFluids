from math import isinf, isnan

__all__ = ["OutputsValidator"]


class OutputsValidator:
    """CoolProp outputs validator."""

    def __init__(self, value: float):
        """
        CoolProp outputs validator.

        :param value: CoolProp output.
        """
        self.__value = value

    def validate(self):
        """Validates the CoolProp output."""
        if isinf(self.__value) or isnan(self.__value):
            raise ValueError("Invalid or not defined state!")
