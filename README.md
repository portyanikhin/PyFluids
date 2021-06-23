# PyFluids

![Python](https://img.shields.io/badge/python-3.7%20%7C%203.8-blue)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/portyanikhin/PyFluids/blob/main/LICENSE)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A simple, full-featured, lightweight [CoolProp] wrapper for Python.

## Installation

The project gets published on [PyPI] as `pyfluids`. 
For install the latest version using `pip`:

```commandline
pip install pyfluids
```

## Quick start

All calculations of thermophysical properties are performed in _SI units_.

The `Fluid` class is responsible for pure fluids and binary mixtures, 
the `Mixture` class - for mixtures with pure fluids components, 
the `HumidAir` class - for humid air.

For `Fluid` use `PureFluids`, `IncompPureFluids`, `IncompMixturesMF`, 
`IncompMixturesVF` enums. For `Mixture` - list of `PureFluids`.

To update the fluid state use `Input` enum (for `Fluid` and `Mixture`) or 
`HAInput` (for `HumidAir`) enum and their `with_value` method (**always**).

You can also convert an instance of `Fluid`, `Mixture` or `HumidAir` 
to a JSON string or dictionary using methods `to_json` and `to_dict`, respectively.

### List of properties

For the `Fluid` and `Mixture` instances:
* `compressibility` - compressibility factor (-)
* `conductivity` - thermal conductivity (W/m/K)
* `critical_pressure` - absolute pressure at the critical point (Pa)
* `critical_temperature` - absolute temperature at the critical point (K)
* `density` - mass density (kg/m3)
* `dynamic_viscosity` - dynamic viscosity (Pa*s)
* `enthalpy` - mass specific enthalpy (J/kg)
* `entropy` - mass specific entropy (J/kg/K)
* `freezing_temperature` - temperature at freezing point (for incompressible fluids) (K)
* `internal_energy` - mass specific internal energy (J/kg)
* `max_pressure` - maximum pressure limit (Pa)
* `max_temperature` - maximum temperature limit (K)
* `min_pressure` - minimum pressure limit (Pa)
* `min_temperature` - minimum temperature limit (K)
* `molar_mass` - molar mass (kg/mol)
* `phase` - phase
* `prandtl` - Prandtl number (-)
* `pressure` - absolute pressure (Pa)
* `quality` - mass vapor quality (-)
* `sound_speed` - sound speed (m/s)
* `specific_heat` - mass specific constant pressure specific heat (J/kg/K)
* `surface_tension` - surface tension (N/m)
* `temperature` - absolute temperature (K)
* `triple_pressure` - absolute pressure at the triple point (Pa)
* `triple_temperature` - absolute temperature at the triple point (K)

For the `HumidAir` instances:
* `compressibility` - compressibility factor (-)
* `conductivity` - thermal conductivity (W/m/K)
* `density` - mass density per humid air unit (kg/m3)
* `dew_temperature` - dew-point absolute temperature (K)
* `dynamic_viscosity` - dynamic viscosity (Pa*s)
* `enthalpy` - mass specific enthalpy per humid air (J/kg)
* `entropy` - mass specific entropy per humid air (J/kg/K)
* `humidity` - absolute humidity ratio (kg/kg d.a.)
* `partial_pressure` - partial pressure of water vapor (Pa)
* `pressure` - absolute pressure (Pa)
* `relative_humidity` - relative humidity ratio (from 0 to 1) (-)
* `specific_heat` - mass specific constant pressure specific heat per humid air (J/kg/K)
* `temperature` - absolute dry-bulb temperature (K)
* `wb_temperature` - absolute wet-bulb temperature (K)

**NB.** If the required property is not present in the instance of the fluid, 
then you can add it using the `add_props` method.

### Examples

#### Pure fluids

To calculate the specific heat of saturated water vapour at _101325 Pa_:

```python
from pyfluids import Fluid, PureFluids, Input

water_vapour = Fluid(PureFluids.Water)
water_vapour.update(Input.Pressure.with_value(101325), Input.Quality.with_value(1))
print(water_vapour.specific_heat)  # 2079.937085633241
```

#### Incompressible binary mixtures

To calculate the dynamic viscosity of propylene glycol aqueous solution 
with _60 %_ mass fraction at _101325 Pa_ and _253.15 K_:

```python
from pyfluids import Fluid, IncompMixturesMF, Input

propylene_glycol = Fluid(IncompMixturesMF.MPG, 0.6)
propylene_glycol.update(
    Input.Pressure.with_value(101325), Input.Temperature.with_value(253.15)
)
print(propylene_glycol.dynamic_viscosity)  # 0.13907391053938847
```

#### Mixtures

To calculate the density of ethanol aqueous solution (with ethanol _40 %_ mass fraction)
at _200 kPa_ and _277.15 K_:

```python
from pyfluids import Mixture, PureFluids, Input

mixture = Mixture([PureFluids.Water, PureFluids.Ethanol], [0.6, 0.4])
mixture.update(Input.Pressure.with_value(200e3), Input.Temperature.with_value(277.15))
print(mixture.density)  # 883.3922771627759
```

#### Humid air

To calculate the wet bulb temperature of humid air at _99 kPa_, _303.15 K_ and _50 %_ 
relative humidity:

```python
from pyfluids import HumidAir, HAInput

humid_air = HumidAir()
humid_air.update(
    HAInput.Pressure.with_value(99e3),
    HAInput.Temperature.with_value(303.15),
    HAInput.RelativeHumidity.with_value(0.5),
)
print(humid_air.wb_temperature)  # 295.0965785590792
```

#### Adding other properties

For example, to add Global Warming Potential (GWP) to the `Fluid` instance:

```python
import CoolProp

from pyfluids import Fluid, PureFluids

refrigerant = Fluid(PureFluids.R32)
new_props = {
    "gwp20": CoolProp.iGWP20,
    "gwp100": CoolProp.iGWP100,
    "gwp500": CoolProp.iGWP500,
}
refrigerant.add_props(new_props)
# Because GWP is a trivial input, you can get it without `update`
print(refrigerant.gwp20)  # 2330.0
print(refrigerant.gwp100)  # 675.0
print(refrigerant.gwp500)  # 205.0
```

#### Converting to JSON or to dict

For example, converting the `Fluid` instance to JSON string with 4 indent:

```python
from pyfluids import Fluid, PureFluids, Input

refrigerant = Fluid(PureFluids.R32)
refrigerant.update(Input.Temperature.with_value(278.15), Input.Quality.with_value(1))
print(refrigerant.to_json(4))
```

As a result:

```json
{
    "name": "R32",
    "fraction": 1,
    "compressibility": 0.8266625877210833,
    "conductivity": 0.013435453854396475,
    "critical_pressure": 5782000.0,
    "critical_temperature": 351.255,
    "density": 25.89088151061046,
    "dynamic_viscosity": 1.2606543144761657e-05,
    "enthalpy": 516105.7800378023,
    "entropy": 2136.2654412978777,
    "freezing_temperature": null,
    "internal_energy": 479357.39743435377,
    "max_pressure": 70000000.0,
    "max_temperature": 435.0,
    "min_pressure": 47.999893876059375,
    "min_temperature": 136.34,
    "molar_mass": 0.052024,
    "phase": "TwoPhase",
    "prandtl": 1.2252282243443504,
    "pressure": 951448.019691762,
    "quality": 1.0,
    "sound_speed": 209.6337575990297,
    "specific_heat": 1305.7899441785378,
    "surface_tension": 0.010110117241546162,
    "temperature": 278.15,
    "triple_pressure": 47.999893876059375,
    "triple_temperature": 136.34
}
```

Absolutely the same way, you can convert any instance of `Fluid`, `Mixture` 
or `HumidAir` to Python dictionary - via `to_dict` method.

[CoolProp]: http://www.coolprop.org/
[PyPI]: https://pypi.org/project/pyfluids/