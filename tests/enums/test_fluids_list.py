import pytest

from pyfluids import FluidsList, Mix


class TestFluidsList:
    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_repr(self, fluid: FluidsList):
        assert repr(fluid) == fluid.name

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_str(self, fluid: FluidsList):
        assert str(fluid) == fluid.name

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_coolprop_name(self, fluid: FluidsList):
        if fluid.coolprop_name.endswith(".mix"):
            pass
        elif fluid is FluidsList.R50:
            assert fluid.coolprop_name == "Methane"
        elif fluid is FluidsList.RE143a:
            assert fluid.coolprop_name == "HFE143m"
        elif fluid is FluidsList.R152a:
            assert fluid.coolprop_name == "R152A"
        elif fluid is FluidsList.R170:
            assert fluid.coolprop_name == "Ethane"
        elif fluid is FluidsList.R290:
            assert fluid.coolprop_name == "n-Propane"
        elif fluid is FluidsList.R600:
            assert fluid.coolprop_name == "n-Butane"
        elif fluid is FluidsList.R600a:
            assert fluid.coolprop_name == "IsoButane"
        elif fluid is FluidsList.R601:
            assert fluid.coolprop_name == "n-Pentane"
        elif fluid is FluidsList.R601a:
            assert fluid.coolprop_name == "Isopentane"
        elif fluid is FluidsList.R702:
            assert fluid.coolprop_name == "Hydrogen"
        elif fluid is FluidsList.R704:
            assert fluid.coolprop_name == "Helium"
        elif fluid is FluidsList.R717:
            assert fluid.coolprop_name == "Ammonia"
        elif fluid is FluidsList.R718:
            assert fluid.coolprop_name == "Water"
        elif fluid is FluidsList.R720:
            assert fluid.coolprop_name == "Neon"
        elif fluid is FluidsList.R728:
            assert fluid.coolprop_name == "Nitrogen"
        elif fluid is FluidsList.R729:
            assert fluid.coolprop_name == "Air"
        elif fluid is FluidsList.R732:
            assert fluid.coolprop_name == "Oxygen"
        elif fluid is FluidsList.R740:
            assert fluid.coolprop_name == "Argon"
        elif fluid is FluidsList.R744:
            assert fluid.coolprop_name == "CarbonDioxide"
        elif fluid is FluidsList.R764:
            assert fluid.coolprop_name == "SulfurDioxide"
        elif fluid is FluidsList.R846:
            assert fluid.coolprop_name == "SulfurHexafluoride"
        elif fluid is FluidsList.R1150:
            assert fluid.coolprop_name == "Ethylene"
        elif fluid is FluidsList.R1270:
            assert fluid.coolprop_name == "Propylene"
        elif fluid is FluidsList.Butene:
            assert fluid.coolprop_name == "1-Butene"
        elif fluid is FluidsList.WaterIncomp:
            assert fluid.coolprop_name == "Water"
        else:
            assert fluid.name == self.remove_chars(fluid.coolprop_name, "-", "(", ")")

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_backend(self, fluid: FluidsList):
        if (
            fluid.fraction_min != 0
            or fluid.fraction_max != 100
            or fluid.mix_type is Mix.Volume
        ):
            assert fluid.coolprop_backend == "INCOMP"
        else:
            assert (
                fluid.coolprop_backend == "HEOS" or fluid.coolprop_backend == "INCOMP"
            )

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_pure(self, fluid: FluidsList):
        if fluid.mix_type is Mix.Volume:
            assert not fluid.pure

    @staticmethod
    def remove_chars(s: str, *chars: str) -> str:
        for char in chars:
            s = s.replace(char, "")
        return s
