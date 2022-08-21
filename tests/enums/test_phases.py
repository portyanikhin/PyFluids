import pytest

from pyfluids import Phases


class TestPhases:
    @pytest.mark.parametrize("phase", list(Phases))
    def test_repr(self, phase: Phases):
        assert repr(phase) == phase.name

    @pytest.mark.parametrize("phase", list(Phases))
    def test_str(self, phase: Phases):
        assert str(phase) == phase.name
