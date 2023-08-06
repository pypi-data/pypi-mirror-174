# tree_units

## Resources

Law is mostly tree-based. This library facilitates the creation of codifications, statutes, and documents in the form of trees. This sets the pydantic-based fields for later use via `sqlpyd` in corpus-trees and enables validated recursive models to serve as branches for the tree.

## Example Data

Some functions to help with tree like (json-ish) python structures.

```python
>>> data = [
        {
            "item": "Preliminary Title",
            "units": [
                {
                    "item": "Chapter 1",
                    "caption": "Effect and Application of Laws",
                    "units": [
                        {
                            "item": "Article 1",
                            "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
                        },
                        {
                            "item": "Article 2",
                            "content": "Laws shall take effect after fifteen days following the completion of their publication either in the Official Gazette or in a newspaper of general circulation in the Philippines, unless it is otherwise provided. (1a)\n",
                        },
                    ],
                }
            ],
        }
    ]
```

## Setter of IDs

```python
>>> from tree_units.utils import set_node_ids
>>> set_node_ids(data)
# all nodes in the tree will now have an `id` key, e.g.:
{
    "item": "Article 1",
    "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
    "id": "1.1.1.1."
},
```

## Getter of Node by ID

```python
>>> from tree_units.utils import get_node_id
>>> get_node_id("1.1.1.1.")
{
    "item": "Article 1",
    "content": 'This Act shall be known as the "Civil Code of the Philippines." (n)\n',
    "id": "1.1.1.1."
}
```

## Enables Limited Enumeration Per Layer

```python
>>> raw = [
    {"content": "Parent Node 1"},
    {
        "content": "Parent Node 2",
        "units": [
            {
                "content": "Hello World!",
                "units": [
                    {"content": "Deeply nested content"},
                    {"content": "Another deeply nested one"},
                ],
            },
            {"content": "Another Hello World!"},
        ],
    },
]
>>> from tree_units.utils import Layers
>>> Layers.DEFAULT(raw) # note the addition of the `item` key to the raw itemless data
[{'content': 'Parent Node 1', 'item': 'I'},
 {'content': 'Parent Node 2',
  'units': [{'content': 'Hello World!',
    'units': [{'content': 'Deeply nested content', 'item': 1},
     {'content': 'Another deeply nested one', 'item': 2}],
    'item': 'A'},
   {'content': 'Another Hello World!', 'item': 'B'}],
  'item': 'II'}]

```

## Fetcher of Values

```python
>>> from tree_units.utils import test_fetch_values_from_key
>>> list(test_fetch_values_from_key(data[0]), "item")
[
    "Preliminary Title",
    "Chapter 1",
    "Article 2",
    "Article 1",
]
```
