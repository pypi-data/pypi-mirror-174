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
    'version': '0.1.1',
    'description': 'A simple package for visualising the results of a cypher-based graph query to Neo4j in Python.',
    'long_description': '# D3 Graph Vis\n\nA simple package for visualising a graph in a Jupyter notebook via D3.js. Supports lists of nodes/edges as well as Cypher queries to a Neo4j database.\n\n![Screenshot of an example graph](https://github.com/nlp-tlp/d3_graph_vis/blob/main/image_1.png?raw=true)\n\n## Installation\n\nIt\'s not an actual python package at the moment but the easiest way of importing it into a Jupyter notebook is to clone this repo into the same folder as the notebook, install the requirements from `requirements.txt`, then call:\n\n    from d3_graph_vis import D3Graph\n\n... one day I might put it on PyPI so that it can be installed via pip.\n\n## Usage\n\nFirst, import the package via\n\n    from d3_graph_vis import D3Graph\n\nThere are two ways to use this class.\n\n### Visualising nodes and links directly\n\nThe first is to visualise a given list of nodes and edges, for example:\n\n    nodes = [\n        {\n          "id": 1,\n          "category": "Person",\n          "name": "Bob",\n        },\n        {\n          "id": 2,\n          "category": "Food",\n          "name": "Jelly",\n        },\n        {\n          "id": 3,\n          "category": "Person",\n          "name": "Alice",\n        }\n    ]\n    links = [\n        {\n          "source": 1,\n          "target": 2,\n          "type": "EATS",\n        },\n        {\n          "source": 3,\n          "target": 1,\n          "type": "LIKES",\n        },\n    ]\n    d3_graph.visualise(nodes, links)\n\nThis will create a graph visualisation with three nodes ("Bob", "Jelly", "Alice"), and two links (Bob eats Jelly, Alice likes Bob). You can have other properties (such as `"age": 45` on Bob) - they\'ll be shown in the tooltip when hovering over a node.\n\nThe `"id"`, `"category"` and `"name"` properties are required on each node. The `"name"` property is what will be written on the nodes in the visualisation, while the `"category"` will determine their colour (more on this below).\n\nFor the links, `"source"` is the id of the source node, `"target"` is the id of the target node, and `"type"` is the type of relationship. These are all required.\n\n### Visualising the result of a Neo4j Cypher query\n\nThe second way is to use it to visualise the result of a Neo4j Cypher query. This requires you to have a Neo4j database running. First, connect D3Graph to neo4j via:\n\n    d3_graph.connect_to_neo4j("password")\n\nThe argument is the password of your Neo4j database. Then, you can run the following:\n\n    d3_graph.visualise_cypher(\'MATCH (n1:Entity)-[r]->(n2:Entity) RETURN n1, r, n2 LIMIT 500\')\n\nI am not sure whether it will work for literally any query, but it should.\n\nNote that unlike Neo4j, which has the \'connect result nodes\' option to automatically connect nodes that have relationships, you will need to return the relationships explicitly in your query. Only relationships in the `RETURN` statement will be visualised.\n\n### About the visualisation\n\nNodes are coloured based on the `category` property.\n\nFor the Cypher visualisation, the way the graph decides on the colour of each node is based on the last label of that node, i.e. if a node had the following labels:\n\n    Entity, Item\n\n... it would be coloured based on the `Item` label. The colours are determined automatically, i.e. each category receives its own unique colour.\n\n## Notes\n\nI am using `neo4j` (the Neo4j driver for Python) rather than `py2neo` because it turns out `py2neo` does not output the exact same results as Neo4j. The way this whole thing works is by creating a list of nodes from all node objects returned by the cypher query, then creating links (by linking nodes via their ids). It didn\'t seem possible in `py2neo`, but was pretty straightforward with the `neo4j` package.\n\nYou can run `src/template/template.html` by itself (i.e. open it directly in Firefox/Chrome) for development purposes. When running it this way, it will be populated by some dummy data specified in `src/template/dummyData.js`. It was a bit tricky to implement this as the template injection doesn\'t make sense in this context, so the code is a little confusing in places - I\'ve tried to comment it to clarify what is going on.\n',
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
