# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['astral']

package_data = \
{'': ['*']}

extras_require = \
{':python_version < "3.7"': ['dataclasses'],
 ':python_version < "3.9"': ['backports.zoneinfo'],
 ':sys_platform == "win32"': ['tzdata']}

setup_kwargs = {
    'name': 'astral',
    'version': '3.1',
    'description': 'Calculations for the position of the sun and moon.',
    'long_description': "# Astral\n\nThis is 'astral' a Python module which calculates\n\n- Times for various positions of the sun: dawn, sunrise, solar noon,\nsunset, dusk, solar elevation, solar azimuth and rahukaalam.\n- The phase of the moon.\n\nFor documentation see the <https://astral.readthedocs.io/en/latest/index.html>\n\n## Package Status\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/sffjunkie/astral/astral-test) ![PyPI - Downloads](https://img.shields.io/pypi/dm/astral)\n",
    'author': 'Simon Kennedy',
    'author_email': 'sffjunkie+code@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sffjunkie/astral',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
