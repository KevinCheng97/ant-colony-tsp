import math, random
from threading import Thread


class Ant(Thread):
    def __init__(self, colony, ant_id, start_node):
        Thread.__init__(self)
        self.id = ant_id
        self.start_node = start_node
        self.colony = colony
        self.cur_node = self.start_node
        self.graph = colony.graph
        self.path_cost = 0
        self.beta = 1
        self.rho = 0.99
        self.nodes = {}

        for i in range(self.graph.num_nodes):
            if i != self.start_node:
                self.nodes[i] = i

        self.vector = []
        self.vector.append(self.start_node)
        self.path_cost = 0
        self.matrix = []

        for i in range(self.graph.num_nodes):
            self.matrix.append([0]*self.graph.num_nodes)

        self.beta = 1
        self.q_0 = 0.5
        self.rho = 0.99

    def run(self):
        graph = self.colony.graph
        while self.nodes:
            graph.lock.acquire()

            new_node = self.state_transition(self.cur_node)
            self.path_cost += graph.delta(self.cur_node, new_node)
            self.vector.append(new_node)
            self.matrix[self.cur_node][new_node] = 1

            print "Ant %s : %s, %s" % (self.id, self.vector, self.path_cost,)

            self.update_pheromone(self.cur_node, new_node)
            graph.lock.release()

            self.cur_node = new_node

        self.path_cost += graph.delta(self.vector[-1], self.vector[0])
        self.colony.update(self)

        print "Ant thread %s terminating." % (self.id,)

        self.__init__(self.colony, self.id, self.start_node)

    def state_transition(self, cur_node):
        graph = self.colony.graph
        q_n = random.random()

        if q_n < self.q_0:
            max_node = self.exploit(cur_node, graph)
        else:
            max_node = self.explore(cur_node, graph)

        if max_node < 0:
            raise AntException("no solution")

        del self.nodes[max_node]
        return max_node

    def exploit(self, cur_node, graph):
        max_val = -1
        max_node = -1

        for node in self.nodes.values():
            if graph.tau(cur_node, node) == 0:
                raise AntException("0 tau")

            cur_val = graph.tau(cur_node, node) * math.pow(graph.etha(cur_node, node), self.beta)
            if cur_val > max_val:
                max_val = cur_val
                max_node = node
        return max_node

    def explore(self, cur_node, graph):
        max_node = -1
        total = 0
        node = -1

        if not self.nodes.values():
            raise AntException("can't explore empty path")

        for node in self.nodes.values():
            if graph.tau(cur_node, node) == 0:
                raise AntException("0 tau")
            total += graph.tau(cur_node, node) * math.pow(graph.etha(cur_node, node), self.beta)

        avg = total / len(self.nodes)

        for node in self.nodes.values():
            path = graph.tau(cur_node, node) * math.pow(graph.etha(cur_node, node), self.beta)
            if path > avg:
                max_node = node
        if max_node == -1:
            return node
        return max_node

    def update_pheromone(self, cur_node, next_node):
        graph = self.colony.graph
        val = (1 - self.rho) * graph.tau(cur_node, next_node) + (self.rho * graph.tau_0)
        graph.update_tau(cur_node, next_node, val)


class AntException(Exception):
    """Specific Ant Exceptions"""
