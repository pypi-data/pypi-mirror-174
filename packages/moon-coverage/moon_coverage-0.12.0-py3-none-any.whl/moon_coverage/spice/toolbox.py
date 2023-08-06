"""SPICE toolbox helper module."""

import numpy as np

import spiceypy as sp

from .limb import limb_ip_pt
from .references import SpiceBody, SpiceInstrument, SpiceObserver
from .times import et
from ..math.sphere import sph_pixel_scale


def is_iter(value):
    """Check if a value is iterable."""
    return isinstance(value, (list, tuple, np.ndarray))


def type_check(value, dtype, func=None):
    """Check input type.

    Parameters
    ----------
    value: any
        Input value.
    dtype: type
        Expected type.
    func: function, optional
        Conversion function. Use dtype if `None` provided (default).

    Returns
    -------
    dtype
        Valid value type.

    """
    return value if isinstance(value, dtype) else \
        dtype(value) if func is None else \
        func(value)


def deg(rad):
    """Convert radian angle in degrees."""
    return np.multiply(rad, sp.dpr())


def rlonlat(pt):
    """Convert point location in planetocentric coordinates.

    Parameters
    ----------
    pt: tuple
        Input XYZ cartesian coordinates.

    Returns
    -------
    float, float, float
        - Point radius (in km).
        - East planetocentric longitude (in degree).
        - North planetocentric latitude (in degree).

    Note
    ----
    - If the X and Y components of `pt` are both zero, the longitude is set to zero.
    - If `pt` is the zero vector, longitude and latitude are both set to zero.

    See Also
    --------
    spiceypy.spiceypy.reclat

    """
    big = np.max(np.abs(pt), axis=0)

    if np.ndim(pt) < 2:
        if big == 0:
            return 0, 0, 0

        xyz = np.divide(pt, big)
    else:
        xyz = np.zeros_like(pt, dtype=float)
        np.divide(pt, big, where=big > 0, out=xyz, casting='unsafe')
        xyz[..., np.isnan(big)] = np.nan

    radius = big * np.sqrt(np.sum(np.power(xyz, 2), axis=0))
    lat_rad = np.arctan2(xyz[2], np.sqrt(np.sum(np.power(xyz[:2], 2), axis=0)))

    lon_e_rad = np.zeros_like(radius)
    np.arctan2(xyz[1], xyz[0], out=lon_e_rad)

    return radius, deg(lon_e_rad) % 360, deg(lat_rad)


def radec(vec):
    """Convert vector on the sky J2000 to RA/DEC coordinates.

    Parameters
    ----------
    vec: tuple
        Input XYZ cartesian vector coordinates in J200 frame.

    Returns
    -------
    float or numpy.ndarray, float or numpy.ndarray
        - Right-ascension (in degree).
        - Declination angle (in degree).

    See Also
    --------
    rlonlat

    """
    _, ra, dec = rlonlat(vec)
    return ra, dec


def sub_obs_pt(time, observer, target, abcorr='NONE', method='NEAR POINT/ELLIPSOID'):
    """Sub-observer point calculation.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    observer: str
        Observer name.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Computation method to be used. Possible values:

        - 'NEAR POINT/ELLIPSOID' (default)
        - 'INTERCEPT/ELLIPSOID'
        - 'NADIR/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'
        - 'INTERCEPT/DSK/UNPRIORITIZED[/SURFACES = <surface list>]'

        (See NAIF :func:`spiceypy.spiceypy.subpnt` for more details).

    Returns
    -------
    (float, float, float) or numpy.ndarray
        Sub-observer XYZ coordinates in the target body fixed frame
        (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    spiceypy.spiceypy.subpnt

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time):
        return np.transpose([
            sub_obs_pt(t, observer, target, abcorr=abcorr, method=method)
            for t in time
        ])

    xyz, *_ = sp.subpnt(method, str(target), time, target.frame,
                        abcorr, str(observer))

    return xyz


def sc_state(time, spacecraft, target, abcorr='NONE'):
    """Spacecraft position and velocity relative to the target.

    The position vector starts from the target body to the spacecraft:

    .. code-block:: text

        target ------> spacecraft
                (km)

    The velocity vector correspond to the spacecraft motion (in km/s).

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the spacecraft location.
    spacecraft: str or SpiceSpacecraft
        Spacecraft name.
    target: str or SpiceBody
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    (float, float, float, float, float, float) or numpy.ndarray
        Spacecraft XYZ position and velocity coordinates in
        the target body fixed frame (expressed in km and km/s).

        If a list of time were provided, the results will be stored
        in a (6, N) array.

    See Also
    --------
    spiceypy.spiceypy.spkezr

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time):
        return np.transpose([
            sc_state(t, spacecraft, target, abcorr=abcorr)
            for t in time
        ])

    state, _ = sp.spkezr(str(target), time, target.frame,
                         abcorr, str(spacecraft))

    return np.negative(state)


def attitude(time, observer, ref='J2000'):
    """C-matrix attitude.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    observer: str or SpiceSpacecraft or SpiceInstrument
        Spacecraft or instrument name.
    ref: str, optional
        Reference for the return pointing.

    Returns
    -------
    numpy.ndarray
        C-matrix relative to the reference frame.

        If a list of time were provided, the results will be stored
        in a (3, 3, N) array.

    Raises
    ------
    ValueError
        If the observer provided is not a Spacecraft or an instrument.

    See Also
    --------
    spiceypy.spiceypy.pxform

    """
    time = type_check(time, float, et)
    observer = type_check(observer, SpiceObserver)

    if is_iter(time):
        return np.moveaxis([
            attitude(t, observer, ref=ref) for t in time
        ], 0, -1)

    return sp.pxform(str(observer.frame), ref, time)


def intersect_pt(time, observer, target, frame, ray, limb=False,
                 abcorr='NONE', method='ELLIPSOID'):
    """Intersection point on a target from a ray at the observer position.

    The intersection is primarily computed with the target surface.
    If no intersection was found and the :py:attr:`limb` flag is set to ``TRUE``,
    the intersection will be search on the target limb (defined as the impact parameter).
    When no value was find, a NaN array will be return.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    observer: str or SpiceSpacecraft or SpiceInstrument
        Spacecraft of instrument observer name.
    target: str or SpiceBody
        Target body name.
    frame: str
        Reference frame relative to which the ray's direction vector is expressed.
    ray: tuple or list of tuple
        Ray direction vector emanating from the observer.
        The intercept with the target body's surface of the ray defined by
        the observer and ray is sought.
    limb: bool, optional
        Compute the intersection on the limb impact parameter
        if no intersection with the surface was found.
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Computation method to be used.
        (See NAIF :func:`spiceypy.spiceypy.sincpt` for more details).

    Returns
    -------
    (float, float, float) or numpy.ndarray
        Surface/limb intersection XYZ position on the target body
        fixed frame (expressed in km).

        If a list of time/ray were provided, the results will be stored
        in a (3, N) array.

    Warning
    -------
    Currently the limb intersection parameter is only available for
    ``abcorr='NONE'`` (an ``NotImplementedError`` will be raised).

    See Also
    --------
    spiceypy.spiceypy.sincpt
    .limb_ip_pt

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)
    observer = type_check(observer, SpiceObserver)

    if is_iter(time) and np.ndim(ray) > 1:
        if len(time) != np.shape(ray)[0]:
            raise ValueError(
                'The ephemeris times and ray vectors must have the same size: '
                f'{len(time)} vs {len(ray)}'
            )

        return np.transpose([
            intersect_pt(t, observer, target, frame, r,
                         limb=limb, abcorr=abcorr, method=method)
            for t, r in zip(time, ray)
        ])

    if is_iter(time):
        return intersect_pt(time, observer, target, frame, [ray] * len(time),
                            limb=limb, abcorr=abcorr, method=method)

    if np.ndim(ray) > 1:
        return intersect_pt([time] * np.shape(ray)[0], observer, target, frame, ray,
                            limb=limb, abcorr=abcorr, method=method)

    try:
        xyz, *_ = sp.sincpt(method, str(target), time, target.frame, abcorr,
                            str(observer), frame, ray)
    except sp.stypes.NotFoundError:
        if limb:
            xyz = limb_ip_pt(time, int(observer), int(target), frame, ray, target.frame,
                             abcorr=abcorr)
        else:
            xyz = np.array([np.nan, np.nan, np.nan])

    return xyz


def boresight_pt(time, observer, target, limb=False, abcorr='NONE', method='ELLIPSOID'):
    """Surface intersection on a target from an instrument/spacecraft boresight.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    observer: str or SpiceSpacecraft or SpiceInstrument
        Spacecraft or instrument name.
    target: str or SpiceBody
        Target body name.
    limb: bool, optional
        Compute the intersection on the limb impact parameter
        if no intersection with the surface was found.
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Computation method to be used.
        (See NAIF :func:`spiceypy.spiceypy.sincpt` for more details).

    Returns
    -------
    (float, float, float) or numpy.ndarray
        Boresight intersection XYZ position on the target surface body
        fixed frame (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    intersect_pt

    """
    observer = type_check(observer, SpiceObserver)

    return intersect_pt(time, observer.spacecraft, target, observer.frame,
                        observer.boresight, limb=limb, abcorr=abcorr, method=method)


def fov_pts(time, inst, target, limb=False, npt=24,
            abcorr='NONE', method='ELLIPSOID'):
    """Surface intersection on a target from an instrument FOV rays.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the observer location.
    inst: str or SpiceInstrument
        Instrument name.
    target: str or SpiceBody
        Target body name.
    limb: bool, optional
        Compute the intersection on the limb impact parameter
        if no intersection with the surface was found.
    npt: int, optional
        Number of points in the field of view contour (default: 24).
    abcorr: str, optional
        Aberration correction (default: 'None'),
    method: str, optional
        Computation method to be used.
        (See NAIF :func:`spiceypy.spiceypy.sincpt` for more details).

    Returns
    -------
    (float, float, float) or numpy.ndarray
        Field of View intersection XYZ positions on the target surface body
        fixed frame (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N, M) array. `M` being the number of bound in the FOV.

    See Also
    --------
    intersect_pt

    Note
    ----
    In the general case, the last point should be different from the 1st one.
    You need to add the 1st point to the end of the list if you want to close
    the polygon of the footprint.

    """
    inst = type_check(inst, SpiceInstrument)

    return np.moveaxis([
        intersect_pt(time, inst.spacecraft, target, inst.frame, ray.copy(),
                     limb=limb, abcorr=abcorr, method=method)
        for ray in inst.rays(npt=npt)
    ], 0, -1)


def local_time(time, lon, target, lon_type='PLANETOCENTRIC'):
    """Local solar time.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target surface point location.
    lon: float or list or tuple
        Longitude of surface point (degree).
    target: str
        Target body name.
    lon_type: str, optional
        Form of longitude supplied by the variable :py:attr:`lon`.
        Possible values:

        - `PLANETOCENTRIC` (default)
        - `PLANETOGRAPHIC`

        (See NAIF :func:`spiceypy.spiceypy.et2lst` for more details).

    Returns
    -------
    float or numpy.ndarray
        Local solar time (expressed in decimal hours).

        If a list of :py:attr:`time` or :py:attr:`lon`
        were provided, the results will be stored
        in an array.

    Raises
    ------
    ValueError
        If the :py:attr:`time` and :py:attr:`lon` are both
        arrays but their size don't match.

    See Also
    --------
    spiceypy.spiceypy.et2lst

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time) and is_iter(lon):
        if len(time) != len(lon):
            raise ValueError(
                'The ephemeris times and longitudes must have the same size: '
                f'{len(time)} vs {len(lon)}'
            )

        return np.transpose([
            local_time(t, l, target, lon_type) for t, l in zip(time, lon)
        ])

    if is_iter(time):
        return local_time(time, [lon] * len(time), target, lon_type)

    if is_iter(lon):
        return local_time([time] * len(lon), lon, target, lon_type)

    if not np.isnan(lon):
        h, m, s, *_ = sp.et2lst(time, int(target), np.radians(lon), lon_type)
    else:
        h, m, s = np.nan, np.nan, np.nan

    return h + m / 60 + s / 3600


def illum_angles(time, spacecraft, target, pt, abcorr='NONE', method='ELLIPSOID'):
    """Illumination angles.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target surface point location.
    spacecraft: str
        Spacecraft name.
    target: str
        Target body name.
    pt: numpy.ndarray
        Surface point (XYZ coordinates).
    abcorr: str, optional
        Aberration correction (default: 'None')
    method: str, optional
        Form of longitude supplied by the variable :py:attr:`lon`.
        Possible values:

        - `ELLIPSOID` (default)
        - `DSK/UNPRIORITIZED[/SURFACES = <surface list>]`

        (See NAIF :func:`spiceypy.spiceypy.ilumin` for more details).

    Returns
    -------
    float or numpy.ndarray
        Solar incidence, emission and phase angles at the surface point (degrees).

        If a list of time were provided, the results will be stored in a (3, N) array.

    Raises
    ------
    ValueError
        If the :py:attr:`time` and :py:attr:`lon` are both
        arrays but their size don't match.

    See Also
    --------
    spiceypy.spiceypy.ilumin

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time) and np.ndim(pt) > 1:
        if len(time) != np.shape(pt)[1]:
            raise ValueError(
                'The ephemeris times and surface point must have the same size: '
                f'{len(time)} vs {len(pt)}'
            )

        return np.transpose([
            illum_angles(t, spacecraft, target, _pt, abcorr=abcorr, method=method)
            for t, _pt in zip(time, np.transpose(pt))
        ])

    if is_iter(time):
        return illum_angles(time, spacecraft, target, np.transpose([pt] * len(time)),
                            abcorr=abcorr, method=method)

    if np.ndim(pt) > 1:
        return illum_angles([time] * np.shape(pt)[1], spacecraft, target,
                            pt, abcorr=abcorr, method=method)

    if not np.isnan(np.max(pt)):
        *_, p, i, e = sp.ilumin(method, str(target), time,
                                target.frame, abcorr, str(spacecraft), pt)
    else:
        i, e, p = np.nan, np.nan, np.nan

    return np.degrees([i, e, p])


def sun_pos(time, target, abcorr='NONE'):
    """Sun position relative to the target.

    The vector starts from the target body to the Sun:

    .. code-block:: text

        target ------> Sun
                (km)

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's center location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    (float, float, float) or numpy.ndarray
        Sun XYZ coordinates in the target body fixed frame
        (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    See Also
    --------
    spiceypy.spiceypy.spkpos

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time):
        return np.transpose([
            sun_pos(t, target, abcorr=abcorr)
            for t in time
        ])

    xyz, _ = sp.spkpos('SUN', time, target.frame, abcorr, str(target))

    return xyz


def solar_longitude(time, target, abcorr='NONE'):
    """Seasonal solar longitude (degrees).

    Compute the angle from the vernal equinox of the main parent
    body.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's center location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')

    Returns
    -------
    float or numpy.ndarray
        Solar longitude angle(s) (degrees).

        If a list of :py:attr:`time` were provided,
        the results will be stored in an array.

    Note
    ----
    If the target parent is not the SUN the target will be change
    for its own parent.

    See Also
    --------
    spiceypy.spiceypy.lspcn

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if target.parent != 'SUN':
        solar_longitude(time, target.parent, abcorr=abcorr)

    if is_iter(time):
        return np.transpose([
            solar_longitude(t, target, abcorr=abcorr)
            for t in time
        ])

    solar_lon = sp.lspcn(target, time, abcorr)

    return np.degrees(solar_lon)


def true_anomaly(time, target, abcorr='NONE', frame='ECLIPJ2000'):
    """Target orbital true anomaly (degrees).

    The angular position of the target in its orbit
    compare to its periapsis.

    Parameters
    ----------
    time: float or list or tuple
        Ephemeris Time or UTC time input(s).
        It refers to time at the target's center location.
    target: str
        Target body name.
    abcorr: str, optional
        Aberration correction (default: 'None')
    frame: str, optional
        Inertial frame to compute the state vector
        (default: `ECLIPJ2000`).

    Returns
    -------
    float or numpy.ndarray
        True anomaly angle (degrees).

        If a list of :py:attr:`time` were provided,
        the results will be stored in an array.

    See Also
    --------
    spiceypy.spiceypy.spkezr
    spiceypy.spiceypy.oscltx

    """
    time = type_check(time, float, et)
    target = type_check(target, SpiceBody)

    if is_iter(time):
        return np.transpose([
            true_anomaly(t, target, abcorr=abcorr, frame=frame)
            for t in time
        ])

    state, _ = sp.spkezr(str(target.parent), time, frame, abcorr, str(target))
    nu = sp.oscltx(np.negative(state), time, target.parent.mu)[8]

    return np.degrees(nu)


def groundtrack_velocity(target, state):
    """Ground track velocity (km/s).

    Speed motion of the sub-observer point along the groundtrack.

    Caution
    -------
    This speed does not correspond to the norm of the rejection
    of the velocity vector of the observer in the target fixed frame.

    Warning
    -------
    This formula is only valid for a spheroid elongated along the
    axis of rotation (``c``). It is not correct for a generic ellipsoid.

    No aberration correction is applied.

    Parameters
    ----------
    target: str
        Target body name.
    state: str
        Target -> observer state position and velocity vectors.
        Computed at the observer time.

    Returns
    -------
    float or numpy.ndarray
        Ground track velocity (km/s).

        If a list of :py:attr:`state` is provided,
        the results will be stored in an array.

    Raises
    ------
    ValueError
        If the :py:attr:`state` arrays doesn't have the good shape.

    Note
    ----
    The tangential speed is obtained as product of the local radius of the
    observed body with the tangential angular speed:

    .. code-block:: text

        latitudinal
        component
            ^   x
            |  /
            | / <- tangential component
            |/
            o----> longitudinal component

                (the cos is to compensate the 'shrinking' of
                 longitude increasing the latitude)

    See Also
    --------
    spiceypy.spiceypy.recgeo
    spiceypy.spiceypy.dgeodr
    spiceypy.spiceypy.mxv

    """
    target = type_check(target, SpiceBody)

    if np.ndim(state) > 1:
        return np.transpose([
            groundtrack_velocity(target, s) for s in np.transpose(state)
        ])

    if np.shape(state)[0] != 6:
        raise ValueError('Invalid `state` shape.')

    xyz, v = state[:3], state[3:]

    re, _, rp = target.radii  # target equatorial and polar radii
    f = (re - rp) / re        # target flattening factor

    # Local radius
    _, lat, _ = sp.recgeo(xyz, re, f)
    r = re * rp / (np.sqrt((re**2 * np.sin(lat)**2) + (rp**2 * np.cos(lat)**2)))

    # Geodetic speed
    jacobi = sp.dgeodr(*xyz, re, f)
    vlon, vlat, vr = sp.mxv(jacobi, v)  # Longitudinal, latitudinal and radial components

    # Groundtrack speed
    gt_speed = np.sqrt(r**2 * ((vlon * np.cos(lat))**2 + vlat**2) + vr**2)

    return gt_speed


def pixel_scale(inst, target, emi, dist):
    """Instrument pixel resolution (km/pixel).

    Only the cross-track iFOV is used and projected
    on the target body in spherical geometry (corrected
    from the local emission angle).

    Parameters
    ----------
    target: str or SpiceBody
        Target body name.
    inst: str or SpiceInstrument
        Instrument name.
    emi: float, list or numpy.ndarray
        Local emission angle (in degrees).
    dist: float, list or numpy.ndarray
        Distance from the observer to the target body center (in km).

    Returns
    -------
    float or numpy.ndarray
        Local instrument pixel resolution (km/pix).

    See Also
    --------
    moon_coverage.math.sphere.sph_pixel_scale

    """
    target = type_check(target, SpiceBody)
    inst = type_check(inst, SpiceInstrument)

    return sph_pixel_scale(emi, inst.ifov_cross_track, dist, target.radius)
