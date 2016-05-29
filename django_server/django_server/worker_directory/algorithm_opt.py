# -*- coding: utf-8 -*-
import datetime

import diplom_django.algorithm.my_new_algorithm as alg


def time_conversion(time):
    hours = time.seconds / 60 / 60
    residue_time = time - datetime.timedelta(hours=hours)

    minutes = residue_time.seconds / 60

    hours = str(hours)

    if (len(hours) == 1):
        hours = "0" + hours

    minutes = str(minutes)
    if (len(minutes) == 1):
        minutes = "0" + minutes

    time_str = hours + ":" + minutes
    return time_str


# основной алгоритм
def get_route_main(request_dict, recom_events):
    date = request_dict['date']
    time_to = request_dict['time_to']
    time_from = request_dict['time_from']

    in_place = request_dict['in_place']
    out_place = request_dict['out_place']
    in_place_split = in_place.split(",")
    out_place_split = out_place.split(",")

    latitude_in = float(in_place_split[0])
    longitude_in = float(in_place_split[1])

    latitude_out = float(out_place_split[0])
    longitude_out = float(out_place_split[1])

    try:
        events, route = \
            alg.get_route(recom_events, date, time_to, time_from, latitude_in, longitude_in, latitude_out,
                          longitude_out)
        array_out = {}

        # возврат адреса
        # время в дороге (int)

        first_dict = {"time_start": time_conversion(route[0][0]), "time_road_next": route[0][-1], \
                      "latitude": events[route[0][4]]['latitude'], "longitude": events[route[0][4]]['longitude']}
        array_out['first_place'] = first_dict

        help_array = []
        for i in xrange(1, len(route) - 1):
            new_dict = {"time_start": time_conversion(route[i][0]),
                        "time_end": time_conversion(route[i][1]),

                        "title": events[route[i][4]]['title'],

                        "time_road_next": route[i][-1],

                        "categories": [events[route[i][4]]['categoriesrus']],
                        "address": events[route[i][4]]['address'],

                        "latitude": events[route[i][4]]['latitude'],
                        "longitude": events[route[i][4]]['longitude'],

                        "description": events[route[i][4]]['description'],
                        "site_url": events[route[i][4]]['url'],
                        "phone": events[route[i][4]]['phone'],
                        "ticket": events[route[i][4]]['ticket']}
            help_array.append(new_dict)

        array_out['medium_place'] = help_array

        last_dict = {"time_end": time_conversion(route[-1][1]), \
                     "latitude": events[route[-1][4]]['latitude'], "longitude": events[route[-1][4]]['longitude']}

        array_out['last_place'] = last_dict

        return array_out
    except Exception as inst:
        None
        return inst
