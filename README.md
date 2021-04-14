[![build](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml/badge.svg)](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml)

# pyRedPocket

Python interface to RedPocket Mobile's website - to get data, messaging and voice balances.

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
