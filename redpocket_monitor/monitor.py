
import configparser
import datetime
import json
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

    def __init__( self, cfg_fil='redpocket.ini' ):
        self.config = configparser.ConfigParser()
        self.config.read( resource_filename( __name__, cfg_fil ) )
        self.balances = []

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
            with open( cfg_fil, 'w' ) as fil:
                config.write( fil )

        # GET balance data
        self.balances = []
        for iden in details_ids:
            r = client.get( url=self.GET_PARAMS_URL % iden )
            data_params = json.loads( r.text )
            self.balances.append( data_params[ 'return_data' ] )


def getRedPocketBalances( cfg_fil='redpocket.ini' ):
    data = RedPocketDataExtractor( cfg_fil )
    return data.balances

if __name__ == '__main__':

    data = RedPocketDataExtractor()

    from pprint import pprint
    pprint( getRedPocketBalances() )
