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
    'version': '0.1.4',
    'description': 'Download resources from several sources across the web',
    'long_description': '# ADW (asset downloader)\n\n## Supported sources\n\n### YouTube\n\nSupport to download both audio and video through *PyTube*.\n\n### Unsplash\n\nUses the [Unsplash API](https://unsplash.com/developers).\nYou need to set your *Unsplash Access key* as the value of the `ADW_UNSPLASH_API_KEY` environment variable.\n\n### Giphy \n\nUses the [Giphy API](https://developers.giphy.com/). \nYou need to set your *Giphy API key* as the value of the `ADW_GIPY_API_KEY` environment variable.\n\n### Iconfinder\n\nUses the [Iconfinder API](https://developer.iconfinder.com/reference/overview-1).\nYou need to set your *Iconfinder API key* as the value of the `ADW_ICONFINDER_API_KEY` environment variable.\n\n### Pexels \n\nUses the [Pexels API](https://www.pexels.com/api/).\nYou need to set your *Pexels API key* as the value of the `ADW_PEXELS_API_KEY` environment variable.\n\n### Pixabay\n\nUses the [Pixabay API](https://pixabay.com/service/about/api/).\nYou need to set your *Pixabay API key* as the value of the `ADW_PIXABAY_API_KEY` environment variable.\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
