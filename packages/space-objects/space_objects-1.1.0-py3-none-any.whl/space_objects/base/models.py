from datetime import datetime, timedelta
from operator import gt, lt
from pathlib import Path

import numpy as np
import skyfield.api as skyfield_api

from ..settings import TLE_FILES_DIRECTORY
from . import spo_types
from .outputs import (
    ForecastListObject,
    ForecastObject,
    ObservationObject,
    OrbitObject,
    PositionObject,
)

load_de421 = skyfield_api.Loader(str(TLE_FILES_DIRECTORY))
de421 = load_de421("de421.bsp")  # the planets file


class TLEFile:
    directory: Path
    default_url: str
    name: str

    def __init__(self) -> None:
        today = datetime.now()
        self.filename = (
            f"{self.name}_{today.year}_{today.month}_{today.day}.txt"
        )
        self.filepath = self.directory / self.filename
        self._satellites: list[
            spo_types.EarthSatellite
        ] = skyfield_api.load.tle_file(
            self.default_url,
            filename=str(self.filepath),
            reload=self.filepath.exists() is False,
        )
        self.satellites: dict[str, spo_types.EarthSatellite] = {
            sat.name: sat for sat in self._satellites
        }
        self.tle_content = [
            i.strip() for i in self.filepath.read_text().splitlines()
        ]

    def list(self):
        return sorted(list(self.satellites.keys()))


class TLEObject:
    tle_file_object: type[TLEFile]

    def __init__(
        self,
        satellite_name: str,
        observation_position_longitude: float = 0.0,
        observation_position_latitude: float = 0.0,
    ):
        self.tle_file: TLEFile = self.tle_file_object()
        if satellite_name not in self.tle_file.satellites:
            raise Exception(f"< {satellite_name} > not in tle file.")
        self.satellite_name = satellite_name
        self.observation_position_longitude = observation_position_longitude
        self.observation_position_latitude = observation_position_latitude

        self.satellite: spo_types.EarthSatellite = self.tle_file.satellites[
            self.satellite_name
        ]

        rotations_number = None
        self.satellite_rotation_direction: spo_types.ORBIT_DIRECTION = (
            "GEOSTATIONARY"
        )
        for line in self.tle_file.tle_content:
            if line.startswith(f"2 {self.satellite.model.satnum}"):
                _a, _b = line.split()[-1], line.split()[-2]
                rotations_number = float(_a) if "." in _a else float(_b)
                self.satellite_rotation_direction = (
                    "W_TO_E" if float(line.split()[2]) < 90 else "E_TO_W"
                )
                break
        self.satellite_rotation_seconds: float = 0.0
        if rotations_number:
            self.satellite_rotation_seconds = 24 / rotations_number * 3600
        bluffton: spo_types.GeographicPosition = skyfield_api.wgs84.latlon(
            self.observation_position_latitude,
            self.observation_position_longitude,
        )

        earth: spo_types.VectorSum = de421["earth"]  # type: ignore
        self.ssb_bluffton: spo_types.VectorSum = earth + bluffton
        self.ssb_satellite: spo_types.VectorSum = earth + self.satellite

    def get_position(self, date: datetime | None = None) -> PositionObject:
        """
        get the satelit position.
        """
        t: spo_types.Time
        if date is None:
            t = skyfield_api.load.timescale().now()
        else:
            date = date.replace(tzinfo=skyfield_api.utc)
            t = skyfield_api.load.timescale().from_datetime(date)

        subpoint: spo_types.GeographicPosition = skyfield_api.wgs84.subpoint(
            self.satellite.at(t)
        )

        return PositionObject(
            longitude=float(subpoint.longitude.degrees),  # type: ignore
            latitude=float(subpoint.latitude.degrees),  # type: ignore
            altitude_kms=float(subpoint.elevation.km),  # type: ignore
            timeposition_utc=t.utc_iso(),  # type: ignore
        )

    def get_observation(
        self, date: datetime | None = None
    ) -> ObservationObject:
        """
        get observation data from the ground.
        return the x and y angle from your position.
        """
        t: spo_types.Time
        if date is None:
            t = skyfield_api.load.timescale().now()
        else:
            date = date.replace(tzinfo=skyfield_api.utc)
            t = skyfield_api.load.timescale().from_datetime(date)
        topocentric2: spo_types.Astrometric = self.ssb_bluffton.at(t).observe(
            self.ssb_satellite
        )
        app: spo_types.Apparent = topocentric2.apparent()
        _: tuple[
            spo_types.Angle, spo_types.Angle, spo_types.Distance
        ] = app.altaz()
        return ObservationObject(
            degrees_vertical=float(_[0].degrees),  # type: ignore
            degrees_horizontal=float(_[1].degrees),  # type: ignore
            distance_kms=float(_[2].km),  # type: ignore
            timeposition_utc=t.utc_iso(),  # type: ignore
        )

    def get_orbit(self, date: datetime | None = None) -> OrbitObject:
        """
        get the orbit of the object.

        Each point will have a step of 10 seconds.
        """
        t: datetime
        if date is None:
            t = datetime.utcnow()
        else:
            t = date

        seconds: np.ndarray = np.arange(
            0, round(self.satellite_rotation_seconds), 10
        )  # 1h32
        ts: spo_types.Timescale = skyfield_api.load.timescale(builtin=True)
        times: spo_types.Time = ts.utc(
            t.year, t.month, t.day, t.hour, t.minute, seconds
        )  # type: ignore
        subpoint: spo_types.GeographicPosition = skyfield_api.wgs84.subpoint(
            self.satellite.at(times)
        )
        orbit = list(
            zip(
                subpoint.longitude.degrees,  # type: ignore
                subpoint.latitude.degrees,  # type: ignore
                subpoint.elevation.km,  # type: ignore
                times.utc_iso(),
            )
        )
        orbit_one: list[PositionObject] = []
        orbit_two: list[PositionObject] = []
        _oper = lt if self.satellite_rotation_direction == "W_TO_E" else gt
        test = False
        for idx, elem in enumerate(orbit):
            try:
                posobj = PositionObject(
                    longitude=float(elem[0]),
                    latitude=float(elem[1]),
                    altitude_kms=float(elem[2]),
                    timeposition_utc=elem[3],
                )
                if _oper(orbit[idx + 1][0], elem[0]):
                    test = True
                if test:
                    orbit_two.append(posobj)
                else:
                    orbit_one.append(posobj)
            except IndexError:
                break
        if orbit_two:
            orbit_one.append(orbit_two.pop(0))
        return OrbitObject(
            part_one=orbit_one,
            part_two=orbit_two,
            direction=self.satellite_rotation_direction,
        )

    def get_observations_forecast_24H(
        self,
        altitude_degrees=15,
        include_observation=True,
        include_position=True,
    ) -> ForecastListObject:
        """
        Return the possible observations for the observer position
        with a forecast of 24 hours.
        """

        def format_data(ti):
            topocentric2: spo_types.Astrometric = self.ssb_bluffton.at(
                ti
            ).observe(
                self.ssb_satellite
            )  # type: ignore
            app: spo_types.Apparent = topocentric2.apparent()
            _: tuple[
                spo_types.Angle, spo_types.Angle, spo_types.Distance
            ] = app.altaz()
            angle = round(_[0].degrees)  # type: ignore
            ti_str = ti.utc_strftime("%Y-%m-%dT%H:%M:%SZ")
            res = {
                "time": ti_str,
                "is_sunlit": bool(self.satellite.at(ti).is_sunlit(de421)),
                "angle_x": angle,
            }

            if include_position:
                subpoint = skyfield_api.wgs84.subpoint(self.satellite.at(ti))
                res["position"] = PositionObject(
                    longitude=float(subpoint.longitude.degrees),  # type: ignore
                    latitude=float(subpoint.latitude.degrees),  # type: ignore
                    altitude_kms=float(subpoint.elevation.km),  # type: ignore
                    timeposition_utc=ti_str,
                )

            if include_observation:
                res["observation"] = ObservationObject(
                    degrees_vertical=float(_[0].degrees),  # type: ignore
                    degrees_horizontal=float(_[1].degrees),  # type: ignore
                    distance_kms=float(_[2].km),  # type: ignore
                    timeposition_utc=ti_str,
                )

            return ForecastObject(**res)

        bluffton: spo_types.GeographicPosition = skyfield_api.wgs84.latlon(
            self.observation_position_latitude,
            self.observation_position_longitude,
        )
        utcnow = datetime.utcnow().replace(tzinfo=skyfield_api.utc)
        futur = utcnow + timedelta(days=1)
        futur = futur.replace(hour=23, minute=59, second=59)
        t0: spo_types.Time = skyfield_api.load.timescale().from_datetime(
            utcnow
        )
        t1: spo_types.Time = skyfield_api.load.timescale().from_datetime(futur)
        times: spo_types.Time
        times, _ = self.satellite.find_events(
            bluffton, t0, t1, altitude_degrees=altitude_degrees
        )
        return ForecastListObject(
            sorted(
                [format_data(ti) for ti in times],
                key=lambda x: x.time,
            )
        )  # type: ignore
