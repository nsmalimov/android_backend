# -*- coding: utf-8 -*-

import os
import pickle
import glob
import copy
import sys

from django.db import connection

import events_id
import get_simple_dist
import data_path

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

def get_all_new_events():
    all_events = []

    path = data_path.folder_direct

    path  = path + "events/"
    for file in glob.glob(path + "*.pkl"):
        filename = open(file, 'r')
        file_data = pickle.load(filename)
        for i in file_data:
            s = copy.deepcopy(i)
            del s['id']
            all_events.append(copy.deepcopy(s))
        filename.close()

    title_array = []

    new_all_events = []

    for i in xrange(len(all_events)):
        if (all_events[i]['title'] in title_array):
            continue
        else:
            title_array.append(copy.deepcopy(all_events[i]['title']))
            new_all_events.append(copy.deepcopy(all_events[i]))

    return new_all_events

def get_day_partition(time):
    import datetime
    answer = 0
    morning = datetime.timedelta(hours=6)
    evening = datetime.timedelta(hours=18)
    day = datetime.timedelta(hours=12)

    if ((time >= morning) and (time <= day)):
        answer = 0

    if ((time >= day) and (time <= evening)):
        answer = 1

    if ((time >= evening)):
        answer = 2

    #0 - утро
    #1 - день
    #2 - вечер
    return answer


def preparing_to_insert(all_events):
    new_all_events = []
    new_dict = {}

    for i in xrange(len(all_events)):
        new_all_events.append(copy.deepcopy(new_dict))
        new_all_events[i]['title'] = all_events[i]['title']
        new_all_events[i]['rank'] = all_events[i]['rank']

        if (all_events[i]['fixedtime']):
            new_all_events[i]['fixed_time'] = 1
        else:
            new_all_events[i]['fixed_time'] = 0

        d = all_events[i]['duration'].seconds/60
        new_all_events[i]['duration'] = d

        categories = events_id.events_categories
        new_all_events[i]['category'] = categories.index(all_events[i]['categories'])

        latitude_center = 59.9324
        longitude1_center = 30.3152
        new_all_events[i]['from_center'] = \
            get_simple_dist.get_dist(all_events[i]['latitude'], all_events[i]['longitude'],\
                                     latitude_center, longitude1_center)

        new_all_events[i]['start_time'] = get_day_partition(all_events[i]['timestart'])

    return new_all_events

def selector_check(cur):
    answer = []
    cur.execute("SELECT title FROM events_table")
    for i in cur:
        answer.append(copy.deepcopy(i[0]))
    return answer

def inserter_func(cur, all_events):
    is_events_title = selector_check(cur)
    count_insert = 0
    for i in all_events:
        title_events = i['title']
        if (str(title_events) in is_events_title):
            continue
        cur.execute(
             """INSERT INTO events_table (title, duration, from_center, category, start_time, rank, fixed_time)
              VALUES (%(title)s, %(duration)s, %(from_center)s, %(category)s,\
               %(start_time)s, %(rank)s, %(fixed_time)s);""",
            {'title': i['title'], 'duration': i['duration'], 'from_center': i['from_center'],\
            'category': i['category'], 'start_time': i['start_time'],\
            'rank': i['rank'], 'fixed_time': i['fixed_time']})
        count_insert += 1
    print count_insert

def insert_events_psql(all_events):
    #cur, conn = connect_to_db(dbname_local, user_local, password_local, 'localhost', "5432")
    cur = connection.cursor()
    inserter_func(cur, all_events)
    connection.commit()
    #disconnect_from_db(cur, conn)

def main_func():
    print "call cache funk"
    s = get_all_new_events()
    all_events = preparing_to_insert(copy.deepcopy(s))
    insert_events_psql(all_events)


