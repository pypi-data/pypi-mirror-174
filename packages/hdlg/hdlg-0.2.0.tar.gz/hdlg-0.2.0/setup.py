# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hdlg', 'hdlg.ui']

package_data = \
{'': ['*'], 'hdlg.ui': ['icons/*']}

install_requires = \
['PySide2>=5.15.2.1,<6.0.0.0',
 'WMI>=1.5.1,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'pywin32==304',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['hdlg = hdlg.hdlg:main']}

setup_kwargs = {
    'name': 'hdlg',
    'version': '0.2.0',
    'description': 'Modern GUI for hdl-dump.',
    'long_description': '![Banner](https://rawcdn.githack.com/rlaphoenix/hdlg/50bab8126da83a63e83bf6a5ce3d4d1f737ced2b/banner.png)\n\n[![Build status](https://github.com/rlaphoenix/hdlg/actions/workflows/ci.yml/badge.svg)](https://github.com/rlaphoenix/hdlg/actions/workflows/ci.yml)\n[![PyPI version](https://img.shields.io/pypi/v/hdlg)](https://pypi.python.org/pypi/hdlg)\n[![Python versions](https://img.shields.io/pypi/pyversions/hdlg)](https://pypi.python.org/pypi/hdlg)\n<a href="https://github.com/rlaphoenix/hdlg/blob/master/LICENSE">\n  <img align="right" src="https://img.shields.io/badge/license-GPLv3-blue" alt="License (GPLv3)"/>\n</a>\n\nHDLG is a modern GUI for hdl-dump with Batch installation capabilities.\n\n**hdl-dump**: <https://github.com/ps2homebrew/hdl-dump>  \n**wLaunchELF**: <https://github.com/ps2homebrew/wLaunchELF>\n\n![Preview](https://user-images.githubusercontent.com/17136956/198822365-f244dcf6-3050-45f2-83dd-c32c4d36f976.png)  \n*Preview as of October 2022.*\n\n## Installation\n\n    pip install --user hdlg\n\nTo run hdlg, type `hdlg` into any terminal, command prompt, app launcher, or the start menu.\n\nIf you wish to manually install from the source, take a look at [Building](#building-source-and-wheel-distributions).\n\n## To-do\n\n- [x] Craft initial GUI with Qt.\n- [x] Push to PyPI and add relevant Badges.\n- [x] Add PyInstaller make file.\n- [x] Add local PS2 HDD connection option.\n- [x] List installed games of selected HDD.\n- [x] Show HDD information like Disk Size, Space Used, and such.\n- [x] Add ability to install a new game to selected HDD.\n- [x] Add batch installation support by selecting more than one file.\n- [ ] Create a file based settings system.\n- [ ] Add per-install settings like startup, flags, and DMA mode.\n- [ ] Add ability to format an HDD for use with a PS2.\n- [ ] Add ability to rename the Game Name of installed games.\n- [ ] Add ability to extract an installed game from the PS2 HDD.\n- [ ] Add ability to view an installed game\'s sector table.\n- [ ] Add ability to set a custom icon to an installed game.\n- [ ] Add remote PS2 HDD (samba) connection option.\n- [ ] Add Inno Setup script.\n- [ ] Add Linux support.\n- [ ] Add macOS support.\n\n## Building\n\nThis project requires [Poetry], so feel free to take advantage and use it for its various conveniences like\nbuilding sdist/wheel packages, creating and managing dependencies, virtual environments, and more.\n\nNote:\n\n- Source Code may have changes that may be old, not yet tested or stable, or may have regressions.\n- Only run or install from Source Code if you have a good reason. Examples would be to test for regressions, test\n  changes (either your own or other contributors), or to research the code (agreeing to the [LICENSE](LICENSE)).\n- [Poetry] is required as it\'s used as the [PEP 517] build system, virtual environment manager, dependency manager,\n  and more.\n\n  [Poetry]: <https://python-poetry.org/docs/#installation>\n  [PEP 517]: <https://www.python.org/dev/peps/pep-0517>\n\n### Install from Source Code\n\n    git clone https://github.com/rlaphoenix/hdlg.git\n    cd hdlg\n    pip install --user .\n\n### Building source and wheel distributions\n\n    poetry build\n\nYou can specify `-f` to build `sdist` or `wheel` only. Built files can be found in the `/dist` directory.\n\n### Packing with PyInstaller\n\n    poetry run python pyinstaller.py\n\nThe build is now available at `./dist`.\n',
    'author': 'PHOENiX',
    'author_email': 'rlaphoenix@pm.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rlaphoenix/hdlg',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
