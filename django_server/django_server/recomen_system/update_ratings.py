# -*- coding: utf-8 -*-

import copy

from django.db import connection

import hybrid


def get_users_data(cur):
    users_data = []
    cur.execute("SELECT vk_id FROM users_table")
    for i in cur:
        users_data.append(copy.deepcopy(i[0]))
    return users_data


def get_events_data(cur):
    events_data = []
    cur.execute("SELECT event_id FROM events_table")
    for i in cur:
        events_data.append(copy.deepcopy(int(i[0])))
    return events_data


def get_ratings_data(cur):
    ratings_data = []
    cur.execute("SELECT event_id, vk_id FROM ratings_table")
    for i in cur:
        ratings_data.append(copy.deepcopy(list(i)))
    return ratings_data


def del_system_asses_var(cur):
    cur.execute("DELETE FROM ratings_table WHERE system_asses=" + str(True))


def select_not_asses(cur):
    not_asses_array_id = []
    del_system_asses_var(cur)
    connection.commit()

    data_users = get_users_data(cur)
    data_events = get_events_data(cur)

    # убрать оценки с system_asses = true

    ratings_data = get_ratings_data(cur)

    # формируем те, которые должны быть (все варианты)
    all_var_array = []

    for i in data_users:
        for j in data_events:
            new_var = [copy.deepcopy(j), copy.deepcopy(i)]
            # если нет оценок в базе
            if (not (new_var in ratings_data)):
                all_var_array.append(copy.deepcopy(new_var))

    return all_var_array


def insert_predicted(cur, predicted_array):
    for i in predicted_array:
        check_array = []

        cur.execute("SELECT (event_id, vk_id) FROM ratings_table WHERE\
                 event_id=" + "'" + str(i[0]) + "'AND vk_id='" + str(i[1]) + "'")

        for i in cur:
            check_array.append(copy.deepcopy(i))

        if (len(check_array) != 0):
            return

        cur.execute(
            """INSERT INTO ratings_table (event_id, vk_id, assessment, system_asses)
             VALUES (%(event_id)s, %(vk_id)s, %(assessment)s , %(system_asses)s);""",
            {'event_id': i[0], 'vk_id': i[1], 'assessment': float(i[2]), 'system_asses': True})


def psql_update_ratings():
    cur = connection.cursor()

    array_to_predict = select_not_asses(cur)

    predicted_array = hybrid.predict(array_to_predict)

    insert_predicted(cur, predicted_array)

    connection.commit()
