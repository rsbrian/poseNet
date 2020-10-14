import pickle
import numpy as np
import matplotlib.pyplot as plt

from analysis import Analysis
analysis = Analysis()

pickle_in = open('points.pickle', 'rb')
points = pickle.load(pickle_in)

left_gradients_x = []
right_gradients_x = []
left_gradients_y = []
right_gradients_y = []

directions_left = []
directions_right = []

angles_right = []

sum_of_right_gradient_x = 0
sum_of_right_gradient_y = 0
sum_of_right_gradients_x = []
sum_of_right_gradients_y = []

xx = []
yy = []

temp = points[0]
for i, point in enumerate(points[1:]):
    left_wrist_x_temp = temp["left_wrist_x"]
    right_wrist_x_temp = temp["right_wrist_x"]
    left_wrist_y_temp = temp["left_wrist_y"]
    right_wrist_y_temp = temp["right_wrist_y"]

    left_wrist_x = point["left_wrist_x"]
    right_wrist_x = point["right_wrist_x"]
    left_wrist_y = point["left_wrist_y"]
    right_wrist_y = point["right_wrist_y"]

    left_gradient_x = (left_wrist_x - left_wrist_x_temp)
    right_gradient_x = (right_wrist_x - right_wrist_x_temp)
    left_gradient_y = (left_wrist_y - left_wrist_y_temp)
    right_gradient_y = (right_wrist_y - right_wrist_y_temp)
    left_distance = np.sqrt(left_gradient_x ** 2 + left_gradient_y ** 2)
    right_distance = np.sqrt(right_gradient_x ** 2 + right_gradient_y ** 2)

    sum_of_right_gradient_x += right_gradient_x
    sum_of_right_gradient_y += right_gradient_y

    left_gradients_x.append(left_gradient_x)
    right_gradients_x.append(right_gradient_x)
    left_gradients_y.append(left_gradient_y)
    right_gradients_y.append(right_gradient_y)

    directions_left.append(left_distance)
    directions_right.append(right_distance)

    if right_gradient_x == 0:
        sum_of_right_gradient_x = 0
    if right_gradient_y > 30:
        sum_of_right_gradient_y = 0

    sum_of_right_gradients_x.append(sum_of_right_gradient_x)
    sum_of_right_gradients_y.append(sum_of_right_gradient_y)

    angle_right = np.degrees(np.arctan2(right_gradient_x, -right_gradient_y))
    angles_right.append(angle_right)

    analysis.load_data([
        [left_gradient_x, left_gradient_y, left_distance],
        [right_gradient_x, right_gradient_y, right_distance]
    ])
    behavior = analysis.predict()
    name = analysis.state.__class__.__name__
    if name != "NoAction":
        xx.append(i)
        if name == "LeftHandsUp":
            yy.append(left_distance)
        # elif name == "RightHandsUp":
        #     yy.append(right_distance)
        else:
            yy.append(right_distance)

x = np.arange(len(left_gradients_x))
y1 = left_gradients_x
y2 = right_gradients_x
y3 = left_gradients_y
y4 = right_gradients_y
y5 = directions_left
y6 = directions_right
y7 = angles_right

y8 = sum_of_right_gradients_x
y9 = sum_of_right_gradients_y

plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)
plt.plot(x, y4)
plt.plot(x, y5)
plt.plot(x, y6)
plt.scatter(xx, yy)
# plt.plot(x, y7)
# plt.plot(x, y8)
# plt.plot(x, y9)
plt.show()
