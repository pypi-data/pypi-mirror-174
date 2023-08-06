"""ESA specific module."""

from .api import debug_esa_api, get_mk, get_tag
from .event_file import EsaMissionEvents, EsaMissionPhases, EsaMissionTimeline
from .export import export_timeline
from .metakernel import ESA_MK, EsaMetakernels
from ..misc import DepreciationHelper
from ..spice import MetaKernel


__all__ = [
    'ESA_MK',
    'EsaMissionEvents',    # depreciated -> read_events()
    'EsaMissionPhases',    # depreciated -> read_events()
    'EsaMissionTimeline',  # depreciated -> read_events()
    'export_timeline',
    'get_mk',
    'get_tag',
    'debug_esa_api',
]


# Depreciations
ESA_CREMAS = DepreciationHelper('ESA_CREMAS', 'ESA_MK', ESA_MK)
JUICE_CREMAS = DepreciationHelper('JUICE_CREMAS', "ESA_MK['JUICE']", ESA_MK['JUICE'])
EsaCremasCollection = DepreciationHelper('EsaCremasCollection', 'EsaMetakernels',
                                         EsaMetakernels)
CReMAs = DepreciationHelper('CReMAs', 'ESA_CREMAS', ESA_CREMAS)
JUICE_CReMA = DepreciationHelper('JUICE_CReMA', 'JUICE_CREMAS', JUICE_CREMAS)
CReMAMetaKernel = DepreciationHelper('CReMAMetaKernel', 'MetaKernel', MetaKernel)
debug_esa_crema = DepreciationHelper('debug_esa_crema', 'debug_esa_api', debug_esa_api)
