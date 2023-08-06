"""ESA variables."""

from pathlib import Path


DATA = Path.home() / '.moon-coverage' / 'esa-mk'

DATA.mkdir(exist_ok=True, parents=True)
