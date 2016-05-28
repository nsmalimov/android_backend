# -*- coding: utf-8 -*-
import datetime
import os
import pickle
import sys

from kudago_get_data import extract_data_places

import need_places

# название
# описание
# адрес
# время начала
# время конца
# телефон
# сайт
# билет
# картинка
# категория по английски
# категория по русски
# score
# долгота
# ширина
# фиксированное время
# продолжительность (минуты)

# +90 минут на событие

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()


# sys.path.append("/Users/Nurislam/PycharmProjects/api_kudago")

# сегодняшняя дата
def get_today_data():
    today_date = datetime.date.today()
    return today_date


# извлечь данные
def data_place_func(filename):
    def extract_data(filename):
        f = open(filename, 'r')
        data = pickle.load(f)
        f.close()
        return data

    def filter_data_no_spb(events_data):
        to_del_array = []
        for i in xrange(len(events_data)):
            if (events_data[i]['location']['slug'] != u'spb'):
                to_del_array.append(events_data[i])
        for i in to_del_array:
            events_data.remove(i)
        return events_data

    events_data_place = extract_data(filename)
    events_data_place = filter_data_no_spb(events_data_place)
    return events_data_place


# фильтруем данные
def filter_place_need(data_place, need_place):
    new_data_place = []

    for i in data_place:
        if i['categories'][0]['slug'] in need_place and i['lat_lon'] != None:
            new_data_place.append(i)

    data_place = new_data_place
    array_to_del = []
    array_keys = []

    for i in data_place:
        some_attr = i.keys()
        for j in some_attr:
            try:
                num = array_keys.index(j)
            except:
                array_keys.append(j)

    for i in xrange(len(array_keys)):
        if (array_keys[i] == u'lat_lon' or array_keys[i] == u'rank' or array_keys[i] == u'categories' or array_keys[
            i] == u'title' or array_keys[i] == u'description' \
                    or array_keys[i] == u'timetable' or array_keys[i] == u'address' or array_keys[i] == u'phone' or
                    array_keys[i] == u'url' or array_keys[i] == u'images'):
            None
        else:
            array_to_del.append(array_keys[i])

    all_rank_array = []

    for i in xrange(len(data_place)):
        all_rank_array.append(data_place[i]['rank'])
        array_key = data_place[i]
        for j in array_to_del:
            if (j in array_key):
                del data_place[i][j]
        time = data_place[i]['timetable']

        try:
            data_place[i]['images'] = "http://kudago.com" + data_place[i]['images'][0]
        except:
            data_place[i]['images'] = "no"

        del data_place[i]['timetable']
        data_place[i]['display_dates_string'] = time
        coordinates = data_place[i]['lat_lon']
        del data_place[i]['lat_lon']

        if (coordinates == None):
            None
        else:
            coord = coordinates.split(",")
        if (len(coord) == 2):
            data_place[i]['latitude'] = float(coord[0])
            data_place[i]['longitude'] = float(coord[1])

    max_rank = float(max(all_rank_array))

    for i in xrange(len(data_place)):
        data_place[i]['rank'] = float(data_place[i]['rank']) / max_rank

        data_place[i]['address'] = u"Санкт-Петербург, " + data_place[i]['address']

        data_place[i]['categoriesrus'] = data_place[i]['categories'][0]['name']

        try:
            num_index = data_place[i]['categoriesrus'].index("(")
            data_place[i]['categoriesrus'] = data_place[i]['categoriesrus'][0:num_index - 1]
        except:
            None

        if (data_place[i]['categoriesrus'] == u"Интересные, забавные памятники природы и арх"):
            data_place[i]['categoriesrus'] = u"Памятники природы"
        data_place[i]['description'] = data_place[i]['description'].replace(u"<p>", "").replace(u"</p>", "")

        if (data_place[i]['phone'] == ''):
            data_place[i]['phone'] = u"no"
        if (data_place[i]['url'] == ''):
            data_place[i]['url'] = u"no"
        if (data_place[i]['title'] == ''):
            data_place[i]['title'] = u"no"
        if (data_place[i]['description'] == ''):
            data_place[i]['description'] = u"no"

    for i in xrange(len(data_place)):
        try:
            if (data_place[i]['address'] == ''):
                del data_place[i]
            if (data_place[i]['display_dates_string'] == ''):
                del data_place[i]
            if (len(data_place[i]['categories']) == 0):
                del data_place[i]

            # нужно добавить
            data_place[i]['categories'] = data_place[i]['categories'][0]['slug']

            data_place[i]['ticket'] = u"no"
        except:
            None

    return data_place


def get_need_time(how_much_days):
    today_date = get_today_data()
    delta = datetime.timedelta(days=1)
    last_date = today_date
    date_array_out = []
    date_array_out.append(str(today_date).replace("-", "_"))
    for i in xrange(how_much_days - 1):
        date = last_date + delta
        date_array_out.append(str(date).replace("-", "_"))
        last_date = date
    return date_array_out


def filter_time(new_time):
    if (len(new_time) != 11):
        new_time_split = new_time.split(":")

        if (len(new_time_split[0]) == 1):
            new_time = "0" + new_time
        new_time_split = new_time.split("-")
        new_time_split_split = new_time_split[1].split(":")
        if (len(new_time_split_split[0]) == 1):
            new_time_split[1] = "0" + new_time_split[1]

        new_time = new_time_split[0] + "-" + new_time_split[1]

    return new_time


def get_good_time(time):
    time = time.lower()
    time = time.replace(u".", u":")
    # ежедневно 10:30-20:30

    # круглосуточно
    if (time == u"круглосуточно"):
        return u"пн 00:00-00:00;вт 00:00-00:00;ср 00:00-00:00;чт 00:00-00:00;пт 00:00-00:00;сб 00:00-00:00;вс 00:00-00:00"

    # строка без времени
    if (time.replace(" ", "").replace(",", "").isalpha() or time == ""):
        return 0

    day_array = [u"пн", u"вт", u"ср", u"чт", u"пт", u"сб", u"вс"]

    answer = ""

    if (len(time) == len(u"ср-сб 20.00-06.00") or len(time) == len(u"пт-сб 22.00–6.00")):
        time = time.replace("24:", "00:")
        if (time[0] == u"8"):
            return 0

        time_split = time.split(" ")

        time_split[0] = time_split[0].replace(u"–", "-")
        if (len(time_split[0]) != 5):
            return 0

        new_time = time_split[1].replace(u"–", "-")
        try:
            new_time = filter_time(new_time)
        except:
            None

        first_day = time_split[0][0:2]
        last_day = time_split[0][3:5]
        try:
            num_day_1 = day_array.index(first_day)
            num_day_2 = day_array.index(last_day)
        except:
            return 0

        for i in xrange(num_day_1, num_day_2, 1):
            answer = answer + day_array[i] + u" " + new_time + u";"

        if (answer == ""):
            return 0
    else:
        return 0

    return answer[0:len(answer) - 1]


def change_timetable(data_place):
    data_answer = []

    for i in data_place:
        time = get_good_time(i['display_dates_string'])
        if (time != 0):
            new_dict = i.copy()
            new_dict['display_dates_string'] = time
            data_answer.append(new_dict.copy())

    return data_answer


# разбиваем по категориям
def filter_categories(data_place, need_place):
    main_array = []
    need_place_new = []

    for i in need_place:
        if (i in need_place):
            need_place_new.append(i)

    need_place = need_place_new

    for i in need_place:
        main_array.append([])

    # по категориям
    for i in data_place:
        num = need_place.index(i['categories'])
        main_array[num].append(i)

    return main_array, need_place


def check_time_work(time_work, one_day_week):
    time_work_split = time_work.split(u";")
    for i in time_work_split:
        day_w = i[0] + i[1]
        if (day_w == one_day_week):
            i_split = i.split(u" ")
            return i_split[1]
    return 0


def time_prepare(time):
    num = time.index(u":") + 3
    end_s = time[num + 1:len(time)]
    time = time[0:num] + "-" + end_s
    return time


# задача сформировать массив на 7 дней
def create_array_good_time(data_place, time_array_need):
    day_array = [u"пн", u"вт", u"ср", u"чт", u"пт", u"сб", u"вс"]
    from datetime import datetime
    today_date = datetime.strptime(time_array_need[0], "%Y-%m-%d")

    need_days = []
    need_weeks_day = []
    import datetime
    delta = datetime.timedelta(days=1)
    need_days.append(str(today_date))
    need_weeks_day.append(day_array[today_date.isoweekday() - 1])
    last_date = today_date

    need_days_help = []

    for i in xrange(len(time_array_need) - 1):
        date = last_date + delta
        need_days.append(str(date))
        need_days_help.append(date)
        need_weeks_day.append(day_array[date.isoweekday() - 1])
        last_date = date

    events_array = []

    for i in data_place:
        events_array.append(i['categories'])

    event_wich_use = list(set(events_array))

    main_array = []
    for i in xrange(len(need_days)):
        main_array.append([])

    format = '%H:%M'
    from datetime import datetime, timedelta

    # распределяем по дням
    # по событиям
    for i in data_place:
        backup = i.copy()
        # проходим внутри категории
        for k in xrange(len(need_weeks_day)):
            get_time = check_time_work(i['display_dates_string'], need_weeks_day[k])
            if (get_time != 0):
                backup['display_dates_string'] = get_time
                backup['timestart'] = datetime.strptime(get_time[0:5], format)
                backup['timeend'] = datetime.strptime(get_time[6:11], format)

                s = backup['timeend'] - backup['timestart']

                if (str(s)[0] == "-" or s == timedelta(hours=0)):
                    backup['timeend'] = backup['timeend'] + timedelta(hours=24)

                del backup['display_dates_string']

                # елси меньше 180 минут, то фиксированно
                try:
                    minutes = backup['timeend'] - backup['timestart']
                    if (minutes <= timedelta(minutes=180)):
                        backup['fixedtime'] = True
                        backup['duration'] = minutes
                    else:
                        backup['fixedtime'] = False

                        # настроить продолжительность для каждого события
                        backup['duration'] = timedelta(minutes=90)

                except:
                    None

                backup['timestart'] = timedelta(hours=backup['timestart'].hour) + timedelta(
                    minutes=backup['timestart'].minute)
                backup['timeend'] = timedelta(hours=backup['timeend'].hour) + timedelta(
                    minutes=backup['timeend'].minute)
                main_array[k].append(backup.copy())

    events_day = main_array
    main_array = []

    for i in xrange(len(need_weeks_day)):
        main_array.append([])

    help_array = []

    for index, i in enumerate(events_day):
        main_array[index] = []
        which_is_cat = []
        for index1, j in enumerate(i):
            which_is_cat.append(events_day[index][index1]['categories'])

        which_is_cat = list(set(which_is_cat))

        for j in which_is_cat:
            help_array.append([])

        for index1, j in enumerate(i):
            num = which_is_cat.index(events_day[index][index1]['categories'])
            help_array[num].append(events_day[index][index1])

        main_array[index] = help_array
        help_array = []

    main_array_new = main_array

    return main_array_new, event_wich_use


def get_all_events_name(data_place):
    dict_events = {}
    count = 0
    for i in data_place:
        if (i['categories'][0]['slug'] in dict_events.values()):
            None
        else:
            dict_events[count] = i['categories'][0]['slug']
            count += 1
    return dict_events.values()


def get_all_events_name_1(data_place):
    dict_events = {}
    count = 0
    for i in data_place:
        if (i['categories'] in dict_events.values()):
            None
        else:
            dict_events[count] = i['categories']
            count += 1
    return dict_events.values()


def get_rus_name_events(data_place, need_place):
    dict_events = {}
    dict_events1 = {}
    count = 0
    for i in data_place:
        if (i['categories'][0]['slug'] in dict_events.values()):
            None
        else:
            if (i['categories'][0]['slug'] in need_place):
                dict_events[count] = i['categories'][0]['slug']
                dict_events1[count] = i['categories'][0]['name']
                count += 1
    array_categories = dict_events1.values()
    for i in xrange(len(array_categories)):
        try:
            num_index = array_categories[i].index("(")
            array_categories[i] = array_categories[i][0:num_index - 1]
        except:
            None
    return array_categories


def work_with_time(time):
    time = time_prepare(time)
    time1 = time[:8] + u':' + time[9:]
    time = time1
    time_split = time.split(u"-")

    time_start = time_split[0]
    time_end = time_split[1]

    time_end_split = time_end.split(u":")
    t0_h = time_end_split[0]
    t0_m = time_end_split[1]
    if (t0_m[0] == "0"):
        t0_m = t0_m[1]

    time_start_split = time_start.split(u":")
    t1_h = time_start_split[0]
    t1_m = time_start_split[1]
    if (t1_m[0] == "0"):
        t1_m = t1_m[1]

    t0_h = int(t0_h)
    t0_m = int(t0_m)

    t1_h = int(t1_h)
    t1_m = int(t1_m)

    h_m = (t1_h - t0_h) * 60

    m_m = (t1_m - t0_m)

    if (m_m < 0):
        m_m = (60 - t0_m) + t1_m
        h_m = h_m - 1

    all_minutes = m_m + h_m

    if (all_minutes < 0):
        all_minutes = -1 * all_minutes

    return all_minutes


def is_file_head(time_array):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + "/places/" + "head_array.pkl"

    if os.path.isfile(filename):
        filename = path + "/places/" + "time_check.pkl"
        input = open(filename, 'r')
        time_check_array = pickle.load(input)
        input.close()

        for i in xrange(len(time_array)):
            if (time_array[i] != time_check_array[i]):
                return False
        return True
    else:
        return False


def get_head_array(time_array):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + "/places/" + "head_array.pkl"

    input = open(filename, 'r')
    head_array = pickle.load(input)
    input.close()

    main_array = head_array[0]
    categories_array_eng = head_array[1]
    categories_array_rus = head_array[2]

    return main_array, time_array, categories_array_eng, categories_array_rus


def write_check_files(main_array, time_array, categories_array_eng, categories_array_rus):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + "/places/" + "head_array.pkl"
    head_array = [main_array, categories_array_eng, categories_array_rus]

    output = open(filename, 'w')
    pickle.dump(head_array, output)
    output.close()

    filename = path + "/places/" + "time_check.pkl"
    output = open(filename, 'w')
    pickle.dump(time_array, output)
    output.close()


def main_func(debug_param, time_array_need):
    try:
        if (not (debug_param)):
            extract_data_places.extract_data()
    except:
        print "Pending places"

    time_array = time_array_need

    # if (is_file_head(time_array)):
    #    print "don't calculate places"
    #    return get_head_array(time_array)

    path = os.path.dirname(os.path.abspath(__file__))[:-15] + "/kudago_get_data/data/"
    data_place = data_place_func(path + "places.pkl")

    need_place_eng = need_places.need_places

    all_events = get_all_events_name(data_place)

    # print all_events[0]
    # for i in all_events:
    #    for j in i:
    #        print i['categoriesrus']

    for i in need_place_eng:
        if (i in all_events):
            None
        else:
            need_place_eng.remove(i)

    need_place_rus = get_rus_name_events(data_place, need_place_eng)

    # print need_place_rus

    # массив контролируем какие данные будем брать по категориям мест
    data_place = filter_place_need(data_place, need_place_eng)

    # приводим время к виду пн 00:00-24:00;вт 00:00-24:00;
    data_place = change_timetable(data_place)

    # по категориям категорий

    # распределеяем по дням в неделе
    main_array, need_place = create_array_good_time(data_place, time_array)

    categories_array_rus = []
    for i in need_place:
        categories_array_rus.append(need_place_rus[need_place_eng.index(i)])

    categories_array_eng = need_place

    main_array, categories_array_eng, categories_array_rus = \
        need_places.prepare_categories(main_array, categories_array_eng, categories_array_rus)

    # write_check_files(main_array, time_array, categories_array_eng, categories_array_rus)
    print "new write"

    return main_array, time_array, categories_array_eng, categories_array_rus

# пустых категорий нет

# date = get_today_data()
# date = ["2015-06-03"]
#
# main_array, time_array, categories_array_eng, categories_array_rus = main_func(True, date)
#
# count = 0
#
# for i in main_array:
#     for j in i:
#         count += 1
#
# print count

# for i in categories_array_rus:
#    print i

# for i in categories_array_rus:
#    print i
# for i in categories_array_rus:
#    print i
# for i in main_array:
#    for j in i:
#        for k in j:
#            print k['categoriesrus']

# print time_array

# for index1, i in enumerate(main_array):
#         count = 0
#         for index2, j in enumerate(i):
#             for index3, k in enumerate(j):
#                 main_array[index1][index2][index3]['id'] = count
#                 count += 1
#
# for index1, i in enumerate(main_array):
#         for index2, j in enumerate(i):
#             for index3, k in enumerate(j):
#                 print k['id']
#         print "next"
