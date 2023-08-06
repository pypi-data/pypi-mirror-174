# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['channels_graphql_ws']

package_data = \
{'': ['*']}

install_requires = \
['Django',
 'aiohttp>=3,<4',
 'asgiref',
 'channels>=3',
 'graphene>=2.1',
 'graphql-core>=2.2',
 'msgpack>=0.6.1,<2']

setup_kwargs = {
    'name': 'django-channels-graphql-ws-django4',
    'version': '0.9.3',
    'description': 'Django Channels based WebSocket GraphQL server with Graphene-like subscriptions',
    'long_description': 'None',
    'author': 'Alexander A. Prokhorov',
    'author_email': 'alexander.prokhorov@datadvance.net',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/datadvance/DjangoChannelsGraphqlWs',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
