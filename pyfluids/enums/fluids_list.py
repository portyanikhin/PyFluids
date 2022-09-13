from enum import Enum

from .mix import Mix

__all__ = ["FluidsList"]


class FluidsList(Enum):
    """
    List of CoolProp fluids:

    http://www.coolprop.org/fluid_properties/PurePseudoPure.html

    http://www.coolprop.org/fluid_properties/Incompressibles.html

    http://www.coolprop.org/coolprop/HighLevelAPI.html#predefined-mixtures
    """

    # Pure and pseudo-pure fluids
    Acetone = "Acetone"
    Air = "Air"
    R729 = "Air"
    Ammonia = "Ammonia"
    R717 = "Ammonia"
    Argon = "Argon"
    R740 = "Argon"
    Benzene = "Benzene"
    Butene = "1-Butene"
    CarbonDioxide = "CarbonDioxide"
    R744 = "CarbonDioxide"
    CarbonMonoxide = "CarbonMonoxide"
    CarbonylSulfide = "CarbonylSulfide"
    cis2Butene = "cis-2-Butene"
    CycloHexane = "CycloHexane"
    CycloPentane = "CycloPentane"
    CycloPropane = "CycloPropane"
    D4 = "D4"
    D5 = "D5"
    D6 = "D6"
    Deuterium = "Deuterium"
    Dichloroethane = "Dichloroethane"
    DiethylEther = "DiethylEther"
    DimethylCarbonate = "DimethylCarbonate"
    DimethylEther = "DimethylEther"
    Ethane = "Ethane"
    R170 = "Ethane"
    Ethanol = "Ethanol"
    EthylBenzene = "EthylBenzene"
    Ethylene = "Ethylene"
    R1150 = "Ethylene"
    EthyleneOxide = "EthyleneOxide"
    Fluorine = "Fluorine"
    HeavyWater = "HeavyWater"
    Helium = "Helium"
    R704 = "Helium"
    HFE143m = "HFE143m"
    RE143a = "HFE143m"
    Hydrogen = "Hydrogen"
    R702 = "Hydrogen"
    HydrogenChloride = "HydrogenChloride"
    HydrogenSulfide = "HydrogenSulfide"
    IsoButane = "IsoButane"
    R600a = "IsoButane"
    IsoButene = "IsoButene"
    Isohexane = "Isohexane"
    Isopentane = "Isopentane"
    R601a = "Isopentane"
    Krypton = "Krypton"
    MD2M = "MD2M"
    MD3M = "MD3M"
    MD4M = "MD4M"
    MDM = "MDM"
    Methane = "Methane"
    R50 = "Methane"
    Methanol = "Methanol"
    MethylLinoleate = "MethylLinoleate"
    MethylLinolenate = "MethylLinolenate"
    MethylOleate = "MethylOleate"
    MethylPalmitate = "MethylPalmitate"
    MethylStearate = "MethylStearate"
    MM = "MM"
    mXylene = "m-Xylene"
    nButane = "n-Butane"
    R600 = "n-Butane"
    nDecane = "n-Decane"
    nDodecane = "n-Dodecane"
    Neon = "Neon"
    R720 = "Neon"
    Neopentane = "Neopentane"
    nHeptane = "n-Heptane"
    nHexane = "n-Hexane"
    Nitrogen = "Nitrogen"
    R728 = "Nitrogen"
    NitrousOxide = "NitrousOxide"
    nNonane = "n-Nonane"
    nOctane = "n-Octane"
    Novec649 = "Novec649"
    nPentane = "n-Pentane"
    R601 = "n-Pentane"
    nPropane = "n-Propane"
    R290 = "n-Propane"
    nUndecane = "n-Undecane"
    OrthoDeuterium = "OrthoDeuterium"
    OrthoHydrogen = "OrthoHydrogen"
    Oxygen = "Oxygen"
    R732 = "Oxygen"
    oXylene = "o-Xylene"
    ParaDeuterium = "ParaDeuterium"
    ParaHydrogen = "ParaHydrogen"
    Propylene = "Propylene"
    R1270 = "Propylene"
    Propyne = "Propyne"
    pXylene = "p-Xylene"
    R11 = "R11"
    R113 = "R113"
    R114 = "R114"
    R115 = "R115"
    R116 = "R116"
    R12 = "R12"
    R123 = "R123"
    R1233zdE = "R1233zd(E)"
    R1234yf = "R1234yf"
    R1234zeE = "R1234ze(E)"
    R1234zeZ = "R1234ze(Z)"
    R124 = "R124"
    R1243zf = "R1243zf"
    R125 = "R125"
    R13 = "R13"
    R134a = "R134a"
    R13I1 = "R13I1"
    R14 = "R14"
    R141b = "R141b"
    R142b = "R142b"
    R143a = "R143a"
    R152a = "R152A"
    R161 = "R161"
    R21 = "R21"
    R218 = "R218"
    R22 = "R22"
    R227ea = "R227ea"
    R23 = "R23"
    R236ea = "R236ea"
    R236fa = "R236fa"
    R245ca = "R245ca"
    R245fa = "R245fa"
    R32 = "R32"
    R365mfc = "R365mfc"
    R40 = "R40"
    R404A = "R404A"
    R407C = "R407C"
    R41 = "R41"
    R410A = "R410A"
    R507A = "R507A"
    RC318 = "RC318"
    SES36 = "SES36"
    SulfurDioxide = "SulfurDioxide"
    R764 = "SulfurDioxide"
    SulfurHexafluoride = "SulfurHexafluoride"
    R846 = "SulfurHexafluoride"
    Toluene = "Toluene"
    trans2Butene = "trans-2-Butene"
    Water = "Water"
    R718 = "Water"
    Xenon = "Xenon"

    # Incompressible pure fluids
    AS10 = "AS10", "INCOMP"
    AS20 = "AS20", "INCOMP"
    AS30 = "AS30", "INCOMP"
    AS40 = "AS40", "INCOMP"
    AS55 = "AS55", "INCOMP"
    DEB = "DEB", "INCOMP"
    DowJ = "DowJ", "INCOMP"
    DowJ2 = "DowJ2", "INCOMP"
    DowQ = "DowQ", "INCOMP"
    DowQ2 = "DowQ2", "INCOMP"
    DSF = "DSF", "INCOMP"
    HC10 = "HC10", "INCOMP"
    HC20 = "HC20", "INCOMP"
    HC30 = "HC30", "INCOMP"
    HC40 = "HC40", "INCOMP"
    HC50 = "HC50", "INCOMP"
    HCB = "HCB", "INCOMP"
    HCM = "HCM", "INCOMP"
    HFE = "HFE", "INCOMP"
    HFE2 = "HFE2", "INCOMP"
    HY20 = "HY20", "INCOMP"
    HY30 = "HY30", "INCOMP"
    HY40 = "HY40", "INCOMP"
    HY45 = "HY45", "INCOMP"
    HY50 = "HY50", "INCOMP"
    NaK = "NaK", "INCOMP"
    NBS = "NBS", "INCOMP"
    PBB = "PBB", "INCOMP"
    PCL = "PCL", "INCOMP"
    PCR = "PCR", "INCOMP"
    PGLT = "PGLT", "INCOMP"
    PHE = "PHE", "INCOMP"
    PHR = "PHR", "INCOMP"
    PLR = "PLR", "INCOMP"
    PMR = "PMR", "INCOMP"
    PMS1 = "PMS1", "INCOMP"
    PMS2 = "PMS2", "INCOMP"
    PNF = "PNF", "INCOMP"
    PNF2 = "PNF2", "INCOMP"
    S800 = "S800", "INCOMP"
    SAB = "SAB", "INCOMP"
    T66 = "T66", "INCOMP"
    T72 = "T72", "INCOMP"
    TCO = "TCO", "INCOMP"
    TD12 = "TD12", "INCOMP"
    TVP1 = "TVP1", "INCOMP"
    TVP1869 = "TVP1869", "INCOMP"
    TX22 = "TX22", "INCOMP"
    TY10 = "TY10", "INCOMP"
    TY15 = "TY15", "INCOMP"
    TY20 = "TY20", "INCOMP"
    TY24 = "TY24", "INCOMP"
    WaterIncomp = "Water", "INCOMP"
    XLT = "XLT", "INCOMP"
    XLT2 = "XLT2", "INCOMP"
    ZS10 = "ZS10", "INCOMP"
    ZS25 = "ZS25", "INCOMP"
    ZS40 = "ZS40", "INCOMP"
    ZS45 = "ZS45", "INCOMP"
    ZS55 = "ZS55", "INCOMP"

    # Incompressible mass-based binary mixtures
    FRE = "FRE", "INCOMP", False, Mix.Mass, 0.19, 0.5
    IceEA = "IceEA", "INCOMP", False, Mix.Mass, 0.05, 0.35
    IceNA = "IceNA", "INCOMP", False, Mix.Mass, 0.05, 0.35
    IcePG = "IcePG", "INCOMP", False, Mix.Mass, 0.05, 0.35
    LiBr = "LiBr", "INCOMP", False, Mix.Mass, 0, 0.75
    MAM = "MAM", "INCOMP", False, Mix.Mass, 0, 0.3
    MAM2 = "MAM2", "INCOMP", False, Mix.Mass, 0.078, 0.236
    MCA = "MCA", "INCOMP", False, Mix.Mass, 0, 0.3
    MCA2 = "MCA2", "INCOMP", False, Mix.Mass, 0.09, 0.294
    MEA = "MEA", "INCOMP", False, Mix.Mass, 0, 0.6
    MEA2 = "MEA2", "INCOMP", False, Mix.Mass, 0.11, 0.6
    MEG = "MEG", "INCOMP", False, Mix.Mass, 0, 0.6
    MEG2 = "MEG2", "INCOMP", False, Mix.Mass, 0, 0.56
    MGL = "MGL", "INCOMP", False, Mix.Mass, 0, 0.6
    MGL2 = "MGL2", "INCOMP", False, Mix.Mass, 0.195, 0.63
    MITSW = "MITSW", "INCOMP", False, Mix.Mass, 0, 0.12
    MKA = "MKA", "INCOMP", False, Mix.Mass, 0, 0.45
    MKA2 = "MKA2", "INCOMP", False, Mix.Mass, 0.11, 0.41
    MKC = "MKC", "INCOMP", False, Mix.Mass, 0, 0.4
    MKC2 = "MKC2", "INCOMP", False, Mix.Mass, 0, 0.39
    MKF = "MKF", "INCOMP", False, Mix.Mass, 0, 0.48
    MLI = "MLI", "INCOMP", False, Mix.Mass, 0, 0.24
    MMA = "MMA", "INCOMP", False, Mix.Mass, 0, 0.6
    MMA2 = "MMA2", "INCOMP", False, Mix.Mass, 0.078, 0.474
    MMG = "MMG", "INCOMP", False, Mix.Mass, 0, 0.3
    MMG2 = "MMG2", "INCOMP", False, Mix.Mass, 0, 0.205
    MNA = "MNA", "INCOMP", False, Mix.Mass, 0, 0.23
    MNA2 = "MNA2", "INCOMP", False, Mix.Mass, 0, 0.23
    MPG = "MPG", "INCOMP", False, Mix.Mass, 0, 0.6
    MPG2 = "MPG2", "INCOMP", False, Mix.Mass, 0.15, 0.57
    VCA = "VCA", "INCOMP", False, Mix.Mass, 0.147, 0.299
    VKC = "VKC", "INCOMP", False, Mix.Mass, 0.128, 0.389
    VMA = "VMA", "INCOMP", False, Mix.Mass, 0.1, 0.9
    VMG = "VMG", "INCOMP", False, Mix.Mass, 0.072, 0.206
    VNA = "VNA", "INCOMP", False, Mix.Mass, 0.07, 0.231

    # Incompressible volume-based binary mixtures
    AEG = "AEG", "INCOMP", False, Mix.Volume, 0.1, 0.6
    AKF = "AKF", "INCOMP", False, Mix.Volume, 0.4
    AL = "AL", "INCOMP", False, Mix.Volume, 0.1, 0.6
    AN = "AN", "INCOMP", False, Mix.Volume, 0.1, 0.6
    APG = "APG", "INCOMP", False, Mix.Volume, 0.1, 0.6
    GKN = "GKN", "INCOMP", False, Mix.Volume, 0.1, 0.6
    PK2 = "PK2", "INCOMP", False, Mix.Volume, 0.3
    PKL = "PKL", "INCOMP", False, Mix.Volume, 0.1, 0.6
    ZAC = "ZAC", "INCOMP", False, Mix.Volume, 0.06, 0.5
    ZFC = "ZFC", "INCOMP", False, Mix.Volume, 0.3, 0.6
    ZLC = "ZLC", "INCOMP", False, Mix.Volume, 0.3, 0.7
    ZM = "ZM", "INCOMP", False, Mix.Volume
    ZMC = "ZMC", "INCOMP", False, Mix.Volume, 0.3, 0.7

    # Predefined mixtures
    AirMix = "Air.mix"
    Amarillo = "Amarillo.mix"
    Ekofisk = "Ekofisk.mix"
    GulfCoast = "GulfCoast.mix"
    GulfCoastGasNIST = "GulfCoastGas(NIST1).mix"
    HighCO2 = "HighCO2.mix"
    HighN2 = "HighN2.mix"
    NaturalGasSample = "NaturalGasSample.mix"
    R401A = "R401A.mix"
    R401B = "R401B.mix"
    R401C = "R401C.mix"
    R402A = "R402A.mix"
    R402B = "R402B.mix"
    R403A = "R403A.mix"
    R403B = "R403B.mix"
    R404AMix = "R404A.mix"
    R405A = "R405A.mix"
    R406A = "R406A.mix"
    R407A = "R407A.mix"
    R407B = "R407B.mix"
    R407CMix = "R407C.mix"
    R407D = "R407D.mix"
    R407E = "R407E.mix"
    R407F = "R407F.mix"
    R408A = "R408A.mix"
    R409A = "R409A.mix"
    R409B = "R409B.mix"
    R410AMix = "R410A.mix"
    R410B = "R410B.mix"
    R411A = "R411A.mix"
    R411B = "R411B.mix"
    R412A = "R412A.mix"
    R413A = "R413A.mix"
    R414A = "R414A.mix"
    R414B = "R414B.mix"
    R415A = "R415A.mix"
    R415B = "R415B.mix"
    R416A = "R416A.mix"
    R417A = "R417A.mix"
    R417B = "R417B.mix"
    R417C = "R417C.mix"
    R418A = "R418A.mix"
    R419A = "R419A.mix"
    R419B = "R419B.mix"
    R420A = "R420A.mix"
    R421A = "R421A.mix"
    R421B = "R421B.mix"
    R422A = "R422A.mix"
    R422B = "R422B.mix"
    R422C = "R422C.mix"
    R422D = "R422D.mix"
    R422E = "R422E.mix"
    R423A = "R423A.mix"
    R424A = "R424A.mix"
    R425A = "R425A.mix"
    R426A = "R426A.mix"
    R427A = "R427A.mix"
    R428A = "R428A.mix"
    R429A = "R429A.mix"
    R430A = "R430A.mix"
    R431A = "R431A.mix"
    R432A = "R432A.mix"
    R433A = "R433A.mix"
    R433B = "R433B.mix"
    R433C = "R433C.mix"
    R434A = "R434A.mix"
    R435A = "R435A.mix"
    R436A = "R436A.mix"
    R436B = "R436B.mix"
    R437A = "R437A.mix"
    R438A = "R438A.mix"
    R439A = "R439A.mix"
    R440A = "R440A.mix"
    R441A = "R441A.mix"
    R442A = "R442A.mix"
    R443A = "R443A.mix"
    R444A = "R444A.mix"
    R444B = "R444B.mix"
    R445A = "R445A.mix"
    R446A = "R446A.mix"
    R447A = "R447A.mix"
    R448A = "R448A.mix"
    R449A = "R449A.mix"
    R449B = "R449B.mix"
    R450A = "R450A.mix"
    R451A = "R451A.mix"
    R451B = "R451B.mix"
    R452A = "R452A.mix"
    R453A = "R453A.mix"
    R454A = "R454A.mix"
    R454B = "R454B.mix"
    R500 = "R500.mix"
    R501 = "R501.mix"
    R502 = "R502.mix"
    R503 = "R503.mix"
    R504 = "R504.mix"
    R507AMix = "R507A.mix"
    R508A = "R508A.mix"
    R508B = "R508B.mix"
    R509A = "R509A.mix"
    R510A = "R510A.mix"
    R511A = "R511A.mix"
    R512A = "R512A.mix"
    R513A = "R513A.mix"
    TypicalNaturalGas = "TypicalNaturalGas.mix"

    def __init__(
        self,
        coolprop_name: str,
        backend: str = "HEOS",
        pure: bool = True,
        mix_type: Mix = Mix.Mass,
        fraction_min: float = 0,
        fraction_max: float = 1,
    ):
        (
            self.__coolprop_name,
            self.__coolprop_backend,
            self.__pure,
            self.__mix_type,
            self.__fraction_min,
            self.__fraction_max,
        ) = (
            coolprop_name,
            backend,
            pure,
            mix_type,
            fraction_min,
            fraction_max,
        )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

    @property
    def coolprop_name(self) -> str:
        """CoolProp internal name."""
        return self.__coolprop_name

    @property
    def coolprop_backend(self) -> str:
        """Type of CoolProp backend."""
        return self.__coolprop_backend

    @property
    def pure(self) -> bool:
        """True if pure or pseudo-pure fluid."""
        return self.__pure

    @property
    def mix_type(self) -> Mix:
        """Mass-based or volume-based mixture."""
        return self.__mix_type

    @property
    def fraction_min(self) -> float:
        """Minimum possible fraction [%]."""
        return self.__fraction_min * 1e2

    @property
    def fraction_max(self) -> float:
        """Maximum possible fraction [%]."""
        return self.__fraction_max * 1e2
