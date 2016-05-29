# -*- coding: utf-8 -*-

import copy
import datetime

import diplom_django.get_simple_dist


def check_name(some_path):
    all_event_id = []
    for i in some_path:
        all_event_id.append(i[-1])

    return all_event_id


def check_time_func(time_in, time_out, path, dist_matrix, events):
    path = path[::-1]

    main_array = []

    for i in path:
        main_array.append([i.event['timestart'], i.event['timeend'], \
                           i.event['duration'], i.event['fixedtime'], i.event['id']])

    first_event = main_array[0]
    last_event = main_array[-1]

    del main_array[0]
    del main_array[-1]

    main_array.sort(key=lambda x: x[0])

    all_time = time_in

    last_id = 0
    last_time = time_in
    new_path = []
    new_path.append(first_event)

    counter = 0
    # плюс проверка на ночное время
    for i in main_array:
        if (i[3]):
            # если событие вообще не в интервале приезда
            if (i[0] < time_in or i[0] > time_out):
                continue

            # если не успеваем доехать до начала события
            if ((last_time + datetime.timedelta(minutes=dist_matrix[last_id][i[-1]])) > i[0]):
                continue

            time_road_to = datetime.timedelta(minutes=dist_matrix[last_id][i[-1]])

            time_road_back = datetime.timedelta(minutes=dist_matrix[i[-1]][len(dist_matrix) - 1])

            all_time += time_road_to + i[2] + + time_road_back

            # если время посещения события и возврат в конечную больше всего интервала времени
            if (all_time > time_out):
                break

            copy_i = copy.deepcopy(i)

            if (time_road_to > datetime.timedelta(minutes=45)):
                continue

            if (i[-1] in check_name(new_path)):
                continue
            new_path.append(copy.deepcopy(i))

            last_id = i[-1]

            # окончательное время окончания последнего события добавленного в массив
            last_time = i[0] + i[2]

        if (not (i[3])):
            check_var = False
            starter_time = last_time

            times_array = []
            all_minutes = i[1] - i[0]

            delta = datetime.timedelta(minutes=30)
            null_time = datetime.timedelta(seconds=0)

            new_time = i[0]
            if (new_time > last_time):
                times_array.append(new_time)
            while (all_minutes > null_time):
                all_minutes = all_minutes - delta
                new_time = new_time + delta
                if (new_time > last_time):
                    times_array.append(new_time)

            for j in times_array:
                time_road_to = datetime.timedelta(minutes=dist_matrix[last_id][i[-1]])
                time_road_back = datetime.timedelta(minutes=dist_matrix[i[-1]][len(dist_matrix) - 1])

                some_time = j + time_road_to + i[2] + time_road_back

                if (some_time < time_out and j > last_time):
                    check_var = True
                    starter_time = copy.deepcopy(j)
                    break

            if (check_var):
                time_road_to = datetime.timedelta(minutes=dist_matrix[last_id][i[-1]])

                time_road_back = datetime.timedelta(minutes=dist_matrix[i[-1]][len(dist_matrix) - 1])

                all_time += (starter_time - all_time) + time_road_to + time_road_back + i[2]

                if (all_time > time_out):
                    break

                to_insert = copy.deepcopy(i)
                to_insert[0] = starter_time
                to_insert[1] = starter_time + i[2]

                latitude1 = events[last_id]['latitude']
                longitude1 = events[last_id]['longitude']

                latitude2 = events[i[-1]]['latitude']
                longitude2 = events[i[-1]]['longitude']
                simple_dist = diplom_django.get_simple_dist.get_dist(latitude1, longitude1, latitude2, longitude2)
                if (simple_dist > 20000 and time_road_to > datetime.timedelta(minutes=20)):
                    continue
                if (time_road_to > datetime.timedelta(minutes=45)):
                    continue

                if (i[-1] in check_name(new_path)):
                    continue

                new_path.append(copy.deepcopy(to_insert))
                last_id = i[-1]
                last_time = starter_time + i[2]

                all_time = last_time
                counter += 1

    new_path.append(last_event)

    for index, i in enumerate(new_path):
        if ((i[-1] + 1) < len(dist_matrix)):
            new_path[index].append(dist_matrix[i[-1]][i[-1] + 1])

    new_path[-1].append(0)

    return new_path


class AStar(object):
    def __init__(self, graph):
        self.graph = graph

    def heuristic(self, node, start, end, dist_matrix):
        raise NotImplementedError

    def search(self, time_in, time_out, start, end, dist_matrix, copy_dist_matrix, events):
        inserted_title = []
        openset = set()
        closedset = set()
        current = start
        openset.add(current)
        last_x = 0
        last_y = 0
        counter = 0
        while openset:
            current = min(openset, key=lambda o: o.g + o.h)

            # обратный ход (если долшли до конца)
            if current == end:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent

                # добавление первого
                path.append(current)

                path = check_time_func(time_in, time_out, path, copy_dist_matrix, events)
                # перевернуть массив с маршрутом
                return path

            openset.remove(current)
            closedset.add(current)

            for node in self.graph[current]:

                if (node in closedset):
                    continue

                if (node.x < last_x or node.y < last_y):
                    continue

                if node in openset:
                    new_g = current.g + current.move_cost(node, copy.deepcopy(dist_matrix))
                    if node.g > new_g:
                        node.g = new_g
                        node.parent = current
                else:
                    g_func = current.move_cost(node, copy.deepcopy(dist_matrix))
                    node.g = current.g + g_func
                    node.h = self.heuristic(node, start, end, copy.deepcopy(dist_matrix))
                    node.parent = current
                    last_x = node.x
                    last_y = node.y
                    openset.add(node)
        return None


class AStarNode(object):
    def __init__(self):
        self.g = 0
        self.h = 0
        self.parent = None

    def move_cost(self, other, dist_matrix):
        raise NotImplementedError
