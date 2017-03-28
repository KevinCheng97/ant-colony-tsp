import sys
import random
from threading import Lock, Condition
from time import sleep

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

        self.condition = Condition()

        self.avg_path_cost = 0
        self.ant_counter = 0

    def colonize(self):
        self.ants = self.populate()
        self.iterations_counter = 0

        while self.iterations_counter < self.iterations:
            self.iterate()

            self.condition.acquire()
            self.condition.wait()
            sleep(2)

            lock = self.graph.lock
            lock.acquire()
            self.colony_pheromone()
            lock.release()

            self.condition.release()

    def clean(self):
        self.best_path = None
        self.best_matrix = None
        self.last_best_iteration = 0
        self.lowest_cost = sys.maxint

    def populate(self):
        self.clean()
        return [Ant(self, i, random.randint(0, self.graph.num_nodes-1))
                for i in range(self.num_ants)]

    def iterate(self):
        self.avg_path_cost = 0
        self.ant_counter = 0
        self.iterations_counter += 1
        for ant in self.ants:
            ant.start()

    def update(self, ant):
        lock = Lock()
        lock.acquire()

        self.ant_counter += 1
        self.avg_path_cost += ant.path_cost

        if ant.path_cost < self.lowest_cost:
            self.lowest_cost = ant.path_cost
            self.best_matrix = ant.matrix
            self.best_path = ant.vector
            self.last_best_iteration = self.iterations_counter

        if self.ant_counter == len(self.ants):
            self.avg_path_cost /= ant.path_cost
            self.condition.acquire()
            self.condition.notifyAll()
            self.condition.release()
        lock.release()

    def colony_pheromone(self):
        for r in range(0, self.graph.num_nodes):
            for s in range(0, self.graph.num_nodes):
                if r != s:
                    delta_tau = self.best_matrix[r][s] / self.lowest_cost
                    evaporation = (1 - self.alpha) * self.graph.tau(r, s)
                    deposition = self.alpha * delta_tau

                    self.graph.update_tau(r, s, evaporation + deposition)
