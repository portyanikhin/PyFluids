import json
from typing import List

import pytest

from pyfluids import Mixture, FluidsList, Input, Phases


class TestMixture:
    fluids = [FluidsList.Water, FluidsList.Ethanol]
    fractions = [50, 50]
    mixture = Mixture(fluids, fractions)

    @pytest.mark.parametrize(
        "fluids, fractions, message",
        [
            (
                [FluidsList.Water],
                fractions,
                "Invalid input! Fluids and fractions should be of the same length.",
            ),
            (
                [FluidsList.MPG, FluidsList.MEG],
                fractions,
                "Invalid components! All of them should be "
                "a pure fluid with HEOS backend.",
            ),
            (
                fluids,
                [-200, 50],
                "Invalid component mass fractions! All of them should be in (0;100) %.",
            ),
            (
                fluids,
                [50, 200],
                "Invalid component mass fractions! All of them should be in (0;100) %.",
            ),
            (
                fluids,
                [80, 80],
                "Invalid component mass fractions! Their sum should be equal to 100 %.",
            ),
        ],
    )
    def test_invalid_input(
        self, fluids: List[FluidsList], fractions: List[float], message: str
    ):
        with pytest.raises(ValueError) as e:
            Mixture(fluids, fractions)
        assert message in str(e.value)

    def test_factory(self):
        new_mixture = self.mixture.factory()
        assert new_mixture.fluids == self.fluids
        assert new_mixture.fractions == self.fractions
        assert new_mixture.phase == Phases.Unknown

    def test_with_state(self):
        new_mixture = self.mixture.with_state(
            Input.pressure(101325), Input.temperature(20)
        )
        assert new_mixture.phase == Phases.Liquid

    def test_cached_input(self):
        new_mixture = self.mixture.with_state(
            Input.pressure(101325), Input.temperature(20)
        )
        assert new_mixture.pressure == 101325
        assert new_mixture.temperature == 20

    def test_equals(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(15))
        same = self.mixture.with_state(Input.pressure(101325), Input.temperature(15))
        other = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        assert origin == same
        assert origin != other
        assert origin != object()

    def test_hash(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(25))
        same = self.mixture.with_state(Input.pressure(101325), Input.temperature(25))
        other = self.mixture.with_state(Input.pressure(101325), Input.temperature(30))
        assert hash(origin) == hash(same)
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    def test_clone(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        clone = origin.clone()
        assert origin == clone
        clone.update(Input.pressure(101325), Input.temperature(30))
        assert origin != clone

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json(self, indented: bool):
        mixture = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        assert mixture.as_json(indented) == json.dumps(
            mixture.as_dict(),
            indent=4 if indented else None,
            default=str,
            sort_keys=False,
        )

    def test_as_dict(self):
        mixture = self.mixture.with_state(Input.pressure(101325), Input.temperature(30))
        assert all(
            key
            in [
                k.split("__")[-1]
                for k in vars(mixture).keys()
                if not k.split("__")[-1].startswith("_")
            ]
            for key in list(mixture.as_dict().keys())
        )
