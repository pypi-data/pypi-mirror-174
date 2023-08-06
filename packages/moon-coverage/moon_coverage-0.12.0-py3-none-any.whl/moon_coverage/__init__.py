"""Moon coverage module."""

from importlib.metadata import version

from .esa import ESA_CREMAS, ESA_MK, JUICE_CREMAS
from .events import read_events
from .maps import (
    CALLISTO, EARTH, EUROPA, GANYMEDE, IO, JUPITER, MAPS, MERCURY, MOON, VENUS
)
from .rois import (
    ROI, CallistoROIs, GanymedeROIs, GeoJsonROI, KmlROIsCollection
)
from .spice import (
    MetaKernel, SpicePool, SpiceRef, datetime, et, sorted_datetimes, tdb, utc
)
from .trajectory import TourConfig, Trajectory


__all__ = [
    'CALLISTO',
    'EARTH',
    'EUROPA',
    'GANYMEDE',
    'MOON',
    'IO',
    'JUPITER',
    'VENUS',
    'MERCURY',
    'MAPS',
    'ROI',
    'ESA_MK',
    'ESA_CREMAS',    # depreciated
    'JUICE_CREMAS',  # depreciated
    'GeoJsonROI',
    'KmlROIsCollection',
    'GanymedeROIs',
    'CallistoROIs',
    'MetaKernel',
    'SpicePool',
    'SpiceRef',
    'datetime',
    'sorted_datetimes',
    'et',
    'tdb',
    'utc',
    'read_events',
    'TourConfig',
    'Trajectory',
]

__version__ = version('moon-coverage')
