# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b_roller']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0', 'python-slugify', 'pytube', 'requests', 'typer']

entry_points = \
{'console_scripts': ['broll = b_roller.__main__:app']}

setup_kwargs = {
    'name': 'b-roller',
    'version': '1.0.0',
    'description': 'Download resources from several sources across the web',
    'long_description': '# B-Roller\n\nDownload B-roll footage from YouTube for fair use purposes\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
