"""ESA API module."""

import json
from shutil import move
from urllib.parse import urlencode
from urllib.request import HTTPError, urlopen, urlretrieve

from .vars import DATA
from ..misc import logger


API = 'https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos'
ESA_API_CACHE = {}

ESA_MK_PREFIXES = {
    'BEPICOLOMBO': 'bc',
    'ENVISION': 'envision',
    'COMET-INTERCEPTOR': 'interceptor',
    'EXOMARS2016': 'em16',
    'EXOMARSRSP': 'emrsp',
    'GAIA': 'gaia',
    'HERA': 'hera',
    'HUYGENS': 'HUYGENS',
    'INTEGRAL': 'integral',
    'JUICE': 'juice',
    'JWST': 'jwst',
    'LUNAR-GATEWAY': 'lg',
    'MARS-EXPRESS': 'MEX',
    'ROSETTA': 'ROS',
    'SMART-1': 'SMART1',
    'SOLAR-ORBITER': 'solo',
    'VENUS-EXPRESS': 'VEX',
}


log_esa_api, debug_esa_api = logger('ESA API')


def esa_api(uri, **params):
    """Retrieve the tags from ESA Cosmos Bitbucket repo.

    Parameters
    ----------
    uri: str
        Cosmos Bitbucket API entrypoint.
    **params:
        Optional entrypoint parameters.

    Returns
    -------
    list
        List of values return by the ESA API.

    Raises
    ------
    IOError
        If the API URL is invalid (usually 404 error code).
    AttributeError
        If the API response does not contain a ``values`` field.

    Warning
    -------
    The API response must be in JSON and contains a `/children/values`
    or `/values` in its output.

    """

    url = uri + '?' + urlencode(params) if params else uri

    if url in ESA_API_CACHE:
        log_esa_api.debug('Use data from the cache: %s.', url)
        return ESA_API_CACHE[url]

    try:
        log_esa_api.debug('Downloading: %s', url)

        with urlopen(f'{API}/{url}') as resp:
            data = json.loads(resp.read())

        log_esa_api.debug('Data: %s', data)

    except HTTPError:
        raise IOError(f'Invalid `{url}`.') from None

    # Extract the output values
    if 'children' in data:
        data = data['children']

    values = data['values']

    # Recursive search is limit and `nextPageStart` is present
    if 'limit' not in params and 'nextPageStart' in data:
        params['start'] = data['nextPageStart']
        values += esa_api(uri, **params)

    # Cache the response values
    log_esa_api.debug('Saved the values in the cache.')
    ESA_API_CACHE[url] = values

    return values


def get_tag(mission, version='latest', **params):
    """Get tag version(s) of the metakernels from ESA Cosmos repo.

    .. code-block:: text

        https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/tags

    Parameters
    ----------
    mission: str
        Mission name in the cosmos repo.
    version: str, optional
        Version short key or ``latest`` or ``all`` (default: 'latest').
    **params
        API paging parameters (``limit``/``start``/``filterText``).

    Returns
    -------
    str or list
        Long SKD version key(s).

    Raises
    ------
    AttributeError
        If the mission name provided is invalid.
    ValueError
        If the requested version was not found.

    Note
    ----
    If multiple version have the same short version key, only
    the most recent will be returned. If you want a specific version
    you need to be as precise as possible.

    """
    if not mission:
        raise AttributeError('The mission name must be defined.')

    if version.lower() == 'all':
        log_esa_api.info('Get all the tags for `%s`.', mission)

    elif version.lower() == 'latest':
        log_esa_api.info('Get the latest tag for `%s`.', mission)
        params.update({'limit': 1})

    else:
        log_esa_api.info('Search for the tag closest to `%s` for `%s`.', version, mission)
        params.update({'filterText': version, 'limit': 1})

    values = esa_api(f'{mission.lower()}/tags', **params)

    tags = [value.get('displayId') for value in values]

    if not tags:
        raise ValueError(f'Version `{version}` is not available.')

    return tags if version.lower() == 'all' else tags[0]


class EsaMissionMetakernels(dict):
    """ESA mission metakernels.

    The metakernels are sorted by versions.

    The list of the metakernels for a given version
    is only computed when it is requested.

    """
    def __init__(self, mission):
        self.mission = mission

    def __repr__(self):
        n = len(self.versions)

        return '\n - '.join([
            f'<{self.__class__.__name__}> Mission: {self.mission} | {n} versions:',
            *self.versions
        ])

    def __contains__(self, version):
        return version in self.versions

    def __missing__(self, version):
        if version not in self.versions:
            raise KeyError(version)

        mks = get_mk(self.mission, mk='all', version=version)

        self[version] = mks
        return mks

    @property
    def versions(self) -> list:
        """Available tag versions."""
        return get_tag(self.mission, version='all')


def get_mk(mission, mk='latest', version='latest'):
    """Get metakernel file(s) from ESA Cosmos repo for a given tag.

    .. code-block:: text

        https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/browse/kernels/mk/?at=refs/tags/v270_20201113_001
        https://repos.cosmos.esa.int/socci/rest/api/1.0/projects/SPICE_KERNELS/repos/juice/raw/kernels/mk/juice_crema_3_0.tm?at=refs/tags/v270_20201113_001

    Parameters
    ----------
    mission: str
        Mission name in the cosmos repo.
    mk: str, optional
        Metakernel name/shortcut to download.
        If `latest` is provided (default), the lastest metakernel will be selected.
        If `all` is provided, the function will search all the available metakernel(s)
        for the provided tag.
    version: str, optional
        Tagged version `latest` (default) or `all`.
        If the version provided is not fully defined, the API will be query
        to search for the closest version.
        If `all` is provided, the function will list all the available metakernel(s)
        for all the tags.

    Returns
    -------
    str or list
        Metakernel file name.

    Raises
    ------
    AttributeError
        If the mission name provided is invalid.
    ValueError
        If not metakernel was found for the requested arguments.
    FileNotFoundError
        If the file is not found on the cosmos repo.

    """
    if not mission:
        raise AttributeError('The mission name must be defined.')

    # Get one or all the metakernel(s) for al the available versions
    if version.lower() == 'all':
        return EsaMissionMetakernels(mission)

    # Check if the version provided is a valid tag
    tag = get_tag(mission, version=version) if len(version) != 17 else version

    # Get all the metakernel for a given version
    if str(mk).lower() in ['latest', 'all']:
        log_esa_api.info('Get all the metakernel at `%s`.', tag)
        values = esa_api(f'{mission.lower()}/browse/kernels/mk/', at=f'refs/tags/{tag}')

        mks = [
            mk_file
            for value in values
            for mk_file in value['path']['components']
            if mk_file.lower().endswith('.tm')
        ]

        if mk.lower() == 'all':
            return mks

        # Select only the latest metakernel for the selected tag.
        mk = mks[-1]

    # Get a single metakernel
    if not str(mk).lower().endswith('.tm'):
        mk = esa_mk_name(mission, mk)

    fname = DATA / mission.lower() / tag / str(mk)

    if not fname.exists():
        log_esa_api.info('Get %s at `%s`.', mk, tag)

        url = f'{API}/{mission.lower()}/raw/kernels/mk/{mk}?at=refs/tags/{tag}'

        try:
            log_esa_api.debug('Download mk at: %s.', url)
            fout, _ = urlretrieve(url)
        except HTTPError:
            raise FileNotFoundError(f'`{mk}` at `{tag}` does not exist.') from None

        fname.parent.mkdir(parents=True, exist_ok=True)
        move(fout, fname)

    return fname


def esa_mk_name(mission, ref):
    """ESA metakernel name shortcuts.

    Parameters
    ----------
    mission: str
        ESA mission name.
    ref: str
        Mission metakernel reference. This could be a MK_IDENTIFIER
        (implicit versioned metakernel filename without ``.tm``),
        a shortcut name (without the mission name prefix) or a
        crema pattern (if it starts with a digit, see ``crema_ref()`` for details).

    Returns
    -------
    str
        Formatted mission metakernel filename.


    """
    mission_name = ESA_MK_PREFIXES.get(mission.upper(), None)

    if not mission_name:
        raise ValueError(
            f'SPICE metakernel not found for mission {mission} on ESA SPICE repository.')

    if str(ref)[0].isdigit():
        mk = f'{mission_name}_crema_{crema_ref(ref)}.tm'
    elif str(ref).lower().startswith(mission_name.lower()):
        mk = f'{ref}.tm'
    else:
        mk = f'{mission_name}_{ref}.tm'

    return mk.upper() if mission_name.isupper() else mk


def crema_ref(ref):
    """Get CReMA ref formatter."""
    crema = str(ref)

    # Replace with underscores
    for c in '.- ':
        crema = crema.replace(c, '_')

    # Special cases
    crema = crema.replace('(', '').replace('_only)', '')  # `(cruise only)` -> `cruise`

    return crema
