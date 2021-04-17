from DRLib.Layer import *
import pandas as pd
import json


class NN:
    def __init__(self, num_layers, sizes):
        self.nl = num_layers
        self.sizes = sizes
        if num_layers != len(sizes)-1:
            raise ValueError
        self.layers = [None]*num_layers
        for i in range(num_layers):
            self.layers[i] = Layer(int(sizes[i]), int(sizes[i+1]))

    def __repr__(self):
        ret =  "Sizes:\n{}\nLayers:\n".format(self.sizes)
        for layer in self.layers:
            ret += str(layer)
        return ret

    def f_pass(self, inputs, how="lin_rect"):
        if type(inputs) == pd.DataFrame:
            self.output = inputs.values#np.array([inputs.values.tolist()]).T.tolist()
        else:
            self.output = inputs
        for i in range(self.nl):
            self.output = self.layers[i].forward(self.output)
            if i < self.nl-1 and how == "sigmoid":
                self.output = self.layers[i].sigmoid_act()
            elif i < self.nl-1 and how == "lin_rect":
                self.output = self.layers[i].lin_rect_act()
        return self.output

    def mutate(self, intensity):
        new = NN(self.nl, self.sizes)
        for i, layer in enumerate(self.layers):
            new.layers[i] = layer.mutate(intensity)
        return new

    def to_series(self, score, code):
        self.series = pd.Series(dtype=object)
        self.series.loc["size"] = json.dumps(self.sizes)
        self.series.loc["score"] = score
        self.series.loc["code"] = code

        for i, layer in enumerate(self.layers):
            self.series.loc["Weights" + str(i)] = json.dumps(layer.weights.tolist())
            self.series.loc["Bias" + str(i)] = json.dumps(layer.bias.tolist())
        return self.series

    def save(self, textfile, score=None, code=None):
        # outfile = open(textfile, "a")
        # outfile.write("\n\n@")
        # if code is not None:
        #     outfile.write("\ncode: "+str(code)+"\n")
        # if score is not None:
        #     outfile.write("\nscore: "+str(score)+"\n")
        # outfile.write(str(self))
        # outfile.write("#")
        # outfile.close()
        s = self.to_series(score, code)
        try:
            df = pd.read_csv("DRLib."+textfile, index_col=0)
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=s.index)
        except FileNotFoundError:
            a = open("DRLib."+textfile, "w")
            a.close()
            df = pd.DataFrame(columns=s.index)
        df.loc[len(df)] = s.transpose()
        df.to_csv(textfile)
