
import configparser
import datetime
import json
import os
from pkg_resources import resource_filename
import re
import requests

def extract_csrf_from_html( html_text ):
    re_tag = r'<input type="hidden" name="csrf" value="([\w|-]+)">'
    match = re.search( re_tag, html_text )
    if match: 
        return match.group( 1 )
    return None


class RedPocketDataExtractor( object ):

    POST_URL = 'https://www.redpocket.com/login'
    GET_DETAILS_ID_URL = 'https://www.redpocket.com/account/get-other-lines'
    GET_PARAMS_URL = 'https://www.redpocket.com/account/get-details?id=%s&type=api'

    def __init__( self, cfg_fil='redpocket.ini', save=False ):
        self.config = configparser.ConfigParser()
        self.cfg_fil = resource_filename( __name__, 'config/' + cfg_fil )
        self.config.read( self.cfg_fil )
        self.balances = []

        self.save = save
        self.data_fil = ''

        self.get_balances()

    def get_balances( self ):
        client = requests.session()

        r = client.get( url=self.POST_URL )

        payload = {
            'mdn' : self.config[ 'redpocket' ][ 'username' ],
            'password' : self.config[ 'redpocket' ][ 'password' ],
            'csrf' : extract_csrf_from_html( r.text ),
        }

        # POST username/password to login
        r = client.post( url=self.POST_URL, data=payload )

        # if no details_id in config, obtain from GET
        try:
            details_ids = json.loads( self.config[ 'redpocket' ][ 'details_ids' ] )

        except KeyError:
            r = client.get( url=self.GET_DETAILS_ID_URL )
            details_params = json.loads( r.text )
            details_ids = []
            for iden in details_params[ 'return_data' ][ 'confirmedLines' ]:
                details_ids.append( iden[ 'hash' ] )

            # save details id to config for future GETs
            self.config[ 'redpocket' ][ 'details_ids' ] = json.dumps( details_ids )
            with open( self.cfg_fil, 'w+' ) as fil:
                self.config.write( fil )

        # GET balance data
        self.balances = []
        for iden in details_ids:
            r = client.get( url=self.GET_PARAMS_URL % iden )
            data_params = json.loads( r.text )[ 'return_data' ]

            # add and format datetime information
            DATE_FMT = '%m/%d/%y'
            TIME_FMT = '%I:%M %p'

            now = datetime.datetime.now()
            data_params[ 'datetime' ] = now
            data_params[ 'aed' ] = datetime.datetime.strptime( data_params[ 'aed' ], '%m/%d/%Y' )
            data_params[ 'remaining_days' ] = ( data_params[ 'aed' ] - now ).days
            data_params[ 'aed' ] = data_params[ 'aed' ].strftime( DATE_FMT )
            data_params[ 'date' ] = now.date().strftime( DATE_FMT )
            data_params[ 'time' ] = now.time().strftime( TIME_FMT )

            self.balances.append( data_params )

        if self.save:
            self.saveBalances()

    def saveBalances( self ):
        save_params = [ 'datetime', 'mdn', 'voice_balance', 'messaging_balance', 'data_balance' ]

        # check if file exists
        self.data_fil = resource_filename( __name__, 'data/data.csv' )
        if not os.path.exists( self.data_fil ):
            with open( self.data_fil, 'w+' ) as fil:
                fil.write( ','.join( save_params ) + '\n' )
        
        for balance in self.balances:
            db_params = { k: v for k, v in balance.items() if k in save_params }
            db_params.update( { k: '-1' for k,v in db_params.items() if v == 'Unlimited' } )
            db_params.update( { k: v.replace( ',', '' ) for k,v in db_params.items() if 'balance' in k } )
            with open( self.data_fil, 'a' ) as fil:
                fil.write( '{datetime},{mdn},{voice_balance},{messaging_balance},{data_balance}\n'.format( **db_params ) )


def getRedPocketBalances( **kwargs ):
    data = RedPocketDataExtractor( **kwargs )
    return data.balances

if __name__ == '__main__':

    data = RedPocketDataExtractor()

