[![build](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml/badge.svg)](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/pyredpocket.svg)](https://pypi.org/project/pyredpocket/)

# pyRedPocket

Python interface to RedPocket Mobile's website - to get current data, messaging and voice balances.

## Installation

```
pip install pyredpocket
```

## Example

```python
from pyredpocket import RedPocket

client = RedPocket(username='username', password='password')

print(client.details)
```
