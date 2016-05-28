# -*- coding: utf-8 -*-

import copy

from sklearn import linear_model

import claster_based
import get_data_recom
import item_based
import metrics


def get_metrics(predicted_array_1, predicted_array_2, actual_array_2, w1, w2):
    main_predict_array = []

    for index, i in enumerate(predicted_array_1):
        if (predicted_array_2[index] == 0):
            main_predict_array.append(predicted_array_1[index])
        elif (predicted_array_1[index] == 0):
            main_predict_array.append(predicted_array_2[index])
        else:
            d = w1 * predicted_array_1[index] + w2 * predicted_array_2[index]
            main_predict_array.append(d)

    rmsd = metrics.root_mean_square_deviation(main_predict_array, actual_array_2)
    mae = metrics.mean_absulutle_error(main_predict_array, actual_array_2)

    print rmsd
    print mae


def hybrid_predict(event_id, vk_id, w1, w2, users_data, events_data, ratings_data):
    predicted_asses = 0

    predict_asses_1 = claster_based.use_clastering_single(event_id, vk_id, users_data, ratings_data)

    ratings_data = copy.deepcopy(claster_based.rating_dict_create(ratings_data))

    predict_asses_2 = \
        item_based.predict_item_based_single(event_id, vk_id, ratings_data, events_data)

    # излишняя проверка для item-based, он всегда возвращает среднее по базе != 0 число
    if (predict_asses_2 == 0):
        predicted_asses = predict_asses_1
    elif (predict_asses_1 == 0):
        predicted_asses = predict_asses_2
    else:
        predicted_asses = w1 * predict_asses_1 + w2 * predict_asses_2

    return predicted_asses


def hybrid_train(predicted_array_1, predicted_array_2, actual_array_1):
    X_train = []

    for i in xrange(len(predicted_array_1)):
        X_train.append([])

    # перекрываем (если один не смог предсказать, заменяем другим)
    for index, i in enumerate(predicted_array_1):
        if (predicted_array_1[index] == 0):
            X_train[index].append(predicted_array_2[index])
        else:
            X_train[index].append(predicted_array_1[index])

        if (predicted_array_2[index] == 0):
            X_train[index].append(predicted_array_1[index])
        else:
            X_train[index].append(predicted_array_2[index])

    regr = linear_model.LinearRegression()

    # коэффициенты (веса)
    regr.fit(X_train, actual_array_1)

    coef = regr.coef_

    w_1 = coef[0]
    w_2 = coef[1]

    return w_1, w_2


def predict(array_to_predict):
    # array_to_predict [event_id, vk_id]
    # event_id, vk_id, assessment
    answer = []

    # обучение модели на существующих данных
    users_data, events_data, ratings_data = get_data_recom.main_get_data_func()

    predicted_array_1, actual_array_1 = claster_based.main(users_data, events_data, ratings_data)
    predicted_array_2, actual_array_2 = item_based.main(users_data, events_data, ratings_data)

    # print len(predicted_array_1), len(actual_array_1)
    # print len(predicted_array_2), len(actual_array_2)

    w1, w2 = hybrid_train(predicted_array_1, predicted_array_2, actual_array_1)

    # print w1, w2

    # get_metrics(predicted_array_1, predicted_array_2, actual_array_2, w1, w2)

    for i in array_to_predict:
        predict_asses = hybrid_predict(i[0], i[1], w1, w2, users_data, events_data, ratings_data)
        answer.append(copy.deepcopy([i[0], i[1], predict_asses]))

    # обучить модель регрессии
    # выбрать лучшие параметры

    # answer = [[3, 21747799, 1], [5, 21747799, 2], [8, 21747799, 3], [9, 21747799, 4], [10, 21747799, 5]]

    return answer
