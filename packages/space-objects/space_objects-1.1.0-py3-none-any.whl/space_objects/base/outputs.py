from dataclasses import dataclass

from tabulate import tabulate

from .spo_types import ORBIT_DIRECTION


@dataclass
class PositionObject:
    """
    An object position representation.
    """

    longitude: float
    latitude: float
    altitude_kms: float
    timeposition_utc: str

    @property
    def simple_list(self):
        return [
            self.longitude,
            self.latitude,
            self.altitude_kms,
            self.timeposition_utc,
        ]

    def to_dict(self):
        return {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "altitude_kms": self.altitude_kms,
            "timeposition_utc": self.timeposition_utc,
        }

    def tprint(self) -> None:
        """
        Tabular print for pretty display
        """
        print(
            tabulate(
                [self.simple_list],
                headers=[
                    "longitude",
                    "latitude",
                    "altitude_kms",
                    "timeposition_utc",
                ],
            )
        )


@dataclass
class ObservationObject:
    """
    An object observation representation.
    """

    degrees_vertical: float
    degrees_horizontal: float

    distance_kms: float  # the distance between the observer and the object
    timeposition_utc: str

    @property
    def simple_list(self):
        return [
            self.degrees_vertical,
            self.degrees_horizontal,
            self.distance_kms,
            self.timeposition_utc,
        ]

    def to_dict(self):
        return {
            "degrees_vertical": self.degrees_vertical,
            "degrees_horizontal": self.degrees_horizontal,
            "distance_kms": self.distance_kms,
            "timeposition_utc": self.timeposition_utc,
        }

    def tprint(self) -> None:
        """
        Tabular print for pretty display
        """
        print(
            tabulate(
                [self.simple_list],
                headers=[
                    "degrees_vertical",
                    "degrees_horizontal",
                    "distance_kms",
                    "timeposition_utc",
                ],
            )
        )


@dataclass
class ForecastObject:
    time: str
    is_sunlit: bool
    angle_x: float | int
    observation: ObservationObject
    position: PositionObject

    def to_dict(self):
        _ = {
            "degrees_vertical": self.angle_x,
            "is_sunlit": self.is_sunlit,
            "timeposition_utc": self.time,
        }
        if self.observation:
            _["observation"] = self.observation.to_dict()
        if self.position:
            _["position"] = self.position.to_dict()
        return _


class ForecastListObject(list[ForecastObject]):
    def to_dict(self):
        return [i.to_dict() for i in self]

    def tprint(self) -> None:
        """
        Tabular print for pretty display
        """
        print(
            tabulate(
                [(i.time, i.angle_x, i.is_sunlit) for i in self],
                headers=[
                    "timeposition_utc",
                    "degrees_vertical",
                    "is_sunlit",
                ],
            )
        )


@dataclass
class OrbitObject:
    """
    An orbit object representation.

    An orbit is divided in two part, before and after meridian.
    """

    part_one: list[PositionObject]
    part_two: list[PositionObject]
    direction: ORBIT_DIRECTION

    @property
    def date_end(self):
        _ = max(
            [
                self.part_one[0],
                self.part_one[-1],
                self.part_two[0],
                self.part_two[-1],
            ],
            key=lambda e: e.timeposition_utc,
        )
        return _.timeposition_utc

    @property
    def date_start(self):
        _ = min(
            [
                self.part_one[0],
                self.part_one[-1],
                self.part_two[0],
                self.part_two[-1],
            ],
            key=lambda e: e.timeposition_utc,
        )
        return _.timeposition_utc

    def to_dict(self):
        return {
            "part_one": [i.to_dict() for i in self.part_one],
            "part_two": [i.to_dict() for i in self.part_two],
            "date_start": self.date_start,
            "date_end": self.date_end,
            "direction": self.direction,
        }
