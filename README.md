[![build](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml/badge.svg)](https://github.com/ronnie-llamado/pyRedPocket/actions/workflows/build.yml)
[![PyPI version](https://badge.fury.io/py/pyredpocket.svg)](https://pypi.org/project/pyredpocket/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pyredpocket)](https://pypi.org/project/pyredpocket/)

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
> ```python
> [ 
>   LineDetails(
>   phone_number='XXXXXXXXXX', 
>   voice_balance=-1, 
>   messaging_balance=-1, 
>   data_balance=2863, 
>   timestamp=1618587283.578837, 
>   start_date=datetime.date(2021, 4, 2), 
>   end_date=datetime.date(2021, 5, 4)
>   ) 
> ]
> ```
