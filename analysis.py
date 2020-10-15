import copy
import numpy as np


class Template(object):
    def __init__(self, tool):
        self.behavior = ""
        self.tool = tool
        self.features = []

        self.close = 70
        self.change_state_thres = 70
        self.scope = 10

    def analyze(self):
        data = self.tool.data
        self.features.append(data)
        if self.enough_data():
            self.features = self.features[1:]
            self.behavior = self.render_state(data)
        return self.behavior

    def enough_data(self):
        return len(self.features) > self.scope

    def cut_interval(self):
        left_distance = [f[0][2] for f in self.features]
        right_distance = [f[1][2] for f in self.features]
        left_y = [f[0][1] for f in self.features]
        right_y = [f[1][1] for f in self.features]
        left_gradient = self.calcGradient(left_distance)
        right_gradient = self.calcGradient(right_distance)
        left_y = self.calcGradient(left_y)
        right_y = self.calcGradient(right_y)
        return left_gradient, right_gradient, left_y, right_y

    def calcGradient(self, feature):
        past = feature[0]
        sum_of_gradient = 0
        for future in feature[1:]:
            diff = (future - past)
            sum_of_gradient += diff
            past = future
        return sum_of_gradient

    def calcMean(self, A, B):
        return (abs(A) + abs(B)) / 2

    def calcPosNegGradient(self, feature):
        pos, neg = 0, 0
        for f in feature:
            if f < 0:
                neg += f
            elif f > 0:
                pos += f
        neg = abs(neg)
        return pos, neg


class NoAction(Template):
    def __init__(self, tool):
        super().__init__(tool)

    def render_state(self, data):
        thres = self.tool.dynamic_thres_by_camera * 10
        left_gradient, right_gradient, left_y, right_y = self.cut_interval()
        left_distance, right_distance = data[0][2], data[1][2]
        left_hand_moved = left_distance > thres
        right_hand_moved = right_distance > thres

        if (left_gradient + right_gradient) == 0:
            return self.behavior
        proportion = abs(left_gradient) / \
            (abs(left_gradient) + abs(right_gradient))

        if left_hand_moved or right_hand_moved:
            if proportion < 0.3 and right_y < 0:
                self.tool.change(RightHandsUp(self.tool, right_distance))
            elif proportion < 0.7 and left_y < 0 and right_y < 0:
                self.tool.change(BothHandsUp(self.tool))
            elif left_y < 0:
                self.tool.change(LeftHandsUp(self.tool, left_distance))

        return self.behavior


class RightHandsUp(Template):
    def __init__(self, tool, right_distance):
        super().__init__(tool)
        self.stop_record = right_distance / 3

    def render_state(self, data):
        left_gradient, right_gradient, left_y, right_y = self.cut_interval()
        finished = right_gradient > -self.stop_record
        if len(self.features) > 50:
            self.tool.change(NoAction(self.tool))

        if finished:
            self.behavior = self.predict()
            self.tool.change(NoAction(self.tool))
        return self.behavior

    def predict(self):
        left_gradient_x = [f[0][0] for f in self.features]
        left_gradient_y = [f[0][1] for f in self.features]
        right_gradient_x = [f[1][0] for f in self.features]
        right_gradient_y = [f[1][1] for f in self.features]
        pos, neg = self.calcPosNegGradient(right_gradient_x)
        print(pos, neg)
        if pos > neg:
            return "向左選取"
        else:
            return "向右選取"


class LeftHandsUp(Template):
    def __init__(self, tool, left_distance):
        super().__init__(tool)
        self.stop_record = left_distance / 3

    def render_state(self, data):
        left_gradient, right_gradient, left_y, right_y = self.cut_interval()
        finished = left_gradient > -self.stop_record
        if len(self.features) > 50:
            self.tool.change(NoAction(self.tool))

        if finished:
            self.behavior = self.predict()
            self.tool.change(NoAction(self.tool))
        return self.behavior
        # left_distance, right_distance = data[0][2], data[1][2]
        # down = left_gradient < 0
        # close_record = left_distance < self.close
        # if down and close_record:
        #     self.behavior = self.predict()
        #     self.tool.change(NoAction(self.tool))
        # return self.behavior

    def predict(self):
        left_gradient_x = [f[0][0] for f in self.features]
        left_gradient_y = [f[0][1] for f in self.features]
        right_gradient_x = [f[1][0] for f in self.features]
        right_gradient_y = [f[1][1] for f in self.features]
        pos, neg = self.calcPosNegGradient(left_gradient_x)
        if pos > neg:
            return "向左選取"
        else:
            return "向右選取"


class BothHandsUp(Template):
    def __init__(self, tool):
        super().__init__(tool)
        self.click_cancel_param = 30  # Above ${param} means cancel

    def render_state(self, data):
        left_gradient, right_gradient, left_y, right_y = self.cut_interval()
        left_distance, right_distance = data[0][2], data[1][2]
        down = left_gradient < 0 and right_gradient < 0
        close_record = left_distance < self.close and right_distance < self.close
        if down and close_record:
            self.behavior = self.predict()
            self.tool.change(NoAction(self.tool))
        return self.behavior

    def predict(self):
        left_gradient_x = [f[0][0] for f in self.features]
        left_gradient_y = [f[0][1] for f in self.features]
        right_gradient_x = [f[1][0] for f in self.features]
        right_gradient_y = [f[1][1] for f in self.features]
        left_mean_x = np.mean(left_gradient_x)
        left_mean_y = np.mean(left_gradient_y)
        right_mean_x = np.mean(right_gradient_x)
        right_mean_y = np.mean(right_gradient_y)
        mean_x = self.calcMean(left_mean_x, right_mean_x)
        mean_y = self.calcMean(left_mean_y, right_mean_y)
        left_g = self.calcGradient(left_gradient_x)
        right_g = self.calcGradient(right_gradient_x)
        print(left_g, right_g)
        if mean_x > self.click_cancel_param:
            return "雙手交叉"
        else:
            return "雙手彎舉"


class Analysis(object):
    def __init__(self):
        self.temp = []
        self.state = NoAction(self)
        self.dynamic_thres_by_camera = None

    def load_data(self, data):
        self.data = data

    def change(self, state):
        self.state = state

    def predict(self, points, face):
        if len(self.temp) == 0 or len(points) == 0 or face[0] is None:
            self.temp = copy.deepcopy(points)
            return ""
        name = self.state.__class__.__name__
        if (name != "NoAction"):
            print(name)
        self.calcPast(points, face)
        return self.state.analyze()

    def calcPast(self, points, face):
        left_wrist_x_temp = self.temp["left_wrist_x"]
        right_wrist_x_temp = self.temp["right_wrist_x"]
        left_wrist_y_temp = self.temp["left_wrist_y"]
        right_wrist_y_temp = self.temp["right_wrist_y"]

        left_wrist_x = points["left_wrist_x"]
        right_wrist_x = points["right_wrist_x"]
        left_wrist_y = points["left_wrist_y"]
        right_wrist_y = points["right_wrist_y"]

        minimum_y = face[1]
        maximum_y = max(points["left_knee_y"], points["right_knee_y"])
        # print(round(maximum_y / minimum_y, 2))
        self.dynamic_thres_by_camera = maximum_y / minimum_y

        left_gradient_x = (left_wrist_x - left_wrist_x_temp)
        right_gradient_x = (right_wrist_x - right_wrist_x_temp)

        left_gradient_y = (left_wrist_y - left_wrist_y_temp)
        right_gradient_y = (right_wrist_y - right_wrist_y_temp)

        left_distance = np.sqrt(left_gradient_x ** 2 + left_gradient_y ** 2)
        right_distance = np.sqrt(right_gradient_x ** 2 + right_gradient_y ** 2)

        self.temp = copy.deepcopy(points)

        self.load_data([
            [left_gradient_x, left_gradient_y, left_distance],
            [right_gradient_x, right_gradient_y, right_distance]
        ])
