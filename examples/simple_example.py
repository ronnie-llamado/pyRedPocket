
import os

from pyredpocket import RedPocket 

client = RedPocket(
    username=os.getenv('REDPOCKET_USER'), 
    password=os.getenv('REDPOCKET_PASSWORD'),
)

for d in client.details:
    print(d)
    print(
        f'{d.time}, '
        f'{d.phone_number}, '
        f'{d.days_remaining}, '
        f'{d.start_date}-{d.end_date}, '
        f'{d.data_balance}, '
        f'{d.messaging_balance}, '
        f'{d.voice_balance}'
    )
