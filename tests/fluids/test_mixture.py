import json
from typing import List

import pytest

from pyfluids import Mixture, FluidsList, Input, Phases


class TestMixture:
    mixture: Mixture = Mixture([FluidsList.Water, FluidsList.Ethanol], [60, 40])

    @pytest.mark.parametrize(
        "fluids, fractions, message",
        [
            (
                [FluidsList.Water],
                mixture.fractions,
                "Invalid input! Fluids and fractions should be of the same length.",
            ),
            (
                [FluidsList.MPG, FluidsList.MEG],
                mixture.fractions,
                "Invalid components! All of them should be "
                "a pure fluid with HEOS backend.",
            ),
            (
                mixture.fluids,
                [-200, 50],
                "Invalid component mass fractions! All of them should be in (0;100) %.",
            ),
            (
                mixture.fluids,
                [50, 200],
                "Invalid component mass fractions! All of them should be in (0;100) %.",
            ),
            (
                mixture.fluids,
                [80, 80],
                "Invalid component mass fractions! Their sum should be equal to 100 %.",
            ),
        ],
    )
    def test_mixture_wrong_fluids_or_fractions_raises_value_error(
        self, fluids: List[FluidsList], fractions: List[float], message: str
    ):
        with pytest.raises(ValueError) as e:
            Mixture(fluids, fractions)
        assert message in str(e.value)

    def test_factory_always_fluids_are_constant(self):
        assert self.mixture.factory().fluids == self.mixture.fluids

    def test_factory_always_fractions_are_constant(self):
        assert self.mixture.factory().fractions == self.mixture.fractions

    def test_factory_always_phase_is_unknown(self):
        assert self.mixture.factory().phase == Phases.Unknown

    def test_clone_always_returns_new_instance_with_same_state(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        clone = origin.clone()
        assert origin == clone
        clone.update(Input.pressure(101325), Input.temperature(30))
        assert origin != clone

    def test_with_state_vodka_in_standard_conditions_phase_is_liquid(self):
        assert (
            self.mixture.with_state(Input.pressure(101325), Input.temperature(20)).phase
            == Phases.Liquid
        )

    def test_update_same_inputs_raises_value_error(self):
        with pytest.raises(ValueError) as e:
            self.mixture.with_state(Input.pressure(101325), Input.pressure(1e5))
        assert "Need to define 2 unique inputs!" in str(e.value)

    def test_update_always_inputs_are_cached(self):
        self.mixture.update(Input.pressure(101325), Input.temperature(20))
        assert self.mixture.pressure == 101325
        assert self.mixture.temperature == 20

    def test_equals_same_returns_true(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(15))
        same = self.mixture.with_state(Input.pressure(101325), Input.temperature(15))
        assert origin == same

    def test_equals_other_returns_false(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(15))
        other = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        assert origin != other
        assert origin != object()

    def test_hash_same_returns_same_hash_code(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(25))
        same = self.mixture.with_state(Input.pressure(101325), Input.temperature(25))
        assert hash(origin) == hash(same)

    def test_hash_other_returns_other_hash_code(self):
        origin = self.mixture.with_state(Input.pressure(101325), Input.temperature(25))
        other = self.mixture.with_state(Input.pressure(101325), Input.temperature(30))
        assert hash(origin) != hash(other)
        assert hash(origin) != hash(object())

    @pytest.mark.parametrize("indented", [True, False])
    def test_as_json_indented_or_not_returns_properly_formatted_json(
        self, indented: bool
    ):
        fluid = self.mixture.with_state(Input.pressure(101325), Input.temperature(20))
        assert fluid.as_json(indented) == json.dumps(
            fluid.as_dict(),
            indent=4 if indented else None,
            default=str,
            sort_keys=False,
        )

    def test_as_dict_always_returns_only_public_properties(self):
        fluid = self.mixture.with_state(Input.pressure(101325), Input.temperature(30))
        assert all(
            key
            in [
                k.split("__")[-1]
                for k in vars(fluid).keys()
                if not k.split("__")[-1].startswith("_")
            ]
            for key in list(fluid.as_dict().keys())
        )
