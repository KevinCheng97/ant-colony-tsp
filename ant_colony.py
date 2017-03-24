import sys
import random

from ant import Ant


class AntColony(object):
    def __init__(self, graph, num_ants, iterations):
        self.graph = graph
        self.num_ants = num_ants
        self.iterations = iterations
        self.iterations_counter = 0
        self.alpha = 0.1

        self.best_path = None
        self.best_matrix = None
        self.last_best_iteration = 0
        self.lowest_cost = sys.maxint
        self.ants = []

        self.avg_path_cost = 0
        self.ant_counter = 0

    def solve(self):
        self.ants = self.populate()
        self.iterations_counter = 0

        while self.iterations_counter < self.iterations:
            self.iterate()

    def clean(self):
        self.best_path = None
        self.best_matrix = None
        self.last_best_iteration = 0
        self.lowest_cost = sys.maxint

    def populate(self):
        self.clean()
        return [Ant(self, i, random.randint(0, self.graph.num_nodes-1)) for i in range(self.num_ants)]

    def iterate(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iterations_counter += 1
        map(lambda ant: ant.start(), self.ants)
