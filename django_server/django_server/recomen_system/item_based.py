# -*- coding: utf-8 -*-
import math
import copy

def get_similarity(array_id_1, array_id_2, array_users_all_dict):
    sim = euclidean_dist(array_users_all_dict[array_id_1], array_users_all_dict[array_id_2])
    return sim

def predict_item_based(user_id, event_id, dict_rate, average_rate, array_users_all, data_events):
    predict_answer = 0

    sum_up = 0
    sum_down = 0

    new_dict = copy.deepcopy(data_events.copy())
    del new_dict[event_id]

    #count = 0
    for i in new_dict.keys():
        try:
            s = copy.deepcopy(dict_rate[user_id][i])
        except:
            #если пользователь не оценивал эту книгу то передаём 0
            sum_up += 0
            sum_down += 0
            continue

        sum_up += get_similarity(i, event_id, data_events) * (dict_rate[user_id][i] - average_rate[i])
        sum_down += get_similarity(i, event_id, data_events)

    if (sum_down != 0):
        predict_answer += (average_rate[event_id] + sum_up/sum_down)
    else:
        predict_answer += average_rate[event_id]
    return predict_answer

def item_based(users, events, dict_rate, users_data, events_data):
    predict_array = []
    actual_array = []

    dict_event = {}

    for i in events_data:
        data_event = copy.deepcopy(i)
        dict_event[i[0]] = copy.deepcopy(data_event[1:])

    average_rate = {}
    for i in dict_event:
        average_rate[i] = copy.deepcopy([])

    for i in dict_rate:
        array_dict = copy.deepcopy(dict_rate[i])
        for j in array_dict.keys():
            average_rate[j].append(copy.deepcopy(array_dict[j]))

    for i in average_rate:
        if (len(average_rate[i]) == 0):
            average_rate[i] = 0
        else:
            average_rate[i] = sum(average_rate[i]) / float(len(average_rate[i]))

    predict_answer = 0
    #по юзерам
    count = 0
    for i in dict_rate:
        inner_dict = copy.deepcopy(dict_rate[i])
        #по книгам для кажого пользователя
        for j in inner_dict:
            assess = copy.deepcopy(inner_dict[j])
            actual_array.append(copy.deepcopy(assess))
            predict_answer = predict_item_based(i, j, dict_rate, average_rate, users, dict_event)
            predict_array.append(copy.deepcopy(predict_answer))
        count += 1

    return predict_array, actual_array

def euclidean_dist(x_array, y_array):
    sum = 0
    for i in xrange(len(x_array)):
        sum += (x_array[i] - y_array[i]) ** 2
    return math.sqrt(sum)

def rating_dict_create(ratings_data):
    dict_rate = {}

    for i in ratings_data:
        try:
            dict_rate[i[1]].update({i[0]:int(i[2])})
        except:
            dict_rate[i[1]] = {i[0]:int(i[2])}

    return dict_rate

def main(users_data, events_data, ratings_data):
    # event_id, vk_id, assessment

    users = []
    for i in ratings_data:
        users.append(i[1])
    users =  list(set(users))

    events = []
    for i in ratings_data:
        events.append(i[0])
    events =  list(set(events))

    dict_rate = rating_dict_create(ratings_data)

    predict_array, actual_array = item_based(users, events, dict_rate, users_data, events_data)

    return predict_array, actual_array

def predict_item_based_single(event_id, user_id, dict_rate, data_events):

    dict_event = {}

    for i in data_events:
        data_event = copy.deepcopy(i)
        dict_event[i[0]] = copy.deepcopy(data_event[1:])

    average_rate = {}
    for i in dict_event:
        average_rate[i] = copy.deepcopy([])

    for i in dict_rate:
        array_dict = copy.deepcopy(dict_rate[i])
        for j in array_dict.keys():
            average_rate[j].append(copy.deepcopy(array_dict[j]))

    for i in average_rate:
        if (len(average_rate[i]) == 0):
            average_rate[i] = 0
        else:
            average_rate[i] = sum(average_rate[i]) / float(len(average_rate[i]))

    predict_answer = 0

    sum_up = 0
    sum_down = 0

    new_dict = copy.deepcopy(dict_event.copy())
    del new_dict[event_id]

    #count = 0
    for i in new_dict.keys():
        try:
            s = copy.deepcopy(dict_rate[user_id][i])
        except:
            #если пользователь не оценивал эту книгу то передаём 0
            sum_up += 0
            sum_down += 0
            continue

        #print data_events[i], data_events[event_id]
        sum_up += get_similarity(i, event_id, dict_event) * (dict_rate[user_id][i] - average_rate[i])
        sum_down += get_similarity(i, event_id, dict_event)

    if (sum_down != 0):
        predict_answer = (average_rate[event_id] + sum_up/sum_down)
    else:
        predict_answer = average_rate[event_id]

    return predict_answer


