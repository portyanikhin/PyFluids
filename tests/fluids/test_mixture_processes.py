import pytest

from pyfluids import Mixture, FluidsList, Input


class TestMixtureProcesses:
    mixture: Mixture = Mixture(
        [FluidsList.Argon, FluidsList.IsoButane], [50, 50]
    ).with_state(Input.pressure(101325), Input.temperature(20))
    temperature_delta: float = 10
    pressure_drop: float = 5e4

    @pytest.mark.parametrize(
        "temperature_delta, pressure_drop, message",
        [
            (5, 0, "During the cooling process, the temperature should decrease!"),
            (-5, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_cooling_to_temperature_wrong_input_raises_value_error(
        self, temperature_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.mixture.cooling_to_temperature(
                self.mixture.temperature + temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_cooling_to_temperature(self):
        assert self.mixture.cooling_to_temperature(
            self.mixture.temperature - self.temperature_delta, self.pressure_drop
        ) == self.mixture.with_state(
            Input.pressure(self.mixture.pressure - self.pressure_drop),
            Input.temperature(self.mixture.temperature - self.temperature_delta),
        )

    @pytest.mark.parametrize(
        "temperature_delta, pressure_drop, message",
        [
            (5, 0, "During the heating process, the temperature should increase!"),
            (-5, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_temperature_wrong_input_raises_value_error(
        self, temperature_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.mixture.heating_to_temperature(
                self.mixture.temperature - temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_temperature(self):
        assert self.mixture.heating_to_temperature(
            self.mixture.temperature + self.temperature_delta, self.pressure_drop
        ) == self.mixture.with_state(
            Input.pressure(self.mixture.pressure - self.pressure_drop),
            Input.temperature(self.mixture.temperature + self.temperature_delta),
        )
