class Ant(object):
    def __init__(self, colony, ant_id, start_note):
        self.id = ant_id
        self.start_node = start_note
        self.colony = colony
        self.cur_node = self.start_node
        self.path_cost = 0
        self.beta = 1
        self.rho = 0.99
        self.nodes = {}

        for i in range(self.graph.num_nodes):
            if i != self.start_node:
                self.nodes[i] = i

        self.graph = colony.graph
        self.matrix = []

        for i in range(self.graph.num_nodes):
            self.matrix.append([0]*self.graph.num_nodes)

