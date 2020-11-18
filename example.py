
import os

from pyredpocket import Client

username = os.getenv('REDPOCKET_USER')
password = os.getenv('REDPOCKET_PASSWORD')
print(username, password)
c = Client(username, password)
lines = c.getLines()
for l in lines:
    d = c.getDetails(l)
    print(d.balances)
