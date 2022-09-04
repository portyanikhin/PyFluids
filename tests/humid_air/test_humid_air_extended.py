from typing import Optional

from pyfluids import HumidAir, InputHumidAir


class HumidAirExtended(HumidAir):
    """An example of how to add new properties to a HumidAir."""

    def __init__(self):
        super().__init__()
        self.__specific_heat_const_volume: Optional[float] = None

    @property
    def specific_heat_const_volume(self) -> float:
        """Mass specific constant volume specific heat [J/kg/K]."""
        if self.__specific_heat_const_volume is None:
            self.__specific_heat_const_volume = self._keyed_output("CVha")
        return self.__specific_heat_const_volume

    def factory(self) -> "HumidAirExtended":
        return HumidAirExtended()

    def reset(self):
        super().reset()
        self.__specific_heat_const_volume = None


class TestHumidAirExtended:
    humid_air = HumidAirExtended().with_state(
        InputHumidAir.pressure(101325),
        InputHumidAir.temperature(20),
        InputHumidAir.relative_humidity(50),
    )

    def test_specific_heat_const_volume(self):
        assert self.humid_air.specific_heat_const_volume == 722.68718970632506
