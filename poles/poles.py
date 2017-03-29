#!/bin/python


class Memoize:
    def __init__(self, f, n, poles):
        self.f = f
        self.n = n
        self.memo = [[None]*n for _ in range(n)]
        self.poles = dict((tuple(each), i) for (i, each) in enumerate(poles))

    def __call__(self, poles):
        index_0 = self.poles[tuple(poles[0])]
        index_1 = self.poles[tuple(poles[-1])]
        if not self.memo[index_0][index_1]:
            self.memo[index_0][index_1] = self.f(poles)
        return self.memo[index_0][index_1]


def cost_fn(poles):
    cost = 0
    for pole in poles[1:]:
        cost += pole[1] * (pole[0] - poles[0][0])
    return cost


def min_cost(k, poles):
    if k == 1:
        return cost_fn(poles)
    else:
        if len(poles) == 1:
            return 0
        return min(map(lambda (x, y): min_cost(1, x) + min_cost(k-1, y), [(poles[0:i], poles[i:]) for i in range(1, len(poles))]))


if __name__ == "__main__":
    n, k = map(int, raw_input().strip().split(' '))
    poles = []
    for a0 in xrange(n):
        poles.append(map(int, raw_input().strip().split(' ')))
    cost_fn = Memoize(cost_fn, n, poles)
    print min_cost(k, poles)