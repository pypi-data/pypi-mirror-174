# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tree_units', 'tree_units.utils']

package_data = \
{'': ['*']}

install_requires = \
['citation-utils>=0.0.13,<0.0.14',
 'email-validator>=1.3.0,<2.0.0',
 'statute-utils>=0.0.11,<0.0.12']

setup_kwargs = {
    'name': 'tree-units',
    'version': '0.0.7',
    'description': 'Law mostly consists of tree-like nodes. This package supports a common tree format for Philippine Codifications, Statutes, and Documents, using a uniform node structure (i.e., leaves of a tree) identified by a given material path.',
    'long_description': '# tree_units\n\n## Resources\n\nLaw is mostly tree-based. This library facilitates the creation of codifications, statutes, and documents in the form of trees. This sets the pydantic-based fields for later use via `sqlpyd` in corpus-trees and enables validated recursive models to serve as branches for the tree.\n\n```python\ntrees=CodeUnit(\n        item=\'Modern Child and Youth Welfare Code\',\n        caption=None,\n        content=None,\n        id=\'1.\',\n        history=None,\n        units=[\n            CodeUnit(\n                item=\'Title I\',\n                caption=\'General Principles\',\n                content=None,\n                id=\'1.1.\',\n                history=None,\n                units=[\n                    CodeUnit(\n                        item=\'Article 1\',\n                        caption=\'Declaration of Policy.\',\n                        content=None,\n                        id=\'1.1.1.\',\n                        history=None,\n                        units=[\n                            CodeUnit(\n                                item=\'Paragraph 1\',\n                                caption=None,\n                                content=\'The Child is one of the most important assets of the nation. Every effort should be exerted to promote his welfare and enhance his opportunities for a useful and happy life.\',\n                                id=\'1.1.1.1.\',\n                                history=None,\n                                units=[]\n                            ),\n                            CodeUnit(\n                                item=\'Paragraph 2\',\n                                caption=None,\n                                content=\'The child is not a mere creature of the State. Hence, his individual traits and aptitudes should be cultivated to the utmost insofar as they do not conflict with the general welfare.\',\n                                id=\'1.1.1.2.\',\n                                history=None,\n                                units=[]\n                            ),\n                        ]\n                    )\n                ]\n            )\n        ]\n    ...\n)\n```\n\n## Example Data\n\nSome functions to help with tree like (json-ish) python structures.\n\n```python\n>>> data = [\n        {\n            "item": "Preliminary Title",\n            "units": [\n                {\n                    "item": "Chapter 1",\n                    "caption": "Effect and Application of Laws",\n                    "units": [\n                        {\n                            "item": "Article 1",\n                            "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n                        },\n                        {\n                            "item": "Article 2",\n                            "content": "Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\\n",\n                        },\n                    ],\n                }\n            ],\n        }\n    ]\n```\n\n## Setter of IDs\n\n```python\n>>> from tree_units.utils import set_node_ids\n>>> set_node_ids(data)\n# all nodes in the tree will now have an `id` key, e.g.:\n{\n    "item": "Article 1",\n    "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n    "id": "1.1.1.1."\n},\n```\n\n## Getter of Node by ID\n\n```python\n>>> from tree_units.utils import get_node_id\n>>> get_node_id("1.1.1.1.")\n{\n    "item": "Article 1",\n    "content": \'This Act shall be known as the "Civil Code of the Philippines." (n)\\n\',\n    "id": "1.1.1.1."\n}\n```\n\n## Enables Limited Enumeration Per Layer\n\n```python\n>>> raw = [\n    {"content": "Parent Node 1"},\n    {\n        "content": "Parent Node 2",\n        "units": [\n            {\n                "content": "Hello World!",\n                "units": [\n                    {"content": "Deeply nested content"},\n                    {"content": "Another deeply nested one"},\n                ],\n            },\n            {"content": "Another Hello World!"},\n        ],\n    },\n]\n>>> from tree_units.utils import Layers\n>>> Layers.DEFAULT(raw) # note the addition of the `item` key to the raw itemless data\n[{\'content\': \'Parent Node 1\', \'item\': \'I\'},\n {\'content\': \'Parent Node 2\',\n  \'units\': [{\'content\': \'Hello World!\',\n    \'units\': [{\'content\': \'Deeply nested content\', \'item\': 1},\n     {\'content\': \'Another deeply nested one\', \'item\': 2}],\n    \'item\': \'A\'},\n   {\'content\': \'Another Hello World!\', \'item\': \'B\'}],\n  \'item\': \'II\'}]\n\n```\n\n## Fetcher of Values\n\n```python\n>>> from tree_units.utils import test_fetch_values_from_key\n>>> list(test_fetch_values_from_key(data[0]), "item")\n[\n    "Preliminary Title",\n    "Chapter 1",\n    "Article 2",\n    "Article 1",\n]\n```\n',
    'author': 'Marcelino G. Veloso III',
    'author_email': 'mars@veloso.one',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
