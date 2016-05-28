# -*_ coding: utf-8 -*-

import copy
import os
import pickle
import sys
from datetime import timedelta

from bileter_get_data import parser

reload(sys)
sys.setdefaultencoding('utf-8')


def open_data_file():
    data = []
    path = os.path.dirname(os.path.abspath(__file__))[:-15] + "/bileter_get_data/data/"
    path = path + "bileter.pkl"
    inputer = open(path, 'r')
    data = pickle.load(inputer)
    inputer.close()
    return data


def prepare_time(display_dates_string, duration):
    timestart_new = 0
    timeend_new = 0
    duration_new = 0

    # print display_dates_string, duration
    from datetime import datetime

    time_split = display_dates_string.split(" ")
    display_dates_string = time_split[-1]

    time_help = timedelta(minutes=0)

    format = '%H:%M'
    timestart_new = datetime.strptime(display_dates_string, format)
    timestart_new = timedelta(hours=timestart_new.hour) + timedelta(minutes=timestart_new.minute)

    duration_new = datetime.strptime(duration, format)
    duration_new = timedelta(hours=duration_new.hour) + timedelta(minutes=duration_new.minute)

    if (duration_new == time_help):
        # plus hours
        timeend_new = timestart_new + timedelta(hours=3)
        duration_new = timedelta(hours=3)
    else:
        timeend_new = timestart_new + duration_new

    return timestart_new, timeend_new, duration_new


def get_time_array(how_many_days):
    import datetime
    today_date = datetime.date.today()

    need_date_array = []
    delta = datetime.timedelta(days=1)
    need_date_array.append(str(today_date))
    last_date = today_date

    date_array_out = []
    date_array_out.append(str(today_date))
    date = last_date

    for i in xrange(how_many_days - 1):
        date = date + delta
        date_array_out.append(str(date))

    return date_array_out


def main_func(debug_param, average_kudago, time_array_need):
    main_array = []
    time_array = []
    categories_array_eng = []
    categories_array_rus = []

    if (not (debug_param)):
        parser.parsing(time_array_need)

    data = open_data_file()

    event_categories_list = ['theater', 'concert', 'show', 'clubs', 'kids', 'excursions', 'exhibition', 'sport']
    time_array = time_array_need

    new_array = []

    # расширяем на дни
    for i in xrange(len(time_array)):
        new_array.append([])

    # расширяем на категории
    for index, i in enumerate(time_array):
        for j in event_categories_list:
            new_array[index].append([])

    # по дням
    for index, i in enumerate(data):
        # по событиям в дне
        for index1, j in enumerate(i):
            num = event_categories_list.index(j['categories'])
            new_array[index][num].append(j)

    data = copy.deepcopy(new_array)

    new_data = []
    for i in xrange(len(data)):
        new_data.append([])

    for index, i in enumerate(data):
        # по категориям
        for index1, j in enumerate(i):
            if (len(j) != 0):
                new_data[index].append(j)

    data = copy.deepcopy(new_data)

    all_eng_categories = []
    all_rus_categories = []

    # по датам
    for index, i in enumerate(data):
        # по категориям
        for index1, j in enumerate(i):
            if (len(j) == 0):
                del data[index][index1]
                continue
            # по каждому в категории
            for index2, k in enumerate(j):

                if (k['images'] != "no" and not (":" in k['images'])):
                    data[index][index1][index2]['images'] = "http://www.bileter.ru" + data[index][index1][index2][
                        'images']

                data[index][index1][index2]['rank'] = float(average_kudago)

                description = data[index][index1][index2]['description']

                description = ' '.join(description.split())

                description = description.replace('\n', "").replace("@", "")

                if (len(description) == 0):
                    data[index][index1][index2]['description'] = "no"

                data[index][index1][index2]['description'] = description

                try:
                    timestart, timeend, duration = prepare_time(data[index][index1][index2]['display_dates_string'], \
                                                                data[index][index1][index2]['duration'])
                except:
                    del data[index][index1][index2]
                    continue

                del data[index][index1][index2]['display_dates_string']

                data[index][index1][index2]['timestart'] = timestart
                data[index][index1][index2]['timeend'] = timeend
                data[index][index1][index2]['duration'] = duration

                all_eng_categories.append(k['categories'])
                all_rus_categories.append(k['categoriesrus'])

    # телефон
    # время

    main_array = copy.deepcopy(data)

    categories_array_eng = list(set(all_eng_categories))
    categories_array_rus = list(set(all_rus_categories))

    return main_array, time_array, categories_array_eng, categories_array_rus

# import datetime

# date = datetime.date.today()

# date = [str(date)]

# main_array, time_array, categories_array_eng, categories_array_rus = main_func(True, 1, date)

# print categories_array_eng
