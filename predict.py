import pickle
import numpy as np
import matplotlib.pyplot as plt

from analysis import Analysis

# Ground Truth
truth = [
    "雙手彎舉",
    "雙手交叉",
    "向左選取",
    "向右選取",
    "向左選取",
    "向右選取",
    "向左選取",
    "向左選取",
    "雙手彎舉",
    "雙手交叉",
    "雙手交叉",
    "雙手彎舉",
]

pickle_in = open('points.pickle', 'rb')
points = pickle.load(pickle_in)

left_x_gradients = []
left_y_gradients = []
left_distances = []

right_x_gradients = []
right_y_gradients = []
right_distance = []

c = 0
analysis = Analysis()
for i, point in enumerate(points):
    analysis.load(point)
    behavior = analysis.predict(point)
    if behavior != "":
        print(behavior)
        if (behavior != truth[c]):
            print("Wrong!!")
        c += 1

    # if i > 900:
    #     break
