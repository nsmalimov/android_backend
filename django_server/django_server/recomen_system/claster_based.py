# -*- coding: utf-8 -*-
import copy

import clastering


def rating_dict_create(ratings_data):
    dict_rate = {}

    for i in ratings_data:
        try:
            dict_rate[i[1]].update({i[0]: i[2]})
        except:
            dict_rate[i[1]] = {i[0]: i[2]}

    return dict_rate


def use_clastering(users_data, ratings_data):
    rating_dict = rating_dict_create(ratings_data)

    predict_array = []
    actual_array = []

    # кластеризовать пользователей
    # {user:claster}
    dict_users_clasters = clastering.make_clast(users_data, ratings_data)

    predict_array = []
    actual_array = []

    for i in rating_dict:
        inner_dict = copy.deepcopy(rating_dict[i])
        for j in inner_dict:
            assess = copy.deepcopy(inner_dict[j])
            actual_array.append(copy.deepcopy(assess))
            cluster = copy.deepcopy(dict_users_clasters[i])
            event_id = copy.deepcopy(j)

            array_assess = []

            for i in dict_users_clasters:
                if (dict_users_clasters[i] == cluster):
                    inner_dict_new = copy.deepcopy(rating_dict[i])
                    if (event_id in inner_dict_new.keys()):
                        array_assess.append(copy.deepcopy(inner_dict_new[event_id]))

            if (len(array_assess) != 0):
                predict_array.append(sum(array_assess) / float(len(array_assess)))
            else:
                predict_array.append(0)

    return predict_array, actual_array


def use_clastering_single(event_id, vk_id, users_data, ratings_data):
    rating_dict = rating_dict_create(ratings_data)

    # кластеризовать пользователей
    # {user:claster}
    dict_users_clasters = clastering.make_clast_single(users_data)

    cluster = copy.deepcopy(dict_users_clasters[vk_id])
    event_id_new = copy.deepcopy(event_id)

    array_assess = []

    for i in dict_users_clasters:
        if (dict_users_clasters[i] == cluster):
            inner_dict_new = copy.deepcopy(rating_dict[i])
            if (event_id in inner_dict_new.keys()):
                array_assess.append(copy.deepcopy(inner_dict_new[event_id_new]))

    if (len(array_assess) != 0):
        predict_asses = sum(array_assess) / float(len(array_assess))
    else:
        predict_asses = 0

    return predict_asses


def main(users_data, events_data, ratings_data):
    predict_array, actual_array = use_clastering(users_data, ratings_data)

    return predict_array, actual_array
