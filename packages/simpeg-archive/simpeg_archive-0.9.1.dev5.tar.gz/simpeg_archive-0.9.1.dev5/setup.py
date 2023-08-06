# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpeg_archive',
 'simpeg_archive.Mesh',
 'simpeg_archive.simpegEM1D',
 'simpeg_archive.utils']

package_data = \
{'': ['*'], 'simpeg_archive.simpegEM1D': ['Fortran/*']}

install_requires = \
['discretize',
 'numpy>=1.7',
 'properties[math]>=0.3.1b2',
 'pymatsolver>=0.1.1',
 'scipy>=0.13']

extras_require = \
{'regular': ['matplotlib']}

setup_kwargs = {
    'name': 'simpeg-archive',
    'version': '0.9.1.dev5',
    'description': 'Mira fork of SimPEG: Simulation and Parameter Estimation in Geophysics',
    'long_description': '.. image:: https://raw.github.com/simpeg/simpeg/master/docs/images/simpeg-logo.png\n    :alt: SimPEG Logo\n\nSimPEG\n======\n\n.. image:: https://img.shields.io/pypi/v/SimPEG.svg\n    :target: https://pypi.python.org/pypi/SimPEG\n    :alt: Latest PyPI version\n\n.. image:: https://img.shields.io/github/license/simpeg/simpeg.svg\n    :target: https://github.com/simpeg/simpeg/blob/master/LICENSE\n    :alt: MIT license\n\n.. image:: https://api.travis-ci.org/simpeg/simpeg.svg?branch=master\n    :target: https://travis-ci.org/simpeg/simpeg\n    :alt: Travis CI build status\n\n.. image:: https://codecov.io/gh/simpeg/simpeg/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/simpeg/simpeg\n    :alt: Coverage status\n\n.. image:: https://api.codacy.com/project/badge/Grade/4fc959a5294a418fa21fc7bc3b3aa078\n    :target: https://www.codacy.com/app/lindseyheagy/simpeg?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=simpeg/simpeg&amp;utm_campaign=Badge_Grade\n    :alt: codacy\n\nSimulation and Parameter Estimation in Geophysics  -  A python package for simulation and gradient based parameter estimation in the context of geophysical applications.\n\nThe vision is to create a package for finite volume simulation with applications to geophysical imaging and subsurface flow. To enable the understanding of the many different components, this package has the following features:\n\n* modular with respect to the spacial discretization, optimization routine, and geophysical problem\n* built with the inverse problem in mind\n* provides a framework for geophysical and hydrogeologic problems\n* supports 1D, 2D and 3D problems\n* designed for large-scale inversions\n\nYou are welcome to join forum and engage with people who use and develop SimPEG at: https://groups.google.com/forum/#!forum/simpeg.\n\nOverview Video\n--------------\n\n.. image:: https://img.youtube.com/vi/yUm01YsS9hQ/0.jpg\n    :target: https://www.youtube.com/watch?v=yUm01YsS9hQ\n    :alt: All of the Geophysics But Backwards\n\nWorking towards all the Geophysics, but Backwards - SciPy 2016\n\nCiting SimPEG\n-------------\n\nThere is a paper about SimPEG!\n\n\n    Cockett, R., Kang, S., Heagy, L. J., Pidlisecky, A., & Oldenburg, D. W. (2015). SimPEG: An open source framework for simulation and gradient based parameter estimation in geophysical applications. Computers & Geosciences.\n\n**BibTex:**\n\n.. code::\n\n    @article{cockett2015simpeg,\n      title={SimPEG: An open source framework for simulation and gradient based parameter estimation in geophysical applications},\n      author={Cockett, Rowan and Kang, Seogi and Heagy, Lindsey J and Pidlisecky, Adam and Oldenburg, Douglas W},\n      journal={Computers \\& Geosciences},\n      year={2015},\n      publisher={Elsevier}\n    }\n\nElectromagnetics\n****************\n\nIf you are using the electromagnetics module of SimPEG, please cite:\n\n    Lindsey J. Heagy, Rowan Cockett, Seogi Kang, Gudni K. Rosenkjaer, Douglas W. Oldenburg, A framework for simulation and inversion in electromagnetics, Computers & Geosciences, Volume 107, 2017, Pages 1-19, ISSN 0098-3004, http://dx.doi.org/10.1016/j.cageo.2017.06.018.\n\n**BibTex:**\n\n.. code::\n\n    @article{heagy2017,\n        title= "A framework for simulation and inversion in electromagnetics",\n        author= "Lindsey J. Heagy and Rowan Cockett and Seogi Kang and Gudni K. Rosenkjaer and Douglas W. Oldenburg",\n        journal= "Computers & Geosciences",\n        volume = "107",\n        pages = "1 - 19",\n        year = "2017",\n        note = "",\n        issn = "0098-3004",\n        doi = "http://dx.doi.org/10.1016/j.cageo.2017.06.018"\n    }\n\n\nInstalling from the sources\n===========================\n\nThis Python package can be installed with ``pip``.\nThe dependencies are defined in ``pyproject.toml``. It replaces the former ``requirements.txt`` and ``setup.py`` files\n(see `pip documentation`_ to learn more about ``pyproject.toml``).\n\nAs this branch is meant to be used with a geopps environment, some conflicting packages have been moved\nto "extras" and declared optional. To use it outside of ``geoapps``, install it with ``simpeg[regular]``.\n\n.. _pip documentation: https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/\n\nInstall from a local clone\n--------------------------\npip install path/to/simpeg[regular]\n\nInstall from a local clone in editable mode\n-------------------------------------------\npip install -e path/to/simpeg[regular]\n\n\nLinks\n-----\n\nWebsite:\nhttp://simpeg.xyz\n\n\nSlack (real time chat):\nhttp://slack.simpeg.xyz\n\n\nDocumentation:\nhttp://docs.simpeg.xyz\n\n\nCode:\nhttps://github.com/simpeg/simpeg\n\n\nTests:\nhttps://travis-ci.org/simpeg/simpeg\n\n\nBugs & Issues:\nhttps://github.com/simpeg/simpeg/issues\n',
    'author': 'Rowan Cockett',
    'author_email': 'rowanc1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://simpeg.xyz/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
}


setup(**setup_kwargs)
