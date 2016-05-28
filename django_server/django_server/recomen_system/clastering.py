# -*- coding: utf-8 -*-
import copy

from sklearn import cluster


def make_clast(users_data, ratings_data):
    users = []
    for i in ratings_data:
        users.append(copy.deepcopy(i[1]))

    users = list(set(users))

    users_inf_dict = {}

    for i in users:
        for j in users_data:
            if (j[0] == i):
                users_inf_dict[i] = copy.deepcopy(j[1:])

    users_numerate_array = users_inf_dict.keys()

    X_array = users_inf_dict.values()

    num_clusters = len(X_array) / 50

    # на сколько кластеров разбивать
    if (num_clusters <= 50): num_clusters = 5
    if (num_clusters > 50 and num_clusters < 150): num_clusters = 10

    k_means = cluster.KMeans(n_clusters=num_clusters)
    k_means.fit(X_array)

    # номер показывает номер кластера
    clusterized_array = list(k_means.labels_)

    dict_users_clasters = {}

    for index, i in enumerate(clusterized_array):
        dict_users_clasters[users_numerate_array[index]] = copy.deepcopy(i)

    return dict_users_clasters


def make_clast_single(users_data):
    users_inf_dict = {}

    for i in users_data:
        users_inf_dict[i[0]] = copy.deepcopy(i[1:])

    users_numerate_array = users_inf_dict.keys()

    X_array = users_inf_dict.values()

    num_clusters = len(X_array) / 50

    # на сколько кластеров разбивать
    if (num_clusters <= 50): num_clusters = 5
    if (num_clusters > 50 and num_clusters < 150): num_clusters = 10

    k_means = cluster.KMeans(n_clusters=num_clusters)
    k_means.fit(X_array)

    # номер показывает номер кластера
    clusterized_array = list(k_means.labels_)

    dict_users_clasters = {}

    for index, i in enumerate(clusterized_array):
        dict_users_clasters[users_numerate_array[index]] = copy.deepcopy(i)

    return dict_users_clasters
