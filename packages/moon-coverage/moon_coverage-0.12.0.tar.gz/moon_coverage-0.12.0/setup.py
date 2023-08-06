# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['moon_coverage',
 'moon_coverage.cli',
 'moon_coverage.debug',
 'moon_coverage.esa',
 'moon_coverage.events',
 'moon_coverage.html',
 'moon_coverage.maps',
 'moon_coverage.math',
 'moon_coverage.misc',
 'moon_coverage.projections',
 'moon_coverage.rois',
 'moon_coverage.spice',
 'moon_coverage.ticks',
 'moon_coverage.trajectory']

package_data = \
{'': ['*'], 'moon_coverage.maps': ['data/*'], 'moon_coverage.rois': ['data/*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'matplotlib>=3.6.0,<4.0.0',
 'numpy>=1.23.0,<2.0.0',
 'spiceypy>=5.1.1,<6.0.0']

extras_require = \
{'juice': ['esa-ptr>=1.0,<2.0']}

entry_points = \
{'console_scripts': ['kernel-download = moon_coverage.cli:cli_kernel_download',
                     'mk-download = moon_coverage.cli:cli_metakernel_download']}

setup_kwargs = {
    'name': 'moon-coverage',
    'version': '0.12.0',
    'description': 'Moon Coverage toolbox',
    'long_description': 'ESA Moon Coverage Toolbox\n=========================\n\n<img src="https://moon-coverage.univ-nantes.fr/en/0.12.0/_static/moon-coverage.svg" align="right" hspace="50" vspace="50" height="200" alt="Moon coverage logo">\n\n[\n    ![CI/CD](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/pipeline.svg)\n    ![Coverage](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/coverage.svg)\n](https://juigitlab.esac.esa.int/datalab/moon-coverage/pipelines/main/latest)\n[\n    ![Documentation Status](https://readthedocs.org/projects/moon-coverage/badge/?version=latest)\n](https://readthedocs.org/projects/moon-coverage/builds/)\n\n[\n    ![Latest version](https://img.shields.io/pypi/v/moon-coverage.svg?label=Latest%20release&color=lightgrey)\n](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/tags)\n[\n    ![License](https://img.shields.io/pypi/l/moon-coverage.svg?color=lightgrey&label=License)\n](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/blob/main/LICENSE.md)\n[\n    ![PyPI](https://img.shields.io/badge/PyPI-moon--coverage-blue?logo=Python&logoColor=white)\n    ![Python](https://img.shields.io/pypi/pyversions/moon-coverage.svg?label=Python&logo=Python&logoColor=white)\n](https://moon-coverage.univ-nantes.fr/pypi)\n\n[\n    ![Docs](https://img.shields.io/badge/Docs-moon--coverage.univ--nantes.fr-blue?&color=orange&logo=Read%20The%20Docs&logoColor=white)\n](https://moon-coverage.univ-nantes.fr)\n[\n    ![DataLab](https://img.shields.io/badge/Datalab-datalabs.esa.int-blue?&color=orange&logo=Jupyter&logoColor=white)\n](https://moon-coverage.univ-nantes.fr/datalab)\n[\n    ![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://juigitlab.esac.esa.int/datalab/moon-coverage/)\n](https://moon-coverage.univ-nantes.fr/swh)\n\n---\n\nThe [moon-coverage](https://moon-coverage.univ-nantes.fr)\npython package is a toolbox to perform\nsurface coverage analysis based on orbital trajectory configuration.\nIts main intent is to provide an easy way to compute observation\nopportunities of specific region of interest above the Galilean\nsatellites for the ESA-JUICE mission but could be extended in the\nfuture to other space mission.\n\nIt is actively developed by\nthe [Laboratory of Planetology and Geosciences](https://lpg-umr6112.fr/)\n(CNRS-UMR 6112) at Nantes University (France), under\n[ESA-JUICE](https://sci.esa.int/web/juice) founding support.\n\n<p align="center">\n  <img src="https://moon-coverage.univ-nantes.fr/en/0.12.0/_images/lpg-esa.png" alt="LPG / ESA logos"/>\n</p>\n\n📦 Installation\n---------------\n\nThe package is available on [PyPI](https://pypi.org/project/moon-coverage/) and can be installed very easily:\n\n- If you are in a [`Jupyter environnement`](https://jupyter.org/), you can use the magic command `%pip` in a notebook cell and ▶️ `Run` it:\n```bash\n%pip install --upgrade moon-coverage\n```\n\n- or, if you are using a `terminal environment`, you can do:\n```bash\npip install --upgrade moon-coverage\n```\n\n> __Note:__ If you plan to use this package with JUICE and you want to enable [PTR simulation with AGM](https://esa-ptr.readthedocs.io/).\n> You can add a `juice` extra parameter in the `pip` install command: `pip install moon-coverage[juice]`\n\n\n✏️ How to cite this package\n---------------------------\n\nIf you use this package for your analyses, please consider using the following citation:\n\n> Seignovert, Benoît, Gabriel Tobie, Rozenn Robidel, Claire Vallat, Inès Belgacem, and Nicolas Altobelli.\n> Python Moon-Coverage Toolbox, LPG - Nantes Université, 2022.\n> Version: 0.12.0, [moon-coverage.univ-nantes.fr](https://moon-coverage.univ-nantes.fr/en/0.12.0/),\n> [hal-03648491](https://hal.inria.fr/hal-03648491),\n> [swh:1:rel:9c89f93a167637432c71cfc7f84263576edc4d1b](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://juigitlab.esac.esa.int/datalab/moon-coverage&release=0.12.0)\n\nor can use this 📙 [BibTeX file](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/raw/main/moon-coverage.bib?inline=false).\n\n\n⚡️ Issues and 💬 feedback\n-------------------------\n\nIf you have any issue with this package, we highly recommend to take a look at:\n\n- 📚 our [extended documentation online](https://moon-coverage.univ-nantes.fr/).\n- 📓 the collection of [notebook examples](https://juigitlab.esac.esa.int/datalab/moon-coverage-notebooks).\n\nIf you did not find a solution there, feel free to:\n\n- 📝 [open an issue](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/issues/new) (if you have an account on the [JUICE Gitlab](https://juigitlab.esac.esa.int/datalab/moon-coverage)).\n- ✉️ send us an email at [&#109;&#111;&#111;&#110;&#45;&#99;&#111;&#118;&#101;&#114;&#97;&#103;&#101;&#64;&#117;&#110;&#105;&#118;&#45;&#110;&#97;&#110;&#116;&#101;&#115;&#46;&#102;&#114;](&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#109;&#111;&#111;&#110;&#45;&#99;&#111;&#118;&#101;&#114;&#97;&#103;&#101;&#64;&#117;&#110;&#105;&#118;&#45;&#110;&#97;&#110;&#116;&#101;&#115;&#46;&#102;&#114;\n)\n\n\n🎨 Contribution and 🐛 fix bugs\n-------------------------------\n\nContributions are always welcome and appreciated.\nAn account on the [JUICE Giltab](https://juigitlab.esac.esa.int/datalab/moon-coverage) is required.\nYou also need to install the latest version of [Poetry](https://python-poetry.org/docs/) (`≥1.2`), for example on _Linux/macOS_, you can run this command:\n\n```bash\ncurl -sSL https://install.python-poetry.org | python3 -\n```\n\nThen you are good to go!\n\n1. 🍴 [Fork this project](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/forks/new)\n\n2. 🐑 Clone and 📦 install the repository locally:\n\n```bash\ngit clone https://juigitlab.esac.esa.int/<YOUR_USERNAME>/moon-coverage\ncd moon-coverage\n\npoetry install --extras juice\n```\n\n3. ✍️ Make your edits and 🚧 write the tests.\n\n4. 🚦 Double-check that the linters are happy 😱 🤔 😃 :\n```bash\npoetry run flake8 src/ tests/ docs/conf.py\npoetry run pylint src/ tests/\n```\n\n5. 🛠 Check that your tests succeed 👍 and you have a coverage of 100% ✨ :\n\n```bash\npoetry run pytest\n```\n\n6. 📖 Complete and ⚙️ build the documentation (if needed):\n```bash\ncd docs/\npoetry run make docs\n```\n\n7. 📤 Push your changes to your forked branch and 🚀 open a [new merge request](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/merge_requests/new) explaining what you changed 🙌 👏 💪.\n',
    'author': 'LPG Nantes Université',
    'author_email': 'moon-coverage@univ-nantes.fr',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://juigitlab.esac.esa.int/datalab/moon-coverage',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
