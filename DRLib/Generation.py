from DRLib.NN import *

class Generation:
    def __init__(self, population, sizes, initial=False):
        if initial:
            NNs = [None] * population
            for i in range(population):
                NNs[i] = NN(len(sizes)-1, sizes)
            self.pop = NNs
            self.done = np.array([None] * population)
            self.scores = np.zeros(population)

        else:
            self.pop = np.array(population)
            self.done = np.array([None] * len(population))
            self.scores = np.zeros(len(population))

        self.sizes = sizes


    def f_pass(self, data, label=None, how="lin_rect"):
        size = len(self.pop)
        y_ = [None] * size
        errors = [None] * size
        for i in range(size):
            if self.pop[i] is not None:
                y_[i] = self.pop[i].f_pass(data, how=how)
                if label is not None:
                    errors[i] = np.sqrt((label - y_[i].T[0])**2).mean()
        if label is not None:
            self.errors = pd.Series(errors).sort_values()
        return y_

    def f_pass_sep_inputs(self, data, label=None, how="lin_rect"):
        size = len(self.pop)
        y_ = [None] * size
        for i in range(size):
            if self.pop[i] is not None:
                y_[i] = self.pop[i].f_pass(data[i], how=how)
        return y_

    def update_score(self, scores):
        self.scores += scores


    def next_gen(self):
        survivors = 3
        # best = self.errors.index.tolist()[:survivors]
        scores = pd.Series(self.scores).sort_values()
        print(scores[:10])
        best = scores.index.tolist()[:survivors]
        next_gen = [None]*survivors*201
        #outfile = open("saved.txt", "a")
        #outfile.write(str(self.pop[best[0]]))
        #outfile.write(str(scores.iloc[0])+"\n\n")
        #outfile.close()
        for i, index in enumerate(best):
            next_gen[i] = self.pop[index]
            self.pop[i].save("saved.csv", score = self.scores[i])
            for ten in range(100):
                if i<2:
                    for q in range(2):
                        next_gen[i*200+ten*2+q+3] = self.pop[index].mutate(ten)
                else:
                    next_gen[i*200+ten*2+3] = self.pop[index].mutate(ten)
                    next_gen[i*200+ten*2+4] = NN(len(self.sizes)-1, self.sizes)
        g = Generation(next_gen, self.sizes)
        g.sizes = self.sizes
        return g

    def next_gen_by_index(self, imax):
        next_gen = [None]*500
        next_gen[0] = self.done[imax]

        for i in range(1, 500, 4):
            for j in range(3):
                next_gen[i+j] = self.done[imax].mutate(i/400)
            next_gen[i+j] = NN(len(self.sizes)-1, self.sizes)
        g = Generation(next_gen, self.sizes)
        return g