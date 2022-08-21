import pytest

from pyfluids import Mix


class TestMix:
    @pytest.mark.parametrize("mix_type", list(Mix))
    def test_repr(self, mix_type: Mix):
        assert repr(mix_type) == mix_type.name

    @pytest.mark.parametrize("mix_type", list(Mix))
    def test_str(self, mix_type: Mix):
        assert str(mix_type) == mix_type.name
