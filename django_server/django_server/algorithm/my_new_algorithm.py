# -*- coding: utf-8 -*-

import copy
import datetime
from datetime import timedelta

import A_star.a_star_make as astar
import get_data


def get_minutes(scikit_model, latitude_1, longitude_1, latitude_2, longitude_2):
    minutes_predict = scikit_model.predict([latitude_1, longitude_1, latitude_2, longitude_2])
    return int(minutes_predict[0])


def reformat_distance_matrix(events, dist_matrix, scikit_model, latitude_in, longitude_in, latitude_out, longitude_out):
    new_dist_matrix = []
    for index, i in enumerate(dist_matrix):
        help_array = copy.deepcopy(i)
        minutes_in = get_minutes(scikit_model, latitude_in, longitude_in, events[index]['latitude'],
                                 events[index]['longitude'])
        help_array.insert(0, copy.deepcopy(minutes_in))

        minutes_out = get_minutes(scikit_model, events[index]['latitude'], events[index]['longitude'], latitude_out,
                                  longitude_out)
        help_array.insert(len(help_array), copy.deepcopy(minutes_out))
        new_dist_matrix.append(copy.deepcopy(help_array))

    first_insert_array = [0]
    for i in events:
        minutes = get_minutes(scikit_model, latitude_in, longitude_in, i['latitude'], i['longitude'])
        first_insert_array.append(copy.deepcopy(minutes))

    first_insert_array.append(get_minutes(scikit_model, latitude_out, longitude_out, latitude_in, longitude_in))
    new_dist_matrix.insert(0, copy.deepcopy(first_insert_array))

    second_insert_array = []
    second_insert_array.append(get_minutes(scikit_model, latitude_out, longitude_out, latitude_in, longitude_in))
    for i in events:
        minutes = get_minutes(scikit_model, latitude_in, longitude_in, i['latitude'], i['longitude'])
        second_insert_array.append(copy.deepcopy(minutes))

    second_insert_array.append(0)
    new_dist_matrix.insert(len(new_dist_matrix), copy.deepcopy(second_insert_array))

    return new_dist_matrix


# функция переформирования матрицы расстояний (важна скорость вычислений)
def main_reformat_dist_matrix(recom_events, dist_matrix, events):
    for i in xrange(len(dist_matrix)):
        for j in xrange(len(dist_matrix[i])):
            fist_event_time_start = events[i]['timestart']

            second_event_time_start = events[j]['timestart']

            one_day = datetime.timedelta(days=1)
            one_second = datetime.timedelta(seconds=0)
            time_diff = second_event_time_start - fist_event_time_start

            # если не успеваем
            if (time_diff < one_second or time_diff == one_second):
                # print events[i]['timestart'], events[j]['timestart'], time_diff
                dist_matrix[i][j] = 10000
                continue

            # не успеваем с ожиданием и время не фиксировано
            if (((events[i]['timestart'] + events[i]['duration']) >= events[j]['timestart']) \
                        and (events[j]['fixedtime'])):
                # print events[i]['timestart'], events[j]['timestart'], time_diff
                dist_matrix[i][j] = 10000
                continue

            if (events[j]['title'] in recom_events):
                dist_matrix[i][j] = dist_matrix[i][j] - dist_matrix[i][j] / 100 * 10

            # если даже с продолжительностю высокое время ожидания между событиями
            first_event_end = events[i]['duration'] + fist_event_time_start
            time_diff = second_event_time_start - first_event_end
            # print duration

            # если ждать более 3 часов
            marker_hour = datetime.timedelta(hours=3)
            if (time_diff > marker_hour):
                # print first_event_end, events[j]['timestart'], time_diff
                dist_matrix[i][j] = 800
                continue

                # print dist_matrix[i][j], time_diff
                # print events[i]['timestart'], events[j]['timestart'], events[i]['duration'], events[i]['fixedtime']

    return dist_matrix


def get_route(recom_events, date, time_to, time_from, latitude_in, longitude_in, latitude_out, longitude_out):
    route_events_array = []

    # описание события, время до следующей точки, время начала, время конца, широта, долгота

    # рекомендации не используем
    # recom_events = []

    local = True
    date = date[6:len(date)] + "-" + date[3:5] + "-" + date[0:2]
    events, dist_matrix, scikit_model = get_data.get_data_from_files(date)

    # print len(events)

    keys = copy.deepcopy(events[0].keys())

    # добавляем в матрицу расстояний 2 столбца
    dist_matrix = reformat_distance_matrix(events, dist_matrix, scikit_model, latitude_in, longitude_in, latitude_out,
                                           longitude_out)

    # print dist_matrix

    # добавить как события первый и последний пункт маршрута в массива событий
    time_in_split = time_to.split(":")
    time_out_split = time_from.split(":")

    time_in = timedelta(hours=int(time_in_split[0]), minutes=int(time_in_split[1]))
    time_out = timedelta(hours=int(time_out_split[0]), minutes=int(time_out_split[1]))

    fist_event_dict = {}
    for i in keys:
        fist_event_dict[i] = "no"

    fist_event_dict['id'] = 0
    fist_event_dict['timestart'] = time_in
    fist_event_dict['timeend'] = time_in
    fist_event_dict['title'] = "Начало маршрута"
    fist_event_dict['duration'] = timedelta(minutes=0)
    fist_event_dict['latitude'] = latitude_in
    fist_event_dict['longitude'] = longitude_in
    fist_event_dict['fixedtime'] = True

    events.insert(0, fist_event_dict)

    last_event_dict = {}
    for i in keys:
        last_event_dict[i] = "no"
    last_event_dict['id'] = events[-1]['id'] + 1
    last_event_dict['timestart'] = time_out
    last_event_dict['timeend'] = time_out
    last_event_dict['title'] = "Конец маршрута"
    last_event_dict['duration'] = timedelta(minutes=0)
    last_event_dict['latitude'] = latitude_out
    last_event_dict['longitude'] = longitude_out
    last_event_dict['fixedtime'] = True

    events.insert(len(events), last_event_dict)

    copy_dist_matrix = copy.deepcopy(dist_matrix)
    dist_matrix = main_reformat_dist_matrix(recom_events, dist_matrix, events)
    # преобразовать матрицу расстояний согласно рангу событий и рекомендаций

    route_events_array = astar.get_route_astar_funk(events, dist_matrix, time_in, time_out, copy_dist_matrix)

    # for i in route_events_array:
    #    print i[0], events[i[4]]['title']

    return events, route_events_array
