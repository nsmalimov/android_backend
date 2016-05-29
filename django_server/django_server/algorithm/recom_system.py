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
    cur = connection.cursor()

    recom_id_event = select_ratings(cur, vk_id)

    recom_title_event = select_event_title(cur, recom_id_event)

    return recom_title_event
