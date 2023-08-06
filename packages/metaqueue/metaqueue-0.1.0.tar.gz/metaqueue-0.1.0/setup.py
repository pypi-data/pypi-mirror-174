# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metaqueue',
 'metaqueue.broker',
 'metaqueue.connectors',
 'metaqueue.engine',
 'metaqueue.exception',
 'metaqueue.instruments',
 'metaqueue.queue',
 'metaqueue.store',
 'metaqueue.tests',
 'metaqueue.tests.broker',
 'metaqueue.tests.connectors',
 'metaqueue.tests.engine',
 'metaqueue.tests.instruments',
 'metaqueue.tests.queue',
 'metaqueue.tests.store',
 'metaqueue.tests.utilities',
 'metaqueue.utilities']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=22.1.0,<23.0.0',
 'numpy>=1.23.4,<2.0.0',
 'psycopg2>=2.9.3,<3.0.0',
 'python-dotenv>=0.21.0,<0.22.0']

setup_kwargs = {
    'name': 'metaqueue',
    'version': '0.1.0',
    'description': 'Metaqueue enables simple and efficient metadata collection',
    'long_description': None,
    'author': 'RaphSku',
    'author_email': 'rapsku.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
