import pytest

from pyfluids import HumidAir, InputHumidAir


class TestHumidAirProcesses:
    humid_air = HumidAir().with_state(
        InputHumidAir.pressure(101325),
        InputHumidAir.temperature(20),
        InputHumidAir.relative_humidity(50),
    )

    temperature_delta = 5
    enthalpy_delta = 5e3
    pressure_drop = 200
    low_humidity = 5e-3
    high_humidity = 9e-3
    low_relative_humidity = 45
    high_relative_humidity = 95

    def test_dry_cooling_to_temperature(self):
        assert self.humid_air.dry_cooling_to_temperature(
            self.humid_air.temperature - self.temperature_delta, self.pressure_drop
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.temperature(
                self.humid_air.temperature - self.temperature_delta
            ),
            InputHumidAir.humidity(self.humid_air.humidity),
        )

    @pytest.mark.parametrize(
        "temperature, pressure_drop, message",
        [
            (50, 0, "During the cooling process, the temperature should decrease!"),
            (
                0,
                0,
                "The outlet temperature after dry heat transfer "
                "should be greater than the dew point temperature!",
            ),
            (15, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_dry_cooling_to_temperature_wrong_input(
        self, temperature: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.dry_cooling_to_temperature(temperature, pressure_drop)
        assert message in str(e.value)

    def test_dry_cooling_to_enthalpy(self):
        assert self.humid_air.dry_cooling_to_enthalpy(
            self.humid_air.enthalpy - self.enthalpy_delta, self.pressure_drop
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.enthalpy(self.humid_air.enthalpy - self.enthalpy_delta),
            InputHumidAir.humidity(self.humid_air.humidity),
        )

    @pytest.mark.parametrize(
        "enthalpy, pressure_drop, message",
        [
            (5e4, 0, "During the cooling process, the enthalpy should decrease!"),
            (
                0,
                0,
                "The outlet enthalpy after dry heat transfer "
                "should be greater than the dew point enthalpy!",
            ),
            (3e4, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_dry_cooling_to_enthalpy_wrong_input(
        self, enthalpy: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.dry_cooling_to_enthalpy(enthalpy, pressure_drop)
        assert message in str(e.value)

    def test_wet_cooling_to_temperature_and_relative_humidity(self):
        assert self.humid_air.wet_cooling_to_temperature_and_relative_humidity(
            self.humid_air.temperature - self.temperature_delta,
            self.low_relative_humidity,
            self.pressure_drop,
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.temperature(
                self.humid_air.temperature - self.temperature_delta
            ),
            InputHumidAir.relative_humidity(self.low_relative_humidity),
        )

    @pytest.mark.parametrize(
        "temperature, relative_humidity, pressure_drop, message",
        [
            (50, 60, 0, "During the cooling process, the temperature should decrease!"),
            (
                15,
                100,
                0,
                "During the wet cooling process, "
                "the absolute humidity ratio should decrease!",
            ),
            (15, 60, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_wet_cooling_to_temperature_and_relative_humidity_wrong_input(
        self,
        temperature: float,
        relative_humidity: float,
        pressure_drop: float,
        message: str,
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.wet_cooling_to_temperature_and_relative_humidity(
                temperature, relative_humidity, pressure_drop
            )
        assert message in str(e.value)

    def test_wet_cooling_to_temperature_and_absolute_humidity(self):
        assert self.humid_air.wet_cooling_to_temperature_and_absolute_humidity(
            self.humid_air.temperature - self.temperature_delta,
            self.low_humidity,
            self.pressure_drop,
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.temperature(
                self.humid_air.temperature - self.temperature_delta
            ),
            InputHumidAir.humidity(self.low_humidity),
        )

    @pytest.mark.parametrize(
        "temperature, humidity, pressure_drop, message",
        [
            (
                50,
                5e-3,
                0,
                "During the cooling process, the temperature should decrease!",
            ),
            (
                15,
                9e-3,
                0,
                "During the wet cooling process, "
                "the absolute humidity ratio should decrease!",
            ),
            (15, 5e-3, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_wet_cooling_to_temperature_and_absolute_humidity_wrong_input(
        self,
        temperature: float,
        humidity: float,
        pressure_drop: float,
        message: str,
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.wet_cooling_to_temperature_and_absolute_humidity(
                temperature, humidity, pressure_drop
            )
        assert message in str(e.value)

    def test_wet_cooling_to_enthalpy_and_relative_humidity(self):
        assert self.humid_air.wet_cooling_to_enthalpy_and_relative_humidity(
            self.humid_air.enthalpy - self.enthalpy_delta,
            self.low_relative_humidity,
            self.pressure_drop,
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.enthalpy(self.humid_air.enthalpy - self.enthalpy_delta),
            InputHumidAir.relative_humidity(self.low_relative_humidity),
        )

    @pytest.mark.parametrize(
        "enthalpy, relative_humidity, pressure_drop, message",
        [
            (5e4, 60, 0, "During the cooling process, the enthalpy should decrease!"),
            (
                3.5e4,
                100,
                0,
                "During the wet cooling process, "
                "the absolute humidity ratio should decrease!",
            ),
            (1.5e4, 60, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_wet_cooling_to_enthalpy_and_relative_humidity_wrong_input(
        self,
        enthalpy: float,
        relative_humidity: float,
        pressure_drop: float,
        message: str,
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.wet_cooling_to_enthalpy_and_relative_humidity(
                enthalpy, relative_humidity, pressure_drop
            )
        assert message in str(e.value)

    def test_wet_cooling_to_enthalpy_and_absolute_humidity(self):
        assert self.humid_air.wet_cooling_to_enthalpy_and_absolute_humidity(
            self.humid_air.enthalpy - self.enthalpy_delta,
            self.low_humidity,
            self.pressure_drop,
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.enthalpy(self.humid_air.enthalpy - self.enthalpy_delta),
            InputHumidAir.humidity(self.low_humidity),
        )

    @pytest.mark.parametrize(
        "enthalpy, humidity, pressure_drop, message",
        [
            (5e4, 5e-3, 0, "During the cooling process, the enthalpy should decrease!"),
            (
                1.5e4,
                9e-3,
                0,
                "During the wet cooling process, "
                "the absolute humidity ratio should decrease!",
            ),
            (1.5e4, 5e-3, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_wet_cooling_to_enthalpy_and_absolute_humidity_wrong_input(
        self,
        enthalpy: float,
        humidity: float,
        pressure_drop: float,
        message: str,
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.wet_cooling_to_enthalpy_and_absolute_humidity(
                enthalpy, humidity, pressure_drop
            )
        assert message in str(e.value)

    def test_heating_to_temperature(self):
        assert self.humid_air.heating_to_temperature(
            self.humid_air.temperature + self.temperature_delta, self.pressure_drop
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.temperature(
                self.humid_air.temperature + self.temperature_delta
            ),
            InputHumidAir.humidity(self.humid_air.humidity),
        )

    @pytest.mark.parametrize(
        "temperature, pressure_drop, message",
        [
            (15, 0, "During the heating process, the temperature should increase!"),
            (50, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_temperature_wrong_input(
        self, temperature: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.heating_to_temperature(temperature, pressure_drop)
        assert message in str(e.value)

    def test_heating_to_enthalpy(self):
        assert self.humid_air.heating_to_enthalpy(
            self.humid_air.enthalpy + self.enthalpy_delta, self.pressure_drop
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.enthalpy(self.humid_air.enthalpy + self.enthalpy_delta),
            InputHumidAir.humidity(self.humid_air.humidity),
        )

    @pytest.mark.parametrize(
        "enthalpy, pressure_drop, message",
        [
            (1.5e4, 0, "During the heating process, the enthalpy should increase!"),
            (5e4, -100, "Invalid pressure drop in the heat exchanger!"),
        ],
    )
    def test_heating_to_enthalpy_wrong_input(
        self, enthalpy: float, pressure_drop: float, message: str
    ):
        with pytest.raises(ValueError) as e:
            self.humid_air.heating_to_enthalpy(enthalpy, pressure_drop)
        assert message in str(e.value)

    def test_humidification_by_water_to_relative_humidity(self):
        assert self.humid_air.humidification_by_water_to_relative_humidity(
            self.high_relative_humidity
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure),
            InputHumidAir.enthalpy(self.humid_air.enthalpy),
            InputHumidAir.relative_humidity(self.high_relative_humidity),
        )

    def test_humidification_by_water_to_relative_humidity_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.humid_air.humidification_by_water_to_relative_humidity(
                self.low_relative_humidity
            )
        assert (
            "During the humidification process, "
            "the absolute humidity ratio should increase!" in str(e.value)
        )

    def test_humidification_by_water_to_absolute_humidity(self):
        assert self.humid_air.humidification_by_water_to_absolute_humidity(
            self.high_humidity
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure),
            InputHumidAir.enthalpy(self.humid_air.enthalpy),
            InputHumidAir.humidity(self.high_humidity),
        )

    def test_humidification_by_water_to_absolute_humidity_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.humid_air.humidification_by_water_to_absolute_humidity(
                self.low_humidity
            )
        assert (
            "During the humidification process, "
            "the absolute humidity ratio should increase!" in str(e.value)
        )

    def test_humidification_by_steam_to_relative_humidity(self):
        assert self.humid_air.humidification_by_steam_to_relative_humidity(
            self.high_relative_humidity
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure),
            InputHumidAir.temperature(self.humid_air.temperature),
            InputHumidAir.relative_humidity(self.high_relative_humidity),
        )

    def test_humidification_by_steam_to_relative_humidity_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.humid_air.humidification_by_steam_to_relative_humidity(
                self.low_relative_humidity
            )
        assert (
            "During the humidification process, "
            "the absolute humidity ratio should increase!" in str(e.value)
        )

    def test_humidification_by_steam_to_absolute_humidity(self):
        assert self.humid_air.humidification_by_steam_to_absolute_humidity(
            self.high_humidity
        ) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure),
            InputHumidAir.temperature(self.humid_air.temperature),
            InputHumidAir.humidity(self.high_humidity),
        )

    def test_humidification_by_steam_to_absolute_humidity_wrong_input(self):
        with pytest.raises(ValueError) as e:
            self.humid_air.humidification_by_steam_to_absolute_humidity(
                self.low_humidity
            )
        assert (
            "During the humidification process, "
            "the absolute humidity ratio should increase!" in str(e.value)
        )

    def test_mixing(self):
        first = self.humid_air.heating_to_temperature(
            self.humid_air.temperature + self.temperature_delta
        )
        second = self.humid_air.humidification_by_water_to_relative_humidity(
            self.high_relative_humidity
        )
        assert self.humid_air.mixing(1, first, 2, second) == self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure),
            InputHumidAir.enthalpy((1 * first.enthalpy + 2 * second.enthalpy) / 3),
            InputHumidAir.humidity((1 * first.humidity + 2 * second.humidity) / 3),
        )

    def test_mixing_wrong_input(self):
        first = self.humid_air.with_state(
            InputHumidAir.pressure(self.humid_air.pressure - self.pressure_drop),
            InputHumidAir.temperature(
                self.humid_air.temperature + self.temperature_delta
            ),
            InputHumidAir.humidity(self.humid_air.humidity),
        )
        second = self.humid_air.humidification_by_water_to_relative_humidity(
            self.high_relative_humidity
        )
        with pytest.raises(ValueError) as e:
            self.humid_air.mixing(1, first, 2, second)
        assert (
            "The mixing process is possible only for flows with the same pressure!"
            in str(e.value)
        )
