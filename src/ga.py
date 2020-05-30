import random
from copy import deepcopy
from time import time

from rbfn import RBFN
from dataset import Dataset


class GA():
    def __init__(self, iteration_times=10000, populations_size=50, 
                 mutation_prob=0.3, crossover_prob=0.8, J=8, 
                 input_dim=5, dataset_path='../data/train6dAll.txt'):
        self.iteration_times = iteration_times
        self.populations_size = populations_size
        self.mutation_prob = mutation_prob
        self.crossover_prob = crossover_prob
        self.J = J
        self.input_dim = input_dim
        self.dataset_path = dataset_path
        self.cross_mask = None
        self.mutation_mask = None
        self.cross_select_prob = 0.5
        self.mutation_select_prob = 0.5
        self.populations = []
        self.fitness = []
        self.best_size = int(self.populations_size/2)
        self.dataset = Dataset(self.dataset_path)
        self.model = RBFN(J=self.J, input_dim=self.input_dim)
        self.best_f = 10000000
        self.start_time = time()

        for _ in range(populations_size):
            r = RBFN(J=self.J, input_dim=self.input_dim)
            f = r.eval(self.dataset.get())
            theta, neurals = r.get_params()
            self.populations.append(RBFN.params2flatten(theta, neurals))
            self.fitness.append(f)

    def roulette(self):
        fitness = g.fitness
        min_fit = min(fitness)
        if min_fit < 0:
            fitness = [fit - min_fit + 1 for fit in fitness]
        posibility = [fit/sum(fitness) for fit in fitness]
        total_posibility = [sum(posibility[:i+1])
                            for i in range(len(posibility))]
        rand = random.random()
        for i, v in enumerate(total_posibility):
            if rand < v:
                return i

    def eval_fitness(self):
        self.fitness = []
        r = RBFN(J=self.J, input_dim=self.input_dim)
        for i in range(self.populations_size):
            theta, neurals = RBFN.flatten2params(
                self.populations[i], self.input_dim)
            # print(neurals)
            r.set_params(theta, neurals)
            f = r.eval(self.dataset.get())
            self.fitness.append(f)

    def select(self):
        next_gen_populations = []
        # keep the best one * 2
        best = deepcopy(
            self.populations[self.fitness.index(min(self.fitness))])
        for _ in range(self.best_size):
            next_gen_populations.append(deepcopy(best))
        theta, neurals = RBFN.flatten2params(best, self.input_dim)
        self.model.set_params(theta, neurals)
        if min(self.fitness) < self.best_f:
            self.model.save()
            self.best_f = min(self.fitness)
        for _ in range(self.populations_size-self.best_size):
            # next_gen_populations.append(
            #    deepcopy(self.populations[self.roulette()]))
            picked = random.sample(self.populations, 2)
            for p in picked:
                next_gen_populations.append(
                    deepcopy(p))
        random.shuffle(next_gen_populations)
        self.populations = next_gen_populations

    def gen_cross_mask(self, force=False):
        if self.cross_mask is None or force:
            cross_mask = []
            for _ in range(len(self.populations[0])):
                rand = random.random()
                if rand < self.cross_select_prob:
                    cross_mask.append(True)
                else:
                    cross_mask.append(False)
            self.cross_mask = cross_mask
            #print("generate cross mask")
            # print(self.cross_mask)

    def crossover(self):
        self.gen_cross_mask()
        for i in range(int(self.populations_size/2)):
            self.gen_cross_mask(True)
            rand = random.random()
            if rand < self.crossover_prob:
                self.cross(self.populations[i*2], self.populations[i*2+1])

                # for j in range(len(self.populations[0])):
                #    if self.cross_mask[j]:
                #        temp = self.populations[i*2][j]
                #        self.populations[i*2][j] = self.populations[i*2+1][j]
                #        self.populations[i*2+1][j] = temp

    def cross(self, a, b):
        ratio = (random.random() - 0.5) * 2 * self.crossover_prob
        aa = deepcopy(a)
        bb = deepcopy(b)
        for i in range(len(a)):
            aa[i] = a[i] + ratio * (a[i] - b[i])
            bb[i] = b[i] - ratio * (a[i] - b[i])
        return aa, bb

    def gen_mutation_mask(self, force=True):
        if self.mutation_mask is None or force:
            mutation_mask = []
            for _ in range(len(self.populations[0])):
                rand = random.random()
                if rand < self.mutation_select_prob:
                    mutation_mask.append(True)
                else:
                    mutation_mask.append(False)
            self.mutation_mask = mutation_mask
            #print("generate mutation mask")
            # print(self.mutation_mask)

    def mutation(self):
        # self.gen_mutation_mask()
        for i in range(int(self.populations_size)):
            rand = random.random()
            # if rand < self.mutation_prob:
            # print("YYYYYYYYYYYY")
            # self.gen_mutation_mask(True)
            # print(self.mutation_mask)
            # print(self.populations[i])

            for j in range(len(self.populations[0])):
                rand = random.random()
                if rand < self.mutation_prob:
                    self.populations[i][j] = self.mutate(
                        self.populations[i][j])
                # if self.mutation_mask[j]:
                #    if (j-1)%(self.input_dim+2) == 0:
                #        self.populations[i][j] = random.uniform(0, 1)
                #    elif (j-1)%(self.input_dim+2) == self.input_dim+1:
                #        self.populations[i][j] = random.uniform(-1, 1)
                #    else:
                #        self.populations[i][j] = random.uniform(0, 40)
            # print(self.populations[i])

    def mutate(self, v):
        ratio = (random.random() - 0.5) * 2 * 0.5
        result = v + v * ratio
        return result

    def train(self):
        for epoch in range(self.iteration_times):
            self.eval_fitness()
            print("time(sec):{} epoch-{} Best fitness = {}, averag fitness = {}".format(
                int(time()-self.start_time), epoch, self.best_f, sum(self.fitness)/self.populations_size))
            #print(list(map(lambda x: int(x), self.fitness)))
            self.select()
            self.crossover()
            self.mutation()


if __name__ == "__main__":

    g = GA()
    g.train()
    '''
    m = 10000
    dataset = Dataset('../data/train4dAll.txt')
    while True:
        r = RBFN(J=3, input_dim=3)
        f = r.eval(dataset.get())
        if f < m:
            m = f
            r.save()
        print("min: {}".format(m))
    '''
    '''
    g = GA()
    print(len(g.populations))
    t = {}
    for i in range(100):
        r = g.roulette()
        if r not in t:
            t[r] = 1
        else:
            t[r] += 1
    print(t)
    '''
