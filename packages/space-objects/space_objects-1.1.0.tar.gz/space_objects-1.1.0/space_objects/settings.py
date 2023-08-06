import os
from pathlib import Path

TLE_FILES_DIRECTORY = Path(os.getenv("TLE_FILES_DIRECTORY", "tle_files"))
TLE_FILES_DIRECTORY.mkdir(exist_ok=True, parents=True)

CELESTRAK_ACTIVE_TLE_URL = (
    "https://www.celestrak.com/NORAD/elements/active.txt"
)
CELESTRAK_WEATHER_TLE_URL = (
    "https://www.celestrak.com/NORAD/elements/weather.txt"
)
