# space_objects

- ![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)


- ![coverage](coverage-badge.svg)


## Presentation

Very simple objects which provides methods to get position and observation for space objects like the ISS station.

- Allow to get position, observation and orbit data for actives and weather satellites.
- Allow to get position, observation data for planets.

This project use the great [skyfield package](https://github.com/skyfielders/python-skyfield),  thanks to it's maintainers.

## Motivation

I was working on a project of an ISS tracker build on a rasperry pi and servo motors.

I needed the ISS observation angles degrees for a given position, the position of the ISS in real time, this ISS orbit and a list of the forecast possible observations from my position.

I needed to be web service agnostic and to be autonomous for the needed data.

Now than this project is ready i decided to clean my researches and algos in appropriates repositories in the hope there will be usefull.

## Environment Variable

This library support one environment variable, this variable is not mandatory.

The skyfield library will load some files, like TLE files and de421.bsp, by default space_objects create a directory `tle_files` in your script path and files will be download in this directory.

You can easily overide this behaviour with an environment variable: `TLE_FILES_DIRECTORY=< you custom path >`

### Get the ISS position

```python
from space_objects.models import SatelliteActive

my_position = {
    "observation_position_longitude": 1.433333,
    "observation_position_latitude": 43.6,
}

iss_object = SatelliteActive(satellite_name="ISS (ZARYA)", **my_position)
position = iss_object.get_position()
```
```python
print(position)
PositionObject(
  longitude=95.42870673510215,
  latitude=-45.701086600061714,
  altitude_kms=433.23953982510665,
  timeposition_utc='2022-10-31T12:48:35Z'
)

```
### Get the ISS observation

```python
from space_objects.models import SatelliteActive

my_position = {
    "observation_position_longitude": 1.433333,
    "observation_position_latitude": 43.6,
}

iss_object = SatelliteActive(satellite_name="ISS (ZARYA)", **my_position)
observation = iss_object.get_observation()
```
```python
print(observation)
ObservationObject(
  degrees_vertical=-59.92007436232538,
  degrees_horizontal=124.47513589616938,
  distance_kms=11504.317997710621,
  timeposition_utc='2022-10-31T12:48:35Z'
)
```

![vertical_orientation](assets/images/vertical_orientation.png)
![horyzontal_orientation](assets/images/horyzontal_orientation.png)

### Get the 24 hours forecast positions and observations for the ISS

```python
forecast_observations = iss_object.get_observations_forecast_24H()
forecast_observations.tprint()
```
```text
timeposition_utc        degrees_vertical  is_sunlit
--------------------  ------------------  -----------
2022-11-01T01:41:39Z                  15  False
2022-11-01T01:44:19Z                  85  False
2022-11-01T01:47:00Z                  15  False
2022-11-01T03:19:29Z                  15  False
2022-11-01T03:21:27Z                  24  False
2022-11-01T03:23:25Z                  15  False
2022-11-01T04:57:16Z                  15  False
2022-11-01T04:59:00Z                  21  True
2022-11-01T05:00:43Z                  15  True
2022-11-01T06:33:41Z                  15  True
2022-11-01T06:36:18Z                  52  True
2022-11-01T06:38:54Z                  15  True
2022-11-01T08:11:01Z                  15  True
2022-11-01T08:12:53Z                  23  True
2022-11-01T08:14:45Z                  15  True
```

```python
forecast_observation = forecast_observations[10].observation
forecast_position = forecast_observations[10].position
print(forecast_position)
print(forecast_observation)
```
```text
PositionObject(
  longitude=3.2171481263959283,
  latitude=46.0182975420938,
  altitude_kms=422.3427194167064,
  timeposition_utc='2022-11-01T06:36:18Z'
)
ObservationObject(
  degrees_vertical=52.03750100701985,
  degrees_horizontal=27.071376289371536,
  distance_kms=525.8886708185943,
  timeposition_utc='2022-11-01T06:36:18Z'
)
```

![forecast_vertical_orientation](assets/images/forecast_vertical_orientation.png)
![forecast_horyzontal_orientation](assets/images/forecast_horyzontal_orientation.png)


### Get the Sun position and observation

```python
from space_objects.models import PlanetObserver

my_position = {
    "observation_position_longitude": 1.433333,
    "observation_position_latitude": 43.6,
}

planet_observer = PlanetObserver(**my_position)
sun_observation = planet_observer.get_observation("SUN")
sun_position = planet_observer.get_position("SUN")

print(sun_observation)
print(sun_position)
```
```text
ObservationObject(
  degrees_vertical=27.123628441099548,
  degrees_horizontal=209.69557585058428,
  distance_kms=148520276.74009204,
  timeposition_utc='2022-10-31T13:26:06Z'
)
PositionObject(
  longitude=-25.61420206366428,
  latitude=-14.209948450817524,
  altitude_kms=148516819.7673485,
  timeposition_utc='2022-10-31T13:26:06Z'
)
```

![vertical_orientation_sun](assets/images/vertical_orientation_sun.png)
![horyzontal_orientation_sun](assets/images/horyzontal_orientation_sun.png)

## Notebooks

- we maintain some Jupyter notebooks for concretes samples and demonstrations.

## Development

- this project use `poetry`
- the code quality tools used are:
  - `black`
  - `isort`
  - `flake8`
  - `coverage`
  - `pytest`
  - `genbadge`

- a precommit hook may be installed with the `pre-commit` python package
- the pre commit hook will play:
  - `black`
  - `isort`
  - `flake8`
  - `coverage run -m pytest -W ignore`
  - `coverage xml`
  - `genbadge coverage -i coverage.xml`


### install the development environment:

```bash
poetry install
pre-commit install
```

### Getting Started

```bash
poetry shell
export PYTHONPATH=.
```


## Authors

  - **Olivier Larrieu** - [larrieu-olivier](https://github.com/larrieu-olivier)

