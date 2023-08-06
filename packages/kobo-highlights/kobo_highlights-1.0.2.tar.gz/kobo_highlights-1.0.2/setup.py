# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['kobo_highlights']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.0,<2.0.0',
 'rich>=12.2.0,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'typer[all]>=0.4.1,<0.5.0']

entry_points = \
{'console_scripts': ['kh = kobo_highlights.main:app']}

setup_kwargs = {
    'name': 'kobo-highlights',
    'version': '1.0.2',
    'description': 'Kobo Highlights is a CLI application to manage the bookmarks of your Kobo ereader. It can import them into a human-friendly markdown database.',
    'long_description': "**DISCLAIMER:** This is an unofficial project that I developed independently from Kobo\nand without any contact with them.\n\n# Kobo highlights \n\nKobo highlights is a simple CLI application to manage bookmarks from a Kobo erader. It\ncan import them into a markdown database where they can be easily accessed.\n\nKobo Highlights was developed in Python using [Typer](https://typer.tiangolo.com/) for\nthe CLI functionality and [Rich](https://github.com/Textualize/rich) for writing nice\ntext to the terminal.\n\nKobo highlights was develop as a personal project and it's design is based on how my\nparticular ereader handles bookmarks, so there are no guarantees that it will work on\nother models.\n\n# Requirements\n\nKobo highlights was developed and tested in [Fedora](https://getfedora.org/) and the\nautomatic tests are run in Ubuntu as macOS. I expect it to work properly on most\nLinux distributions and on macOS. It has not been testes on Windows, but you can try\nit.\n\nKobo highlights requires Python 3.10.\n\n# Installation\n\nThis project was developed using [Poetry](https://python-poetry.org/) and there are\nmultiple ways of installing it:\n\n* The recommended installation method is [downloading it from pypi](\n    https://pypi.org/project/kobo-highlights/): `pip install kobo-highlights`.\n\n* If you want to install Kobo Highlights directly from this repo note that development\ntakes place in the main branch, so make sure to install it from the commit corresponding\nto the last release.\nIn this case you cant install it with Poetry (run `poetry install` inside the repo) or\nwith pip (run `pip install .` inside the repo).\n\n# Quick guide\n\nOnce Kobo Highlights has been installed, it can be accessed running the `kh` command.\nIf you run `kh --help` you should see something like this:\n\nFrom that message, you can see that the available options from Kobo Highlights are:\n\n* `kh config` to manage your configuration.\n\n* `kh ls` to list your bookmarks. By default is prints only new bookmarks, you can use\nthe `--all` option to print all bookmarks instead.\n\n* `kh import` to import your bookmarks. It can be called with `all`, `new` (default),\na bookmark ID, a list of bookmarks IDs, a book title or a book author. Use\n`kh import --help` for more information.\n\nYou can run any of these commands with the `--help` option to find out more on how to\nuse them.\n\nThe first time you run Kobo Highlights you will be probably told that you need to create\na configuration file before doing anything else. You can just follow the instructions\nto create a valid configuration file. In the next section the program configuration is\nexplained in more detail.\n\n# Configuration\n\nKobo Highlights uses a [toml](https://github.com/toml-lang/toml) configuration file that\nis stored in the default directory \n[designated by Typer](https://typer.tiangolo.com/tutorial/app-dir/). In most Linux\nsystems this is in `~/.config/kobo_highlights`. The configuration file contains two\nfields:\n\n* `ereader_dir`: Is the absolute path to the directory where your erader is mounter.\nNotably, your ereader doesn't need to be mounted when you create the config file,\nbut you should specify the directory where you expect it to be mounted when you manage\nyour bookmarks.\n\n* `target_dir`: Is the absolute path to the directory where you want your markdown\ndatabase to be created. This database will contain one markdown file per book with\nthe highlighted text stored in block quotes.\n\nEvert time you run Kobo Highlights it will try to find a configuration file, if it\nfails, it will ask you if you want to create one interactively and save it. If you\ndon't want to create a configuration file, Kobo Highlights will stop.\n\nYou can manage your configuration file with the `kh config` command. In particular\nyou cant use `config show` to show your current configuration and `config new` to\ncreate and save a new configuration.\n\n# The markdown database\n\nThe main goal of Kobo highlights is to read the bookmarks from the ereader and format\nthem in a way in which they are easy to work with. I choose to do this by creating\na markdown database of the bookmarks. This database is located in the directory\nspecified in the configuration and will have a markdown file per book. The names\nof these files follow the convention `<book title> - <book author(s)>.md`.\n\nThe markdown files will contain, for each bookmark in that book, a\n[markdown block quote](https://spec.commonmark.org/0.30/#block-quotes) that contains\nthe text highlighted in the ereader potentially followed by a set of paragraphs\ncontaining the possible annotations that were made about the highlighted text.\n\nNote that Kobo highlights by default only imports new bookmarks to the markdown\ndatabase. To determine if a bookmark is already in the database, Kobo highlights creates\na hidden JSON file inside the markdown directory. Inside this hidden file Kobo\nHighlights stores the IDs of the bookmarks that have already been imported. This means\nthat even if you modify the markdown files (or even delete the completely), Kobo\nHighlights will  remember that bookmarks that you had imported and they will not be\nconsidered new.",
    'author': 'Pedro Videgain Barranco',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/videbar/kobo-highlights',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
