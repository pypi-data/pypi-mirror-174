# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['gqvis']
install_requires = \
['ipython==7.34.0', 'neo4j>=5.2.0,<6.0.0']

setup_kwargs = {
    'name': 'gqvis',
    'version': '0.1.0',
    'description': 'A simple package for visualising the results of a cypher-based graph query to Neo4j in Python.',
    'long_description': None,
    'author': 'Michael Stewart',
    'author_email': 'michael.stewart.webdev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
