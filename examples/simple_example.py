
import os

from pyRedPocket import Client

username = os.getenv('REDPOCKET_USER')
password = os.getenv('REDPOCKET_PASSWORD')

client = Client(username=username, password=password)
for line, d in client.details.items():
    print(
        f'{d.time}, '
        f'{d.phone_number}, '
        f'{d.start_date}-{d.end_date}, '
        f'{d.data_balance}, '
        f'{d.messaging_balance}, '
        f'{d.voice_balance}'
    )
