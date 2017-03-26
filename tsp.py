import sys

from ant_colony import AntColony
from ant_graph import AntGraph, GraphException
from ant import Ant, AntException

GRAPH_STRING = "{(A,B,100),(B,C,200),(C,A,1000),(D,B,500),(D,C,200)}"
ANTS = 20
ITERATIONS = 5
REPETITIONS = 1
START_CITY = 0


def main(ants, iterations, repetitions):
    graph_tuples = [s.split(',') for s in GRAPH_STRING.strip('{()}').split('),(')]
    #graph_tuples = [s.split(',') for s in raw_input().strip('{()}').split('),(')]
    cities, cost_matrix = build_matrix(graph_tuples)

    if all(map(lambda c: len(c) != len(cost_matrix), cost_matrix)):
        raise GraphException("There exists a city with no path to it")

    graph = AntGraph(len(cost_matrix), cost_matrix)
    best_path_cost = sys.maxint
    best_path = []
    lowest_cost = sys.maxint
    for i in range(repetitions):
        graph.reset_tau()
        ant_colony = AntColony(graph, ants, iterations)
        ant_colony.colonize()
        if ant_colony.lowest_cost < best_path_cost:
            best_path = ant_colony.best_path
            lowest_cost = ant_colony.lowest_cost
    best_path += [best_path[0]]

    if best_path and lowest_cost != sys.maxint:
        print_path = str(tuple([cities[city] for city in best_path]))
        print "{%s, %s}" % (print_path, lowest_cost)
    else:
        print "No solution"


def build_matrix(tuples):
    matrix_dict = {}
    cities = []

    for each in tuples:
        if each[0] not in cities:
            cities.append(each[0])
            matrix_dict[each[0]] = {}
        if each[1] not in cities:
            cities.append(each[1])
            matrix_dict[each[1]] = {}

        matrix_dict[each[0]][each[1]] = int(each[2])
        matrix_dict[each[1]][each[0]] = int(each[2])

    return cities, [[matrix_dict[city].get(key, sys.maxint) for key in cities] for city in cities]


if __name__ == "__main__":
    try:
        main(ANTS, ITERATIONS, REPETITIONS)
        sys.exit(0)
    except AntException as ae:
        print "Exception caught in Ant object: {0}".format(ae.args[0])
        raise
    except GraphException as ge:
        print "Exception caught in Graph object: {0}".format(ge.args[0])
        raise
    except Exception:
        print "Unexpected {0}: {1}".format(sys.exc_info()[0].__name__, sys.exc_info()[1])
        raise
