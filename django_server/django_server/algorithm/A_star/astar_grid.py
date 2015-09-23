# -*- coding: utf-8 -*-

from astar import AStar, AStarNode
from math import sqrt
import copy

class AStarGrid(AStar):
    def heuristic(self, node, start, end, dist_matrix):
        return sqrt((end.x - node.x)**2 + (end.y - node.y)**2)

class AStarGridNode(AStarNode):
    def __init__(self, x, y, event):
        self.x, self.y = x, y
        self.event = copy.deepcopy(event)
        super(AStarGridNode, self).__init__()

    def move_cost(self, other, dist_matrix):
        #ошибка?
        fist_id = copy.deepcopy(self.event['id'])
        second_id = copy.deepcopy(other.event['id'])

        cost_g = dist_matrix[fist_id][second_id]

        if (cost_g == 0):
            return 1000

        return cost_g