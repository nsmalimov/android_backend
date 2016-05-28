# -*- coding: utf-8 -*-

import copy

import diplom_django.worker_directory.psql_preferences as pref
from django.db import connection


def connect_to_db():
    db_name = pref.dbname_local
    db_user = pref.user_local
    db_password = pref.password_local
    db_localhost = pref.host_local
    db_port = pref.port_local

    cur, conn = pref.connect_to_db(db_name, db_user, db_password, db_localhost, db_port)

    # cur = connection.cursor()

    return cur, conn


def get_users_data(cur):
    users_data = []
    cur.execute("SELECT * FROM users_table")
    for i in cur:
        users_data.append(copy.deepcopy(list(i)))
    return users_data


def get_events_data(cur):
    events_data = []
    cur.execute("SELECT event_id, duration, from_center, category, start_time, rank, fixed_time FROM events_table")
    for i in cur:
        help_rewrite = copy.deepcopy(list(i))
        help_rewrite[0] = int(help_rewrite[0])
        events_data.append(copy.deepcopy(help_rewrite))
    return events_data


def get_ratings_data(cur):
    ratings_data = []
    cur.execute("SELECT event_id, vk_id, assessment FROM ratings_table")
    for i in cur:
        ratings_data.append(copy.deepcopy(list(i)))
    return ratings_data


def main_get_data_func():
    # cur, conn = connect_to_db()

    cur = connection.cursor()
    users_data = get_users_data(cur)  # [3404185, 214, 0, 2, 226, 0, 18]

    events_data = get_events_data(cur)  # [1, 110, 1251, 65, 2, 0, 1]

    ratings_data = get_ratings_data(cur)  # [1, 21747799, 5] [events_id, vk_id, assessment]

    # pref.disconnect_from_db(cur, conn)
    # connection.close()

    return users_data, events_data, ratings_data
