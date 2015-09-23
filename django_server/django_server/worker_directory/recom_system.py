# -*- coding: utf-8 -*-

import copy

from django.db import connection


def select_ratings(cur, vk_id):
    recom_id_event = []
    cur.execute("SELECT event_id FROM ratings_table WHERE vk_id=" + str(vk_id) + \
            "AND ((assessment=4)" + "OR (assessment=5))")
    for i in cur:
        recom_id_event.append(copy.deepcopy(i[0]))
    return recom_id_event

def select_event_title(cur, recom_id_event):
    event_title_recom = []
    for i in recom_id_event:
        cur.execute("SELECT title FROM events_table WHERE event_id=" + str(i))
        for i in cur:
            event_title_recom.append(copy.deepcopy(i[0]))
    return list(set(event_title_recom))

def main_func(vk_id):
    recom_title_event = []

    # db_name = psql_preferences.dbname_local
    # db_user = psql_preferences.user_local
    # db_password = psql_preferences.password_local
    # db_localhost = psql_preferences.host_local
    # db_port = psql_preferences.port_local

    # cur, conn = psql_preferences.connect_to_db(db_name, db_user, db_password, db_localhost, db_port)

    cur = connection.cursor()

    recom_id_event = select_ratings(cur, vk_id)

    recom_title_event = select_event_title(cur, recom_id_event)

    #connection.close()
    #psql_preferences.disconnect_from_db(cur, conn)

    return recom_title_event

#main_func(21747799)
