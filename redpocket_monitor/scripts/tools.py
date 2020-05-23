
import argparse 
import os
import sys

import redpocket_monitor 


balance_string = \
'''
Phone Number     : {mdn}
Current Date/Time: {date} {time}
Refresh Date     : {aed}
Days Remaining   : {remaining_days}
Voice Balance    : {voice_balance}
Messaging Balance: {messaging_balance}
Data Balance (MB): {data_balance}
'''

def get_balances():

    parser = argparse.ArgumentParser()
    parser.add_argument( '--save', action='store_true' )
    parser.add_argument( '--print', action='store_true' )
    args = parser.parse_args()

    balances = redpocket_monitor.getRedPocketBalances( save=args.save )

    if args.print:
        for i in balances:
            print( balance_string.format( **i ) )

    if args.save:
        print( 'RedPocket balances recorded.' )

def dump_balances():

    parser = argparse.ArgumentParser()
    parser.add_argument( '-n', default=5, type=int )
    args = parser.parse_args()

    data_fil = os.path.join( os.path.dirname( redpocket_monitor.__file__ ), 'data', 'data.csv' )
    print( data_fil )
    with open( data_fil ) as fil:
        lines = fil.readlines()

    print( ' '.join( lines[ 0 ].strip().split( ',' ) ) )
    for line in lines[ -1 * args.n + 1: ] :
        print( ' '.join( line.strip().split( ',' ) ) )
    print( '' )
