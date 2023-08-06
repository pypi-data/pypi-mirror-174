from datetime import datetime
from pathlib import Path

import skyfield.api as skyfield_api

from .base import spo_types
from .base.models import TLE_FILES_DIRECTORY, TLEFile, TLEObject, de421
from .base.outputs import ObservationObject, PositionObject
from .settings import CELESTRAK_ACTIVE_TLE_URL, CELESTRAK_WEATHER_TLE_URL


class TLEFileWeather(TLEFile):
    directory: Path = TLE_FILES_DIRECTORY
    default_url = CELESTRAK_WEATHER_TLE_URL
    name = "weather_satellites"


class TLEFileSatelliteActive(TLEFile):
    directory: Path = TLE_FILES_DIRECTORY
    default_url = CELESTRAK_ACTIVE_TLE_URL
    name = "actives_satellites"


class SatelliteWeather(TLEObject):
    """
    This object allow to work with weather satellites.
    """

    tle_file_object: type[TLEFile] = TLEFileWeather


class SatelliteActive(TLEObject):
    """
    This object allow to work with actives satellites.
    """

    tle_file_object: type[TLEFile] = TLEFileSatelliteActive


class PlanetObserver:
    """
    This object allow planets observations.
    """

    directory: Path = TLE_FILES_DIRECTORY
    planets = de421
    planets_names = [
        "JUPITER",
        "MARS",
        "MERCURY",
        "MOON",
        "NEPTUNE",
        "PLUTO",
        "SATURN",
        "SUN",
        "URANUS",
        "VENUS",
    ]

    def __init__(
        self, observation_position_latitude, observation_position_longitude
    ):
        (
            self.observation_position_latitude,
            self.observation_position_longitude,
        ) = (
            observation_position_latitude,
            observation_position_longitude,
        )
        bluffton = skyfield_api.wgs84.latlon(
            self.observation_position_latitude,
            self.observation_position_longitude,
        )

        earth: spo_types.VectorSum = self.planets["earth"]  # type: ignore
        self.ssb_bluffton: spo_types.VectorSum = earth + bluffton

    def get_position(
        self, planetname: str, date: datetime | None = None
    ) -> PositionObject:
        """
        get the satelit position.
        """

        if planetname.upper() not in self.planets_names:
            raise Exception(f"< {planetname} > planet is not provided")
        try:
            planet: spo_types.ChebyshevPosition = self.planets[planetname]  # type: ignore
        except KeyError:
            planet: spo_types.ChebyshevPosition = self.planets[
                f"{planetname.upper()}_BARYCENTER"
            ]  # type: ignore
        if date is None:
            t: spo_types.Time = skyfield_api.load.timescale().now()
        else:
            date = date.replace(tzinfo=skyfield_api.utc)
            t: spo_types.Time = skyfield_api.load.timescale().from_datetime(
                date
            )

        position: spo_types.Astrometric = (
            self.planets["earth"].at(t).observe(planet)  # type: ignore
        )
        lat_lon: tuple[
            spo_types.Angle, spo_types.Angle
        ] = skyfield_api.wgs84.latlon_of(position)
        latitude = lat_lon[0]
        longitude = lat_lon[1]
        height: spo_types.Distance = skyfield_api.wgs84.height_of(position)
        return PositionObject(
            longitude=float(longitude.degrees),  # type: ignore
            latitude=float(latitude.degrees),  # type: ignore
            altitude_kms=float(height.km),  # type: ignore
            timeposition_utc=t.utc_iso(),  # type: ignore
        )

    def get_observation(
        self, planetname: str, date: datetime | None = None
    ) -> ObservationObject:

        if planetname.upper() not in self.planets_names:
            raise Exception(f"< {planetname} > planet is not provided")
        try:
            planet: spo_types.ChebyshevPosition = self.planets[
                planetname
            ]  # type: ignore
        except KeyError:
            planet: spo_types.ChebyshevPosition = self.planets[
                f"{planetname.upper()}_BARYCENTER"
            ]  # type: ignore

        ts: spo_types.Timescale = skyfield_api.load.timescale()

        if date:
            date = date.replace(tzinfo=skyfield_api.utc)
        t: spo_types.Time = ts.from_datetime(date) if date else ts.now()
        subpoint: spo_types.Astrometric = self.ssb_bluffton.at(t).observe(  # type: ignore
            planet
        )

        app: spo_types.Apparent = subpoint.apparent()
        _: tuple[
            spo_types.Angle, spo_types.Angle, spo_types.Distance
        ] = app.altaz()
        return ObservationObject(
            degrees_vertical=float(_[0].degrees),  # type: ignore
            degrees_horizontal=float(_[1].degrees),  # type: ignore
            distance_kms=float(_[2].km),  # type: ignore
            timeposition_utc=t.utc_iso(),  # type: ignore
        )
