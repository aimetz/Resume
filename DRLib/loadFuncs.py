import pandas as pd
from DRLib.NN import NN
import numpy as np
import json


def loadBest(filename):
    saved = pd.read_csv("DRLib/"+filename, index_col=0)
    saved.sort_values("score", inplace=True)
    best = saved.iloc[0]
    sizes = json.loads(best["size"])
    new = NN(len(sizes)-1, sizes)
    for i in range(len(sizes)-1):
        new.layers[i].weights = np.array(json.loads(best["Weights"+str(i)]))
        new.layers[i].bias = np.array(json.loads(best["Bias"+str(i)]))
    return new


def loadIndex(filename, index):
    saved = pd.read_csv("DRLib/"+filename, index_col=0)
    best = saved.iloc[index]
    sizes = json.loads(best["size"])
    new = NN(len(sizes)-1, sizes)
    for i in range(len(sizes)-1):
        new.layers[i].weights = np.array(json.loads(best["Weights"+str(i)]))
        new.layers[i].bias = np.array(json.loads(best["Bias"+str(i)]))
    return new