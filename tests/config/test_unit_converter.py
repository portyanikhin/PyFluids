import os
from pathlib import Path

import pytest

from pyfluids import PyFluidsConfigBuilder, UnitConverter, UnitsSystem


class TestUnitConverter:
    config_builder: PyFluidsConfigBuilder = PyFluidsConfigBuilder()

    @pytest.mark.parametrize("units_system", list(UnitsSystem))
    def test_units_system_returns_configured_value(
        self, units_system: UnitsSystem, tmp_path: Path
    ):
        self.__configure(units_system, tmp_path)
        assert UnitConverter().units_system == units_system

    @pytest.mark.parametrize(
        "units_system, value, expected_result",
        [
            (UnitsSystem.SI, 293.15, 293.15),
            (UnitsSystem.SIWithCelsius, 293.15, 20),
            (UnitsSystem.SIWithCelsiusAndPercents, 293.15, 20),
        ],
    )
    def test_convert_temperature_from_si(
        self,
        units_system: UnitsSystem,
        value: float,
        expected_result: float,
        tmp_path: Path,
    ):
        self.__configure(units_system, tmp_path)
        assert UnitConverter().convert_temperature_from_si(value) == expected_result

    @pytest.mark.parametrize(
        "units_system, value, expected_result",
        [
            (UnitsSystem.SI, 293.15, 293.15),
            (UnitsSystem.SIWithCelsius, 20, 293.15),
            (UnitsSystem.SIWithCelsiusAndPercents, 20, 293.15),
        ],
    )
    def test_convert_temperature_to_si(
        self,
        units_system: UnitsSystem,
        value: float,
        expected_result: float,
        tmp_path: Path,
    ):
        self.__configure(units_system, tmp_path)
        assert UnitConverter().convert_temperature_to_si(value) == expected_result

    @pytest.mark.parametrize(
        "units_system, value, expected_result",
        [
            (UnitsSystem.SI, 0.5, 0.5),
            (UnitsSystem.SIWithCelsius, 0.5, 0.5),
            (UnitsSystem.SIWithCelsiusAndPercents, 0.5, 50),
        ],
    )
    def test_convert_decimal_fraction_from_si(
        self,
        units_system: UnitsSystem,
        value: float,
        expected_result: float,
        tmp_path: Path,
    ):
        self.__configure(units_system, tmp_path)
        assert (
            UnitConverter().convert_decimal_fraction_from_si(value) == expected_result
        )

    @pytest.mark.parametrize(
        "units_system, value, expected_result",
        [
            (UnitsSystem.SI, 0.5, 0.5),
            (UnitsSystem.SIWithCelsius, 0.5, 0.5),
            (UnitsSystem.SIWithCelsiusAndPercents, 50, 0.5),
        ],
    )
    def test_convert_decimal_fraction_to_si(
        self,
        units_system: UnitsSystem,
        value: float,
        expected_result: float,
        tmp_path: Path,
    ):
        self.__configure(units_system, tmp_path)
        assert UnitConverter().convert_decimal_fraction_to_si(value) == expected_result

    def __configure(self, units_system: UnitsSystem, tmp_path: Path):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyfluids.ini"
        config_file.write_text(
            f"""
            [pyfluids]
            units_system = {units_system}
            """
        )
        self.config_builder._reset()
