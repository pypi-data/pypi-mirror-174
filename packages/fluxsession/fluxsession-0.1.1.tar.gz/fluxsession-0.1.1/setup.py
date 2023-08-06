# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fluxsession']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0', 'telethon>=1.25.4,<2.0.0']

setup_kwargs = {
    'name': 'fluxsession',
    'version': '0.1.1',
    'description': 'A Session converter for Telegram unoffical client.',
    'long_description': '# FluxSession\n',
    'author': 'Md. Hasibul Kabir',
    'author_email': '46620128+HasibulKabir@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
