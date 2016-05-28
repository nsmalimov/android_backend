# -*- coding: utf-8 -*-

import glob
import pickle

import diplom_django.data_path


def get_events(path, date):
    events = []
    need_filename = path + "events/" + "events_" + str(date) + ".pkl"

    path = path + "events/"
    for file in glob.glob(path + "*.pkl"):
        # print file, need_filename
        if (file == need_filename):
            # print file
            # print need_filename
            filename = open(file, 'r')
            events = pickle.load(filename)
            filename.close()
            return events

    return events


def get_distance_matrix(path, date):
    dist_matrix = []
    need_filename = path + "distance_matrix/" + "dist_" + str(date) + ".pkl"

    path = path + "distance_matrix/"
    for file in glob.glob(path + "*.pkl"):
        if (file == need_filename):
            # print file
            filename = open(file, 'r')
            dist_matrix = pickle.load(filename)
            filename.close()
            return dist_matrix

    return dist_matrix


def get_data_from_files(date):
    events = []
    dist_matrx = []
    list_events = []
    scikit_model = []

    path = diplom_django.data_path.folder_direct

    f = open(path + "scikit_model/scikit_model.pkl", "r")
    scikit_model = pickle.load(f)
    f.close()

    events = get_events(path, date)
    dist_matrx = get_distance_matrix(path, date)

    return events, dist_matrx, scikit_model
