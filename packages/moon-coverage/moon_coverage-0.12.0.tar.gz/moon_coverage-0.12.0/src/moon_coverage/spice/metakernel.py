"""Metakernel module.

The full metakernel specifications are available on NAIF website:

https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/req/kernel.html

"""

import re
from functools import reduce
from multiprocessing import Pool
from pathlib import Path
from tempfile import NamedTemporaryFile

from .kernel import format_data, kernel_parser
from ..misc import wget


KERNEL_MAX_LENGTH = 255


class MetaKernel:
    """Metakernel object.

    Parameters
    ----------
    mk: str or pathlib.Path
        Metakernel file name.
    download: bool, optional
        Download the missing kernels (default: ``False``).
    remote: str or int, optional
        Remote kernel source. If none is provided (default), the content of
        the file will be parsed to search for a remote base value (with ``://``).
        If multiple remotes are present, the first one will be used by default.
        You can provide an integer to choose which one you want to use.
        This value is not required if all the kernel are present locally (it is only
        used to download the missing kernels).
    **kwargs: dict, optional
        Path key(s) and value(s) to be substituted in ``KERNELS_TO_LOAD``.

    Raises
    ------
    FileNotFoundError
        If the metakernel file does not exists locally.
    KeyError
        If the file provided does not a ``KERNELS_TO_LOAD`` key.
        Or, if a keyword argument is provided but is neither
        ``PATH_SYMBOLS`` nor ``PATH_VALUES`` are present.
    ValueError
        If one of the provided key is not part of the
        available ``SYMBOLS``.

    """
    _tmp_mk = None

    def __init__(self, mk, download=False, remote=0, **kwargs):
        self.__content, self.data = None, None
        self.fname = mk
        self.remote = remote

        if kwargs:
            self.update_path_values(**kwargs, download=download)
        else:
            self.check(download=download)

    def __str__(self):
        return self.fname.name

    def __repr__(self):
        return f'<{self.__class__.__name__}> {self}'

    def __iter__(self):
        """Iterate on the metakernel itself.

        This function should be used in combination with
        :func:`spiceypy.furnsh` function.
        Ir  will create a temporary metakernel file
        with an edited ``PATH_VALUES`` to load the kernel
        where they are really located.

        """
        with self as f:
            yield f

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __hash__(self):
        """Metakernel content hash."""
        return hash(tuple(self.kernels))

    def __enter__(self):
        """Create and open a temporary Metakernel file with the new content."""
        if self._tmp_mk is None:
            self._tmp_mk = NamedTemporaryFile(
                'w',
                prefix=self.fname.stem + '-',
                suffix='.tm',
                delete=False,
            )
            self._tmp_mk.write(self.content)
            self._tmp_mk.seek(0)

        return self._tmp_mk.name

    def __exit__(self, *args):
        """Close and remove the temporary file."""
        self._tmp_mk.close()
        Path(self._tmp_mk.name).unlink()
        self._tmp_mk = None

    @property
    def fname(self):
        """Metakernel filename."""
        return self.__fname

    @fname.setter
    def fname(self, fname):
        """Metakernel filename setter and content checker.

        Raises
        ------
        FileNotFoundError
            If the file does not exists locally.
        KeyError
            If the file provided does not a KERNELS_TO_LOAD key.

        """
        self.__fname = Path(fname)

        if not self.fname.exists():
            raise FileNotFoundError(self.fname)

        self.load_mk()

    @property
    def remote(self):
        """Kernel remote source."""
        return self.__remote

    @remote.setter
    def remote(self, remote):
        """Kernel remote source setter."""
        self.__remote = remote if isinstance(remote, str) else self.get_remote(remote)

    def load_mk(self):
        """Load kernel content and data."""
        self.__content, self.data = kernel_parser(self.fname)

        if 'KERNELS_TO_LOAD' not in self.data:
            raise KeyError('KERNELS_TO_LOAD key is missing.')

    def update_path_values(self, download=False, **kwargs):
        """Update path values.

        Parameters
        ----------
        download: bool, optional
            Download the missing kernels (default: ``False``).
        **kwargs: any
            Path symbol and value to edit in the file.

        Raises
        ------
        KeyError
            If the file provided does not a PATH_VALUES
            or PATH_SYMBOLS keys.
        ValueError
            If the provided key was not part of the
            available SYMBOLS.

        """
        for required in ('PATH_VALUES', 'PATH_SYMBOLS'):
            if required not in self.data:
                raise KeyError(f'{required} key is missing')

        symbols = self.data['PATH_SYMBOLS']

        for key, value in kwargs.items():
            symbol = key.upper()

            if symbol not in symbols:
                raise ValueError(f'Symbol: `{symbol}` is not '
                                 'part of PATH_SYMBOLS (`' +
                                 '`, `'.join(symbols) +
                                 '`)')

            index = symbols.index(symbol)
            self.data['PATH_VALUES'][index] = str(value)

        self.check(download=download)

    @property
    def content(self):
        """Metakernel content."""
        if 'PATH_VALUES' not in self.data:
            return self.__content

        return re.sub(
            r' *PATH_VALUES\s*=\s*\(\s*[\w\'\_\-\.]+\s*\)',
            format_data(path_values=self.data['PATH_VALUES']),
            self.__content)

    def get_remote(self, i=0) -> str:
        """Get remote URL kernel source from the file content.

        Raises
        ------
        ValueError
            If more than one remote was found in the content.
            An explicit remote can be supplied in ``__init__`` to avoid
            this issue.

        """
        remotes = [line.strip() for line in self.content.splitlines() if '://' in line]

        if not remotes:
            return None

        return remotes[i]

    def _replace(self, values) -> list:
        """Replace symbols by values."""
        symbols = ['$' + symbol for symbol in self.data.get('PATH_SYMBOLS', [])]
        return [
            reduce(lambda s, kv: s.replace(*kv), zip(symbols, values), kernel)
            for kernel in self.data['KERNELS_TO_LOAD']
        ]

    @property
    def kernels(self) -> list:
        """Kernels to load."""
        return self._replace(self.data.get('PATH_VALUES', []))

    @property
    def urls(self) -> list:
        """Kernels urls based on the remote source.

        If the remote was not provided either in ``__init__``
        nor in the file content, the urls will be empty.

        """
        remote, n = self.remote, len(self.data.get('KERNELS_TO_LOAD', []))

        return self._replace(n * [remote]) if remote is not None else n * [None]

    def check(self, download=False):
        """Check if all the kernels are locally available.

        SPICE constrains:

        - The maximum length of any file name, including any path
          specification, is 255 characters.

        Parameters
        ----------
        download: bool, str
            Download all the missing kernels.

        Raises
        ------
        BufferError
            If the resulting kernel length is larger than
            the SPICE constrain of 255 characters.
        FileNotFoundError
            If the kernel is missing locally.

        """
        missing = []
        for kernel, url in zip(self.kernels, self.urls):
            if len(kernel) > KERNEL_MAX_LENGTH:
                raise BufferError(f'`{kernel}` is too long '
                                  f'({KERNEL_MAX_LENGTH} characters max).')

            if not Path(kernel).exists():
                if not download:
                    raise MissingKernel(kernel, remote=self.remote,
                                        symbols=self.data.get('PATH_SYMBOLS'))

                if url is None:
                    raise MissingKernelsRemote(kernel)

                missing.append((url, kernel))

        # Use all core available to download the missing kernels.
        if missing:
            with Pool() as p:
                p.starmap(wget, set(missing))  # SET => avoid duplicates


class MissingKernel(FileNotFoundError):
    """Missing kernel locally."""
    def __init__(self, kernel, remote=None, symbols=None):
        msg = f'`{kernel}` was not found locally. '
        msg += 'You can add `download=True` to download it automatically'
        msg += f' from `{remote}`' if remote else ''

        if symbols:
            _symbols = '|'.join([symbol.lower() for symbol in symbols])

            msg += ' or/and you can change the kernel path value(s) by adding '
            msg += f"`{_symbols}='path/to/my/kernels'`"

        msg += '.'

        super().__init__(msg)


class MissingKernelsRemote(FileNotFoundError):
    """Missing kernels remote source."""
    def __init__(self, kernel):
        msg = f'Impossible to download the missing kernel `{kernel}`. '
        msg += "You need to provide a `remote='[https|http|ftp]://kernels.domain.tld/'`."
        super().__init__(msg)
