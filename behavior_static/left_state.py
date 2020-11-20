import numpy as np


class Open(object):
    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, points, face):
        x1 = points["left_shoulder_x"]
        y1 = points["left_shoulder_y"]
        x2 = points["left_wrist_x"]
        y2 = points["left_wrist_y"]
        x3 = points["left_elbow_x"]
        y3 = points["left_elbow_y"]
        angle1 = self.cal_angle(x1, y1, x2, y2)
        angle2 = self.cal_angle(x1, y1, x3, y3)
        angle3 = self.cal_angle(x2, y2, x3, y3)

        left = self.check_left(angle1, angle2, angle3)

        dist1 = self.analysis.norm(x1, y1, x3, y3)
        dist2 = self.analysis.norm(x2, y2, x3, y3)
        dist = self.analysis.norm(x2, y2, x1, y1)
        thres = (dist1 + dist2) - 10

        _, y = self.analysis.calc_left_thres(points, 2)
        diff = y - y2
        if diff < -10 or dist > thres:
            self.analysis.change_left_state(LeftClose(self.analysis))

        return "" or left

    def cal_angle(self, x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        return np.arctan2(dy, dx) / np.pi * 180

    def check_left(self, angle1, angle2, angle3):
        c1 = 140 < abs(angle1) and abs(angle1) < 200
        c2 = 140 < abs(angle2) and abs(angle2) < 200
        c3 = 0 < abs(angle3) and abs(angle3) < 40
        if (c1 and c2 and c3):
            return "取消"

    def change(self, new_state):
        self.state = new_state


class LeftClose(object):
    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, points, face):
        x1 = points["left_wrist_x"]
        y1 = points["left_wrist_y"]
        x2 = points["left_shoulder_x"]
        y2 = points["left_shoulder_y"]
        dist = self.analysis.norm(x1, y1, x2, y2)
        if dist < 40:
            self.analysis.change_left_state(Open(self.analysis))
        return ""
