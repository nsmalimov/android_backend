# -*- coding: utf-8 -*-

from astar_grid import AStarGrid, AStarGridNode
from itertools import product
import copy

def make_graph(width, height, events):
    nodes = []
    for i in xrange(width):
        nodes.append([])
        for j in xrange(height):
            nodes[i].append([])

    #построение графа
    for i in xrange(0, width):
        num = i
        for j in xrange(0, height):
            nodes[i][j] = AStarGridNode(i, j, events[num])
            num += 1
            if (num >= (height-1)):
                num = 1

    nodes[-1][-1] = AStarGridNode(width, width, events[-1])

    #print events[-1]['id']
    #for i in nodes:
    #   for j in i:
    #       print j.event['id'],
    #   print

    graph = {}
    for x, y in product(range(width), range(height)):
        node = nodes[x][y]
        graph[node] = []

        for i, j in product([-1, 0, 1], [-1, 0, 1]):
           if not (0 <= x + i < width):
               continue
           if not (0 <= y + j < height):
               continue
           graph[nodes[x][y]].append(nodes[x+i][y+j])
           graph[nodes[x][y]].append(nodes[x+i][y+j])

    return graph, nodes

def get_route_astar_funk(events, dist_matrix, time_in, time_out, copy_dist_matrix):
    graph, nodes = make_graph(len(events), len(events), events)

    paths = AStarGrid(graph)
    start, end = nodes[0][0], nodes[len(events)-1][len(events)-1]

    path = paths.search(time_in, time_out, start, end, dist_matrix, copy_dist_matrix, events)

    some_array = []

    all_cost = 0

    last_x = 0
    last_y = 0

    #for i in path:
    #    print i.x, i.y, i.event['title'], i.event['timestart'], i.event['timeend']

    #for i in path:
    #    print i.x, i.y, i.event['title'], i.event['id']
    #    all_cost += dist_matrix[last_x][i.event['id']]
    #    last_x = i.event['id']

    return path
