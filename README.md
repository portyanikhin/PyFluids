# ![PyFluids](https://raw.githubusercontent.com/portyanikhin/PyFluids/main/pictures/header.png)

[![Build & Tests](https://github.com/portyanikhin/PyFluids/actions/workflows/build-tests.yml/badge.svg)](https://github.com/portyanikhin/PyFluids/actions/workflows/build-tests.yml)
[![CodeQL](https://github.com/portyanikhin/PyFluids/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/portyanikhin/PyFluids/actions/workflows/codeql-analysis.yml)
[![PyPI](https://img.shields.io/pypi/v/pyfluids)](https://pypi.org/project/pyfluids/)
[![Python](https://img.shields.io/pypi/pyversions/pyfluids)](https://pypi.org/project/pyfluids/)
[![License](https://img.shields.io/github/license/portyanikhin/PyFluids)](https://github.com/portyanikhin/PyFluids/blob/master/LICENSE)
[![codecov](https://codecov.io/gh/portyanikhin/PyFluids/branch/main/graph/badge.svg?token=I1LL66AOJW)](https://codecov.io/gh/portyanikhin/PyFluids)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A simple, full-featured, lightweight [CoolProp](http://www.coolprop.org) wrapper for Python.

## Navigation

- [How to install](#how-to-install)
- [Project structure](#project-structure)
- [Units systems](#units-systems)
  - [Available units systems](#available-units-systems)
  - [Available types of configuration files](#available-types-of-configuration-files)
    - [`pyfluids.ini` example](#pyfluidsini-example)
    - [`pyfluids.json` example](#pyfluidsjson-example)
    - [`pyproject.toml` example](#pyprojecttoml-example)
    - [`tox.ini` example](#toxini-example)
- [List of properties](#list-of-properties)
    - [Properties of `Fluid` and `Mixture` instances](#properties-of-fluid-and-mixture-instances)
    - [Properties of `HumidAir` instances](#properties-of-humidair-instances)
- [List of methods](#list-of-methods)
    - [Methods of `Fluid` instances](#methods-of-fluid-instances)
    - [Methods of `Mixture` instances](#methods-of-mixture-instances)
    - [Methods of `HumidAir` instances](#methods-of-humidair-instances)
- [Examples](#examples)
    - [Pure fluids](#pure-fluids)
    - [Incompressible binary mixtures](#incompressible-binary-mixtures)
    - [Mixtures](#mixtures)
    - [Humid air](#humid-air)
    - [Equality of instances](#equality-of-instances)
    - [Converting to a JSON string](#converting-to-a-json-string)
    - [Converting to a Python dict](#converting-to-a-python-dict)
    - [Deep cloning](#deep-cloning)
    - [Adding other properties](#adding-other-properties)
    - [Adding other inputs](#adding-other-inputs)

## How to install

Run the following command:

```shell
pip install pyfluids
```

## Project structure

* `Fluid` class - an implementation of pure fluids and binary mixtures.
* `Mixture` class - an implementation of mixtures with pure fluids components.
* `FluidsList` enum - the list of all available fluids.
* `Input` class - the inputs for the `Fluid` and `Mixture` classes.
* `HumidAir` class - an implementation of real humid air.
* `InputHumidAir` class - the inputs for the `HumidAir` class.

## Units systems

Using a configuration file, you can choose the units system 
that will be used in your project (for both inputs and outputs of `PyFluids`).

### Available units systems

- **SI (`UnitsSystem.SI`):**
    - temperature unit - Kelvin _(K)_;
    - decimal fraction unit - dimensionless _(from 0 to 1)_;
- **SI with Celsius (`UnitsSystem.SIWithCelsius`):**
    - temperature unit - degree Celsius _(°C)_;
    - decimal fraction unit - dimensionless _(from 0 to 1)_;
- **SI with Celsius and percents (`UnitsSystem.SIWithCelsiusAndPercents`) _- by default_:**
    - temperature unit - degree Celsius _(°C)_;
    - decimal fraction unit - percent _(%, from 0 to 100)_.

### Available types of configuration files

- `pyfluids.ini`;
- `pyfluids.json`;
- `pyproject.toml`;
- `tox.ini`.

#### `pyfluids.ini` example

```ini
[pyfluids]
units_system = SI
```

#### `pyfluids.json` example

```json5
{
    "pyfluids": {
        "units_system": "SIWithCelsius"
    }
}
```

#### `pyproject.toml` example

```toml
[tool.pyfluids]
units_system = "SIWithCelsiusAndPercents"
```

#### `tox.ini` example

```ini
[pyfluids]
units_system = SI
```

## List of properties

If the required property is not present in the instance of the fluid, then you can add it by extending
the `Fluid`, `Mixture` or `HumidAir` classes (see [how to add other properties](#adding-other-properties)).

### Properties of `Fluid` and `Mixture` instances

* `compressibility` - compressibility factor _(dimensionless)_.
* `conductivity` - thermal conductivity _(W/m/K)_.
* `critical_pressure` - absolute pressure at the critical point _(Pa)_.
* `critical_temperature` - temperature at the critical point _(by default, °C; see [how to change it](#units-systems))_.
* `density` - mass density _(kg/m3)_.
* `dynamic_viscosity` - dynamic viscosity _(Pa*s)_.
* `enthalpy` - mass specific enthalpy _(J/kg)_.
* `entropy` - mass specific entropy _(J/kg/K)_.
* `freezing_temperature` - temperature at the freezing point (for incompressible fluids) _(by default, °C; see [how to change it](#units-systems))_.
* `internal_energy` - mass specific internal energy _(J/kg)_.
* `kinematic_viscosity` - kinematic viscosity _(m2/s)_.
* `max_pressure` - maximum pressure limit _(Pa)_.
* `max_temperature` - maximum temperature limit _(by default, °C; see [how to change it](#units-systems))_.
* `min_pressure` - minimum pressure limit _(Pa)_.
* `min_temperature` - minimum temperature limit _(by default, °C; see [how to change it](#units-systems))_.
* `molar_mass` - molar mass _(kg/mol)_.
* `phase` - phase state _(enum)_.
* `prandtl` - Prandtl number _(dimensionless)_.
* `pressure` - absolute pressure _(Pa)_.
* `quality` - mass vapor quality _(by default, %; see [how to change it](#units-systems))_.
* `sound_speed` - sound speed _(m/s)_.
* `specific_heat` - mass specific constant pressure specific heat _(J/kg/K)_.
* `specific_volume` - mass specific volume _(m3/kg)_.
* `surface_tension` - surface tension _(N/m)_.
* `temperature` - temperature _(by default, °C; see [how to change it](#units-systems))_.
* `triple_pressure` - absolute pressure at the triple point _(Pa)_.
* `triple_temperature` - temperature at the triple point _(by default, °C; see [how to change it](#units-systems))_.
* `units_system` - configured units system _(enum)_.

### Properties of `HumidAir` instances

* `compressibility` - compressibility factor _(dimensionless)_.
* `conductivity` - thermal conductivity _(W/m/K)_.
* `density` - mass density per humid air unit _(kg/m3)_.
* `dew_temperature` - dew-point temperature _(by default, °C; see [how to change it](#units-systems))_.
* `dynamic_viscosity` - dynamic viscosity _(Pa*s)_.
* `enthalpy` - mass specific enthalpy per humid air _(J/kg)_.
* `entropy` - mass specific entropy per humid air _(J/kg/K)_.
* `humidity` - absolute humidity ratio _(kg/kg d.a.)_.
* `kinematic_viscosity` - kinematic viscosity _(m2/s)_.
* `partial_pressure` - partial pressure of water vapor _(Pa)_.
* `prandtl` - Prandtl number _(dimensionless)_.
* `pressure` - absolute pressure _(Pa)_.
* `relative_humidity` - relative humidity ratio _(by default, %; see [how to change it](#units-systems))_.
* `specific_heat` - mass specific constant pressure specific heat per humid air _(J/kg/K)_.
* `specific_volume` - mass specific volume per humid air unit _(m3/kg)_.
* `temperature` - dry-bulb temperature _(by default, °C; see [how to change it](#units-systems))_.
* `wet_bulb_temperature` - wet-bulb temperature _(by default, °C; see [how to change it](#units-systems))_.
* `units_system` - configured units system _(enum)_.

## List of methods

For more information, see the docstrings.

### Methods of `Fluid` instances

* `factory` - returns a new fluid instance with no defined state.
* `with_state` - returns a new fluid instance with a defined state.
* `update` - updates the state of the fluid.
* `reset` - resets all non-trivial properties.
* `specify_phase` - specify the phase state for all further calculations.
* `unspecify_phase` - unspecify the phase state and go back to calculating it based on the inputs.
* `clone` - performs deep (full) copy of the fluid instance.
* `isentropic_compression_to_pressure` - the process of isentropic compression to a given pressure.
* `compression_to_pressure` - the process of compression to a given pressure.
* `isenthalpic_expansion_to_pressure` - the process of isenthalpic expansion to a given pressure.
* `isentropic_expansion_to_pressure` - the process of isentropic expansion to a given pressure.
* `expansion_to_pressure` - the process of expansion to a given pressure.
* `cooling_to_temperature` - the process of cooling to a given temperature.
* `cooling_to_enthalpy` - the process of cooling to a given enthalpy.
* `heating_to_temperature` - the process of heating to a given temperature.
* `heating_to_enthalpy` - the process of heating to a given enthalpy.
* `bubble_point_at_pressure` - bubble point at a given pressure.
* `bubble_point_at_temperature` - bubble point at a given temperature.
* `dew_point_at_pressure` - dew point at a given pressure.
* `dew_point_at_temperature` - dew point at a given temperature.
* `two_phase_point_at_pressure` - two-phase point at a given pressure.
* `mixing` - the mixing process.
* `as_json` - converts the fluid instance to a JSON string.
* `as_dict` - converts the fluid instance to a dict.

### Methods of `Mixture` instances

* `factory` - returns a new mixture instance with no defined state.
* `with_state` - returns a new mixture instance with a defined state.
* `update` - updates the state of the mixture.
* `reset` - resets all non-trivial properties.
* `specify_phase` - specify the phase state for all further calculations.
* `unspecify_phase` - unspecify the phase state and go back to calculating it based on the inputs.
* `clone` - performs deep (full) copy of the mixture instance.
* `cooling_to_temperature` - the process of cooling to a given temperature.
* `heating_to_temperature` - the process of heating to a given temperature.
* `as_json` - converts the mixture instance to a JSON string.
* `as_dict` - converts the mixture instance to a dict.

### Methods of `HumidAir` instances

* `factory` - returns a new humid air instance with no defined state.
* `with_state` - returns a new humid air instance with a defined state.
* `update` - updates the state of the humid air.
* `reset` - resets all properties.
* `clone` - performs deep (full) copy of the humid air instance.
* `dry_cooling_to_temperature` - the process of cooling without dehumidification to a given temperature.
* `dry_cooling_to_enthalpy` - the process of cooling without dehumidification to a given enthalpy.
* `wet_cooling_to_temperature_and_relative_humidity` - the process of cooling with dehumidification to a given temperature and relative humidity ratio.
* `wet_cooling_to_temperature_and_absolute_humidity` - the process of cooling with dehumidification to a given temperature and absolute humidity ratio.
* `wet_cooling_to_enthalpy_and_relative_humidity` - the process of cooling with dehumidification to a given enthalpy and relative humidity ratio.
* `wet_cooling_to_enthalpy_and_absolute_humidity` - the process of cooling with dehumidification to a given enthalpy and absolute humidity ratio.
* `heating_to_temperature` - the process of heating to a given temperature.
* `heating_to_enthalpy` - the process of heating to a given enthalpy.
* `humidification_by_water_to_relative_humidity` - the process of humidification by water (isenthalpic) to a given relative humidity ratio.
* `humidification_by_water_to_absolute_humidity` - the process of humidification by water (isenthalpic) to a given absolute humidity ratio.
* `humidification_by_steam_to_relative_humidity` - the process of humidification by steam (isothermal) to a given relative humidity ratio.
* `humidification_by_steam_to_absolute_humidity` - the process of humidification by steam (isothermal) to a given absolute humidity ratio.
* `mixing` - the mixing process.
* `as_json` - converts the humid air instance to a JSON string.
* `as_dict` - converts the humid air instance to a dict.

## Examples

### Pure fluids

To calculate the specific heat of saturated water vapor at _1 atm_:

```python
from pyfluids import Fluid, FluidsList

water_vapour = Fluid(FluidsList.Water).dew_point_at_pressure(101325)
print(water_vapour.specific_heat)  # 2079.937085633241
```

### Incompressible binary mixtures

To calculate the dynamic viscosity of propylene glycol aqueous solution 
with _60 %_ mass fraction at _100 kPa_ and _-20 °C_:

```python
from pyfluids import Fluid, FluidsList, Input

propylene_glycol = Fluid(FluidsList.MPG, 60).with_state(
    Input.pressure(100e3), Input.temperature(-20)
)
print(propylene_glycol.dynamic_viscosity)  # 0.13907391053938878
```

### Mixtures

To calculate the density of ethanol aqueous solution (with ethanol _40 %_ mass fraction) 
at _200 kPa_ and _4 °C_:

```python
from pyfluids import Mixture, FluidsList, Input

mixture = Mixture([FluidsList.Water, FluidsList.Ethanol], [60, 40]).with_state(
    Input.pressure(200e3), Input.temperature(4)
)
print(mixture.density)  # 883.3922771627963
```

### Humid air

To calculate the wet bulb temperature of humid air 
at _300 m_ above sea level, _30 °C_ and _50 %_ relative humidity:

```python
from pyfluids import HumidAir, InputHumidAir

humid_air = HumidAir().with_state(
    InputHumidAir.altitude(300),
    InputHumidAir.temperature(30),
    InputHumidAir.relative_humidity(50),
)
print(humid_air.wet_bulb_temperature)  # 21.917569033181564
```

### Equality of instances

You can simply determine the equality of `Fluid`, `Mixture` and `HumidAir` instances by its state.
Just use the equality operators (`==` or `!=`).
Exactly the same way you can compare inputs (`Input` and `InputHumidAir`).

For example:

```python
from pyfluids import HumidAir, InputHumidAir

humid_air = HumidAir().with_state(
    InputHumidAir.altitude(0),
    InputHumidAir.temperature(20),
    InputHumidAir.relative_humidity(50),
)
same_humid_air = HumidAir().with_state(
    InputHumidAir.pressure(101325),
    InputHumidAir.temperature(20),
    InputHumidAir.relative_humidity(50),
)
print(humid_air == same_humid_air)  # True
print(InputHumidAir.altitude(0) == InputHumidAir.pressure(101325))  # True
```

### Converting to a JSON string

The `Fluid`, `Mixture` and `HumidAir` classes have a method `as_json`,
which performs converting of instance to a JSON string.
For example, converting a `Fluid` instance to an _indented_ JSON string:

```python
from pyfluids import Fluid, FluidsList

refrigerant = Fluid(FluidsList.R32).dew_point_at_temperature(5)
print(refrigerant.as_json())
```

As a result:

```json5
{
    "compressibility": 0.8266625877210833,
    "conductivity": 0.013435453854396475,
    "critical_pressure": 5782000.0,
    "critical_temperature": 78.10500000000002,
    "density": 25.89088151061046,
    "dynamic_viscosity": 1.2606543144761657e-05,
    "enthalpy": 516105.7800378023,
    "entropy": 2136.2654412978777,
    "fraction": 100,
    "freezing_temperature": null,
    "internal_energy": 479357.39743435377,
    "kinematic_viscosity": 4.869105418289953e-07,
    "max_pressure": 70000000.0,
    "max_temperature": 161.85000000000002,
    "min_pressure": 47.999893876059375,
    "min_temperature": -136.80999999999997,
    "molar_mass": 0.052024,
    "name": "R32",
    "phase": "TwoPhase",
    "prandtl": 1.2252282243443504,
    "pressure": 951448.019691762,
    "quality": 100.0,
    "sound_speed": 209.6337575990297,
    "specific_heat": 1305.7899441785378,
    "specific_volume": 0.03862363664945844,
    "surface_tension": 0.010110117241546162,
    "temperature": 5.0,
    "triple_pressure": 47.999893876059375,
    "triple_temperature": -136.80999999999997,
    "units_system": "SIWithCelsiusAndPercents"
}
```

### Converting to a Python dict

The `Fluid`, `Mixture` and `HumidAir` classes have a method `as_dict`,
which performs converting of instance to a Python dict.
For example:

```python
from pyfluids import Fluid, FluidsList

refrigerant = Fluid(FluidsList.R32).dew_point_at_temperature(5)
print(refrigerant.as_dict())  # {'compressibility': 0.8266625877210833, 'conductivity': ... 
```

### Deep cloning

The `Fluid`, `Mixture` and `HumidAir` classes have a method `clone`, 
which performs deep (full) copy of instance:

```python
from pyfluids import Fluid, FluidsList, Input

origin = Fluid(FluidsList.Water).with_state(
    Input.pressure(101325), Input.temperature(20)
)
clone = origin.clone()
print(origin == clone)  # True
clone.update(Input.pressure(101325), Input.temperature(30))
print(origin == clone)  # False
```

### Adding other properties

* [Example for the `Fluid` and `Mixture`](https://github.com/portyanikhin/PyFluids/blob/main/tests/fluids/test_fluid_extended.py).
* [Example for the `HumidAir`](https://github.com/portyanikhin/PyFluids/blob/main/tests/fluids/test_input_extended.py).

### Adding other inputs

* [Example for the `Fluid` and `Mixture`](https://github.com/portyanikhin/PyFluids/blob/main/tests/humid_air/test_humid_air_extended.py).
* [Example for the `HumidAir`](https://github.com/portyanikhin/PyFluids/blob/main/tests/humid_air/test_input_humid_air_extended.py).