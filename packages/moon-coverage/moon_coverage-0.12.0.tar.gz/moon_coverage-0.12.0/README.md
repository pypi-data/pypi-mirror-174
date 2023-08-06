ESA Moon Coverage Toolbox
=========================

<img src="https://moon-coverage.univ-nantes.fr/en/0.12.0/_static/moon-coverage.svg" align="right" hspace="50" vspace="50" height="200" alt="Moon coverage logo">

[
    ![CI/CD](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/pipeline.svg)
    ![Coverage](https://juigitlab.esac.esa.int/datalab/moon-coverage/badges/main/coverage.svg)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/pipelines/main/latest)
[
    ![Documentation Status](https://readthedocs.org/projects/moon-coverage/badge/?version=latest)
](https://readthedocs.org/projects/moon-coverage/builds/)

[
    ![Latest version](https://img.shields.io/pypi/v/moon-coverage.svg?label=Latest%20release&color=lightgrey)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/tags)
[
    ![License](https://img.shields.io/pypi/l/moon-coverage.svg?color=lightgrey&label=License)
](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/blob/main/LICENSE.md)
[
    ![PyPI](https://img.shields.io/badge/PyPI-moon--coverage-blue?logo=Python&logoColor=white)
    ![Python](https://img.shields.io/pypi/pyversions/moon-coverage.svg?label=Python&logo=Python&logoColor=white)
](https://moon-coverage.univ-nantes.fr/pypi)

[
    ![Docs](https://img.shields.io/badge/Docs-moon--coverage.univ--nantes.fr-blue?&color=orange&logo=Read%20The%20Docs&logoColor=white)
](https://moon-coverage.univ-nantes.fr)
[
    ![DataLab](https://img.shields.io/badge/Datalab-datalabs.esa.int-blue?&color=orange&logo=Jupyter&logoColor=white)
](https://moon-coverage.univ-nantes.fr/datalab)
[
    ![Software Heritage](https://archive.softwareheritage.org/badge/origin/https://juigitlab.esac.esa.int/datalab/moon-coverage/)
](https://moon-coverage.univ-nantes.fr/swh)

---

The [moon-coverage](https://moon-coverage.univ-nantes.fr)
python package is a toolbox to perform
surface coverage analysis based on orbital trajectory configuration.
Its main intent is to provide an easy way to compute observation
opportunities of specific region of interest above the Galilean
satellites for the ESA-JUICE mission but could be extended in the
future to other space mission.

It is actively developed by
the [Laboratory of Planetology and Geosciences](https://lpg-umr6112.fr/)
(CNRS-UMR 6112) at Nantes University (France), under
[ESA-JUICE](https://sci.esa.int/web/juice) founding support.

<p align="center">
  <img src="https://moon-coverage.univ-nantes.fr/en/0.12.0/_images/lpg-esa.png" alt="LPG / ESA logos"/>
</p>

📦 Installation
---------------

The package is available on [PyPI](https://pypi.org/project/moon-coverage/) and can be installed very easily:

- If you are in a [`Jupyter environnement`](https://jupyter.org/), you can use the magic command `%pip` in a notebook cell and ▶️ `Run` it:
```bash
%pip install --upgrade moon-coverage
```

- or, if you are using a `terminal environment`, you can do:
```bash
pip install --upgrade moon-coverage
```

> __Note:__ If you plan to use this package with JUICE and you want to enable [PTR simulation with AGM](https://esa-ptr.readthedocs.io/).
> You can add a `juice` extra parameter in the `pip` install command: `pip install moon-coverage[juice]`


✏️ How to cite this package
---------------------------

If you use this package for your analyses, please consider using the following citation:

> Seignovert, Benoît, Gabriel Tobie, Rozenn Robidel, Claire Vallat, Inès Belgacem, and Nicolas Altobelli.
> Python Moon-Coverage Toolbox, LPG - Nantes Université, 2022.
> Version: 0.12.0, [moon-coverage.univ-nantes.fr](https://moon-coverage.univ-nantes.fr/en/0.12.0/),
> [hal-03648491](https://hal.inria.fr/hal-03648491),
> [swh:1:rel:9c89f93a167637432c71cfc7f84263576edc4d1b](https://archive.softwareheritage.org/browse/origin/directory/?origin_url=https://juigitlab.esac.esa.int/datalab/moon-coverage&release=0.12.0)

or can use this 📙 [BibTeX file](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/raw/main/moon-coverage.bib?inline=false).


⚡️ Issues and 💬 feedback
-------------------------

If you have any issue with this package, we highly recommend to take a look at:

- 📚 our [extended documentation online](https://moon-coverage.univ-nantes.fr/).
- 📓 the collection of [notebook examples](https://juigitlab.esac.esa.int/datalab/moon-coverage-notebooks).

If you did not find a solution there, feel free to:

- 📝 [open an issue](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/issues/new) (if you have an account on the [JUICE Gitlab](https://juigitlab.esac.esa.int/datalab/moon-coverage)).
- ✉️ send us an email at [&#109;&#111;&#111;&#110;&#45;&#99;&#111;&#118;&#101;&#114;&#97;&#103;&#101;&#64;&#117;&#110;&#105;&#118;&#45;&#110;&#97;&#110;&#116;&#101;&#115;&#46;&#102;&#114;](&#109;&#97;&#105;&#108;&#116;&#111;&#58;&#109;&#111;&#111;&#110;&#45;&#99;&#111;&#118;&#101;&#114;&#97;&#103;&#101;&#64;&#117;&#110;&#105;&#118;&#45;&#110;&#97;&#110;&#116;&#101;&#115;&#46;&#102;&#114;
)


🎨 Contribution and 🐛 fix bugs
-------------------------------

Contributions are always welcome and appreciated.
An account on the [JUICE Giltab](https://juigitlab.esac.esa.int/datalab/moon-coverage) is required.
You also need to install the latest version of [Poetry](https://python-poetry.org/docs/) (`≥1.2`), for example on _Linux/macOS_, you can run this command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Then you are good to go!

1. 🍴 [Fork this project](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/forks/new)

2. 🐑 Clone and 📦 install the repository locally:

```bash
git clone https://juigitlab.esac.esa.int/<YOUR_USERNAME>/moon-coverage
cd moon-coverage

poetry install --extras juice
```

3. ✍️ Make your edits and 🚧 write the tests.

4. 🚦 Double-check that the linters are happy 😱 🤔 😃 :
```bash
poetry run flake8 src/ tests/ docs/conf.py
poetry run pylint src/ tests/
```

5. 🛠 Check that your tests succeed 👍 and you have a coverage of 100% ✨ :

```bash
poetry run pytest
```

6. 📖 Complete and ⚙️ build the documentation (if needed):
```bash
cd docs/
poetry run make docs
```

7. 📤 Push your changes to your forked branch and 🚀 open a [new merge request](https://juigitlab.esac.esa.int/datalab/moon-coverage/-/merge_requests/new) explaining what you changed 🙌 👏 💪.
