# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['codeowners_backstage']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28,<3.0']

setup_kwargs = {
    'name': 'codeowners-backstage',
    'version': '0.1.3',
    'description': 'Preprocesses CODEOWNERS file, substituting group names with member emails taken from Backstage.',
    'long_description': '# codeowners-backstage\nPreprocesses CODEOWNERS file, substituting group names with member emails \nusing User/Group information taken from a [Backstage](https://backstage.io/) catalog.\n\n',
    'author': 'Adam Dziendziel',
    'author_email': 'adam.dziendziel@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/AdamDz/codeowners-backstage',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.7,<4.0.0',
}


setup(**setup_kwargs)
