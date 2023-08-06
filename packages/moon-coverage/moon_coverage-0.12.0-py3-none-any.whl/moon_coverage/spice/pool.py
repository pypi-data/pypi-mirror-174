"""Spice kernel pool module."""

from functools import wraps

import numpy as np

import spiceypy as sp

from .kernel import get_item
from .metakernel import MetaKernel
from .references import SpiceRef
from .times import tdb, utc
from ..misc import depreciated, logger


log_spice_pool, debug_spice_pool = logger('Spice Pool')


class MetaSpicePool(type):
    """Meta Spice kernel pool object."""
    # pylint: disable=no-value-for-parameter, unsupported-membership-test

    MK_HASH = {}

    def __repr__(cls):
        n = int(cls)
        if n == 0:
            desc = 'EMPTY'
        else:
            desc = f'{n} kernel'
            desc += 's'
            desc += ' loaded:\n - '
            desc += '\n - '.join(cls.kernels)

        return f'<{cls.__name__}> {desc}'

    def __int__(cls):
        return cls.count()

    def __len__(cls):
        return cls.count()

    def __hash__(cls):
        return cls.hash(cls.kernels)

    def __eq__(cls, other):
        if isinstance(other, (str, tuple, list)):
            return hash(cls) == cls.hash(other)

        return hash(cls) == other

    def __iter__(cls):
        return iter(cls.kernels)

    def __contains__(cls, kernel):
        return cls.contains(kernel)

    def __add__(cls, kernel):
        return cls.add(kernel)

    def __sub__(cls, kernel):
        return cls.remove(kernel)

    def __getitem__(cls, item):
        return get_item(item)

    @staticmethod
    def count() -> int:
        """Count the number of kernels in the pool."""
        return int(sp.ktotal('ALL'))

    @property
    def kernels(cls):
        """Return the list of kernels loaded in the pool."""
        return tuple(
            sp.kdata(i, 'ALL')[0] for i in range(cls.count())
        )

    def hash(cls, kernels) -> int:
        """Hash a (meta)kernel or a list of (meta)kernels."""
        if isinstance(kernels, (str, MetaKernel)):
            return cls.hash((kernels, ))

        kernels_hash = ()
        for kernel in kernels:
            if isinstance(kernel, MetaKernel):
                mk = kernel
                # Hash of the metakernel and all the `kernels` loaded with it
                kernels_hash += (hash(mk), *(hash(k) for k in mk.kernels))

            elif kernel in cls.MK_HASH:  # Check if the kernel is in mk hash cached
                kernels_hash += (cls.MK_HASH[kernel],)

            elif kernel is not None:  # If not found, use the kernel hash if not None
                kernels_hash += (hash(kernel),)

        return hash(kernels_hash)

    def contains(cls, kernel):
        """Check if the kernel is in the pool."""
        return kernel in cls.kernels or hash(kernel) in cls.MK_HASH.values()

    def add(cls, kernel, purge=False):
        """Add a kernel to the pool."""
        if purge:
            cls.purge()

        if isinstance(kernel, (tuple, list)):
            for _kernel in kernel:
                cls.add(_kernel, purge=False)

        elif kernel in cls:
            raise ValueError(f'Kernel `{kernel}` is already in the pool.')

        elif kernel is not None:
            log_spice_pool.debug('Add `%s` in the SPICE pool', kernel)

            if isinstance(kernel, MetaKernel):
                with kernel as mk:
                    # `mk` is the name of a `NamedTemporaryFile` (see `MetaKernel`)
                    sp.furnsh(mk)

                    log_spice_pool.debug('Cache metakernel original hash.')
                    cls.MK_HASH[mk] = hash(kernel)
            else:
                sp.furnsh(kernel)

    def remove(cls, kernel):
        """Remove the kernel from the pool if present."""
        if kernel not in cls:
            raise ValueError(f'Kernel `{kernel}` is not in the pool.')

        log_spice_pool.debug('Remove %s', kernel)
        sp.unload(kernel)

    def purge(cls):
        """Purge the pool from all its content."""
        log_spice_pool.info('Purge the pool')
        sp.kclear()
        cls.MK_HASH = {}

    def windows(cls, *refs, fmt='UTC'):
        """Get kernels windows on a collection of bodies in the pool.

        Parameters
        ----------
        refs: str, int or SpiceRef
            Body(ies) reference(s).
        fmt: str, optional
            Output format:

            - ``UTC`` (default)
            - ``TDB``
            - ``ET``

        Returns
        -------
        np.array([[float,float], …])
            Start and stop times windows in the requested format.

        Raises
        ------
        KeyError
            If the requested reference does not have a specific coverage
            range in the pool.

        """
        refs = {int(ref): ref for ref in map(SpiceRef, refs)}

        windows = []
        for i in range(cls.count()):
            kernel, ext, *_ = sp.kdata(i, 'ALL')

            if ext == 'CK':
                ids = set(sp.ckobj(kernel))
                cov = cls._ck_cov

            elif ext == 'PCK':
                ids = sp.cell_int(1000)
                sp.pckfrm(kernel, ids)
                ids = set(ids)
                cov = cls._pck_cov

            elif ext == 'SPK':
                ids = set(sp.spkobj(kernel))
                cov = cls._spk_cov

            else:
                ids = set()
                cov = None

            for ref in ids & set(refs):
                log_spice_pool.debug('Found `%s` in %s', refs[ref], kernel)

                if ets := cov(kernel, ref):
                    windows.append([np.min(ets), np.max(ets)])  # Coverage per file

        if not windows:
            values = list(refs.values())
            err = 'The windows for '
            err += f'{values[0]} was' if len(values) == 1 else f'{values} were'
            err += ' not found.'
            raise KeyError(err)

        return cls._fmt_windows(windows, fmt=fmt)

    @staticmethod
    def _fmt_windows(ets_windows, fmt='UTC'):
        """Format ET windows.

        Parameters
        ----------
        ets_windows: list
            ET windows.
        fmt: str, optional
            Output format:

            - ``UTC`` (default)
            - ``TDB``
            - ``ET``

        Returns
        -------
        np.array([[float,float], …])
            Start and stop times windows in the requested format.

        Raises
        ------
        TypeError
            If the provided format is invalid.

        """
        if fmt.upper() == 'ET':
            return np.array(ets_windows)

        if fmt.upper() == 'UTC':
            return np.array([utc(w) for w in ets_windows], dtype=np.datetime64)

        if fmt.upper() == 'TDB':
            return np.array([tdb(w) for w in ets_windows], dtype='<U27')

        raise TypeError(f'Output format unknown: `{fmt}`, '
                        'only [`UTC`|`TDB`|`ET`] are accepted.')

    @staticmethod
    def _ck_cov(ck, ref: int):
        """Get CK coverage for given body."""
        cover = sp.ckcov(ck, ref, False, 'SEGMENT', 0.0, 'TDB')
        ets = [
            [cover[i * 2], cover[i * 2 + 1]] for i in range(sp.wncard(cover))
        ]

        log_spice_pool.debug('ET windows: %r', ets)
        return ets

    @staticmethod
    def _pck_cov(pck, ref: int):
        """Get PCK coverage for given body."""
        cover = sp.cell_double(2000)
        sp.pckcov(pck, ref, cover)
        ets = list(cover)

        log_spice_pool.debug('ET coverage: %r', ets)
        return [ets]

    @staticmethod
    def _spk_cov(spk, ref: int):
        """Get SPK coverage for given body."""
        ets = list(sp.spkcov(spk, ref))

        log_spice_pool.debug('ET coverage: %r', ets)
        return [ets]

    def coverage(cls, *refs, fmt='UTC'):
        """Get coverage for a collection of bodies in the pool.

        Parameters
        ----------
        refs: str, int or SpiceRef
            Body(ies) reference(s).
        fmt: str, optional
            Output format:

            - ``UTC`` (default)
            - ``TDB``
            - ``ET``

        Returns
        -------
        [str, str] or [float, float]
            Start and stop times covered for the requested format.

        Note
        ----
        If multiple values are available, only the ``max(start)``
        and ``min(stop)`` are kept.

        Raises
        ------
        TypeError
            If the output format is invalid.
        ValueError
            If the start time is after the stop time

        """
        starts, ends = cls.windows(*refs, fmt='ET').T

        start, stop = np.max(starts), np.min(ends)

        if start > stop:
            raise ValueError(
                f'MAX start time ({tdb(start)}) is after MIN stop time ({tdb(stop)}).')

        if fmt.upper() == 'UTC':
            start, stop = utc(start, stop)

        elif fmt.upper() == 'TDB':
            start, stop = tdb(start, stop)

        elif fmt.upper() != 'ET':
            raise TypeError(
                f'Output format unknown: `{fmt}`, only [`UTC`|`TDB`|`ET`] are accepted.')

        return start, stop


class SpicePool(metaclass=MetaSpicePool):
    """Spice kernel pool singleton.

    See: :class:`.MetaSpicePool` for details.

    """


def check_kernels(func):
    """Spice Pool kernels checker decorator.

    The parent object must implement a :func:`__hash__`
    function and have a :attr:`kernels` attribute.

    """
    @wraps(func)
    def wrapper(_self, *args, **kwargs):
        """Check if the content of pool have changed.

        If the content changed, the pool will be purge and the kernels reloaded.

        """
        if SpicePool != hash(_self):
            log_spice_pool.info(
                'The content of the pool changed -> the kernels will be reloaded.')
            SpicePool.add(_self.kernels, purge=True)

        return func(_self, *args, **kwargs)
    return wrapper


@depreciated('0.8.0')
class SPICEPool(SpicePool):
    """Spice kernel pool object."""
