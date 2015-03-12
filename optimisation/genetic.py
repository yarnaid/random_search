import numpy as np
import bisect
import copy
__author__ = 'yarnaid'


def run(init_population, fitness, limits, max_iter=100, mutate_p=0.1,
        retain=0.3):
    best_x = [init_population[0]]
    best_score = [fitness(best_x[0])]
    population = init_population
    f_key = lambda xx: xx[1]
    for x in xrange(max_iter):
        population = evolve(population, fitness, limits, mutate_p, retain)
        fitnesses = [(p, fitness(p)) for p in population]
        fitnesses.sort(key=f_key)
        print [f_key(f) for f in fitnesses]
        if fitnesses[-1][1] > best_score[-1]:
            best_res = fitnesses[-1]
            best_x.append(best_res[0])
            best_score.append(best_res[1])
    return best_x, best_score


def evolve(parents, fitness, limits, mutate_p, retain):
    key = lambda x: fitness(x)
    parents.sort(key=key)
    children = parents[int(len(parents) * (1 - retain)):]
    wrg = WeightedRandomGenerator(grade(parents, fitness))
    max_iter = len(parents) * 10
    while len(children) < len(parents):
        male = parents[wrg()]
        female = parents[wrg()]
        max_iter -= 1
        if np.any(male != female) or max_iter < 0:
            half = np.random.randint(
                0, len(parents[0]) - 1) if len(parents[0]) > 2 else 0
            child = list(male[:half]) + list(female[half:])
            children.append(child)
    for i in xrange(len(children)):
        if np.random.random() < mutate_p:
            children[i] = mutate(children[i], limits)
    children.sort(key=key)
    return children


def mutate(genome, limits):
    res = copy.deepcopy(genome)
    pos_to_mutate = np.random.randint(0, len(genome))
    lims = limits[pos_to_mutate]
    new_value = lims[0] + np.random.random() * lims[1]
    res[pos_to_mutate] = new_value
    return res


class WeightedRandomGenerator(object):

    def __init__(self, weights):
        self.totals = []
        running_total = 0

        for w in weights:
            running_total += w
            self.totals.append(running_total)

    def next(self):
        rnd = np.random.random() * self.totals[-1]
        return bisect.bisect_right(self.totals, rnd)

    def __call__(self):
        return self.next()


def grade(population, fitness):
    full_fitness = np.sum([fitness(p) for p in population])
    return [fitness(p) / full_fitness for p in population]
