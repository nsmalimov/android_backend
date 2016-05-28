# -*- coding: utf-8 -*-

import copy
import random

from diplom_django.worker_directory import psql_preferences
from diplom_django.worker_directory import vk_api

vk_id_array = [21747799, 3404185, 31493186, 22679845, 13185289, \
               165191686, 67415706, 84223404, 10083456, 9453118, \
               52410586, 31446501, 4908037, 82718748]


def insert_vk_id(cur, vk_inform, user_id):
    cur.execute(
        """INSERT INTO users_table (vk_id, count_friends, age, gender, count_audios, country, count_photos)
           VALUES (%(vkid)s, %(countfriends)s, %(age)s, %(gender)s, %(count_audios)s, %(country)s, %(countphotos)s);""",
        {'vkid': user_id, 'countfriends': vk_inform['count_friends'], \
         'age': vk_inform['age'], 'gender': vk_inform['gender'], 'count_audios': vk_inform['count_audios'], \
         'country': vk_inform['country'], 'countphotos': vk_inform['count_photos']})


def add_user(cur):
    for i in vk_id_array:
        try:
            vk_inform = vk_api.user_information(i)
            insert_vk_id(cur, vk_inform, i)
        except:
            print "error"


def insert_one_rating_table(cur, assesment, vk_id, events_id):
    cur.execute("SELECT event_id, vk_id FROM ratings_table WHERE\
                 event_id=" + "'" + str(events_id) + "'AND vk_id='" + str(vk_id) + "'")

    check_array = []

    for i in cur:
        check_array.append(copy.deepcopy(i))

    if (len(check_array) != 0):
        return

    cur.execute(
        """INSERT INTO ratings_table (event_id, vk_id, assessment, system_asses)
          VALUES (%(event_id)s, %(vk_id)s, %(assessment)s, %(system_asses)s);""",
        {'event_id': events_id, 'vk_id': vk_id, 'assessment': float(assesment), 'system_asses': False})


def filling_rating_table(cur):
    events_id_array = []
    vk_id_array = []

    cur.execute("SELECT vk_id FROM users_table")
    for i in cur:
        vk_id_array.append(copy.deepcopy(i[0]))

    cur.execute("SELECT event_id FROM events_table")
    for i in cur:
        events_id_array.append(copy.deepcopy(i[0]))

    # вставить в среднем 100 событий на пользователя

    for i in vk_id_array:
        for j in xrange(100):
            assesment_rand = random.randint(1, 5)
            event_num = random.randint(0, len(events_id_array) - 1)
            insert_one_rating_table(cur, assesment_rand, i, events_id_array[event_num])


def main_work():
    db_name = psql_preferences.dbname_local
    db_user = psql_preferences.user_local
    db_password = psql_preferences.password_local
    db_localhost = psql_preferences.host_local
    db_port = psql_preferences.port_local

    cur, conn = psql_preferences.connect_to_db(db_name, db_user, db_password, db_localhost, db_port)

    try:
        # добавление пользователей
        # add_user(cur)

        # добавление оценок событиям
        filling_rating_table(cur)

        conn.commit()
    except Exception as inst:
        print inst
    finally:
        psql_preferences.disconnect_from_db(cur, conn)


main_work()
