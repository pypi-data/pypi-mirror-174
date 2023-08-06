# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['graphtask']

package_data = \
{'': ['*']}

install_requires = \
['joblib>=1.1.1,<2.0.0', 'networkx>=2.8.7,<3.0.0', 'stackeddag>=0.3.3,<0.4.0']

extras_require = \
{'visualize': ['pygraphviz==1.10']}

setup_kwargs = {
    'name': 'graphtask',
    'version': '0.0.1',
    'description': 'Build implicit task graphs from functions and process them in parallel.',
    'long_description': '# graphtask\n\n[![Check Status](https://github.com/davnn/graphtask/workflows/check/badge.svg?branch=main&event=push)](https://github.com/davnn/graphtask/actions?query=workflow%3Acheck)\n[![Dependencies Status](https://img.shields.io/badge/dependencies-up%20to%20date-brightgreen.svg)](https://github.com/davnn/graphtask/pulls?utf8=%E2%9C%93&q=is%3Apr%20author%3Aapp%2Fdependabot)\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Security: bandit](https://img.shields.io/badge/security-bandit-green.svg)](https://github.com/PyCQA/bandit)\n[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/davnn/graphtask/blob/main/.pre-commit-config.yaml)\n[![Semantic Versions](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--versions-e10079.svg)](https://github.com/davnn/graphtask/releases)\n![Coverage Report](assets/images/coverage.svg)\n\nThe project roughly follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html).\n',
    'author': 'David Muhr',
    'author_email': 'muhrdavid+github@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davnn/graphtask',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
