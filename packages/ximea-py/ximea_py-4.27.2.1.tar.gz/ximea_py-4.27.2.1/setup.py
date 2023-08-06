# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ximea']

package_data = \
{'': ['*'],
 'ximea': ['libs/x32/*', 'libs/x64/*', 'libs/xarm32/*', 'libs/xarm64/*']}

setup_kwargs = {
    'name': 'ximea-py',
    'version': '4.27.2.1',
    'description': 'XIMEA camera API',
    'long_description': '# ximea-py\n\nThis module provides a python interface to XIMEA cameras. It is simply a repackaging of XIMEA\'s python drivers available at https://www.ximea.com/downloads/recent/XIMEA_Linux_SP.tgz (package/api/Python/v3/ximea) in order to allow for easier installation with pip, e.g. into virtual or conda environments.\n\n# Installation\n\nOn Linux, add users that will use the camera to the "plugdev" group:\n\n`sudo usermod -aG plugdev <myuser>`\n\nInstall with:\n\n`pip install ximea-py`\n\nand use like so:\n\n```\nimport ximea.xiapi\n\nximea.xiapi.Camera()\n...\n```\n',
    'author': 'Jacob Feder',
    'author_email': 'jacobsfeder@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
