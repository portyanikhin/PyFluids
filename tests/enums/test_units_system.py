import pytest

from pyfluids import UnitsSystem


class TestUnitsSystem:
    @pytest.mark.parametrize("units_system", list(UnitsSystem))
    def test_repr_always_returns_name(self, units_system: UnitsSystem):
        assert repr(units_system) == units_system.name

    @pytest.mark.parametrize("units_system", list(UnitsSystem))
    def test_str_always_returns_name(self, units_system: UnitsSystem):
        assert str(units_system) == units_system.name
