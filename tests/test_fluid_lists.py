#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

import pytest

from pyfluids import *

fluid_list = (
    list(PureFluids)
    + list(IncompPureFluids)
    + list(IncompMixturesMF)
    + list(IncompMixturesVF)
)


class TestFluidLists:
    @pytest.mark.parametrize("name", fluid_list)
    def test_coolprop_name(self, name):
        try:
            assert name.coolprop_name == {
                PureFluids.cis2Butene: "cis-2-Butene",
                PureFluids.nDecane: "n-Decane",
                PureFluids.nNonane: "n-Nonane",
                PureFluids.nPropane: "n-Propane",
                PureFluids.nUndecane: "n-Undecane",
                PureFluids.R1234zeZ: "R1234ze(Z)",
                PureFluids.trans2Butene: "trans-2-Butene",
            }[name]
        except KeyError:
            return name.coolprop_name == name.name

    @pytest.mark.parametrize("name", fluid_list)
    def test_repr(self, name):
        assert repr(name) == name.name

    @pytest.mark.parametrize("name", fluid_list)
    def test_str(self, name):
        assert str(name) == name.name
