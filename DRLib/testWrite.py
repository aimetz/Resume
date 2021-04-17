from DRLib.NN import NN
import pandas as pd
a = NN(2, [1, 2, 1])

# print(a)
b = [123, 435, 235, 235, 325, 52354, -18263, 63345]
for num in b:
    a.save("new.csv", score=num)
print(pd.read_csv("new.csv", index_col=0).sort_values("score"))