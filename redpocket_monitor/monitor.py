
import configparser
import datetime
import json
import re
import requests

from pprint import pprint

POST_URL = 'https://www.redpocket.com/login'
GET_DETAILS_ID_URL = 'https://www.redpocket.com/account/get-other-lines'
GET_PARAMS_URL = 'https://www.redpocket.com/account/get-details?id=%s&type=api'

def extract_csrf_from_html( html_text ):
    re_tag = r'<input type="hidden" name="csrf" value="([\w|-]+)">'
    match = re.search( re_tag, html_text )
    if match: 
        return match.group( 1 )
    return None

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read( 'redpocket.ini' )

    client = requests.session()

    r = client.get( url=POST_URL )

    payload = {
      'mdn' : config[ 'redpocket' ][ 'username' ],
      'password' : config[ 'redpocket' ][ 'password' ],
      'csrf' : extract_csrf_from_html( r.text ),
    }

    r = client.post( url=POST_URL, data=payload )

    try:
        details_ids = json.loads( config[ 'redpocket' ][ 'details_ids' ] )

    except KeyError:
        r = client.get( url=GET_DETAILS_ID_URL )
        details_params = json.loads( r.text )
        details_ids = []
        for iden in details_params[ 'return_data' ][ 'confirmedLines' ]:
          details_ids.append( iden[ 'hash' ] )

        config[ 'redpocket' ][ 'details_ids' ] = json.dumps( details_ids )
        with open( 'redpocket.ini', 'w' ) as fil:
            config.write( fil )

    for iden in details_ids:
      r = client.get( url=GET_PARAMS_URL % iden )
      data_params = json.loads( r.text )
      data = data_params[ 'return_data' ]
      pprint( data )
