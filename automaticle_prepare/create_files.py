# -*- coding: utf-8 -*-
import copy
import datetime
import glob
import os
import pickle
import sys
import time
import urllib2

from RF_model import Random_forest_func
from kudago_prepare import write_to_db_events
from kudago_prepare import write_to_db_places

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

path_to_file = "work_files"


def union_func():
    main_array = []
    return main_array


def write_categories_file(union_categories_rus, path):
    output = open(path + "/list_categories/" + "list_categories.pkl", 'wb')

    pickle.dump(union_categories_rus, output)
    output.close()


def write_events(union_main_array, time_array, path):
    for index, i in enumerate(time_array):
        new_path = "events_" + i + ".pkl"
        output = open(path + "/events/" + new_path, 'wb')

        title_array = []
        events_to_write = []
        for j in union_main_array[index]:
            for k in j:
                event_help_var = copy.deepcopy(k)
                if not (event_help_var['title'] in title_array):
                    events_to_write.append(event_help_var)
                    delta = datetime.timedelta(days=1)
                    title_array.append(event_help_var['title'])

        events_to_write = add_id_identify(events_to_write)
        pickle.dump(events_to_write, output)
        output.close()


def get_avarege_kudago(array_events, array_places):
    help_array = []

    for i in array_events:
        for j in i:
            for k in j:
                help_array.append(k['rank'])

    for i in array_places:
        for j in i:
            for k in j:
                help_array.append(k['rank'])

    average = sum(help_array) / len(help_array)

    return average


def union_parsers_func(array_kassir, array_bileter, cat_eng_kassir, cat_eng_bileter):
    equal_elem = []
    # одинаковые категории
    for index, i in enumerate(cat_eng_kassir):
        if (i in cat_eng_bileter):
            equal_elem.append(i)

    union_array = []

    # объединение массивов (всё в одно)

    how_much_days = len(array_kassir)

    for i in xrange(how_much_days):
        help_array = array_bileter[i] + array_kassir[i]
        union_array.append(copy.deepcopy(help_array))
        help_array = []

    new_union = []

    for index_main, i in enumerate(union_array):
        data_one_day = copy.deepcopy(union_array[index_main])

        equal_cat = []
        equal_num = []
        cat_array = []
        non_equal_num = []

        array_to_del = []
        for i in xrange(len(data_one_day)):
            if len(data_one_day[i]) == 0:
                array_to_del.append(copy.deepcopy(i))

        new_data_one_day = []

        for i in xrange(len(data_one_day)):
            if not (i in array_to_del):
                new_data_one_day.append(copy.deepcopy(data_one_day[i]))

        data_one_day = copy.deepcopy(new_data_one_day)

        for j in data_one_day:
            cat_array.append(j[0]['categories'])

        for index, j in enumerate(cat_array):
            index_cat = cat_array.index(j)
            if (cat_array.count(j) == 2 and index_cat != index):
                equal_cat.append([cat_array.index(j), index])
            else:
                non_equal_num.append(index)

        new_array_day = []

        for j in equal_cat:
            one_array = data_one_day[j[0]]
            second_array = data_one_day[j[1]]
            new_array_day.append(one_array + second_array)

        for j in non_equal_num:
            new_array_day.append(copy.deepcopy(data_one_day[j]))

        new_union.append(new_array_day)

    union_cat = list(set(cat_eng_kassir + cat_eng_bileter))

    return new_union, union_cat


def check_internet():
    try:
        response = urllib2.urlopen('http://www.google.ru', timeout=1)
        return True
    except urllib2.URLError as err:
        pass
    return False


def train_model(main_array, path, flag_rf):
    mix_coordinates_array = []

    # соберем все координаты в новых массивах
    for i in main_array:
        for j in i:
            for k in j:
                mix_coordinates_array.append(tuple((k['latitude'], k['longitude'])))

    # проверим есть ли уже файл с старыми координатами
    train_dist_path = path + "coordinates/" + "coordinates.pkl"
    is_file = os.path.exists(train_dist_path)

    # если есть то загрузим их
    if (is_file):
        inputer = open(train_dist_path, 'r')

        train_dist_dict = pickle.load(inputer)
        inputer.close()

        if (len(train_dist_dict) > 60000):
            if (flag_rf):
                return_array = Random_forest_func(path)
            else:
                return []
            return return_array
    # иначе создадим новый словарь
    else:
        train_dist_dict = {}

    # перемшаем всё заново (добавим и новые и старые)
    if (len(train_dist_dict) != 0):
        for i in train_dist_dict:
            mix_coordinates_array.append(tuple((i[0], i[1])))
            mix_coordinates_array.append(tuple((i[2], i[3])))

    # уберем повторы
    mix_coordinates_array = list(set(mix_coordinates_array))

    # новый перемешанный словарь
    all_mix_array = {}
    for i in mix_coordinates_array:
        for j in mix_coordinates_array:
            all_mix_array[i + j] = "no"

    flag_to_return = False

    # если уже раньше считали расстояние, то запишем его
    for i in all_mix_array:
        try:
            all_mix_array[i] = train_dist_dict[i]
            flag_to_return = True
        except Exception as inst:
            None

    if ((len(all_mix_array) > 60000 or not (flag_to_return)) and (is_file)):
        if (flag_rf):
            return_array = Random_forest_func(path)
        else:
            return []
        return return_array

    if (flag_rf):
        return_array = Random_forest_func(path)
    else:
        return []

    return return_array


def get_minutes(scikit_model, latitude_1, longitude_1, latitude_2, longitude_2):
    minutes_predict = scikit_model.predict([latitude_1, longitude_1, latitude_2, longitude_2])
    return int(minutes_predict[0])


def dist_array(events, path):
    input = open(path + "/scikit_model/" + "scikit_model.pkl", 'r')
    regr = pickle.load(input)
    input.close()

    distance_matrix = []

    for i in xrange(len(events)):
        help_array = []
        for j in xrange(len(events)):
            help_array.append(copy.deepcopy([]))
        distance_matrix.append(copy.deepcopy(help_array))

    for i in xrange(len(events)):
        for j in xrange(len(events)):
            if (i == j):
                distance_matrix[i][j] = 0
                continue

            minutes = get_minutes(regr, \
                                  events[i]['latitude'], events[i]['longitude'], events[j]['latitude'],
                                  events[j]['longitude'])

            distance_matrix[i][j] = copy.deepcopy(minutes)

    return distance_matrix


def create_dist_matrix(path):
    for file in glob.glob(path + "/events/" + "*.pkl"):
        input = open(file, "r")
        day_data = pickle.load(input)
        input.close()

        day_dist_data = dist_array(day_data, path)

        name_new_file = file.split("/")[-1].replace("events", "dist")

        output = open(path + "/distance_matrix/" + name_new_file, 'w')
        pickle.dump(day_dist_data, output)
        output.close()


def add_id_identify(main_array):
    # по дням\
    counter = 1
    for i in xrange(len(main_array)):
        # по событиям
        main_array[i]['id'] = counter
        counter += 1

    return main_array


def safety_write_coordinates(path, some_data):
    output = open(path + "/coordinates/" + "coordinates.pkl", 'w')

    pickle.dump(some_data, output)

    output.close()


def write_log_file(text, path, is_first):
    if (is_first):
        os.remove(path + "log.txt")
        from time import gmtime, strftime
        time_today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f = open(path + "log.txt", "w")
        f.write(time_today + "\n")
        f.close()
    else:
        f = open(path + "log.txt", "a")
        f.write(text + "\n")
        f.close()


def get_time_array(how_many_days, flag):
    import datetime
    today_date = datetime.date.today()

    need_date_array = []

    if (flag == "today"):
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

    if (flag == "next"):
        delta = datetime.timedelta(days=1)
        need_date_array.append(str(today_date))
        last_date = today_date
        today_date = today_date + datetime.timedelta(days=7)

        date_array_out = []
        date_array_out.append(str(today_date))
        date = today_date

        for i in xrange(how_many_days - 1):
            date = date + delta
            date_array_out.append(str(date))
        return date_array_out


def create_work_files():
    # парсинг на эту неделю и на следующую
    time_array_need = get_time_array(7, "next")

    local = True

    if (local):
        path = "/automaticle_prepare/"
    else:
        path = "/home/azureuser/data_files/"

    write_log_file("nothing", path, True)

    try:
        if not (check_internet()):
            write_log_file("not connect to internet", path, False)
            print "not connect to internet"
            return 0
    except Exception as inst:
        write_log_file(str(inst), path, False)
        print inst

    debug_param = True

    array_events, time_array, cat_eng_events, cat_rus_events = \
        write_to_db_events.main_func(debug_param, copy.deepcopy(time_array_need))
    write_log_file("kudago events end", path, False)
    print "kudago events end"

    array_places, time_array, cat_eng_places, cat_rus_places = \
        write_to_db_places.main_func(debug_param, copy.deepcopy(time_array_need))
    write_log_file("kudago places end", path, False)
    print "kudago places end"

    average_kudago = 1
    average_kudago = get_avarege_kudago(array_events, array_places)

    debug_param = False

    array_kassir, time_array, cat_eng_kassir, cat_rus_kassir = \
        prepare_files_kassir.main_func(debug_param, average_kudago, copy.deepcopy(time_array_need))
    write_log_file("kassir parser end", path, False)
    print "kassir parser end"

    array_bileter, time_array, cat_eng_bileter, cat_rus_bileter = \
        prepare_files_bileter.main_func(debug_param, average_kudago, copy.deepcopy(time_array_need))
    write_log_file("bileter parser end", path, False)
    print "bileter parser end"

    union_cat_rus = cat_rus_places + list(set(cat_rus_events + cat_rus_kassir + cat_rus_bileter))
    write_categories_file(union_cat_rus, path)

    union_parsers, union_cat_parsers = \
        union_parsers_func(array_kassir, array_bileter, cat_eng_kassir, cat_eng_bileter)

    # объединение данных эвентов и парсеров
    union_events_parsers, union_cat_events_parsers = \
        union_parsers_func(union_parsers, array_events, union_cat_parsers, cat_eng_events)

    # объединение данных с местами
    main_array, main_cat_array = \
        union_parsers_func(union_events_parsers, array_places, union_cat_events_parsers, cat_eng_places)

    write_events(main_array, time_array, path)
    write_log_file("events file end", path, False)
    print "events file end"

    flag_rf = False

    all_mix_array = train_model(main_array, path, flag_rf)
    write_log_file("RF model end", path, False)
    print "RF model end"

    if (len(all_mix_array) != 0):
        safety_write_coordinates(path, all_mix_array)
    else:
        write_log_file("empty return to coordinates", path, False)
        print "empty return to coordinates"

    create_dist_matrix(path)
    write_log_file("distance matrix end", path, False)
    print "distance matrix end"


start_time = time.time()

create_work_files()

end_time = (time.time() - start_time)

print end_time
