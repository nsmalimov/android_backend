# -*- coding: utf-8 -*-
import json

import requests

# модуль для тестирования работы сервера
server_url_net = ""
server_url_local = "http://127.0.0.1:8000/"


def create_sample_dict():
    response_data = {}
    response_data['events'] = [u"концерты", u"музеи", u"клубы", u"театры", u"кафе"]

    response_data['date'] = "19.05.2015"

    response_data['time_to'] = "08:00"
    response_data['time_from'] = "22:00"

    response_data['latitude_in'] = 59.932987
    response_data['longitude_in'] = 30.301477

    response_data['latitude_out'] = 59.971040
    response_data['longitude_out'] = 30.371605

    return response_data


# GET request
def do_get_request(server_url):
    r = requests.get(server_url + "preferences")
    print r
    return r.json()

def do_post_request(server_url, file_to_post):
    r = requests.post(server_url + "route", data=json.dumps(file_to_post))
    print r
    return r.json()


dict_test = create_sample_dict()

content = do_post_request(server_url_net, dict_test)

print content
