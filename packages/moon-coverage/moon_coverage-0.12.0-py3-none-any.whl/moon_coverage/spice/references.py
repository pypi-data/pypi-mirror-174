"""SPICE reference module."""

import numpy as np

import spiceypy as sp

from .fov import SpiceFieldOfView
from .kernel import get_item
from .times import sclk
from ..misc import cached_property, depreciated, warn


def spice_name_code(ref):
    """Get name and code from a reference.

    Parameters
    ----------
    ref: str or int
        Reference name or code id.

    Returns
    -------
    str, int
        Reference name and code id.

    Raises
    ------
    ValueError
        If this reference is not known in the kernel pool.

    """
    try:
        code = sp.bods2c(str(ref).upper())
        name = sp.bodc2n(code)

    except sp.stypes.NotFoundError:
        raise ValueError(f'Unknown reference: `{ref}`')

    return str(name), int(code)


class AbstractSpiceRef:
    """SPICE reference helper.

    Parameters
    ----------
    ref: str or int
        Reference name or code id.

    Raises
    ------
    KeyError
        If this reference is not known in the kernel pool.

    """

    def __init__(self, ref):
        self.name, self.id = spice_name_code(ref)

        if not self.is_valid():
            raise KeyError(f'{self.__class__.__name__} invalid id: `{int(self)}`')

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self} (ID: {int(self):_})'

    def __int__(self):
        return self.id

    def __eq__(self, other):
        return str(self) == other or int(self) == other

    def __getitem__(self, item):
        return get_item(item)

    @property
    def code(self):
        """SPICE reference ID as string."""
        return str(self.id)

    def is_valid(self):
        """Generic SPICE reference.

        Returns
        -------
        bool
            Generic SPICE reference should always ``True``.

        """
        return isinstance(int(self), int)


class SpiceBody(AbstractSpiceRef):
    """SPICE planet/satellite body reference.

    Parameters
    ----------
    name: str or int
        Body name or code id.

    """

    def __getitem__(self, item):
        return get_item(f'BODY{int(self)}_{item.upper()}')

    def is_valid(self):
        """Check if the code is valid for a SPICE body.

        Refer to the `NAIF Integer ID codes
        <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/req/naif_ids.html>`_
        in section `Planets and Satellites` for more details.

        Returns
        -------
        bool
            Valid bodies are 10 (SUN) and any value between 101 and 999.

        """
        return int(self) == 10 or 100 < int(self) < 1_000

    @property
    def is_planet(self):
        """Check if the body is a planet."""
        return self.code[-2:] == '99'

    @cached_property
    def frame(self):
        """Body centered reference frame."""
        return sp.cidfrm(int(self))[1]

    @cached_property
    def parent(self):
        """Parent body."""
        return SpiceBody('SUN' if self.is_planet else self.code[0] + '99')

    @cached_property
    def barycenter(self):
        """Body barycenter."""
        if self.is_planet or int(self) == 10:
            return SpiceRef(int(self) // 100)

        return self.parent.barycenter

    @cached_property
    def radii(self):
        """Body radii, if available (km)."""
        return self['RADII']

    @property
    def radius(self):
        """Body mean radius, if available (km)."""
        return np.cbrt(np.product(self.radii))

    @property
    def r(self):
        """Body mean radius alias."""
        return self.radius

    @property
    def re(self):
        """Body equatorial radius, if available (km)."""
        return self.radii[0]

    @property
    def rp(self):
        """Body polar radius, if available (km)."""
        return self.radii[2]

    @property
    def f(self):
        """Body flattening coefficient, if available (km)."""
        re, _, rp = self.radii  # pylint: disable=unbalanced-tuple-unpacking
        return (re - rp) / re

    @cached_property
    def mu(self):
        """Gravitational parameter (GM, km³/sec²)."""
        return self['GM']


class SpiceObserver(AbstractSpiceRef):
    """SPICE observer reference.

    Parameters
    ----------
    ref: str or int
        Reference name or code id.

    Raises
    ------
    KeyError
        If the provided key is neither spacecraft nor an instrument.

    """

    def __init__(self, ref):
        super().__init__(ref)

        # Spacecraft object promotion
        if SpiceSpacecraft.is_valid(self):
            self.__class__ = SpiceSpacecraft

        # Instrument object promotion
        elif SpiceInstrument.is_valid(self):
            self.__class__ = SpiceInstrument

        else:
            raise KeyError('A SPICE observer must be a valid Spacecraft or Instrument')


class SpiceSpacecraft(SpiceObserver):
    """SPICE spacecraft reference.

    Parameters
    ----------
    name: str or int
        Spacecraft name or code id.

    """

    BORESIGHT = [0, 0, 1]

    def is_valid(self):
        """Check if the code is valid for a SPICE spacecraft.

        Refer to the `NAIF Integer ID codes
        <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/req/naif_ids.html>`_
        in sections `Spacecraft` and `Earth Orbiting Spacecraft` for more details.

        - Interplanetary spacecraft is normally the negative of the code assigned
          to the same spacecraft by JPL's Deep Space Network (DSN) as determined
          the NASA control authority at Goddard Space Flight Center.

        - Earth orbiting spacecraft are defined as: ``-100000 - NORAD ID code``

        Returns
        -------
        bool
            Valid spacecraft ids are between -999 and -1 and between
            -119,999 and -100,001.

        """
        return -1_000 < int(self) < 0 or -120_000 < int(self) < -100_000

    @cached_property
    def instruments(self):
        """SPICE instruments in the pool associated with the spacecraft."""
        keys = sp.gnpool(f'INS{int(self)}%%%_FOV_FRAME', 0, 1_000)

        codes = sorted([int(key[3:-10]) for key in keys], reverse=True)

        return list(map(SpiceInstrument, codes))

    def instr(self, name):
        """SPICE instrument from the spacecraft."""
        return SpiceInstrument(f'{self}_{name}')

    @property
    def spacecraft(self):
        """Spacecraft SPICE reference."""
        return self

    def sclk(self, *time):
        """Continuous encoded spacecraft clock ticks.

        Parameters
        ----------
        *time: float or str
            Ephemeris time (ET)  or UTC time inputs.

        """
        return sclk(int(self), *time)

    @cached_property
    def frame(self):
        """Spacecraft frame (if available)."""
        return str(SpiceRef(f'{self}_SPACECRAFT'))

    @property
    def boresight(self):
        """Spacecraft z-axis boresight.

        For an orbiting spacecraft, the Z-axis points from the
        spacecraft to the closest point on the target body.

        The component of inertially referenced spacecraft velocity
        vector orthogonal to Z is aligned with the -X axis.

        The Y axis is the cross product of the Z axis and the X axis.

        You can change the :attr:`SpiceSpacecraft.BORESIGHT` value manually.

        """
        return np.array(self.BORESIGHT)


class SpiceInstrument(SpiceObserver, SpiceFieldOfView):
    """SPICE instrument reference.

    Parameters
    ----------
    name: str or int
        Instrument name or code id.

    """
    def __getitem__(self, item):
        return get_item(f'INS{int(self)}_{item.upper()}')

    def is_valid(self):
        """Check if the code is valid for a SPICE instrument.

        Refer to the `NAIF Integer ID codes
        <https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/FORTRAN/req/naif_ids.html>`_
        in section `Instruments` for more details.

        .. code-block:: text

            NAIF instrument code = (s/c code)*(1000) - instrument number

        Returns
        -------
        bool
            Valid instrument ids is below -1,000 and have a valid
            field of view definition.

        Warning
        -------
        Based on the SPICE documentation, the min value of the NAIF code
        should be -1,000,000. This rule is not enforced because some
        instrument of JUICE have value below -2,800,000
        (cf. ``JUICE_PEP_JDC_PIXEL_000 (ID: -2_851_000)`` in `juice_pep_v09.ti`).

        """
        if int(self) >= -1_000:
            return False

        try:
            # Check if the FOV is valid and init the value if not an `int`.
            if isinstance(self, int):
                _ = SpiceFieldOfView(self)
            else:
                SpiceFieldOfView.__init__(self, int(self))

            return True
        except ValueError:
            return False

    @cached_property
    def spacecraft(self):
        """Parent spacecraft.

        Warning
        -------
        The current definition of JUICE PEP instruments IDs
        (in `juice_pep_v09.ti`) are out-of-range NAIF code rules.
        This special case is expected to be an exception and manually
        fixed here with a ``DepreciationWarning``.
        See `issue #12
        <https://juigitlab.esac.esa.int/datalab/moon-coverage/-/issues/12>`_
        to get more details.

        """
        try:
            return SpiceSpacecraft(-(-int(self) // 1_000))

        except ValueError as err:
            if str(self).startswith('JUICE_PEP_'):
                warn.warning(
                    'Invalid JUICE/PEP instrument NAIF IDs (%i) for `%s`. '
                    'The parent spacecraft ID is manually set to `JUICE` (-28). '
                    'See issue #12 '
                    '(https://juigitlab.esac.esa.int/datalab/moon-coverage/-/issues/12) '
                    'for more details.',
                    int(self), str(self)
                )
                return SpiceSpacecraft('JUICE')

            raise err

    def sclk(self, *time):
        """Continuous encoded parent spacecraft clock ticks.

        Parameters
        ----------
        *time: float or str
            Ephemeris time (ET)  or UTC time inputs.

        """
        return sclk(int(self.spacecraft), *time)

    @property
    def ns(self):
        """Instrument number of samples."""
        try:
            return int(self['PIXEL_SAMPLES'])
        except KeyError:
            return 1

    @property
    def nl(self):
        """Instrument number of lines."""
        try:
            return int(self['PIXEL_LINES'])
        except KeyError:
            return 1

    def _rad_fov(self, key):
        """Get FOV angle value in radians"""
        angle = self[f'FOV_{key}']

        return angle if self['FOV_ANGLE_UNITS'] == 'RADIANS' else np.radians(angle)

    @property
    def fov_along_track(self):
        """Instrument field of view along-track angle (radians)."""
        if self.shape == 'POLYGON':
            return np.nan

        return 2 * self._rad_fov('REF_ANGLE')

    @property
    def fov_cross_track(self):
        """Instrument field of view cross-track angle (radians)."""
        if self.shape in ['CIRCLE', 'POLYGON']:
            return self.fov_along_track

        return 2 * self._rad_fov('CROSS_ANGLE')

    @property
    def ifov(self):
        """Instrument instantaneous field of view angle (radians).

        Danger
        ------
        This calculation expect that the sample direction is
        aligned with the cross-track direction (ie. 1-line acquisition
        in push-broom mode should be in the direction of flight).

        Warning
        -------
        ``JUICE_JANUS`` instrument in ``v06`` does not follow this convention.
        We manually manage this exception for the moment.
        See `MR !27
        <https://juigitlab.esac.esa.int/datalab/moon-coverage/-/merge_requests/27>`_
        for more details.

        """
        if self != 'JUICE_JANUS':
            along_track = self.fov_along_track / self.nl
            cross_track = self.fov_cross_track / self.ns
        else:
            along_track = self.fov_along_track / self.ns
            cross_track = self.fov_cross_track / self.nl

        return along_track, cross_track

    @property
    def ifov_along_track(self):
        """Instrument instantaneous along-track field of view angle (radians)."""
        return self.ifov[0]

    @property
    def ifov_cross_track(self):
        """Instrument instantaneous cross-track field of view angle (radians)."""
        return self.ifov[1]


class SpiceRef(AbstractSpiceRef):
    """SPICE reference generic helper.

    Parameters
    ----------
    ref: str or int
        Reference name or code id.

    """

    def __init__(self, ref):
        super().__init__(ref)

        # Body object promotion
        if SpiceBody.is_valid(self):
            self.__class__ = SpiceBody

        # Spacecraft object promotion
        elif SpiceSpacecraft.is_valid(self):
            self.__class__ = SpiceSpacecraft

        # Instrument object promotion
        elif SpiceInstrument.is_valid(self):
            self.__class__ = SpiceInstrument

    @property
    def spacecraft(self):
        """Spacecraft SPICE reference.

        Not implemented for a :class:`SpiceRef`.

        """
        raise NotImplementedError

    def sclk(self, *time):
        """Continuous encoded parent spacecraft clock ticks.

        Not implemented for a :class:`SpiceRef`.

        """
        raise NotImplementedError


# pylint: disable=abstract-method
@depreciated('0.8.0')
class SPICERef(SpiceRef):
    """SPICE reference helper."""
