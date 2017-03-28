from threading import Lock


class AntGraph(object):
    def __init__(self, num_nodes, delta_matrix, tau_matrix=[]):
        if len(delta_matrix) != num_nodes:
            raise GraphException("mismatched sizes")

        self.num_nodes = num_nodes
        self.delta_matrix = delta_matrix
        self.lock = Lock()

        self.tau_matrix = tau_matrix
        if not tau_matrix:
            self.tau_matrix = [[0]*num_nodes for i in range(self.num_nodes)]

        self.tau_0 = 1.0 / (self.num_nodes * 0.5 * self.average_delta())

    def delta(self, x, y):
        return self.delta_matrix[x][y]

    def tau(self, x, y):
        return self.tau_matrix[x][y]

    def etha(self, x, y):
        return 1.0 / self.delta(x, y)

    def update_tau(self, x, y, value):
        lock = Lock()
        lock.acquire()
        self.tau_matrix[x][y] = value
        lock.release()

    def reset_tau(self):
        lock = Lock()
        lock.acquire()
        avg = self.average_delta()

        self.tau_0 = 1.0 / (self.num_nodes * 0.5 * avg)

        for x in range(self.num_nodes):
            for y in range(self.num_nodes):
                self.tau_matrix[x][y] = self.tau_0
        lock.release()

    def average_tau(self):
        return average(self.tau_matrix)

    def update_delta(self, x, y, value):
        lock = Lock()
        lock.acqiure()
        self.delta_matrix[x][y] = value
        lock.release()

    def average_delta(self):
        return self.average(self.delta_matrix)

    def average(self, matrix):
        return sum(matrix[x][y] for x in range(self.num_nodes) for y in range(self.num_nodes)) / pow(self.num_nodes, 2)


class GraphException(Exception):
    """Specific AntGraph Exceptions"""
