"""Generic Events file reader module."""

from pathlib import Path

from .csv import CsvEventsFile
from .evf import EvfEventsFile
from .itl import ItlEventsFile


def read_events(fname, **kwargs):
    """Read ESA events file.

    Parameters
    ----------
    fname: str or pathlib.Path
        File name to parse
    **kwargs:
        Parsing properties.

    Returns
    -------
    CsvEventFile, EvfEventFile or ItlEventFile
        Parsed events list from the provided file.

    Raises
    ------
    FileNotFoundError
        If the filename provided does not exist.
    IOError
        When it's not possible to parse the provided file.

    Note
    ----
    The function will try to guess the layout of the file based on
    the filename extension.

    See Also
    --------
    moon_coverage.events.CsvEventsFile
    moon_coverage.events.EvfEventsFile
    moon_coverage.events.ItlEventsFile

    """
    fname = Path(fname)

    if not fname.exists():
        raise FileNotFoundError(fname)

    ext = fname.suffix.lower()

    if ext == '.evf':
        return EvfEventsFile(fname)

    if ext == '.itl':
        return ItlEventsFile(fname, evf=kwargs.get('evf'))

    if kwargs:
        return CsvEventsFile(fname, **kwargs)

    csv_kwargs = [
        {'primary_key': 'Name'},        # mission_phases.csv
        {'primary_key': 'Event Name'},  # mission_timeline.csv
        {                               # mission_events.csv
            'primary_key': 'name',
            'header': '# name, t_start, t_end, subgroup, working_group',
        }
    ]

    for kwargs in csv_kwargs:
        try:
            return CsvEventsFile(fname, **kwargs)
        except (KeyError, ValueError, IOError):
            pass

    raise IOError(f'Impossible to parse the events in: {fname}')
