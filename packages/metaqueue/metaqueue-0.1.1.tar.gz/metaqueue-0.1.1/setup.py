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
    'version': '0.1.1',
    'description': 'Metaqueue enables simple and efficient metadata collection',
    'long_description': '[![Author][contributors-shield]][contributors-url]\n[![BSD-3 Clause License][license-shield]][license-url]\n![example workflow](https://github.com/RaphSku/metaqueue/actions/workflows/ci.yml/badge.svg)\n[![Metaqueue CD](https://github.com/RaphSku/metaqueue/actions/workflows/cd.yml/badge.svg)](https://github.com/RaphSku/metaqueue/actions/workflows/cd.yml)\n\n# metaqueue\n\n\n### Goal\nEfficiently run tasks concurrently and write metadata to a repository and write metainformation in a PostgresSQL database.\n\n### How to install it\n1. `pip install metaqueue`\n\n### How to use it\n1. Create tasks with any signature you like but this function has to fulfill two requirements, one is that you have to pass a `metadataengine` into the task and the other is that you have to declare it as async.\n2. In order to push metadata to the metadataengine, you can use the following:\n```python\nmetadataengine.publish_to_topic(Metadata(data, name, location, context))\n```\nThe metadata is associated to a topic which defines what kind of metadata is collected by the metadataengine. Metadata consists of 4 attributes, the data itself, the name, the location and a context. \nNote that a metadataengine is defined as\n```python\nMetadataEngine(topic, queue)\n```\nwhere topic is an enum element and queue is a metaqueue. A metaqueue is like a queue but with extra functionality. You don\'t have to worry about it but it is useful to know how a metaqueue is defined.\n```python\nMetaQueue(buffer_size = 3, dtype = int)\n```\nYou can provide a `buffer_size` which is the maximum capacity of the queue and `dtype` specifies which kind of data can be stored in it.\n3. Now, you are ready to kickstart the `TaskRunner` which is running the defined tasks concurrently. You can use it in the following way\n```python\nawait TaskRunner.run(async_funcs = [task1, task2], args = [task1_args, task2_args])\n```\nwhere the arguments are given as tuples into the list `args`. In this step, the tasks are not only run concurrently but also the metadata are collected via the metadataengine.\n4. Afterwards, we can define a Metabroker which will then push the metadata to a repository and push the information associated to the metadata into the PostgreSQL database.\n```python\nconnector  = StoreToLocalhost(path = "./log.txt")\nmetastore  = MetaStore(**db_info)\nmetabroker = MetaBroker(metadataengines = [engines[0], engines[1]], metastore = metastore, connector = connector)\nmetabroker.run(timeout = 10)\n```\nUp until now, only one connector is supported and that is a local file where the metadata gets written to. Since the MetaStore is using PostgreSQL as a database, you have to provide a running instance of that database. The easiest way is to spin up a docker container and pass the connection information to the MetaStore as `db_info`. `db_info` is a dict which contains the following keys: host, database, user, password, port. On the run method of the metabroker you can define a `timeout`. This should prevent running the metabroker for too long.\n5. View the result, inside of your PostgreSQL database you should find your database with a table `metadata` in which you can find all the information associated to your metadata. Also, the log file should be created and contain all the metadata in a format which resembles the OpenMetrics format.\n  \n[contributors-url]: https://github.com/RaphSku\n[license-url]: https://github.com/RaphSku/Metaqueue/blob/main/LICENSE\n\n[contributors-shield]: https://img.shields.io/badge/Author-RaphSku-red\n[license-shield]: https://img.shields.io/badge/License-BSD--3%20Clause-green\n',
    'author': 'RaphSku',
    'author_email': 'rapsku.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RaphSku/Metaqueue',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
