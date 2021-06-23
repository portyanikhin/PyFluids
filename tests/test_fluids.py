#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from math import isnan, isinf
from typing import Union

import CoolProp
import pytest
from CoolProp.CoolProp import PropsSI

from pyfluids import *

# noinspection PyProtectedMember
from pyfluids.fluid_props.fluids import AbstractFluid

prop_names = {
    "compressibility": "Z",
    "conductivity": "L",
    "critical_pressure": "p_critical",
    "critical_temperature": "T_critical",
    "density": "D",
    "dynamic_viscosity": "V",
    "enthalpy": "H",
    "entropy": "S",
    "freezing_temperature": "T_freeze",
    "internal_energy": "U",
    "max_pressure": "P_max",
    "max_temperature": "T_max",
    "min_pressure": "P_min",
    "min_temperature": "T_min",
    "molar_mass": "M",
    "prandtl": "Prandtl",
    "sound_speed": "A",
    "specific_heat": "C",
    "surface_tension": "I",
    "triple_pressure": "p_triple",
    "triple_temperature": "T_triple",
}

pure_fluids = list(PureFluids) + list(IncompPureFluids)
incomp_mixtures = list(IncompMixturesMF) + list(IncompMixturesVF)


class TestAbstractFluid:
    def test_post_init(self):
        AbstractFluid.__post_init__(Fluid(PureFluids.Water))


class TestFluid:
    @pytest.mark.parametrize(
        "name, fraction",
        [
            (IncompMixturesMF.MPG, None),
            (IncompMixturesMF.MPG, -2),
            (IncompMixturesMF.MPG, 2),
        ],
    )
    def test_post_init(self, name, fraction):
        with pytest.raises(ValueError):
            Fluid(name, fraction)

    @pytest.mark.parametrize("name", pure_fluids)
    @pytest.mark.parametrize("pressure", [1e6, 1e7, 1e8])
    def test_update_pure_fluids(self, name, pressure):
        self.update(name, self.coolprop_name(name), pressure)

    @pytest.mark.parametrize("name", incomp_mixtures)
    @pytest.mark.parametrize("pressure", [1e6, 1e7, 1e8])
    def test_update_incomp_mixtures(self, name, pressure):
        coolprop_name = self.coolprop_name(name)
        fraction = PropsSI("fraction_max", coolprop_name) - 0.01
        coolprop_name += f"-{fraction * 100}%"
        self.update(name, coolprop_name, pressure, fraction)

    @pytest.mark.parametrize("name", pure_fluids)
    def test_add_props_pure_fluids(self, name):
        self.add_props(name, self.coolprop_name(name))

    @pytest.mark.parametrize("name", incomp_mixtures)
    def test_add_props_incomp_mixtures(self, name):
        coolprop_name = self.coolprop_name(name)
        fraction = PropsSI("fraction_max", coolprop_name) - 0.01
        coolprop_name += f"-{fraction * 100}%"
        self.add_props(name, coolprop_name, fraction)

    def update(
        self,
        name: Union[PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF],
        coolprop_name: str,
        pressure: float,
        fraction: float = None,
    ):
        fluid = Fluid(name, fraction)
        temperature = fluid.min_temperature * 0.25 + fluid.max_temperature * 0.75
        fluid.update(
            Input.Pressure.with_value(pressure),
            Input.Temperature.with_value(temperature),
        )
        actual = fluid.to_dict()
        for key, value in prop_names.items():
            try:
                expected = PropsSI(
                    value,
                    "P",
                    pressure,
                    "T",
                    temperature,
                    coolprop_name,
                )
                expected = self.convert(expected)
            except ValueError:
                expected = None
            try:
                assert actual[key] == expected
            except AssertionError:
                assert round(actual[key], 7) == round(expected, 7)

    def add_props(
        self,
        name: Union[PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF],
        coolprop_name: str,
        fraction: float = None,
    ):
        fluid = Fluid(name, fraction)
        new_props = {
            "gwp20": CoolProp.iGWP20,
            "gwp100": CoolProp.iGWP100,
            "gwp500": CoolProp.iGWP500,
        }
        fluid.add_props(new_props)
        actual = fluid.to_dict()
        for key, value in new_props.items():
            try:
                expected = self.convert(
                    PropsSI(
                        key.upper(),
                        "P",
                        1e6,
                        "T",
                        fluid.min_temperature * 0.25 + fluid.max_temperature * 0.75,
                        coolprop_name,
                    )
                )
            except ValueError:
                expected = None
            assert actual[key] == expected

    @staticmethod
    def coolprop_name(
        name: Union[PureFluids, IncompPureFluids, IncompMixturesMF, IncompMixturesVF]
    ) -> str:
        return ("" if name in PureFluids else "INCOMP::") + name.coolprop_name

    @staticmethod
    def convert(value):
        return (
            None
            if isinstance(value, (int, float)) and (isnan(value) or isinf(value))
            else value
        )


class TestMixture:
    def setup(self):
        self.mixture = Mixture([PureFluids.Water, PureFluids.Ethanol], [0.6, 0.4])
        self.mixture._backend.set_mole_fractions([0.6, 0.4])
        self.mixture_name = "Water[0.6]&Ethanol[0.4]"

    @pytest.mark.parametrize(
        "components, fractions",
        [
            ([PureFluids.Water, PureFluids.Ethanol], [0.2, 0.3, 0.4]),
            ([PureFluids.Water, PureFluids.Ethanol], [-0.6, 1.6]),
            ([PureFluids.Water, PureFluids.Ethanol], [1, 1]),
        ],
    )
    def test_post_init(self, components, fractions):
        with pytest.raises(ValueError):
            Mixture(components, fractions)

    @pytest.mark.parametrize("pressure", [1e5, 1e6, 1e7])
    @pytest.mark.parametrize("temperature", list(range(253, 333, 10)))
    def test_update(self, pressure, temperature):
        self.mixture.update(
            Input.Pressure.with_value(pressure),
            Input.Temperature.with_value(temperature),
        )
        actual = self.mixture.to_dict()
        for key, value in prop_names.items():
            try:
                expected = PropsSI(
                    value,
                    "P",
                    pressure,
                    "T",
                    temperature,
                    self.mixture_name,
                )
                expected = TestFluid.convert(expected)
            except ValueError:
                expected = None
            assert actual[key] == expected
