
from redpocket_monitor import getRedPocketBalances


balance_string = \
'''RedPocket Balances for {mdn} as of {date} at {time}

Refresh Date     : {aed}
Days Remaining   : {remaining_days}
Voice Balance    : {voice_balance}
Messaging Balance: {messaging_balance}
Data Balance (MB): {data_balance}
'''

def print_balances():
    balances = getRedPocketBalances()
    for i in balances:
        print( balance_string.format( **i ) )
