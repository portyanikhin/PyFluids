from pyfluids import PyFluidsConfig, UnitsSystem


class TestPyFluidsConfig:
    def test_pyfluids_config_default_unit_system_is_si_with_celsius_and_percents(self):
        assert PyFluidsConfig().units_system == UnitsSystem.SIWithCelsiusAndPercents
