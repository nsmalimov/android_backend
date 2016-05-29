# -*- coding: utf-8 -*-

import json
import pickle
import sys
import urllib2

from sklearn.ensemble.forest import RandomForestRegressor

path_to_file = "work_files"

reload(sys)
sys.setdefaultencoding('utf-8')
sys.getdefaultencoding()

flag = "driving"


# driving - на общественном транспорте
# walking - пешком
# на велосипеде

def get_distance(latitude1, longitude1, latitude2, longitude2, flag):
    # Элементов на запрос: 100
    # Элементов за 10 секунд: 100
    # Элементов за 24 часа: 2500

    import time
    time.sleep(0.5)
    main_str = "http://maps.googleapis.com/maps/api/directions/json?origin=" \
               + str(latitude1) + "," + str(longitude1) + \
               "&" + "destination=" + str(latitude2) + "," + str(longitude2) \
               + "&mode=" + flag

    try:
        response = urllib2.urlopen(main_str)
        data = json.load(response)
    except:
        return "no"

    if (u'status' in data.keys() and data['status'] != "OK"):
        print main_str, data['status']
        return "limit"

    try:
        times = str(data["routes"][0]["legs"][0]["duration"]["text"])
    except Exception as inst:
        return "no"

    split_time = times.split(" ")
    if (len(split_time) == 2):
        return split_time[0]
    else:
        return str(int(split_time[0]) * 60 + int(split_time[2]))


def Random_forest_func(path):
    input = open(path + "/coordinates/" + "coordinates.pkl", 'r')

    train_dist = pickle.load(input)

    input.close()

    new_train_dist = {}

    count_calculate_dist = 0

    print "rf", len(train_dist)
    for i in train_dist:
        if (train_dist[i] == "no"):
            try:
                latitude1 = i[0]
                longitude1 = i[1]

                latitude2 = i[2]
                longitude2 = i[3]

                new_dist = get_distance(latitude1, longitude1, latitude2, longitude2, flag)

                if (new_dist == "limit"):
                    print "Google api break"
                    break

                new_train_dist[i] = new_dist
                train_dist[i] = new_dist

                count_calculate_dist += 1

            except Exception as inst:
                print inst
        else:
            new_train_dist[i] = train_dist[i]

    regr = RandomForestRegressor()

    X = []
    Y = []

    for i in new_train_dist:
        X.append(list(i))
        Y.append(new_train_dist[i])

    if (len(X) == 0):
        print "len(X) == 0"
        return []

    regr.fit(X, Y)

    output = open(path + "/scikit_model/" + "scikit_model.pkl", 'w')
    pickle.dump(regr, output)

    output.close()

    return train_dist
