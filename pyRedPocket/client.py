
import re

import requests

from .details import AccountDetails, LineDetails

BASE_URL = 'https://www.redpocket.com/'
URL_LOGIN = BASE_URL + 'login'
URL_POST_LOGIN = BASE_URL + 'my-lines'
URL_GET_OTHER_LINES = BASE_URL + 'account/get-other-lines'
URL_GET_DETAILS = BASE_URL + 'account/get-details?id={}&type=api'


class Client(object):

    def __init__(self, username, password):
        self._client = requests.Session()
        self._logged_in = False
        self._username = username
        self._password = password

        self.lines = []
        self.details = {}

        self._process()

    def _extract_csrf(self, text):
        return re.findall(r'name="csrf" value="([\w|-]+)"', text)[0]

    def _process(self):
        if not self._logged_in:
            self._login()

        self.lines = self._get_lines()

        for lin in self.lines:
            self.details[lin] = self._get_details(lin)

    def _login(self):
        r = self._client.get(URL_LOGIN)
        d = {
            'mdn': self._username,
            'password': self._password,
            'csrf': self._extract_csrf(r.text),
        }
        req = self._client.post(URL_LOGIN, data=d)
        if req.url == URL_POST_LOGIN:
            self._loggedIn = True
        else:
            raise Exception

    def _get_lines(self):
        if not self._logged_in:
            self._login()

        req = self._client.get(URL_GET_OTHER_LINES)
        if req.status_code != 200:
            raise Exception
        processed_details = AccountDetails.from_dict(**req.json())
        return [i.hash for i in processed_details.confirmed_lines]

    def _get_details(self, hashId):
        req = self._client.get(URL_GET_DETAILS.format(hashId))
        if req.status_code != 200:
            raise Exception
        return LineDetails.from_dict(**req.json())
