"""ESA events files module."""

from ..events import CsvEventsFile
from ..misc import depreciated


@depreciated('0.12.0', 'read_events()')
class EsaMissionPhases(CsvEventsFile):
    """ESA mission phases event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Name')


@depreciated('0.12.0', 'read_events()')
class EsaMissionTimeline(CsvEventsFile):
    """ESA mission timeline event file."""

    def __init__(self, fname):
        super().__init__(fname, primary_key='Event Name')


@depreciated('0.12.0', 'read_events()')
class EsaMissionEvents(CsvEventsFile):
    """Generic ESA mission events file.

    By default, a header is appended to the file with the
    following parameters:

    .. code-block:: text

        # name, t_start, t_end, subgroup, working_group

    but you can provide your own or set it to ``None`` is
    the first row is already the header.

    The primary key is also initialized at ``name`` but you
    can use any other column.

    """

    def __init__(
        self, fname,
        primary_key='name',
        header='# name, t_start, t_end, subgroup, working_group'
    ):
        super().__init__(fname, primary_key=primary_key, header=header)
