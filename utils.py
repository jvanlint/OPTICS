import zoneinfo
import logging


logger = logging.getLogger(__name__)


def get_timezones():
    zones = []
    try:
        zones = zoneinfo.available_timezones()
        zones = sorted(zones)
    except zoneinfo.ZoneInfoNotFoundError:
        logger.error("No timezone file found /n pip install tzdata")
    return [(name, name) for name in zones]

