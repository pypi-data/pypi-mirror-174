from typing import Literal

from skyfield.api import EarthSatellite
from skyfield.jpllib import ChebyshevPosition
from skyfield.positionlib import Apparent, Astrometric
from skyfield.timelib import Time, Timescale
from skyfield.toposlib import GeographicPosition
from skyfield.units import Angle, Distance
from skyfield.vectorlib import VectorSum

ORBIT_DIRECTION = Literal["GEOSTATIONARY", "E_TO_W", "W_TO_E"]
