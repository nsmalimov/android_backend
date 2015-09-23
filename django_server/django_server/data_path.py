# -*- coding: utf-8 -*-

import glob

local = False

if (local):
    folder_direct = "/Users/Nurislam/Documents/data_files/"
else:
    folder_direct = "/home/azureuser/data_files/"


def get_wich_days():
    #номер месяца - число без 0
    #"06-18-2015"
    dates = []
    path = folder_direct

    path  = path + "events/"

    for file in glob.glob(path + "*.pkl"):
        file = file.replace(path, "")
        file = file.replace(".pkl", "")
        file = file.replace("events_", "")
        file_split = file.split("-")
        years = file_split[0]

        month = file_split[1]
        if (month[0] == "0"):
            month = month[1]

        days = file_split[-1]
        if (days[0] == "0"):
            days = days[1]

        dates.append(month + "-" + days + "-" + years)

    #dates.append("6-15-2015")
    #print dates
    return dates
