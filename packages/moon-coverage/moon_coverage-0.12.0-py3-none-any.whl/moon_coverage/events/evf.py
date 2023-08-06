"""EVF events file module."""

import re

from .event import AbstractEventsCollection, AbstractEventsFile
from ..html import table
from ..spice.datetime import datetime, np_datetime_str, sorted_datetimes


EVF_FMT = re.compile(r'([\w_-]+)(?:\s*\(COUNT\s*=\s*(\d*)\))?')


def evf_key(key) -> tuple:
    """Parse EVF key and count number."""
    if match := EVF_FMT.findall(key):
        return match[0][0].upper(), int(match[0][1]) if match[0][1] else None

    raise KeyError(f'Invalid EVF key: {key}')


def evf_rows(content):
    """Read EVF content to extract comments and data."""
    comments = []
    data = {}
    for line in content.splitlines():
        if line.startswith('#'):
            comments.append(line[1:].strip())
            continue

        mapps_time, key = line.split(maxsplit=1)

        # Parse time as an explicit ISO string
        time = np_datetime_str(datetime(mapps_time))

        # Parse EVF key
        keyword, count = evf_key(key)

        if keyword not in data:
            data[keyword] = [time]
        elif len(data[keyword]) + 1 == count:
            data[keyword].append(time)
        else:
            raise KeyError(f'`{keyword}` missing (COUNT = {count - 1})')

    return comments, data


class EvfEventsFile(AbstractEventsFile):
    """EVF event file object.

    EVF are in MAPPS format.

    Parameters
    ----------
    fname: str or pathlib.Path
        EVF filename to parse.

    """

    def __init__(self, fname):
        super().__init__(fname, 'name')  # primary_key='name'

    def _repr_html_(self):
        rows = [
            [
                event.key,
                len(event) if isinstance(event, AbstractEventsCollection) else '-',
                event.start_date,
                event.stop_date,
            ]
            for event in self
        ]
        return table(rows, header=('event', '#', 't_start', 't_stop'))

    def __contains__(self, key):
        if isinstance(key, str):
            keyword, _ = evf_key(key)
            if keyword in self.data.keys():
                return True

        return super().__contains__(key)

    def __getitem__(self, key):
        keyword, count = evf_key(key)

        if keyword not in self.data.keys():
            raise KeyError(key)

        events = self.data[keyword]

        if count is None:
            return events

        if 0 < count <= len(events):
            return events[count - 1]

        raise IndexError(count)

    def _read_rows(self):
        """Read EVF rows content."""
        content = self.fname.read_text(encoding='utf-8')

        # EVF columns
        self.fields = ['event time [utc]', 'name']

        # Extract comments and rows content (and check COUNT values)
        self.comments, data = evf_rows(content)

        # Flatten the rows
        self.rows = sorted_datetimes([
            (time, key) for key, times in data.items() for time in times
        ], index=0)
