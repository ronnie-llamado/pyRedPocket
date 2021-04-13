
import re

import requests

from .details import AccountDetails, LineDetails

BASE_URL = 'https://www.redpocket.com/'
URL_LOGIN = BASE_URL + 'login'
URL_POST_LOGIN = BASE_URL + 'https://www.redpocket.com/my-lines'
URL_GET_OTHER_LINES = BASE_URL + 'account/get-other-lines'
URL_GET_DETAILS = BASE_URL + 'account/get-details?id={}&type=api'


class Client(object):

    def __init__(self, username, password):
        self.__client = requests.Session()
        self.__loggedIn = False
        self.__username = username
        self.__password = password
        self.__hashIds = []

        self.login()

    def _extract_csrf(self, text):
        return re.findall(r'name="csrf" value="([\w|-]+)"', text)[0]

    def login(self):
        r = self.__client.get(URL_LOGIN)
        d = {
            'mdn': self.__username,
            'password': self.__password,
            'csrf': self._extract_csrf(r.text),
        }
        s = self.__client.post(URL_LOGIN, data=d)
        if s.url == URL_POST_LOGIN:
            self.__loggedIn = True
        else:
            raise Exception

    def getLines(self):
        if not self.__loggedIn:
            self.login()
        r = AccountDetails(self.__client.get(URL_GET_OTHER_LINES))
        self.__hashIds = \
            list(map(lambda x: x.get('hash'), r.data['confirmedLines']))
        return self.__hashIds

    def getDetails(self, hashId):
        return LineDetails(self.__client.get(URL_GET_DETAILS.format(hashId)))
