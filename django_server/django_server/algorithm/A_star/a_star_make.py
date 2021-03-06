# -*- coding: utf-8 -*-

from itertools import product

from astar_grid import AStarGrid, AStarGridNode


def make_graph(width, height, events):
    nodes = []
    for i in xrange(width):
        nodes.append([])
        for j in xrange(height):
            nodes[i].append([])

    # построение графа
    for i in xrange(0, width):
        num = i
        for j in xrange(0, height):
            nodes[i][j] = AStarGridNode(i, j, events[num])
            num += 1
            if (num >= (height - 1)):
                num = 1

    nodes[-1][-1] = AStarGridNode(width, width, events[-1])

    graph = {}
    for x, y in product(range(width), range(height)):
        node = nodes[x][y]
        graph[node] = []

        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < width):
                continue
            if not (0 <= y + j < height):
                continue
            graph[nodes[x][y]].append(nodes[x + i][y + j])
            graph[nodes[x][y]].append(nodes[x + i][y + j])

    return graph, nodes


def get_route_astar_funk(events, dist_matrix, time_in, time_out, copy_dist_matrix):
    graph, nodes = make_graph(len(events), len(events), events)

    paths = AStarGrid(graph)
    start, end = nodes[0][0], nodes[len(events) - 1][len(events) - 1]

    path = paths.search(time_in, time_out, start, end, dist_matrix, copy_dist_matrix, events)

    return path
