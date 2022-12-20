import pytest

from pyfluids import Phases


class TestPhases:
    @pytest.mark.parametrize("phase", list(Phases))
    def test_repr_always_returns_name(self, phase: Phases):
        assert repr(phase) == phase.name

    @pytest.mark.parametrize("phase", list(Phases))
    def test_str_always_returns_name(self, phase: Phases):
        assert str(phase) == phase.name
