import copy
import glob
import pickle


def get_minutes(scikit_model, latitude_1, longitude_1, latitude_2, longitude_2):
    minutes_predict = scikit_model.predict([latitude_1, longitude_1, latitude_2, longitude_2])
    return int(minutes_predict[0])


def create_dist_matrix(forest, path):
    for file in glob.glob(path + "/events/" + "*.pkl"):
        input = open(file, "r")
        day_data = pickle.load(input)
        input.close()

        day_dist_data = dist_array(forest, day_data, path)

        name_new_file = file.split("/")[-1].replace("events", "dist")

        output = open(path + "/distance_matrix/" + name_new_file, 'w')
        pickle.dump(day_dist_data, output)
        output.close()


def dist_array(forest, events, path):
    distance_matrix = []

    for i in xrange(len(events)):
        help_array = []
        for j in xrange(len(events)):
            help_array.append(copy.deepcopy([]))
        distance_matrix.append(copy.deepcopy(help_array))

    for i in xrange(len(events)):
        for j in xrange(len(events)):
            if (i == j):
                distance_matrix[i][j] = 0
                continue

            minutes = get_minutes(forest, events[i]['latitude'], events[i]['longitude'], events[j]['latitude'],
                                  events[j]['longitude'])

            distance_matrix[i][j] = copy.deepcopy(minutes)

    return distance_matrix


path = "/home/azureuser/data_files/"

f = open(path + "coordinates/coordinates.pkl", "r")
coord = pickle.load(f)
f.close()

from sklearn.ensemble import RandomForestRegressor

X_train = []
Y_train = []
for i in coord:
    if (coord[i] != "no"):
        X_train.append(copy.deepcopy(list(i)))
        Y_train.append(copy.deepcopy(int(coord[i])))

forest1 = RandomForestRegressor()

forest1.fit(X_train, Y_train)

create_dist_matrix(forest1, path)

# f = open(path + "distance_matrix/dist_2015-06-09.pkl", "r")

# dist_matrix = pickle.load(f)

# f.close()
# for i in dist_matrix:
#	print i


f = open(path + "scikit_model/scikit_model.pkl", "w")

pickle.dump(forest1, f)

f.close()
