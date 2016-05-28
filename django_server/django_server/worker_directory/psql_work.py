# -*- coding: utf-8 -*-

from django.db import connection

import vk_api


def insert_to_table(cur, vk_inform, user_id):
    cur.execute(
        """INSERT INTO users_table (vk_id, count_friends, age, gender, count_audios, country, count_photos)
           VALUES (%(vkid)s, %(countfriends)s, %(age)s, %(gender)s, %(count_audios)s, %(country)s, %(countphotos)s);""",
        {'vkid': user_id, 'countfriends': vk_inform['count_friends'], \
         'age': vk_inform['age'], 'gender': vk_inform['gender'], 'count_audios': vk_inform['count_audios'], \
         'country': vk_inform['country'], 'countphotos': vk_inform['count_photos']})


def commit_to_db(conn):
    conn.commit()


def add_user(vk_id):
    cur = connection.cursor()
    try:
        vk_inform = vk_api.user_information(vk_id)
        insert_to_table(cur, vk_inform, vk_id)
    except:
        None
    connection.commit()


def add_assesment(request_dict):
    cur = connection.cursor()

    # cur, conn = connect_to_db(dbname_local, user_local, password_local, 'localhost', "5432")

    event_base_id = 1
    cur.execute("SELECT event_id FROM events_table WHERE title=" + "'" + request_dict['event_name'] + "'")

    for i in cur:
        event_base_id = int(i[0])

    cur.execute("SELECT (event_id, vk_id) FROM ratings_table WHERE\
                 event_id=" + "'" + str(event_base_id) + "'AND vk_id='" + request_dict['id'] + "'")

    check_array = []

    for i in cur:
        if (len(i) != 0):
            check_array.append(i[0])

    assesment_new = float(request_dict['asses'])

    if (len(check_array) != 0):
        # assesment_old = check_array[0]
        cur.execute(
            """UPDATE ratings_table SET assessment=""" + str(assesment_new) +
            """ WHERE event_id=""" + str(event_base_id) + """ AND """ +
            """vk_id=""" + str(request_dict['id']) + """;""")

    if (len(check_array) == 0):
        cur.execute(
            """INSERT INTO ratings_table (event_id, vk_id, assessment, system_asses)
              VALUES (%(event_id)s, %(vk_id)s, %(assessment)s, %(system_asses)s);""",
            {'event_id': event_base_id, 'vk_id': int(request_dict['id']), \
             'assessment': assesment_new, 'system_asses': False})

    # conn.commit()
    # conn.close()
    connection.commit()
