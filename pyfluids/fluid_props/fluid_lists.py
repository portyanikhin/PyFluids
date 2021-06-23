#  PyFluids
#  Copyright (c) 2021 Vladimir Portyanikhin

from enum import Enum, auto

__all__ = [
    "PureFluids",
    "IncompPureFluids",
    "IncompMixturesMF",
    "IncompMixturesVF",
]


class FluidList(Enum):
    """Fluid list base class"""

    def _generate_next_value_(self, start, count, last_values):
        return self

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def coolprop_name(self) -> str:
        """Name of the fluid properties for CoolProp"""
        return self.name


class PureFluids(FluidList):
    # noinspection HttpUrlsUsage
    """List of CoolProp pure and pseudo-pure fluids.

    See Also:
        http://www.coolprop.org/fluid_properties/PurePseudoPure.html
    """

    Acetone = auto()
    Air = auto()
    Ammonia = auto()
    Argon = auto()
    Benzene = auto()
    Butene = auto()
    CarbonDioxide = auto()
    CarbonMonoxide = auto()
    CarbonylSulfide = auto()
    cis2Butene = auto()
    CycloHexane = auto()
    Cyclopentane = auto()
    CycloPropane = auto()
    D4 = auto()
    D5 = auto()
    D6 = auto()
    Deuterium = auto()
    Dichloroethane = auto()
    DiethylEther = auto()
    DimethylCarbonate = auto()
    DimethylEther = auto()
    Ethane = auto()
    Ethanol = auto()
    EthylBenzene = auto()
    Ethylene = auto()
    EthyleneOxide = auto()
    Fluorine = auto()
    HeavyWater = auto()
    Helium = auto()
    HFE143m = auto()
    Hydrogen = auto()
    HydrogenChloride = auto()
    HydrogenSulfide = auto()
    IsoButane = auto()
    IsoButene = auto()
    Isohexane = auto()
    Isopentane = auto()
    Krypton = auto()
    mXylene = auto()
    MD2M = auto()
    MD3M = auto()
    MD4M = auto()
    MDM = auto()
    Methane = auto()
    Methanol = auto()
    MethylLinoleate = auto()
    MethylLinolenate = auto()
    MethylOleate = auto()
    MethylPalmitate = auto()
    MethylStearate = auto()
    MM = auto()
    nButane = auto()
    nDecane = auto()
    nDodecane = auto()
    nHeptane = auto()
    nHexane = auto()
    nNonane = auto()
    nOctane = auto()
    nPentane = auto()
    nPropane = auto()
    nUndecane = auto()
    Neon = auto()
    Neopentane = auto()
    Nitrogen = auto()
    NitrousOxide = auto()
    Novec649 = auto()
    oXylene = auto()
    OrthoDeuterium = auto()
    OrthoHydrogen = auto()
    Oxygen = auto()
    pXylene = auto()
    ParaDeuterium = auto()
    ParaHydrogen = auto()
    Propylene = auto()
    Propyne = auto()
    R11 = auto()
    R113 = auto()
    R114 = auto()
    R115 = auto()
    R116 = auto()
    R12 = auto()
    R123 = auto()
    R1233zdE = auto()
    R1234yf = auto()
    R1234zeE = auto()
    R1234zeZ = auto()
    R124 = auto()
    R1243zf = auto()
    R125 = auto()
    R13 = auto()
    R134a = auto()
    R13I1 = auto()
    R14 = auto()
    R141b = auto()
    R142b = auto()
    R143a = auto()
    R152A = auto()
    R161 = auto()
    R21 = auto()
    R218 = auto()
    R22 = auto()
    R227EA = auto()
    R23 = auto()
    R236EA = auto()
    R236FA = auto()
    R245ca = auto()
    R245fa = auto()
    R32 = auto()
    R365MFC = auto()
    R40 = auto()
    R404A = auto()
    R407C = auto()
    R41 = auto()
    R410A = auto()
    R507A = auto()
    RC318 = auto()
    SES36 = auto()
    SulfurDioxide = auto()
    SulfurHexafluoride = auto()
    Toluene = auto()
    trans2Butene = auto()
    Water = auto()
    Xenon = auto()

    @property
    def coolprop_name(self) -> str:
        """Name of the fluid properties for CoolProp"""
        try:
            return {
                self.cis2Butene: "cis-2-Butene",
                self.nDecane: "n-Decane",
                self.nNonane: "n-Nonane",
                self.nPropane: "n-Propane",
                self.nUndecane: "n-Undecane",
                self.R1234zeZ: "R1234ze(Z)",
                self.trans2Butene: "trans-2-Butene",
            }[self]
        except KeyError:
            return self.name


class IncompPureFluids(FluidList):
    # noinspection HttpUrlsUsage
    """List of CoolProp incompressible pure fluids.

    See Also:
        http://www.coolprop.org/fluid_properties/Incompressibles.html
    """

    AS10 = auto()
    AS20 = auto()
    AS30 = auto()
    AS40 = auto()
    AS55 = auto()
    DEB = auto()
    DSF = auto()
    DowJ = auto()
    DowJ2 = auto()
    DowQ = auto()
    DowQ2 = auto()
    HC10 = auto()
    HC20 = auto()
    HC30 = auto()
    HC40 = auto()
    HC50 = auto()
    HCB = auto()
    HCM = auto()
    HFE = auto()
    HFE2 = auto()
    HY20 = auto()
    HY30 = auto()
    HY40 = auto()
    HY45 = auto()
    HY50 = auto()
    NBS = auto()
    NaK = auto()
    PBB = auto()
    PCL = auto()
    PCR = auto()
    PGLT = auto()
    PHE = auto()
    PHR = auto()
    PLR = auto()
    PMR = auto()
    PMS1 = auto()
    PMS2 = auto()
    PNF = auto()
    PNF2 = auto()
    S800 = auto()
    SAB = auto()
    T66 = auto()
    T72 = auto()
    TCO = auto()
    TD12 = auto()
    TVP1 = auto()
    TVP1869 = auto()
    TX22 = auto()
    TY10 = auto()
    TY15 = auto()
    TY20 = auto()
    TY24 = auto()
    Water = auto()
    XLT = auto()
    XLT2 = auto()
    ZS10 = auto()
    ZS25 = auto()
    ZS40 = auto()
    ZS45 = auto()
    ZS55 = auto()


class IncompMixturesMF(FluidList):
    # noinspection HttpUrlsUsage
    """List of CoolProp incompressible mass-based binary mixtures.

    See Also:
        http://www.coolprop.org/fluid_properties/Incompressibles.html
    """

    FRE = auto()
    IceEA = auto()
    IceNA = auto()
    IcePG = auto()
    LiBr = auto()
    MAM = auto()
    MAM2 = auto()
    MCA = auto()
    MCA2 = auto()
    MEA = auto()
    MEA2 = auto()
    MEG = auto()
    MEG2 = auto()
    MGL = auto()
    MGL2 = auto()
    MITSW = auto()
    MKA = auto()
    MKA2 = auto()
    MKC = auto()
    MKC2 = auto()
    MKF = auto()
    MLI = auto()
    MMA = auto()
    MMA2 = auto()
    MMG = auto()
    MMG2 = auto()
    MNA = auto()
    MNA2 = auto()
    MPG = auto()
    MPG2 = auto()
    VCA = auto()
    VKC = auto()
    VMA = auto()
    VMG = auto()
    VNA = auto()


class IncompMixturesVF(FluidList):
    # noinspection HttpUrlsUsage
    """List of CoolProp incompressible volume-based binary mixtures.

    See Also:
        http://www.coolprop.org/fluid_properties/Incompressibles.html
    """

    AEG = auto()
    AKF = auto()
    AL = auto()
    AN = auto()
    APG = auto()
    GKN = auto()
    PK2 = auto()
    PKL = auto()
    ZAC = auto()
    ZFC = auto()
    ZLC = auto()
    ZM = auto()
    ZMC = auto()
