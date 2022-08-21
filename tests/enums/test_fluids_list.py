import pytest

from pyfluids.enums.fluids_list import FluidsList
from pyfluids.enums.mix import Mix


class TestFluidsList:
    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_repr(self, fluid: FluidsList):
        assert repr(fluid) == fluid.name

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_str(self, fluid: FluidsList):
        assert str(fluid) == fluid.name

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_coolprop_name(self, fluid: FluidsList):
        match fluid:
            case fluid if fluid.coolprop_name.endswith(".mix"):
                pass
            case FluidsList.R50:
                assert fluid.coolprop_name == "Methane"
            case FluidsList.RE143a:
                assert fluid.coolprop_name == "HFE143m"
            case FluidsList.R152a:
                assert fluid.coolprop_name == "R152A"
            case FluidsList.R170:
                assert fluid.coolprop_name == "Ethane"
            case FluidsList.R290:
                assert fluid.coolprop_name == "n-Propane"
            case FluidsList.R600:
                assert fluid.coolprop_name == "n-Butane"
            case FluidsList.R600a:
                assert fluid.coolprop_name == "IsoButane"
            case FluidsList.R601:
                assert fluid.coolprop_name == "n-Pentane"
            case FluidsList.R601a:
                assert fluid.coolprop_name == "Isopentane"
            case FluidsList.R702:
                assert fluid.coolprop_name == "Hydrogen"
            case FluidsList.R704:
                assert fluid.coolprop_name == "Helium"
            case FluidsList.R717:
                assert fluid.coolprop_name == "Ammonia"
            case FluidsList.R718:
                assert fluid.coolprop_name == "Water"
            case FluidsList.R720:
                assert fluid.coolprop_name == "Neon"
            case FluidsList.R728:
                assert fluid.coolprop_name == "Nitrogen"
            case FluidsList.R729:
                assert fluid.coolprop_name == "Air"
            case FluidsList.R732:
                assert fluid.coolprop_name == "Oxygen"
            case FluidsList.R740:
                assert fluid.coolprop_name == "Argon"
            case FluidsList.R744:
                assert fluid.coolprop_name == "CarbonDioxide"
            case FluidsList.R764:
                assert fluid.coolprop_name == "SulfurDioxide"
            case FluidsList.R846:
                assert fluid.coolprop_name == "SulfurHexafluoride"
            case FluidsList.R1150:
                assert fluid.coolprop_name == "Ethylene"
            case FluidsList.R1270:
                assert fluid.coolprop_name == "Propylene"
            case FluidsList.Butene:
                assert fluid.coolprop_name == "1-Butene"
            case FluidsList.WaterIncomp:
                assert fluid.coolprop_name == "Water"
            case _:
                assert fluid.name == self.remove_chars(
                    fluid.coolprop_name, "-", "(", ")"
                )

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_backend(self, fluid: FluidsList):
        if (
            fluid.fraction_min != 0
            or fluid.fraction_max != 1
            or fluid.mix_type is Mix.Volume
        ):
            assert fluid.backend == "INCOMP"
        else:
            assert fluid.backend == "HEOS" or fluid.backend == "INCOMP"

    @pytest.mark.parametrize("fluid", list(FluidsList))
    def test_pure(self, fluid: FluidsList):
        if fluid.mix_type is Mix.Volume:
            assert not fluid.pure

    @staticmethod
    def remove_chars(s: str, *chars: str) -> str:
        for char in chars:
            s = s.replace(char, "")
        return s
