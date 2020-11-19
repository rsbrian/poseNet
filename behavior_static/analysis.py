import cv2
import copy
import numpy as np

from behavior.left_state import LeftClose
from behavior.both_state import BothClose


class Analysis(object):
    def __init__(self, brain):
        self.brain = brain
        self.left_state = LeftClose(self)
        self.both_state = BothClose(self)
        self.behavior_cache = ""
        self.continue_click = []
        self.means = []

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def predict(self):
        face = self.brain.face
        points = self.brain.human.points

        both_behavior = self.both_state(points, face)
        left_behavior = self.left_state(points, face)

        x, y, c = face
        x1 = points["right_shoulder_x"]
        y1 = points["right_shoulder_y"]
        x2 = points["right_wrist_x"]
        y2 = points["right_wrist_y"]
        x3 = points["right_elbow_x"]
        y3 = points["right_elbow_y"]
        x4 = points["left_shoulder_x"]
        y4 = points["left_shoulder_y"]

        dy1 = y1 - y3
        dy2 = y3 - y2
        dy3 = y - y2
        dy = (dy1, dy2, dy3)

        diff = x2 - x4
        dist = self.norm(x2, y2, x4, y4)

        angle1 = self.cal_angle(x1, y1, x2, y2)
        angle2 = self.cal_angle(x1, y1, x3, y3)
        angle3 = self.cal_angle(x2, y2, x3, y3)
        # print(
        #     round(angle1, 2),
        #     round(angle2, 2),
        #     round(angle3, 2),
        #     round(dist, 2), 
        #     round(diff, 2))

        up = self.check_up(angle1, angle2, angle3, dy)
        right = self.check_right(angle1, angle2, angle3)
        left = self.check_left(angle1, angle2, angle3, dist, diff)
        down = self.check_down_leg(points)
        behaviors = [both_behavior, up, right, left, down, left_behavior]
        behavior = self.behaviors_filter(behaviors)

        if self.behavior_cache != behavior:
            self.behavior_cache = behavior
            return self.behavior_cache
        return ""

    def checking(self, behavior):
        self.continue_click.append(behavior)
        if len(self.continue_click) > 3:
            if "向下選取" in self.continue_click and \
                "向左選取" in self.continue_click:
                behavior = "向左選取"
            self.continue_click = self.continue_click[1:]
            return behavior
        return ""

    def behaviors_filter(self, behaviors):
        for behavior in behaviors:
            if behavior:
                return behavior
        return ""

    def check_up(self, angle1, angle2, angle3, dy):
        dy1, dy2, dy3 = dy
        c1 = 70 < angle1 and angle1 < 95
        c2 = 55 < angle2 and angle2 < 90
        c3 = 55 < abs(angle3) and abs(angle3) < 100
        c4 = dy1 > 45
        c5 = dy2 > 45
        c6 = dy3 > 30
        if (c1 and c2 and c3 and c4 and c5) or c6:
            return "向上選取"

    def check_right(self, angle1, angle2, angle3):
        c1 = -20 < angle1 and angle1 < 20
        c2 = -45 < angle2 and angle2 < 45
        c3 = 145 < abs(angle3) and abs(angle3) < 200
        if c1 and c2 and c3:
            return "向左選取"

    def check_left(self, angle1, angle2, angle3, dist, diff):
        c1 = 145 < abs(angle1) and abs(angle1) < 200
        c2 = -200 < angle2 and angle2 < -70
        c3 = -40 < angle3 and angle3 < 20
        c4 = dist < 45
        c5 = diff > 0
        if (c1 and c2 and c3) or c4 or c5:
            return "向右選取"

    def check_down(self, angle1, angle2, angle3):
        c1 = -60 < angle1 and angle1 < -30
        c2 = -60 < angle2 and angle2 < -30
        c3 = 130 < angle3 and angle3 < 160
        if c1 and c2 and c3:
            return "向下選取"

    def check_down_leg(self, points):
        thres = 40
        lhy = points["left_hip_y"]
        rhy = points["right_hip_y"]
        lsy = points["left_shoulder_y"]
        rsy = points["right_shoulder_y"]

        msy = ((lsy + rsy) / 2)
        mhy = ((lhy + rhy) / 2)
        t = ((msy + mhy) / 2)

        self.means.append(mhy)
        if len(self.means) > 10:
            self.means = self.means[1:]
            gradients = self.cal_gradient(self.means)
            print(gradients)
            if gradients > thres:
                return "向下選取"

    def cal_gradient(self, lst):
        s = 0
        past = lst[0]
        for mean in lst[1:]:
            diff = (mean - past)
            s += diff
            past = mean
        return s

    def cal_angle(self, x1, y1, x2, y2):
        dx = x1 - x2
        dy = y1 - y2
        return np.arctan2(dy, dx) / np.pi * 180

    def change_both_state(self, new_both_state):
        self.both_state = new_both_state

    def change_left_state(self, new_left_state):
        self.left_state = new_left_state

    def calc_left_thres(self, points, param):
        hip_y = points["left_hip_y"]
        shoulder_y = points["left_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return (0, y)
    
    def calc_right_thres(self, points, param):
        hip_y = points["right_hip_y"]
        shoulder_y = points["right_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return (0, y)

    def is_drop_the_hands(self, points):
        y = points["right_wrist_y"]
        _, thres = self.calc_right_thres(points, 10)
        return y > thres
