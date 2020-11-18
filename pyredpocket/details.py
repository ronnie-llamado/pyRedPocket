
import datetime
import time


class AccountDetails(object):

    def __init__(self, response, timestamp=True):
        self.__response = response.json()
        self.timestamp = time.time() if timestamp else None

    @property
    def code(self):
        return self.__response['return_code']

    @property
    def text(self):
        return self.__response['return_text']

    @property
    def data(self):
        return self.__response['return_data']


class LineDetails(AccountDetails):

    def __init__(self, response, timestamp=True):
        super(LineDetails, self).__init__(response, timestamp=timestamp)

    @property
    def balances(self):
        return {
            'data': self.data['data_balance'],
            'messaging': self.data['messaging_balance'],
            'voice': self.data['voice_balance'],
        }

    @property
    def days_remaining(self):
        return (datetime.datetime.strptime(self.data['aed'], '%m/%d/%Y') - datetime.datetime.now()).days
