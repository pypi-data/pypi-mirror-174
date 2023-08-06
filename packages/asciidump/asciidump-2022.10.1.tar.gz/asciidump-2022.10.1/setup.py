# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['asciidump']

package_data = \
{'': ['*'], 'asciidump': ['templates/*']}

install_requires = \
['Jinja2>=3.0.1,<4.0.0',
 'libsass>=0.21.0,<0.22.0',
 'rich>=10.11.0,<11.0.0',
 'tomli>=2.0.0,<3.0.0']

entry_points = \
{'console_scripts': ['asciidump = asciidump:main']}

setup_kwargs = {
    'name': 'asciidump',
    'version': '2022.10.1',
    'description': '',
    'long_description': None,
    'author': 'Matthew Barber',
    'author_email': 'quitesimplymatt@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/honno/asciidump',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
