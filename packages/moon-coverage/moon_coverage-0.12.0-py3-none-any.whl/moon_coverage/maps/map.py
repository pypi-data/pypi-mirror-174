"""Map module."""

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt

from PIL import Image

from ..projections.axes import ProjAxes
from ..projections.equi import Equirectangular
from ..ticks import lat_ticks, lon_e_ticks


# ByPass DecompressionBombWarning for large images
# See: https://github.com/zimeon/iiif/issues/11#issuecomment-131129062
Image.MAX_IMAGE_PIXELS = 1_000_000_000


class Map:
    """Map object.

    By default, the map must be in a
    equirectangular projection centered
    in longitude 180°. You can set
    :py:attr:`centered_0=True` to flip
    the image internally.

    Parameters
    ----------
    fname: str or pathlib.Path
        Equirectangular map filename.
    body: str, optional
        Target body name.
    centered_0: bool, optional
        Flip the image if the map is center on 0°
        (default: ``False``).
    size: tuple, optional
        Optional ``(width, height)`` image size.
    radius: float, optional
        Optional body radius (km).

    """
    def __init__(self, fname, body=None, centered_0=False, size=None, radius=None):
        self.body = body
        self._centered_0 = centered_0
        self._size = size
        self._radius = radius
        self.fname = fname

    def __str__(self):
        return self.body if self.body is not None else self.fname.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self} | Radius {self.radius} km'

    @property
    def fname(self) -> Path:
        """Map filename."""
        return self.__fname

    @fname.setter
    def fname(self, fname):
        """Filename setter."""
        self.__fname = Path(fname)

        # Load the image
        img = Image.open(self.fname)

        # Resize image if `resize` is set
        if self._size is not None:
            img = img.resize(self._size)

        # Flip the image if `centered_0` is set
        if self._centered_0:
            im = np.asarray(img)
            if np.ndim(im) == 2:
                _, w = np.shape(im)
                img = Image.fromarray(np.hstack([im[:, w // 2:], im[:, :w // 2]]))
            else:
                _, w, _ = np.shape(im)
                img = Image.fromarray(np.hstack([im[:, w // 2:, :], im[:, :w // 2, :]]))

        self.__img = img

    @property
    def img(self):
        """Map background map image."""
        return self.__img

    def map(self, ax=None, fout=False):
        """Plot map.

        Parameters
        ----------
        ax: matplotlib.axes.Axes, optional
            Input axis to draw on.
        fout: str or pathlib.Path, optional
            Save map as image (default ``False``).

        """
        if ax is None:
            _, ax = plt.subplots(figsize=(16, 8))

        ax.imshow(self.img, extent=[0, 360, -90, 90], cmap='gray')

        ax.set_xticks(np.arange(0, 361, 30))
        ax.set_yticks(np.arange(-90, 91, 30))

        ax.grid(lw=.5, color='k')

        ax.xaxis.set_major_formatter(lon_e_ticks)
        ax.yaxis.set_major_formatter(lat_ticks)

        if fout:
            plt.savefig(fout, transparent=True, bbox_inches='tight', pad_inches=0)
            plt.close()

        return fout

    @property
    def radius(self):
        """Body radius (km)."""
        return self._radius

    def _as_mpl_axes(self):
        if self._centered_0:
            raise NotImplementedError('Only 180° centered map are accepted right now.')

        return ProjAxes, {
            'proj': Equirectangular(),
            'bg': self.fname,
            'bg_extent': [0, 360, -90, 90],
            'target': self.body,
        }


DATA = Path(__file__).parent / 'data'


# Mean radius from `pck00010.tpc` kernel
CALLISTO = Map(DATA / 'Callisto.jpg', 'Callisto', radius=2_410.3)
EARTH = Map(DATA / 'Earth.jpg', 'Earth', radius=6_371.0)
EUROPA = Map(DATA / 'Europa.jpg', 'Europa', radius=1_560.8)
GANYMEDE = Map(DATA / 'Ganymede.jpg', 'Ganymede', radius=2_631.2)
MOON = Map(DATA / 'Moon.jpg', 'Moon', radius=1_737.4)
IO = Map(DATA / 'Io.jpg', 'Io', radius=1_821.5)
JUPITER = Map(DATA / 'Jupiter.jpg', 'Jupiter', radius=69_911.3)
VENUS = Map(DATA / 'Venus.jpg', 'Venus', radius=6_051.8)
MERCURY = Map(DATA / 'Mercury.jpg', 'Mercury', radius=2_439.7)


# Global maps registry
class MapsRegistry(dict):
    """Basemaps registry."""
    def __getitem__(self, key):
        return super().__getitem__(str(key).upper())

    def __setitem__(self, key, value):
        super().__setitem__(str(key).upper(), value)

    def __contains__(self, key):
        return super().__contains__(str(key).upper())


MAPS = MapsRegistry({
    'CALLISTO': CALLISTO,
    'EARTH': EARTH,
    'EUROPA': EUROPA,
    'GANYMEDE': GANYMEDE,
    'MOON': MOON,
    'IO': IO,
    'JUPITER': JUPITER,
    'VENUS': VENUS,
    'MERCURY': MERCURY,
})
