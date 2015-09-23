# -*- coding: utf-8 -*-
import datetime
from datetime import date, timedelta
import sys
import pickle
import need_events
from kudago_get_data import extract_data_events
import os
import copy

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

#допущение на +3 часа на событие

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

def get_today_data():
    today_date = datetime.date.today()
    return today_date


def time_plusser(time_to_show, how_much_plus):
    time_to_show_split = time_to_show.split("-")

    from datetime import datetime, timedelta


    if (10 == len(time_to_show) or 11 == len(time_to_show) or 9 == len(time_to_show)):
        return time_to_show, "no"

    try:
        check = time_to_show_split[1]
        return time_to_show, "no"
    except:
        format = '%H:%M'
        timestart = datetime.strptime(time_to_show_split[0], format)

        timeend = timestart + timedelta(hours=how_much_plus)
        timeend = str(timeend).split(" ")[-1].split(":")[0:2]
        timeend = timeend[0] + ":" + timeend[1]

        result_time = time_to_show_split[0] + "-" + timeend

        return result_time, "yes"

def extract_data_event(filename):
    f = open(filename, 'r')
    data = pickle.load(f)
    f.close()
    return data

def extract_data_place_help(filename_place):
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

    events_data_place = extract_data(filename_place)

    events_data_place = filter_data_no_spb(events_data_place)

    return events_data_place

def main_filter_data(events_data, need_places):
    to_del_array = []
    for i in xrange(len(events_data)):
        #[0] [1] проверка по всем категориям
        if (events_data[i]['location']['slug'] != u'spb' or not(events_data[i]['categories'][0]['slug'] in need_places)):
           to_del_array.append(events_data[i])

    for i in to_del_array:
       events_data.remove(i)
    return events_data

def del_ins_excess_inform(events_data):
    array_keys = []
    for i in events_data:
        some_attr = i.keys()
        for j in some_attr:
           try:
             num = array_keys.index(j)
           except: 
             array_keys.append(j)

    array_to_del = []
    for i in xrange(len(array_keys)):
        if (array_keys[i] == u'rank' or array_keys[i] == u'categories'\
         or array_keys[i] == u'title'\
         or array_keys[i] == u'description' or array_keys[i] == u'display_dates_string' \
         or array_keys[i] == u'place_id' or array_keys[i] == u'images' or array_keys[i] == u'all_dates'):
            None
        else:
            array_to_del.append(array_keys[i])

    for i in xrange(len(events_data)):
        try:
            events_data[i]['images'] = "http://kudago.com" + events_data[i]['images'][0]
        except:
            events_data[i]['images'] = "no"
        for j in array_to_del:
            try:
              del events_data[i][j]
            except: None
        events_data[i]['address'] = u""
        events_data[i]['phone'] = u""
        events_data[i]['url'] = u""
        #нужно добавить
        events_data[i]['ticket'] = u"no"
        events_data[i]['coordinates'] = u""

    return events_data

def filter_time(new_time):
    new_time = new_time.replace("–", "-")
    new_time_split = new_time.split(":")
    if (len(new_time_split[0]) == 1):
        new_time = "0" + new_time

    new_time_split = new_time.split("-")
    new_time_split_split = new_time_split[1].split(":")
    if (len(new_time_split_split[0]) == 1):
        new_time_split[1] = "0" + str(new_time_split[1])
    new_time = new_time_split[0] + "-" + new_time_split[1]

    return new_time 

def only_time_check(date_is, need_date_array):
    num_day = []

    #словарей несколько
    for i in date_is:
        start_date = date.fromtimestamp(i[u'start_date'])
        end_date = i[u'end_date']
        date_between = []

        if (end_date == start_date):
            try:
                num_day.append(need_date_array.index(start_date))
                continue
            except:
                continue

        if (end_date != None):
            end_date = date.fromtimestamp(i[u'end_date'])
            now_date = start_date
            date_between.append(now_date)

            while (now_date <= end_date):
                now_date = now_date #+ datetime.timedelta(days=1)
                date_between.append(now_date)
            for i in date_between:
                try:
                    num_day.append(need_date_array.index(i))
                except:
                    None
        else:
            try:
                num_day.append(need_date_array.index(start_date))
                continue
            except:
                continue
    return num_day

def get_need_time(num_days):
    today_date = get_today_data()
    delta = datetime.timedelta(days = 1)
    last_date = today_date
    date_array_out = []
    date_array_out.append(str(today_date))
    for i in xrange(num_days-1):
        date = last_date + delta
        date_array_out.append(str(date))
        last_date = date
    return date_array_out

def create_array_good_time(events_data, time_array_need):

    events_day = []
    for i in xrange(len(time_array_need)):
        events_day.append([])

    month_array = [u'января' , u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря']
    #today_date = get_today_data()
  
    need_date_array = time_array_need

    for i in xrange(len(need_date_array)):
        date_split = need_date_array[i].split("-")
        date_split[1] = month_array[int(date_split[1])-1]
   
        if (date_split[2][0] == '0'):
            date_split[2] = date_split[2][1:]
        need_date_array[i] = date_split[2] + " " + date_split[1]

    #существуют временные промежутки, отсеять по датам
    index_array = []

    for index, i in enumerate(events_data):
      if (u":" in i['display_dates_string']):
        data_in_file_mn = i['display_dates_string'].split(u",")
        data_in_file = data_in_file_mn[0].replace(u" 2015", "")
        try:
            index_found = need_date_array.index(data_in_file)
            try:
                #маркер ожидания и прибавляем 3 часа к любым из событий
                i['display_dates_string'], check_wait = time_plusser(data_in_file_mn[1].replace(" ", ""), 3)
                i['display_dates_string'] = filter_time(i['display_dates_string'])
                events_day[index_found].append(i)
            except :
                index_array.append(index)
        except:
            None


    #дополнительная проверка на вхождение в интервал
    for i in index_array:
        day_num = only_time_check(events_data[i]['all_dates'], need_date_array)
        for j in day_num:
            dict = {}
            for k in events_data[i].keys():
                if (k != u'all_dates'):
                    dict[k] = events_data[i][k]
            events_day[j].append(dict)

    return events_day

def get_duration(timestart, timeend):
    diff_time = timeend - timestart

    diff_time = str(diff_time).split(" ")
    if (len(diff_time) == 1):
       diff_time = diff_time[0]
    if (len(diff_time) == 3):
       diff_time = diff_time[-1]

    diff_time_split = str(diff_time).split(":")
    hours = int(diff_time_split[0]) * 60
    minutes = int(diff_time_split[1])

    return timedelta(minutes = hours + minutes)

def insert_other_information(events_day, events_data_place):
    extract_pull_array = []
    #по дням
    for i in xrange(len(events_day)):
        #по событиям
        for j in xrange(len(events_day[i])):
            extract_pull_array.append(events_day[i][j]['place_id'])

    for i in events_data_place:
         if (i['id'] in extract_pull_array):
            for j in xrange(len(events_day)):
                for k in xrange(len(events_day[j])):
                    if (events_day[j][k]['place_id'] == i['id']):
                        events_day[j][k]['phone'] = i['phone']
                        events_day[j][k]['url'] = i['url']
                        events_day[j][k]['address'] = u"Санкт-Петербург, " + i['address']
                        events_day[j][k]['coordinates'] = i['lat_lon']

    events_day_new = []
    for i in xrange(len(events_day)):
        events_day_new.append([])

    all_rank_array = []
    format = '%H:%M'
    from datetime import datetime, timedelta

    for i in xrange(len(events_day)):
        for j in xrange(len(events_day[i])):
            all_rank_array.append(events_day[i][j]['rank'])
            events_day[i][j]['timestart'] = datetime.strptime(events_day[i][j]['display_dates_string'][0:5], format)
            events_day[i][j]['timeend'] = datetime.strptime(events_day[i][j]['display_dates_string'][6:11], format)

            s = events_day[i][j]['timeend'] - events_day[i][j]['timestart']

            if (str(s)[0] == "-" or s == timedelta(hours=0)):
                events_day[i][j]['timeend'] = events_day[i][j]['timeend'] + timedelta(hours=24)

            coord = events_day[i][j]['coordinates'].split(",")
            if (len(coord) == 2):
                events_day[i][j]['latitude'] = float(coord[0])
                events_day[i][j]['longitude'] = float(coord[1])
            events_day[i][j]['duration'] = get_duration(events_day[i][j]['timestart'], events_day[i][j]['timeend'])

            events_day[i][j]['timestart'] =  timedelta(hours = events_day[i][j]['timestart'].hour)\
                                             + timedelta(minutes = events_day[i][j]['timestart'].minute)
            events_day[i][j]['timeend'] = timedelta(hours = events_day[i][j]['timeend'].hour)\
                                          + timedelta(minutes = events_day[i][j]['timeend'].minute)

            if (len(events_day[i][j]['address']) != 0):
                events_day_new[i].append(events_day[i][j].copy())

    max_rank = float(max(all_rank_array))

    for i in xrange(len(events_day_new)):
        for j in xrange(len(events_day_new[i])):
            if (events_day_new[i][j]['duration'] > timedelta(minutes = 180)):
                events_day_new[i][j]['duration'] = timedelta(minutes = 90)
            #else:
            events_day_new[i][j]['fixedtime'] = True

            if (events_day_new[i][j]['phone'] == ''):
                events_day_new[i][j]['phone'] = u"no"
            if (events_day_new[i][j]['url'] == ''):
                events_day_new[i][j]['url'] = u"no"
            if (events_day_new[i][j]['description'] == ''):
                events_day_new[i][j]['description'] = u"no"
            if (events_day_new[i][j]['title'] == ''):
                events_day_new[i][j]['title'] = u"no"

            events_day_new[i][j]['rank'] = float(events_day_new[i][j]['rank']) / max_rank


            events_day_new[i][j]['description'] = events_day_new[i][j]['description'].replace(u"<p>", "").replace(u"</p>", "")

            #его может и не быть
            try:
               del events_day_new[i][j][u'place_id']
            except:
               None
            try:
               del events_day_new[i][j][u'display_dates_string']
            except:
               None
            try:
               del events_day_new[i][j][u'coordinates']
            except:
               None
            try:
               del events_day_new[i][j][u'all_dates']
            except:
               None

    return events_day_new

def by_categories(events_day, how_much_days):

    events_array = []
    for i in events_day:
        for j in i:
            events_array.append(j['categories'][0]['slug'])

    event_wich_use = list(set(events_array))

    main_array = []
    for i in xrange(how_much_days):
        main_array.append([])

    help_array = []

    #по дням
    for index, i in enumerate(events_day):
        main_array[index] = []
        which_is_cat = []
        for index1, j in enumerate(i):
            events_day[index][index1]['categoriesrus'] = events_day[index][index1]['categories'][0]['name']

            try:
                num_index = events_day[index][index1]['categoriesrus'].index("(")
                events_day[index][index1]['categoriesrus'] = events_day[index][index1]['categoriesrus'][0:num_index-1]
            except:
                None

            events_day[index][index1]['categories'] = events_day[index][index1]['categories'][0]['slug']

            which_is_cat.append(events_day[index][index1]['categories'])

        which_is_cat = list(set(which_is_cat))

        for j in which_is_cat:
            help_array.append([])

        for index1, j in enumerate(i):
            num = which_is_cat.index(events_day[index][index1]['categories'])
            help_array[num].append(events_day[index][index1])

        main_array[index] = help_array
        help_array = []

    return main_array, event_wich_use

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

#есть такие дни, когда нет выставок и кинотеатров

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
            array_categories[i] = array_categories[i][0:num_index-1]
        except:
            None

    return array_categories

def get_all_keys(events_data):
    dict = {}
    count = 0
    for i in events_data:
        array_keys = i.keys()
        for j in array_keys:
            if (j in dict.values()):
                None
            else:
                dict[count] = j
                count += 1
    return dict.values()

def is_file_head(time_array):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + "/events/" + "head_array.pkl"

    if os.path.isfile(filename):
       filename = path + "/events/" + "time_check.pkl"
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
    filename = path + "/events/" + "head_array.pkl"

    input = open(filename, 'r')
    head_array = pickle.load(input)
    input.close()

    main_array = head_array[0]
    categories_array_eng = head_array[1]
    categories_array_rus = head_array[2]

    return main_array, time_array, categories_array_eng, categories_array_rus

def write_check_files(main_array, time_array, categories_array_eng, categories_array_rus):
    path = os.path.dirname(os.path.abspath(__file__))
    filename = path + "/events/" + "head_array.pkl"
    head_array = [main_array, categories_array_eng, categories_array_rus]

    output = open(filename, 'w')
    pickle.dump(head_array, output)
    output.close()

    filename = path + "/events/" + "time_check.pkl"
    output = open(filename, 'w')
    pickle.dump(time_array, output)
    output.close()

def main_func(debug_param, time_array_need):

    try:
        if (not(debug_param)):
            extract_data_events.extract_data()
    except:
        print "Pending events"

    time_array = time_array_need

    #for i in xrange(len(time_array)):
    #    time_array[i] = time_array[i][0:4] + "_" + time_array[i][5:7] + "_" + time_array[i][8:len(time_array[i])]

    #############
    #if (is_file_head(time_array)):
    #    print "don't calculate events"
    #    return get_head_array(time_array)

    #извлекаем все данные
    path = os.path.dirname(os.path.abspath(__file__))[:-15] + "/kudago_get_data/data/"

    events_data = extract_data_event(path + "events.pkl")

    #надо разобраться с событиями
    need_place = need_events.need_events

    all_events = get_all_events_name(events_data)

    for i in need_place:
        if (i in all_events):
            None
        else:
            need_place.remove(i)

    need_place_rus = get_rus_name_events(events_data, need_place)

    #не спб и не подходит по категории
    events_data = main_filter_data(events_data, need_place)

    #убираем лишнюю информацию
    events_data = del_ins_excess_inform(events_data)

    #выделяем данные на неделю по каждому из дней
    events_day = create_array_good_time(events_data, time_array_need)

    #задача собрать нужную информацю по месту
    events_data_place = extract_data_place_help(path + "places.pkl")

    events_day = insert_other_information(events_day, events_data_place)

    main_array, categories_array_eng = by_categories(events_day, len(time_array))

    categories_array_rus = []
    for i in categories_array_eng:
        categories_array_rus.append(need_place_rus[need_place.index(i)])

    main_array, categories_array_eng, categories_array_rus =\
        need_events.prepare_categories(main_array, categories_array_eng, categories_array_rus)

    ##########
    #write_check_files(main_array, time_array, categories_array_eng, categories_array_rus)

    print "new write"
    return main_array, time_array, categories_array_eng, categories_array_rus

#пустых категорий нет

#date = get_today_data()
# date = ["2015-06-03"]
#
# #print date
# main_array, time_array, categories_array_eng, categories_array_rus = main_func(True, date)
#
# count = 0
#
# for i in main_array:
#     for j in i:
#         count += 1
#
# print count

#for i in categories_array_eng:
#    print i



