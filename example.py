
import os

from pyredpocket import Client

username = os.getenv('REDPOCKET_USER')
password = os.getenv('REDPOCKET_PASSWORD')
print(username, password)
c = Client(username, password)
lines = c.getLines()
for lin in lines:
    d = c.getDetails(lin)
    nd = {
        'time': d.timestamp,
        'phone_number': d.data['mdn'],
        'data': d.data_balance,
        'messaging': d.messaging_balance,
        'voice': d.voice_balance,
        'start_date': d.start_date,
        'end_date': d.end_date,
    }
    print(
        '{phone_number},'
        '{start_date}, '
        '{end_date}, '
        '{time}, '
        '{data}, '
        '{messaging}, '
        '{voice}'
        .format(**nd)
    )
