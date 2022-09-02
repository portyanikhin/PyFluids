import pytest

from pyfluids import Fluid, FluidsList, Input


class TestFluidProcesses:
    water = Fluid(FluidsList.Water).with_state(
        Input.pressure(101325), Input.temperature(150)
    )

    high_pressure = 2 * water.pressure
    low_pressure = 0.5 * water.pressure
    isentropic_efficiency = 80
    temperature_delta = 10
    enthalpy_delta = 5e4
    pressure_drop = 5e4

    def test_isentropic_compression_to_pressure(self):
        assert self.water.isentropic_compression_to_pressure(
            self.high_pressure
        ) == self.water.with_state(
            Input.pressure(self.high_pressure), Input.entropy(self.water.entropy)
        )

    def test_isentropic_compression_to_pressure_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.water.isentropic_compression_to_pressure(self.low_pressure)
        assert (
            "Compressor outlet pressure should be higher than inlet pressure!"
            in str(e.value)
        )

    def test_compression_to_pressure(self):
        assert self.water.compression_to_pressure(
            self.high_pressure, self.isentropic_efficiency
        ) == self.water.with_state(
            Input.pressure(self.high_pressure),
            Input.enthalpy(
                self.water.enthalpy
                + (
                    self.water.isentropic_compression_to_pressure(
                        self.high_pressure
                    ).enthalpy
                    - self.water.enthalpy
                )
                / (self.isentropic_efficiency * 1e-2)
            ),
        )

    @pytest.mark.parametrize(
        "pressure_ratio, isentropic_efficiency, message",
        [
            (
                0.5,
                80,
                "Compressor outlet pressure should be higher than inlet pressure!",
            ),
            (2, 0, "Invalid compressor isentropic efficiency!"),
            (2, 100, "Invalid compressor isentropic efficiency!"),
        ],
    )
    def test_compression_to_pressure_wrong_input(
        self, pressure_ratio: float, isentropic_efficiency: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.compression_to_pressure(
                pressure_ratio * self.water.pressure, isentropic_efficiency
            )
        assert message in str(e.value)

    def test_isenthalpic_expansion_to_pressure(self):
        assert self.water.isenthalpic_expansion_to_pressure(
            self.low_pressure
        ) == self.water.with_state(
            Input.pressure(self.low_pressure), Input.enthalpy(self.water.enthalpy)
        )

    def test_isenthalpic_expansion_to_pressure_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.water.isenthalpic_expansion_to_pressure(self.high_pressure)
        assert (
            "Expansion valve outlet pressure should be lower than inlet pressure!"
            in str(e.value)
        )

    def test_isentropic_expansion_to_pressure(self):
        assert self.water.isentropic_expansion_to_pressure(
            self.low_pressure
        ) == self.water.with_state(
            Input.pressure(self.low_pressure), Input.entropy(self.water.entropy)
        )

    def test_isentropic_expansion_to_pressure_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.water.isentropic_expansion_to_pressure(self.high_pressure)
        assert "Expander outlet pressure should be lower than inlet pressure!" in str(
            e.value
        )

    def test_expansion_to_pressure(self):
        assert self.water.expansion_to_pressure(
            self.low_pressure, self.isentropic_efficiency
        ) == self.water.with_state(
            Input.pressure(self.low_pressure),
            Input.enthalpy(
                self.water.enthalpy
                - (
                    self.water.enthalpy
                    - self.water.isentropic_expansion_to_pressure(
                        self.low_pressure
                    ).enthalpy
                )
                * (self.isentropic_efficiency * 1e-2)
            ),
        )

    @pytest.mark.parametrize(
        "pressure_ratio, isentropic_efficiency, message",
        [
            (2, 80, "Expander outlet pressure should be lower than inlet pressure!"),
            (0.5, 0, "Invalid expander isentropic efficiency!"),
            (0.5, 100, "Invalid expander isentropic efficiency!"),
        ],
    )
    def test_expansion_to_pressure_wrong_input(
        self, pressure_ratio: float, isentropic_efficiency: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.expansion_to_pressure(
                pressure_ratio * self.water.pressure, isentropic_efficiency
            )
        assert message in str(e.value)

    def test_cooling_to_temperature(self):
        assert self.water.cooling_to_temperature(
            self.water.temperature - self.temperature_delta, self.pressure_drop
        ) == self.water.with_state(
            Input.pressure(self.water.pressure - self.pressure_drop),
            Input.temperature(self.water.temperature - self.temperature_delta),
        )

    @pytest.mark.parametrize(
        "temperature_delta, pressure_drop, message",
        [
            (5, 0, "During the cooling process, the temperature should decrease!"),
            (-5, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_cooling_to_temperature_wrong_input(
        self, temperature_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.cooling_to_temperature(
                self.water.temperature + temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_cooling_to_enthalpy(self):
        assert self.water.cooling_to_enthalpy(
            self.water.enthalpy - self.enthalpy_delta, self.pressure_drop
        ) == self.water.with_state(
            Input.pressure(self.water.pressure - self.pressure_drop),
            Input.enthalpy(self.water.enthalpy - self.enthalpy_delta),
        )

    @pytest.mark.parametrize(
        "enthalpy_delta, pressure_drop, message",
        [
            (5e3, 0, "During the cooling process, the enthalpy should decrease!"),
            (-5e3, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_cooling_to_enthalpy_wrong_input(
        self, enthalpy_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.cooling_to_enthalpy(
                self.water.enthalpy + enthalpy_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_temperature(self):
        assert self.water.heating_to_temperature(
            self.water.temperature + self.temperature_delta, self.pressure_drop
        ) == self.water.with_state(
            Input.pressure(self.water.pressure - self.pressure_drop),
            Input.temperature(self.water.temperature + self.temperature_delta),
        )

    @pytest.mark.parametrize(
        "temperature_delta, pressure_drop, message",
        [
            (5, 0, "During the heating process, the temperature should increase!"),
            (-5, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_temperature_wrong_input(
        self, temperature_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.heating_to_temperature(
                self.water.temperature - temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_enthalpy(self):
        assert self.water.heating_to_enthalpy(
            self.water.enthalpy + self.enthalpy_delta, self.pressure_drop
        ) == self.water.with_state(
            Input.pressure(self.water.pressure - self.pressure_drop),
            Input.enthalpy(self.water.enthalpy + self.enthalpy_delta),
        )

    @pytest.mark.parametrize(
        "enthalpy_delta, pressure_drop, message",
        [
            (5e3, 0, "During the heating process, the enthalpy should increase!"),
            (-5e3, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_enthalpy_wrong_input(
        self, enthalpy_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.water.heating_to_enthalpy(
                self.water.enthalpy - enthalpy_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_bubble_point_at_pressure(self):
        assert self.water.bubble_point_at_pressure(101325) == self.water.with_state(
            Input.pressure(101325), Input.quality(0)
        )

    def test_bubble_point_at_temperature(self):
        assert self.water.bubble_point_at_temperature(100) == self.water.with_state(
            Input.temperature(100), Input.quality(0)
        )

    def test_dew_point_at_pressure(self):
        assert self.water.dew_point_at_pressure(101325) == self.water.with_state(
            Input.pressure(101325), Input.quality(100)
        )

    def test_dew_point_at_temperature(self):
        assert self.water.dew_point_at_temperature(100) == self.water.with_state(
            Input.temperature(100), Input.quality(100)
        )

    def test_two_phase_point(self):
        assert self.water.two_phase_point_at_pressure(
            101325, 50
        ) == self.water.with_state(Input.pressure(101325), Input.quality(50))

    def test_mixing(self):
        first = self.water.cooling_to_temperature(
            self.water.temperature - self.temperature_delta
        )
        second = self.water.heating_to_temperature(
            self.water.temperature + self.temperature_delta
        )
        assert self.water.mixing(1, first, 2, second) == self.water.with_state(
            Input.pressure(self.water.pressure),
            Input.enthalpy((1 * first.enthalpy + 2 * second.enthalpy) / 3),
        )

    def test_mixing_wrong_fluids(self):
        first = Fluid(FluidsList.Ammonia).dew_point_at_pressure(101325)
        second = self.water.heating_to_temperature(
            self.water.temperature + self.temperature_delta
        )
        with pytest.raises(ValueError) as e:
            self.water.mixing(1, first, 2, second)
        assert "The mixing process is possible only for the same fluids!" in str(
            e.value
        )

    def test_mixing_wrong_pressures(self):
        first = self.water.clone()
        second = self.water.isentropic_compression_to_pressure(self.high_pressure)
        with pytest.raises(ValueError) as e:
            self.water.mixing(1, first, 2, second)
        assert (
            "The mixing process is possible only for flows with the same pressure!"
            in str(e.value)
        )
