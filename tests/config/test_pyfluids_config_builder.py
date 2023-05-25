import os
from pathlib import Path

import pytest

from pyfluids import PyFluidsConfigBuilder, PyFluidsConfig, UnitsSystem

INVALID_CONTENT = "Hello, World!"

PYFLUIDS_INI_CONTENT = """
[pyfluids]
units_system = SI
"""

PYFLUIDS_JSON_CONTENT = """
{
    "pyfluids": {
        "units_system": "SIWithCelsius"
    }
}
"""

PYPROJECT_TOML_CONTENT = """
[tool.pyfluids]
units_system = "SIWithCelsiusAndPercents"
"""

TOX_INI_CONTENT = PYFLUIDS_INI_CONTENT


class TestPyFluidsConfigBuilder:
    config_builder: PyFluidsConfigBuilder = PyFluidsConfigBuilder()

    def test_config_builder_is_singleton(self):
        first_config_builder = PyFluidsConfigBuilder()
        second_config_builder = PyFluidsConfigBuilder()
        assert hash(first_config_builder) == hash(second_config_builder)

    def test_build_invokes_once_then_returns_config_from_cache(self, tmp_path: Path):
        os.chdir(tmp_path)
        self.config_builder._reset()
        first_config = self.config_builder.build()
        config_file = tmp_path / "pyfluids.ini"
        config_file.write_text(PYFLUIDS_INI_CONTENT)
        second_config = self.config_builder.build()
        assert first_config == second_config

    def test_build_when_config_file_is_not_found_returns_default_config(
        self, tmp_path: Path
    ):
        os.chdir(tmp_path)
        self.config_builder._reset()
        config = self.config_builder.build()
        assert config == PyFluidsConfig()

    def test_build_from_pyfluids_ini_when_content_is_invalid_raises_value_error(
        self, tmp_path: Path
    ):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyfluids.ini"
        config_file.write_text(INVALID_CONTENT)
        self.config_builder._reset()
        with pytest.raises(ValueError) as e:
            self.config_builder.build()
        assert (
            "Invalid PyFluids configuration! "
            f"Check your configuration file: {config_file}" in str(e.value)
        )

    def test_build_from_pyfluids_ini_returns_specified_config(self, tmp_path: Path):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyfluids.ini"
        config_file.write_text(PYFLUIDS_INI_CONTENT)
        self.config_builder._reset()
        config = self.config_builder.build()
        assert config.units_system == UnitsSystem.SI

    def test_build_from_pyfluids_json_when_content_is_invalid_raises_value_error(
        self, tmp_path: Path
    ):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyfluids.json"
        config_file.write_text(INVALID_CONTENT)
        self.config_builder._reset()
        with pytest.raises(ValueError) as e:
            self.config_builder.build()
        assert (
            "Invalid PyFluids configuration! "
            f"Check your configuration file: {config_file}" in str(e.value)
        )

    def test_build_from_pyfluids_json_returns_specified_config(self, tmp_path: Path):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyfluids.json"
        config_file.write_text(PYFLUIDS_JSON_CONTENT)
        self.config_builder._reset()
        config = self.config_builder.build()
        assert config.units_system == UnitsSystem.SIWithCelsius

    def test_build_from_pyproject_toml_when_content_is_invalid_returns_default_config(
        self, tmp_path: Path
    ):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(INVALID_CONTENT)
        self.config_builder._reset()
        assert self.config_builder.build() == PyFluidsConfig()

    def test_build_from_pyproject_toml_returns_specified_config(self, tmp_path: Path):
        os.chdir(tmp_path)
        config_file = tmp_path / "pyproject.toml"
        config_file.write_text(PYPROJECT_TOML_CONTENT)
        self.config_builder._reset()
        config = self.config_builder.build()
        assert config.units_system == UnitsSystem.SIWithCelsiusAndPercents

    def test_build_from_tox_ini_when_content_is_invalid_returns_default_config(
        self, tmp_path: Path
    ):
        os.chdir(tmp_path)
        config_file = tmp_path / "tox.ini"
        config_file.write_text(INVALID_CONTENT)
        self.config_builder._reset()
        assert self.config_builder.build() == PyFluidsConfig()

    def test_build_from_tox_ini_returns_specified_config(self, tmp_path: Path):
        os.chdir(tmp_path)
        config_file = tmp_path / "tox.ini"
        config_file.write_text(TOX_INI_CONTENT)
        self.config_builder._reset()
        config = self.config_builder.build()
        assert config.units_system == UnitsSystem.SI
