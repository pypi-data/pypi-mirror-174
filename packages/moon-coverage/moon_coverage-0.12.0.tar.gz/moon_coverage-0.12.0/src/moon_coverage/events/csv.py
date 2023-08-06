"""Events csv file module."""

from .event import AbstractEventsFile
from ..html import Html, table
from ..misc import depreciated


class CsvEventsFile(AbstractEventsFile):
    """CSV events file object.

    Parameters
    ----------
    fname: str or pathlib.Path
        Input CSV event filename.
    primary_key: str, optional
        Header primary key (default: `name`)
    header: str, optional
        Optional header definition (to be appended at the beginning of the file).

    """
    fields, rows = [], []

    def __init__(self, fname, primary_key='name', header=None):
        super().__init__(fname, primary_key, header)

    def __getitem__(self, key):
        if isinstance(key, str) and key.lower() in self.fields:
            i = self.fields.index(key.lower())
            return [row[i] for row in self.rows]

        return super().__getitem__(key)

    def _ipython_key_completions_(self):
        return list(self.keys()) + self.fields

    def _read_rows(self):
        """Read CSV rows content."""
        content = (self.header + '\n') if self.header else ''
        content += self.fname.read_text(encoding='utf-8')

        header, *lines = content.splitlines()

        # Parse header columns
        self.fields = [
            field.lower().replace('#', '').strip() if field else f'column_{i}'
            for i, field in enumerate(header.split(','))
        ]

        # Strip rows content
        self.rows = [
            tuple(value.strip() for value in line.split(','))
            for line in lines
            if not line.startswith('#') and line.strip()
        ]

    @property
    def csv(self):
        """Formatted CSV content."""
        return Html(table(self.rows, header=self.fields))


@depreciated('0.12.0')
class EventsFile(CsvEventsFile):
    """OLD Event file object replaced by CsvEventFile."""
