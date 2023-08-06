"""SPICE limb computation."""

import numpy as np

import spiceypy as sp

from ..math.vectors import vector_rejection


def limb_ip_pt(et_obs, observer_id, target_id, obs_frame, obs_ray, target_frame,
               abcorr='NONE'):
    r"""Limb impact parameter point on a target from a ray at the observer position.

    Impact parameter vector based on the ray emerging form the observer.
    No check is performed to know it the surface of the target is intersected.

    .. code-block:: text

        · target
        | ∖
        |   ·
        |     ∖  <- Target -> Impact parameter vector
        |       ·  Impact parameter point ( ip vector ⟂ ray)
        |     ⋰
        |   ·
        | /  <- Observer emerging Ray
        · Observer

    Parameters
    ----------
    time: float
        Observer Ephemeris Time.
    observer_id: int
        Observer id code.
    target_id: int
        Target body id code.
    obs_frame: str
        Observer reference frame relative to which
        the ray's direction vector is expressed.
    obs_ray: tuple or list of tuple
        Ray direction vector emanating from the observer.
    target_frame: str
        Target reference frame relative to impact parameter
        vector is expressed (from the target center).
    abcorr: str, optional
        Aberration correction (default: 'None').
        See ``Danger`` section below.

    Returns
    -------
    (float, float, float) or np.ndarray
        Limb impact parameter XYZ coordinates in the target body fixed frame
        (expressed in km).

        If a list of time were provided, the results will be stored
        in a (3, N) array.

    Raises
    ------
    NotImplementedError
        If a light time correction is required.

    Danger
    ------
    No implementation of the limb impact parameter is directly available in
    the NAIF SPICE routines. In this function we tried to implement our own
    but support for light aberration correction is not implemented yet.
    Use it at your own risks.

    See Also
    --------
    spiceypy.spiceypy.spkezp

    """
    if abcorr.upper() != 'NONE':
        raise NotImplementedError('Light time correction are not implemented yet')

    # No light time correction
    s = 0

    # Get the observer -> target vector
    target_j2000, lt = sp.spkezp(target_id, et_obs, 'J2000', abcorr, observer_id)

    # Invert the vector and compute the time
    obs_j2000 = np.negative(target_j2000)  # Target -> Observer
    et_target = et_obs - s * lt            # Target time

    # Inverted ray in J2000 frame when the observe received it
    cmat = sp.pxform(obs_frame, 'J2000', et_obs)
    ray_j2000 = sp.mxv(cmat, np.negative(obs_ray))

    # Check that the ray is pointing to the target direction
    if np.dot(obs_j2000, ray_j2000) <= 0:
        return np.array([np.nan, np.nan, np.nan])

    # Compute the impact parameter in J2000 frame
    ip_j2000 = vector_rejection(obs_j2000, ray_j2000)

    # Convert the impact parameter from J2000 to target fixed frame
    tmat = sp.pxform('J2000', target_frame, et_target)
    ip_target = sp.mxv(tmat, ip_j2000)

    return ip_target
