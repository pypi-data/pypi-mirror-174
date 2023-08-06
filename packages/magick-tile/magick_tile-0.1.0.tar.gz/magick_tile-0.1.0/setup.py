# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['magick_tile']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.9.1,<2.0.0', 'typer[all]>=0.6.1,<0.7.0']

entry_points = \
{'console_scripts': ['magick_tile = magick_tile.main:app']}

setup_kwargs = {
    'name': 'magick-tile',
    'version': '0.1.0',
    'description': 'Use Imagemagick to efficiently create derivative tiles of a very large image, and structure them into directories compliant with IIIF Level 0',
    'long_description': 'None',
    'author': 'Matthew Lincoln',
    'author_email': 'matthew.d.lincoln@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
