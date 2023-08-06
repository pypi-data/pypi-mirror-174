# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wf_test']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.0,<8.0.0', 'tox>=3.27.0,<4.0.0']

extras_require = \
{':extra == "docs"': ['sphinx[docs]>=5.3.0,<6.0.0',
                      'sphinx-autodoc-typehints[docs]>=1.19.4,<2.0.0',
                      'sphinx-click[docs]>=4.3.0,<5.0.0',
                      'myst-parser[docs]>=0.18.1,<0.19.0',
                      'furo[docs]>=2022.9.29,<2023.0.0']}

setup_kwargs = {
    'name': 'wf-test',
    'version': '0.1.1rc1',
    'description': 'Test Workflows.',
    'long_description': '# Workflows-test\n\nThis is just a dummy repo to test the [`workflows`](https://github.com/hrshdhgd/workflows) GitHub Action project.\n',
    'author': 'Harshad Hegde',
    'author_email': 'hhegde@lbl.gov',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
