# -*- coding: utf-8 -*-

import datetime
import logging
import time

import requests

logger = logging.getLogger(__name__)


class VkError(Exception):
    pass


PROFILE_FIELDS = ','.join(['sex', 'bdate', 'personal' \
                                           'city', 'relation', 'country', \
                           'counters', 'home_town', 'universities', \
                           'schools', 'connections', 'relation', 'relatives', \
                           'interests', 'books', 'last_seen', 'occupation'])


# https://vk.com/dev/fields
# universities (информация об университете)

def get_age(date_birth):
    age = 0
    # DD.MM.YYYY

    today_date = datetime.date.today()
    format = '%d.%m.%Y'
    try:
        time_bith = datetime.datetime.strptime(str(date_birth), format)
    except:
        return 0

    age = today_date.year - time_bith.year - ((today_date.month, today_date.day) \
                                              < (time_bith.month, time_bith.day))
    return age


class VkAPI(object):
    def __init__(self, token=None):
        self.session = requests.Session()
        self.session.headers['Accept'] = 'application/json'
        self.session.headers['Content-Type'] = 'application/x-www-form-urlencoded'

        self.token = token
        self.requests_times = []

    def _do_api_call(self, method, params):
        self._pause_before_request()

        if self.token:
            params['access_token'] = self.token
        params['v'] = '5.33'

        param_str = '&'.join(['%s=%s' % (k, v) for k, v in params.iteritems()])
        url = 'https://api.vk.com/method/%s?%s' % (method, param_str)

        logger.debug('API request: %s' % (method))

        response = self.session.get(url)

        if response.status_code is not 200:
            time.sleep(10)
            response = self.session.get(url)
            if response.status_code is not 200:
                raise VkError('Can\'t get %s, code %s' % (url, response.status_code))

        json = response.json()
        if 'response' not in json:
            raise VkError('Api call error %s - %s' % (url, json))

        return json['response']

    def _pause_before_request(self):
        if len(self.requests_times) > 2:
            first = self.requests_times[0]
            diff = time.time() - first
            if diff < 1.:
                logger.info('Sleepping for %s sec' % (1. - diff))
                time.sleep(1. - diff)
            self.requests_times = self.requests_times[1:]
        self.requests_times.append(time.time())

    def get_user_profile(self, user_id, fields=PROFILE_FIELDS):
        profile = self._do_api_call('users.get', {'user_ids': user_id, 'fields': fields})
        return profile[0]

    def get_friends(self, user_id, fields=PROFILE_FIELDS):
        response = self._do_api_call('friends.get', {'user_id': user_id, 'fields': fields})
        return response['items']

    def close(self):
        self.session.close()


def user_information(user_id):
    api = VkAPI()

    inform_dict = {}

    users_profiles = api.get_user_profile(user_id)

    try:
        inform_dict['count_friends'] = len(api.get_friends(user_id))
    except:
        inform_dict['count_friends'] = 0

    try:
        inform_dict['age'] = get_age(users_profiles['bdate'])
    except:
        inform_dict['age'] = 0

    try:
        inform_dict['gender'] = users_profiles['sex']
    except:
        inform_dict['gender'] = 0

    try:
        inform_dict['count_audios'] = users_profiles['counters']['audios']
    except:
        inform_dict['count_audios'] = 0

    try:
        inform_dict['count_photos'] = users_profiles['counters']['photos']
    except:
        inform_dict['count_photos'] = 0

    try:
        inform_dict['country'] = users_profiles['country']['id']
    except:
        inform_dict['country'] = 0

    return inform_dict
