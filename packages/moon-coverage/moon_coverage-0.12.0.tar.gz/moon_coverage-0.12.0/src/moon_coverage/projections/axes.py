"""Ground projection axes module."""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.axes._base import _process_plot_format as mpl_fmt
from matplotlib.axis import XAxis, YAxis
from matplotlib.cm import ScalarMappable
from matplotlib.collections import LineCollection, PatchCollection
from matplotlib.colors import Normalize
from matplotlib.legend_handler import HandlerPolyCollection
from matplotlib.patches import PathPatch
from matplotlib.ticker import FixedLocator, NullLocator

from ..ticks import (
    UnitFormatter, deg_ticks, hr_ticks, km_pix_ticks,
    km_s_ticks, km_ticks, lat_ticks, lon_e_ticks
)


PROPS = {
    'alt': ('Altitude', km_ticks),
    'dist': ('Distance', km_ticks),
    'local_time': ('Local time', hr_ticks),
    'inc': ('Incidence angle', deg_ticks),
    'emi': ('Emission angle', deg_ticks),
    'phase': ('Phase angle', deg_ticks),
    'solar_zenith_angle': ('Solar zenith angle', deg_ticks),
    'solar_longitude': ('Seasonal solar longitude', deg_ticks),
    'true_anomaly': ('True anomaly angle', deg_ticks),
    'groundtrack_velocity': ('Groundtrack velocity', km_s_ticks),
    'pixel_scale': ('Pixel scale', km_pix_ticks),
}


def get_values(traj, attr):
    """Get trajectory attribute values."""
    if hasattr(traj, attr):
        return getattr(traj, attr)

    # Check if the provided key is a valid matplotlib string (and return an empty array)
    try:
        mpl_fmt(attr)
    except ValueError:
        raise ValueError(
            f'The second argument `{attr}` must be a '
            f'`{traj.__class__.__name__}` property '
            'or a valid matplotlib format string (eg. `ro`).'
        ) from None

    return []


class ProjAxes(Axes):
    """An abstract base class for geographic projections."""

    def __init__(self, *args, proj='equi', bg=None, bg_extent=False, target='', **kwargs):
        self.proj = proj
        self.bg = bg
        self.bg_extent = bg_extent
        self.target = target
        self._cbar = None

        super().__init__(*args, **kwargs)

    def _init_axis(self):
        self.xaxis = XAxis(self)
        self.yaxis = YAxis(self)
        self._update_transScale()

    def clear(self):
        """Clear axes."""
        Axes.clear(self)
        self.set_aspect(1)

        self.xaxis.set_minor_locator(NullLocator())
        self.yaxis.set_minor_locator(NullLocator())

        self.set_longitude_grid(30)
        self.set_latitude_grid(30)

        self.set_background()
        self.grid(lw=.5, color='k')

        Axes.set_xlim(self, *self.proj.extent[:2])
        Axes.set_ylim(self, *self.proj.extent[2:])

    def _check_target(self, obj):
        """Check object target name."""
        if hasattr(obj, 'target'):
            proj_target = str(getattr(self, 'target')).upper()
            obj_target = str(getattr(obj, 'target')).upper()

            if proj_target != obj_target:
                raise ProjectionMapTargetError(
                    f'Target mismatch: {proj_target} map with {obj_target} data.')

    def plot(self, *args, scalex=True, scaley=True, data=None, **kwargs):
        """Generic plot function with projection."""
        if hasattr(args[0], 'lonlat'):
            traj = args[0]

            self._check_target(traj)

            if len(args) > 1 and isinstance(args[1], str):
                attr = args[1].lower().replace(' ', '_')

                if any(values := get_values(traj, attr)):

                    x, y, data = self.proj.xy_plot(*traj.lonlat, values=values)

                    label, fmt = PROPS.get(attr, (None, None))
                    kwargs = {'label': label, 'fmt': fmt, **kwargs}

                    return self.plot_colorline(x, y, data, **kwargs)

            x, y = self.proj.xy_plot(*traj.lonlat)
            args = args[1:]

        elif len(args) >= 2 and isinstance(args[0], (int, float)) \
                and isinstance(args[1], (int, float)):
            x, y = self.proj.xy_plot([args[0]], [args[1]])
            args = args[2:]

        elif len(args[0]) == 2 and isinstance(args[0], (tuple, list)) \
                and np.ndim(args[0]) == 2:
            x, y = self.proj.xy_plot(*args[0])
            args = args[1:]

        elif len(args) > 2 and '.' not in args[2] and 'o' not in args[2]:
            x, y = self.proj.xy_plot(*args[:2])
            args = args[2:]

        else:
            x, y = self.proj.xy(*args[:2])
            args = args[2:]

        return super().plot(x, y, *args,
                            scalex=scalex, scaley=scaley, data=data, **kwargs)

    def plot_colorline(self, x, y, data, cmap=None, vmin=None, vmax=None, norm=None,
                       label=None, fmt=None, orientation='horizontal', cbar=True,
                       **kwargs):  # pylint: disable=too-many-locals
        """Plot a colored line with a colorbar.

        Parameters
        ----------
        x: numpy.ndarray
            Projected x-coordinates.
        y: numpy.ndarray
            Projected y-coordinates.
        data: numpy.ndarray
            Value to use to color the line.
        cmap: str, optional
            Matplotlib colormap name (default: `turbo_r`)
        vmin: int or float
            Color scaling min value. If ``None`` is provided (default)
            the data are scaled to the lowest (not-NaN) value.
        vmax: int or float
            Color scaling max value. If ``None`` is provided (default)
            the data are scaled to the lowest (not-NaN) value.
        norm: matplotlib.colors.Normalize
            Normalization colors normalizer. By default
            the values will be normalized between :py:attr:`vmin`
            and :py:attr:`vmax`.
        label: str, optional
            Colorbar label.
        fmt: str, optional
            Colorbar ticks formatter.
        orientation: str, optional
            Colorbar orientation (default: `horizontal`).
        **kwargs:
            Keyword attributes for :py:class:`LineCollection`.

        Note
        ----
        If the range provided (with :py:attr:`vmin` and :py:attr:`vmax`)
        is smaller than the range of the data, the colorbar will
        be extended with arrows.

        """
        points = np.transpose([x, y]).reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        data = np.array(data)
        values = .5 * (data[1:] + data[:-1])

        if vmin is None:
            vmin = np.nanmin(data)
        if vmax is None:
            vmax = np.nanmax(data)

        if cmap is None:
            cmap = 'turbo_r'
        if norm is None:
            norm = plt.Normalize(vmin, vmax)

        lc = LineCollection(segments, cmap=cmap, norm=norm, **kwargs)
        lc.set_array(values)

        lines = super(Axes, self).add_collection(lc)  # pylint: disable=bad-super-call

        if not cbar:
            return lines

        # Colorbar extend is based on the data range
        cmin = np.nanmin(data) < vmin
        cmax = np.nanmax(data) > vmax

        extend = 'both' if cmin and cmax else 'min' \
            if cmin else 'max' if cmax else 'neither'

        cbar_kwargs = {
            'cmap': cmap,
            'orientation': orientation,
            'extend': extend,
            'format': fmt,
            'label': label,
        }

        return self.colorbar(vmin, vmax, **cbar_kwargs)

    def add_path(self, path, *args, **kwargs):
        """Draw path."""
        self.add_patch(PathPatch(path, *args, **kwargs))

    def add_patch(self, p):
        """Draw patch."""
        self._check_target(p)
        super().add_patch(self.proj.xy_patch(p))

    def add_collection(self, collection, autolim=True):
        """Draw patches collection."""
        self._check_target(collection)
        super().add_collection(self.proj.xy_collection(collection), autolim=autolim)

    def legend(self, *args, **kwargs):
        """Add HandlerPolyCollection to `handler_map` for PatchCollection."""
        if 'handler_map' not in kwargs:
            kwargs['handler_map'] = {}

        if PatchCollection not in kwargs['handler_map']:
            kwargs['handler_map'][PatchCollection] = HandlerPolyCollection()

        return super().legend(*args, **kwargs)

    def colorbar(self, vmin, vmax, cmap='turbo_r',
                 orientation='horizontal',
                 shrink=.6,
                 aspect=40,
                 pad=0.05,
                 **kwargs):
        """Add a standalone colorbar on the axis.

        Parameters
        ----------
        vmin: int or float, optional
            Color scaling min value. If ``None`` is provided (default)
            the data are scaled to the lowest (not-NaN) value.
        vmax: int or float, optional
            Color scaling max value. If ``None`` is provided (default)
            the data are scaled to the lowest (not-NaN) value.
        cmap: str, optional
            Matplotlib colormap name (default: `turbo_r`)
        orientation: str, optional
            Colorbar orientation (default: `horizontal`).
        label: str, optional
            Colorbar label (shortcuts are available).
        **kwargs:
            Keyword attributes for :py:class:`Colorbar`.

        Returns
        -------
        matplotlib.colorbar.Colorbar
            Output colorbar.

        """
        norm = Normalize(vmin, vmax)

        # Shortcut to format the ticks of known units
        if 'label' in kwargs and kwargs['label'] in PROPS:
            kwargs.update(zip(
                ('label', 'format'), PROPS[kwargs['label']]
            ))

        self._cbar = self.figure.colorbar(
            ScalarMappable(norm=norm, cmap=cmap),
            ax=self,
            orientation=orientation,
            shrink=shrink,
            aspect=aspect,
            pad=pad,
            **kwargs
        )

        return self._cbar

    def twin_colorbar(self, label=None, format=None,  # pylint: disable=redefined-builtin
                      offset=.05, ticks=None):
        """Twin colorbar with a secondary axis.

        Parameters
        ----------
        label: str, optional
            Twin colorbar label (no shortcut).
        format: matplotlib.ticker.Formatter, optional
            Optional ticks formatter.
        offset: float, optional
            Colorbar offset (default: `0.05`).
        ticks: list, optional
            Custom list of ticks (default: ``None``).

        """
        if self._cbar is None:
            raise ValueError('No parent colorbar found.')

        pos = self._cbar.ax.get_position()
        self._cbar.ax.set_aspect('auto')  # change default `equal` to `auto`

        # Relocate ticks for UnitFormatter
        if ticks and isinstance(format, UnitFormatter):
            ticks = format @ ticks

        # Shift the colorbar to avoid to overlap the figure
        if self._cbar.orientation == 'horizontal':
            pos.y0 -= offset
            pos.y1 -= offset
            ax = self._cbar.ax.twiny()
            ax.set_xlim(self._cbar.ax.get_xlim())
            set_label = ax.set_xlabel
            set_ticks = ax.set_xticks
            set_formatter = ax.xaxis.set_major_formatter

        else:
            pos.x0 += offset
            pos.x1 += offset
            ax = self._cbar.ax.twinx()
            ax.set_ylim(self._cbar.ax.get_ylim())
            set_label = ax.set_ylabel
            set_ticks = ax.set_yticks
            set_formatter = ax.yaxis.set_major_formatter

        # Change label/ticks and formatter
        if label:
            set_label(label)

        if ticks:
            set_ticks(ticks)

        if format:
            set_formatter(format)

        # Move original colorbar position
        self._cbar.ax.set_position(pos)
        ax.set_position(pos)

        # Remove the frame borders
        for border in ax.spines:
            ax.spines[border].set_visible(False)

        return ax

    def set_longitude_grid(self, degrees):
        """Set the number of degrees between each longitude grid."""
        grid = np.linspace(0, 360, int(360 / degrees) + 1).astype(int)
        self.xaxis.set_major_locator(FixedLocator(grid))
        self.xaxis.set_major_formatter(lon_e_ticks)

    def set_latitude_grid(self, degrees):
        """Set the number of degrees between each longitude grid."""
        grid = np.linspace(-90, 90, int(180 / degrees) + 1).astype(int)
        self.yaxis.set_major_locator(FixedLocator(grid))
        self.yaxis.set_major_formatter(lat_ticks)

    def set_background(self):
        """Set image basemap background."""
        if self.bg:
            im = plt.imread(self.bg)
            self.imshow(im, extent=self.bg_extent, cmap='gray')


class ProjectionMapTargetError(Exception):
    """Mismatch between the projection map target and the data."""
