
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
    def start_date(self):
        return self.data['recurring']['last_date']

    @property
    def end_date(self):
        return self.data['aed']

    @property
    def data_balance(self):
        value = self.data['data_balance']
        if value == 'Unlimited':
            return -1
        return int(value.replace(',',''))

    @property
    def messaging_balance(self):
        value = self.data['messaging_balance']
        if value == 'Unlimited':
            return -1
        return int(value.replace(',',''))

    @property
    def voice_balance(self):
        value = self.data['voice_balance']
        if value == 'Unlimited':
            return -1
        return int(value.replace(',',''))

    @property
    def balances(self):
        return {
            'data': self.data_balance,
            'messaging': self.messaging_balance,
            'voice': self.voice_balance,
        }

    @property
    def days_remaining(self):
        return (datetime.datetime.strptime(self.data['aed'], '%m/%d/%Y') - datetime.datetime.now()).days
