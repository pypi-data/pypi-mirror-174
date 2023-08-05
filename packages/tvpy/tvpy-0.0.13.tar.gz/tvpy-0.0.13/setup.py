# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tvpy']

package_data = \
{'': ['*']}

install_requires = \
['1337x>=1.2.3,<2.0.0',
 'Pillow>=9.2.0,<10.0.0',
 'beautifulsoup4>=4.11.1,<5.0.0',
 'climage>=0.1.3,<0.2.0',
 'fire>=0.4.0,<0.5.0',
 'fs.smbfs>=1.0.5,<2.0.0',
 'libtorrent>=2.0.7,<3.0.0',
 'parse-torrent-title>=2.4,<3.0',
 'pyright>=1.1.273,<2.0.0',
 'requests>=2.28.1,<3.0.0',
 'rich>=12.5.1,<13.0.0',
 'toml>=0.10.2,<0.11.0',
 'tqdm>=4.64.0,<5.0.0',
 'websockets>=10.3,<11.0']

entry_points = \
{'console_scripts': ['tv-down = tvpy.main:tv_down',
                     'tv-html = tvpy.main:tv_html',
                     'tv-info = tvpy.main:tv_info',
                     'tv-json = tvpy.main:tv_json',
                     'tv-klyn = tvpy.main:tv_klyn',
                     'tv-renm = tvpy.main:tv_renm',
                     'tv-subs = tvpy.main:tv_subs',
                     'tvpy = tvpy.main:tvpy']}

setup_kwargs = {
    'name': 'tvpy',
    'version': '0.0.13',
    'description': '📺 TvPy',
    'long_description': '# 📺 TvPy \nCommand line tv show manager.\n\n[![asciicast](https://asciinema.org/a/hQeLoj8lYcGtJvErlTWifdmfo.svg)](https://asciinema.org/a/hQeLoj8lYcGtJvErlTWifdmfo)\n\n## Installation\n```shell\n> pip install tvpy\n```\n\n<!-- ## Get an API Key\nYou need to get an API key from [TMDB](https://www.themoviedb.org/settings/api) and save it as `key.txt` in your working directory. -->\n\n## Usage\n```shell\n> mkdir Carnival.Row \n> tvpy Carnival.Row \n```\n\n## Other commands\n\nDownload information from TMDB:\n```shell\n> mkdir Carnival.Row \n> tv-json Carnival.Row\n```\n\nDisplay information about a tv show:\n```shell\n> mkdir Carnival.Row \n> tv-info Carnival.Row\n```\n\nDownload a tv show:\n```shell\n> mkdir Carnival.Row \n> tv-down Carnival.Row\n```\n\nDownload (Hebrew) subtitles for a tv show:\n```shell\n> mkdir Carnival.Row \n> tv-subs Carnival.Row\n```\n\nRename files to match the pattern `<title>.S<season>E<episode>.<ext>`\n```shell\n> mkdir Carnival.Row \n> tv-renm Carnival.Row\n```\n\n| :exclamation:  Danger   |\n|-------------------------|\n\nRemove unused files\n```shell\n> mkdir Carnival.Row \n> tv-klyn Carnival.Row\n```\n\n\n',
    'author': 'Gilad Kutiel',
    'author_email': 'gilad.kutiel@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/gkutiel/tvpy/tree/master',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
