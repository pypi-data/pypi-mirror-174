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
    'version': '0.1.1',
    'description': 'Use Imagemagick to efficiently create derivative tiles of a very large image, and structure them into directories compliant with IIIF Level 0',
    'long_description': "# magick-tile\n\n[![PyPi version](https://img.shields.io/pypi/v/magick-tile.svg)](https://pypi.org/project/magick-tile/)\n[![pytest](https://github.com/mdlincoln/magick_tile/actions/workflows/pytest.yml/badge.svg)](https://github.com/mdlincoln/magick_tile/actions/workflows/pytest.yml)\n\nThis package and command-line utility relies on Imagemagick to efficiently create derivative tiles of a very large image, and structure them into directories compliant with [IIIF Level 0](https://iiif.io/api/image/3.0/compliance/#5-level-0-compliance) specification for static sites.\n\nThis takes inspiration heavily from https://github.com/zimeon/iiif/blob/master/iiif_static.py, but uses ImageMagick rather than Pillow in order to speed up generation at the expense of a less flexible treatment of images.\n\n## Prerequisites\n\n- Python > 3.9\n- [Imagemagick](https://imagemagick.org/index.php) must be available on your path\n\n## Installation\n\n```\npip install magick-tile\n```\n\n## Run\n\n```\n Usage: magick_tile [OPTIONS] SOURCE OUTPUT IDENTIFIER\n\n Efficiently create derivative tiles of a very large image, and structure them into\n directories compliant with IIIF Level 0.\n\n╭─ Arguments ──────────────────────────────────────────────────────────────────────╮\n│ *    source          FILE       [required]                                       │\n│ *    output          DIRECTORY  Destination directory for tiles [required]       │\n│ *    identifier      TEXT       Image identifier to be written to final          │\n│                                 info.json (e.g.                                  │\n│                                 https://example.com/iiif/my_image)               │\n│                                 [required]                                       │\n╰──────────────────────────────────────────────────────────────────────────────────╯\n╭─ Options ────────────────────────────────────────────────────────────────────────╮\n│ --tile-size                 INTEGER                   Tile size to produce       │\n│                                                       [default: 512]             │\n│ --format                    [jpg|tif|png|gif|jp2|pdf  File formats to generate   │\n│                             |webp]                    (must be supported by      │\n│                                                       Imagemagick's 'convert')   │\n│                                                       [default: jpg]             │\n│ --install-completion                                  Install completion for the │\n│                                                       current shell.             │\n│ --show-completion                                     Show completion for the    │\n│                                                       current shell, to copy it  │\n│                                                       or customize the           │\n│                                                       installation.              │\n│ --help                                                Show this message and      │\n│                                                       exit.                      │\n╰──────────────────────────────────────────────────────────────────────────────────╯\n\n```\n\nThis will create and populate the specified output directory with tiles from a given image.\n\nN.b. because several of the Imagemagick utilities called here already utilize multiple cores, returns for running this script in parallel diminish rapidly.\n\n---\n[Matthew Lincoln](https://matthewlincoln.net)\n",
    'author': 'Matthew Lincoln',
    'author_email': 'matthew.d.lincoln@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mdlincoln/magick-tile',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
