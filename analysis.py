import numpy as np


class Template(object):
    def __init__(self, tool):
        self.behavior = ""
        self.tool = tool
        self.close = 70
        self.button = False
        self.features = []

        self.scope = 10
        self.start = 0
        self.end = self.start + self.scope

    def analyze(self):
        data = self.tool.data
        self.features.append(data)
        if self.enough_data():
            self.behavior = self.render_state(data)
        return self.behavior

    def enough_data(self):
        return len(self.features) > self.scope

    def cut_interval(self):
        feature = self.features[self.start:self.end]
        left_distance = [f[0][2] for f in feature]
        right_distance = [f[1][2] for f in feature]
        left_gradient = self.calcGradient(left_distance)
        right_gradient = self.calcGradient(right_distance)
        self.start += 1
        self.end = self.start + self.scope
        return left_gradient, right_gradient

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
        past = feature[0]
        pos, neg = 0, 0
        for future in feature[1:]:
            diff = (future - past)
            if diff > 0:
                pos += diff
            elif diff < 0:
                neg += diff
        return pos, abs(neg)


class NoAction(Template):
    def __init__(self, tool):
        super().__init__(tool)
        self.change_state_thres = 70

    def render_state(self, data):
        left_gradient, right_gradient = self.cut_interval()
        left_distance, right_distance = data[0][2], data[1][2]
        left_hand_moved = left_distance > self.change_state_thres
        right_hand_moved = right_distance > self.change_state_thres
        proportion = left_gradient / (left_gradient + right_gradient)
        up = 0.1 < proportion and proportion < 0.9
        if left_hand_moved or right_hand_moved:
            if proportion > 0.9:
                self.tool.change(LeftHandsUp(self.tool))
            elif proportion > 0.1:
                self.tool.change(BothHandsUp(self.tool))
            else:
                self.tool.change(RightHandsUp(self.tool))
        return self.behavior


class RightHandsUp(Template):
    def __init__(self, tool):
        super().__init__(tool)

    def render_state(self, data):
        left_gradient, right_gradient = self.cut_interval()
        left_distance, right_distance = data[0][2], data[1][2]
        down = right_gradient < 0
        close_record = right_distance < self.close
        if down and close_record:
            self.behavior = self.predict()
            self.tool.change(NoAction(self.tool))
        return self.behavior

    def predict(self):
        left_gradient_x = [f[0][0] for f in self.features]
        left_gradient_y = [f[0][1] for f in self.features]
        right_gradient_x = [f[1][0] for f in self.features]
        right_gradient_y = [f[1][1] for f in self.features]
        pos, neg = self.calcPosNegGradient(right_gradient_x)
        if pos > neg:
            return "向左選取"
        else:
            return "向右選取"


class LeftHandsUp(Template):
    def __init__(self, tool):
        super().__init__(tool)

    def render_state(self, data):
        left_gradient, right_gradient = self.cut_interval()
        left_distance, right_distance = data[0][2], data[1][2]
        down = left_gradient < 0
        close_record = left_distance < self.close
        if down and close_record:
            self.behavior = self.predict()
            self.tool.change(NoAction(self.tool))
        return self.behavior

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
        left_gradient, right_gradient = self.cut_interval()
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
        if mean_x > self.click_cancel_param:
            return "雙手交叉"
        else:
            return "雙手彎舉"


class Analysis(object):
    def __init__(self):
        self.temp = None
        self.state = NoAction(self)

    def load(self, points):
        if self.temp is None:
            self.temp = points

    def load_data(self, data):
        self.data = data

    def change(self, state):
        self.state = state

    def predict(self, points):
        if self.temp is None:
            return ""
        self.calcPast(points)
        return self.state.analyze()

    def calcPast(self, points):
        left_wrist_x_temp = self.temp["left_wrist_x"]
        right_wrist_x_temp = self.temp["right_wrist_x"]
        left_wrist_y_temp = self.temp["left_wrist_y"]
        right_wrist_y_temp = self.temp["right_wrist_y"]

        left_wrist_x = points["left_wrist_x"]
        right_wrist_x = points["right_wrist_x"]
        left_wrist_y = points["left_wrist_y"]
        right_wrist_y = points["right_wrist_y"]

        left_gradient_x = (left_wrist_x - left_wrist_x_temp)
        right_gradient_x = (right_wrist_x - right_wrist_x_temp)

        left_gradient_y = (left_wrist_y - left_wrist_y_temp)
        right_gradient_y = (right_wrist_y - right_wrist_y_temp)

        left_distance = np.sqrt(left_gradient_x ** 2 + left_gradient_y ** 2)
        right_distance = np.sqrt(right_gradient_x ** 2 + right_gradient_y ** 2)

        self.load_data([
            [left_gradient_x, left_gradient_y, left_distance],
            [right_gradient_x, right_gradient_y, right_distance]
        ])
