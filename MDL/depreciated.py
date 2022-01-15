# class Tensor:
#    def __init__(self, shape=None, data=None):
#        #self.tensor = np.ndarray(shape=shape, dtype=dtype)
#        if data is None:
#            self.tensor = np.zeros(shape)
#        elif type(data) == np.ndarray:
#            self.tensor = data
#        else:
#            print(type(data))
#            raise ValueError
#
#    def dot(self, other):
#        return np.dot(self.tensor, other.tensor)
#    def __mul__(self, other):
#        return Tensor(data=np.dot(self.tensor, other.tensor))
#    def __add__(self, other):
#        return Tensor(data=(self.tensor+other.tensor))
#    def __repr__(self):
#        return str(self.tensor)


# class Layer:
#    def __init__(self, n_inputs, n_neurons):
#        self.size = (n_inputs, n_neurons)
#        self.weights = np.random.randn(n_inputs, n_neurons)
#        self.bias = np.zeros((1, n_neurons))

#    def __repr__(self):
#        return "Weights:\n{}\nBias:\n{}\n".format(self.weights, self.bias)

#    def forward(self, inputs):
#        self.output = np.dot(inputs, self.weights) + self.bias
#        return self.output

#    def lin_rect_act(self):
#        self.output_act = np.maximum(0, self.output)
#        return self.output_act

#    def sigmoid_act(self):
#        self.output_act = 1/(1+np.power(np.e, self.output))
#        return self.output_act

#    def mutate(self, intensity):
#        new = Layer(self.size[0], self.size[1])
#        new.weights = self.weights+.001*intensity*np.random.randn(self.size[0], self.size[1])
#        new.bias = self.bias+.001*intensity*np.random.randn(1, self.size[1])
#        return new
#

# class MaxPool:
#    def __init__(self, size_dims):
#        self.pool = np.array([np.array([np.array(0)]*size_dims[0])]*size_dims[1])

#    def forward(self, input):
#        for i in range(len(self.pool)):
#            for j in range(len(self.pool[i])):
#                self.pool[i][j] = max(input[i][j])
#        return self.pool


# class Convolution:
#    def __init__(self, size_dims, filter):
#        self.filter = filter
#        self.conv = np.array([np.array([np.array(0)]*(size_dims[0]-filter+1))]*(size_dims[1]-filter+1))

#    def forward(self, input):
#        for i in range(len(self.conv)):
#            for j in range(len(self.conv[i])):
#                for f in range(self.filter):
#                    for f2 in range(self.filter):
#                        self.conv[i][j] += input[i+f][j+f2]
#        return self.conv


#class NN:
#    def __init__(self, num_layers, sizes):
#        self.nl = num_layers
#        self.sizes = sizes
#        self.score = 0
#        if num_layers != len(sizes)-1:
#            raise ValueError
#        self.layers = [None]*num_layers
#        for i in range(num_layers):
#            self.layers[i] = Layer(sizes[i], sizes[i+1])

#    def __repr__(self):
#        return str(self.score)
#            #"Sizes:\n{}\nLayers:\n{}".format(self.sizes, self.layers)

#    def f_pass(self, inputs, how="lin_rect"):
#        if type(inputs) == pd.DataFrame:
#            self.output = inputs.values#np.array([inputs.values.tolist()]).T.tolist()
#        else:
#            self.output = inputs
#        for i in range(self.nl):
#            self.output = self.layers[i].forward(self.output)
#            if i < self.nl-1 and how == "sigmoid":
#                self.output = self.layers[i].sigmoid_act()
#            elif i < self.nl-1 and how == "lin_rect":
#                self.output = self.layers[i].lin_rect_act()
#        return self.output

#    def mutate(self, intensity):
#        new = NN(self.nl, self.sizes)
#        for i, layer in enumerate(self.layers):
#            new.layers[i] = layer.mutate(intensity)
#        return new

#    def updateScore(self, score):
#        self.score += score

#    def __lt__(self, other):
#        if self.score < other.score:
#            return other
#        return self

#    def to_series(self, score, code):
#        self.series = pd.Series(dtype=object)
#        self.series.loc["size"] = json.dumps(self.sizes)
#        self.series.loc["score"] = score
#        self.series.loc["code"] = code
#        for i, layer in enumerate(self.layers):
#            self.series.loc["Weights" + str(i)] = json.dumps(layer.weights.tolist())
#            self.series.loc["Bias" + str(i)] = json.dumps(layer.bias.tolist())
#        return self.series

#    def save(self, textfile, code=None):
#        s = self.to_series(self.score, code)
#        try:
#            df = pd.read_csv(textfile, index_col=0)
#        except pd.errors.EmptyDataError:
#            df = pd.DataFrame(columns=s.index)
#        except FileNotFoundError:
#            a = open(textfile, "w")
#            a.close()
#            df = pd.DataFrame(columns=s.index)
#        df.loc[len(df)] = s.transpose()
#        df.to_csv(textfile)


#class ConvNN:
#    def __init__(self, sizes):
#        self.sizes = sizes
#        self.score = 0
#        self.layers = [None]*(len(sizes)+1)
#        self.layers[0] = MaxPool([7, 6])
#        self.layers[1] = Convolution([7, 6], 3)
#        for i in range(len(sizes)-1):
#            self.layers[i+2] = Layer(sizes[i], sizes[i+1])

#    def __repr__(self):
#        return "Sizes:\n{}\nLayers:\n{}".format(self.sizes, self.layers)

#    def f_pass(self, inputs):
#        self.output = inputs
#        for i in range(len(self.layers)):
#            if i == 2:
#                self.output = self.output.flatten()
#            self.output = self.layers[i].forward(self.output)
#            if 2 <= i < len(self.layers)-1:
#                self.output = self.layers[i].lin_rect_act()
#        return self.output

#    def mutate(self, intensity):
#        new = ConvNN(self.sizes)
#        for i, layer in enumerate(self.layers):
#            if i>=2:
#                new.layers[i] = layer.mutate(intensity)
#        return new

#    def updateScore(self, score):
#        self.score += score

#    def __lt__(self, other):
#        if self.score < other.score:
#            return other
#        return self

#    def to_series(self, score, code):
#        self.series = pd.Series(dtype=object)
#        self.series.loc["size"] = json.dumps(self.sizes)
#        self.series.loc["score"] = score
#        self.series.loc["code"] = code
#        for i, layer in enumerate(self.layers):
#            if i >= 2:
#                self.series.loc["Weights" + str(i)] = json.dumps(layer.weights.tolist())
#                self.series.loc["Bias" + str(i)] = json.dumps(layer.bias.tolist())
#        return self.series

#    def save(self, textfile, code=None):
#        s = self.to_series(self.score, code)
#        try:
#            df = pd.read_csv(textfile, index_col=0)
#        except pd.errors.EmptyDataError:
#            df = pd.DataFrame(columns=s.index)
#        except FileNotFoundError:
#            a = open(textfile, "w")
#            a.close()
#            df = pd.DataFrame(columns=s.index)
#        df.loc[len(df)] = s.transpose()
#        df.to_csv(textfile)

#def loadBest(filename):
#    saved = pd.read_csv(filename, index_col=0)
#    saved.sort_values("score", inplace=True)
#    best = saved.iloc[0]
#    sizes = json.loads(best["size"])
#    new = NN(len(sizes)-1, sizes)
#    for i in range(len(sizes)-1):
#        new.layers[i].weights = np.array(json.loads(best["Weights"+str(i)]))
#        new.layers[i].bias = np.array(json.loads(best["Bias"+str(i)]))
#    return new

#def loadIndex(filename, index):
#    saved = pd.read_csv(filename, index_col=0)
#    best = saved.iloc[index]
#    layers = json.loads(best["size"])
#    new = NeuralNet(layers)
#    for i in range(len(sizes)-1):
#        new.layers[i].weights = np.array(json.loads(best["Weights"+str(i)]))
#        new.layers[i].bias = np.array(json.loads(best["Bias"+str(i)]))
#    return new


#a = NeuralNet([
#    Linear(4, 2),
#    Tanh()
#])
#a = pd.read_csv("new.csv")
#a.sort_values("code", inplace=True)
#b = NeuralNet([
#    Linear(4, 2),
#    Tanh
#])
#print(a.iloc[0])
#b.save("new.csv", 2)
#b.layers[0].params["w"] = np.array(json.loads(a.iloc[0]["Weights0"]))
#b.layers[0].params["b"] = np.array(json.loads(a.iloc[0]["Bias0"]))

#b.save("new.csv", 3)