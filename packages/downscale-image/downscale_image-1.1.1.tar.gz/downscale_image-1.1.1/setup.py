# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['downscale_image']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0', 'pathspec>=0.10.1,<0.11.0']

entry_points = \
{'console_scripts': ['downscale-image = downscale_image.__main__:main']}

setup_kwargs = {
    'name': 'downscale-image',
    'version': '1.1.1',
    'description': 'downscale image to desired file size',
    'long_description': '# downscale_image\nA utility to downscale an image to the desired file size.\n\nRelies on an install of ffmpeg to incrementally downscale the image file into a new file.\n\nThis modules provides the script `downscale-image`\n\n```\n> downscale-image --help\nUsage: downscale-image [OPTIONS] IN_FILE\n\n  Downscale in_file to desired max-size.\n\nOptions:\n  --max-size INTEGER RANGE   Max output size (in MB)  [default: 2; x>0]\n  --add-to-right-click-menu  (Windows only) Register this program in right\n                             click menu for supported file types.\n  --help                     Show this message and exit.\n```\n',
    'author': 'mshafer1',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mshafer1/downscale_image',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
