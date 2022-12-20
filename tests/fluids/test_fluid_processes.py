import pytest

from pyfluids import Fluid, FluidsList, Input


class TestFluidProcesses:
    fluid: Fluid = Fluid(FluidsList.Water).with_state(
        Input.pressure(101325), Input.temperature(150)
    )
    high_pressure: float = 2 * fluid.pressure
    low_pressure: float = 0.5 * fluid.pressure
    isentropic_efficiency: float = 80
    temperature_delta: float = 10
    enthalpy_delta: float = 5e4
    pressure_drop: float = 5e4

    def test_isentropic_compression_to_wrong_pressure_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.fluid.isentropic_compression_to_pressure(self.low_pressure)
        assert (
            "Compressor outlet pressure should be higher than inlet pressure!"
            in str(e.value)
        )

    def test_isentropic_compression_to_high_pressure(self):
        assert self.fluid.isentropic_compression_to_pressure(
            self.high_pressure
        ) == self.fluid.with_state(
            Input.pressure(self.high_pressure), Input.entropy(self.fluid.entropy)
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
    def test_compression_to_pressure_wrong_input_raises_value_error(
        self, pressure_ratio: float, isentropic_efficiency: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.fluid.compression_to_pressure(
                pressure_ratio * self.fluid.pressure, isentropic_efficiency
            )
        assert message in str(e.value)

    def test_compression_to_pressure(self):
        assert self.fluid.compression_to_pressure(
            self.high_pressure, self.isentropic_efficiency
        ) == self.fluid.with_state(
            Input.pressure(self.high_pressure),
            Input.enthalpy(
                self.fluid.enthalpy
                + (
                    self.fluid.isentropic_compression_to_pressure(
                        self.high_pressure
                    ).enthalpy
                    - self.fluid.enthalpy
                )
                / (self.isentropic_efficiency * 1e-2)
            ),
        )

    def test_isenthalpic_expansion_to_wrong_pressure_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.fluid.isenthalpic_expansion_to_pressure(self.high_pressure)
        assert (
            "Expansion valve outlet pressure should be lower than inlet pressure!"
            in str(e.value)
        )

    def test_isenthalpic_expansion_to_pressure(self):
        assert self.fluid.isenthalpic_expansion_to_pressure(
            self.low_pressure
        ) == self.fluid.with_state(
            Input.pressure(self.low_pressure), Input.enthalpy(self.fluid.enthalpy)
        )

    def test_isentropic_expansion_to_wrong_pressure_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.fluid.isentropic_expansion_to_pressure(self.high_pressure)
        assert "Expander outlet pressure should be lower than inlet pressure!" in str(
            e.value
        )

    def test_isentropic_expansion_to_pressure(self):
        assert self.fluid.isentropic_expansion_to_pressure(
            self.low_pressure
        ) == self.fluid.with_state(
            Input.pressure(self.low_pressure), Input.entropy(self.fluid.entropy)
        )

    @pytest.mark.parametrize(
        "pressure_ratio, isentropic_efficiency, message",
        [
            (2, 80, "Expander outlet pressure should be lower than inlet pressure!"),
            (0.5, 0, "Invalid expander isentropic efficiency!"),
            (0.5, 100, "Invalid expander isentropic efficiency!"),
        ],
    )
    def test_expansion_to_pressure_wrong_input_raises_value_error(
        self, pressure_ratio: float, isentropic_efficiency: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.fluid.expansion_to_pressure(
                pressure_ratio * self.fluid.pressure, isentropic_efficiency
            )
        assert message in str(e.value)

    def test_expansion_to_pressure(self):
        assert self.fluid.expansion_to_pressure(
            self.low_pressure, self.isentropic_efficiency
        ) == self.fluid.with_state(
            Input.pressure(self.low_pressure),
            Input.enthalpy(
                self.fluid.enthalpy
                - (
                    self.fluid.enthalpy
                    - self.fluid.isentropic_expansion_to_pressure(
                        self.low_pressure
                    ).enthalpy
                )
                * (self.isentropic_efficiency * 1e-2)
            ),
        )

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
            self.fluid.cooling_to_temperature(
                self.fluid.temperature + temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_cooling_to_temperature(self):
        assert self.fluid.cooling_to_temperature(
            self.fluid.temperature - self.temperature_delta, self.pressure_drop
        ) == self.fluid.with_state(
            Input.pressure(self.fluid.pressure - self.pressure_drop),
            Input.temperature(self.fluid.temperature - self.temperature_delta),
        )

    @pytest.mark.parametrize(
        "enthalpy_delta, pressure_drop, message",
        [
            (5e3, 0, "During the cooling process, the enthalpy should decrease!"),
            (-5e3, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_cooling_to_enthalpy_wrong_input_raises_value_error(
        self, enthalpy_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.fluid.cooling_to_enthalpy(
                self.fluid.enthalpy + enthalpy_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_cooling_to_enthalpy(self):
        assert self.fluid.cooling_to_enthalpy(
            self.fluid.enthalpy - self.enthalpy_delta, self.pressure_drop
        ) == self.fluid.with_state(
            Input.pressure(self.fluid.pressure - self.pressure_drop),
            Input.enthalpy(self.fluid.enthalpy - self.enthalpy_delta),
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
            self.fluid.heating_to_temperature(
                self.fluid.temperature - temperature_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_temperature(self):
        assert self.fluid.heating_to_temperature(
            self.fluid.temperature + self.temperature_delta, self.pressure_drop
        ) == self.fluid.with_state(
            Input.pressure(self.fluid.pressure - self.pressure_drop),
            Input.temperature(self.fluid.temperature + self.temperature_delta),
        )

    @pytest.mark.parametrize(
        "enthalpy_delta, pressure_drop, message",
        [
            (5e3, 0, "During the heating process, the enthalpy should increase!"),
            (-5e3, -10, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_enthalpy_wrong_input_raises_value_error(
        self, enthalpy_delta: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.fluid.heating_to_enthalpy(
                self.fluid.enthalpy - enthalpy_delta, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_enthalpy(self):
        assert self.fluid.heating_to_enthalpy(
            self.fluid.enthalpy + self.enthalpy_delta, self.pressure_drop
        ) == self.fluid.with_state(
            Input.pressure(self.fluid.pressure - self.pressure_drop),
            Input.enthalpy(self.fluid.enthalpy + self.enthalpy_delta),
        )

    def test_bubble_point_at_pressure(self):
        assert self.fluid.bubble_point_at_pressure(101325) == self.fluid.with_state(
            Input.pressure(101325), Input.quality(0)
        )

    def test_bubble_point_at_temperature(self):
        assert self.fluid.bubble_point_at_temperature(100) == self.fluid.with_state(
            Input.temperature(100), Input.quality(0)
        )

    def test_dew_point_at_pressure(self):
        assert self.fluid.dew_point_at_pressure(101325) == self.fluid.with_state(
            Input.pressure(101325), Input.quality(100)
        )

    def test_dew_point_at_temperature(self):
        assert self.fluid.dew_point_at_temperature(100) == self.fluid.with_state(
            Input.temperature(100), Input.quality(100)
        )

    def test_two_phase_point(self):
        assert self.fluid.two_phase_point_at_pressure(
            101325, 50
        ) == self.fluid.with_state(Input.pressure(101325), Input.quality(50))

    def test_mixing_wrong_fluids_raises_value_error(self):
        first = Fluid(FluidsList.Ammonia).dew_point_at_pressure(101325)
        second = self.fluid.heating_to_temperature(
            self.fluid.temperature + self.temperature_delta
        )
        with pytest.raises(ValueError) as e:
            self.fluid.mixing(1, first, 2, second)
        assert "The mixing process is possible only for the same fluids!" in str(
            e.value
        )

    def test_mixing_wrong_pressures_raises_value_error(self):
        first = self.fluid.clone()
        second = self.fluid.isentropic_compression_to_pressure(self.high_pressure)
        with pytest.raises(ValueError) as e:
            self.fluid.mixing(1, first, 2, second)
        assert (
            "The mixing process is possible only for flows with the same pressure!"
            in str(e.value)
        )

    def test_mixing(self):
        first = self.fluid.cooling_to_temperature(
            self.fluid.temperature - self.temperature_delta
        )
        second = self.fluid.heating_to_temperature(
            self.fluid.temperature + self.temperature_delta
        )
        assert self.fluid.mixing(1, first, 2, second) == self.fluid.with_state(
            Input.pressure(self.fluid.pressure),
            Input.enthalpy((1 * first.enthalpy + 2 * second.enthalpy) / 3),
        )
