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

    def predict(self):
        face = self.brain.face
        points = self.brain.human.points

        both_behavior = self.both_state(points, face)
        left_behavior = self.left_state(points, face)

        x1 = points["right_shoulder_x"]
        y1 = points["right_shoulder_y"]
        x2 = points["right_wrist_x"]
        y2 = points["right_wrist_y"]
        x3 = points["right_elbow_x"]
        y3 = points["right_elbow_y"]

        angle1 = self.cal_angle(x1, y1, x2, y2)
        angle2 = self.cal_angle(x1, y1, x3, y3)
        angle3 = self.cal_angle(x2, y2, x3, y3)

        up = self.check_up(angle1, angle2, angle3)
        right = self.check_right(angle1, angle2, angle3)
        left = self.check_left(angle1, angle2, angle3)
        down = self.check_down(angle1, angle2, angle3)
        behaviors = [both_behavior, up, right, left, down, left_behavior]

        behavior = self.behaviors_filter(behaviors)
        behavior = self.checking(behavior)

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

    def check_up(self, angle1, angle2, angle3):
        if 70 < angle1 and angle1 < 95 and \
            55 < angle2 and angle2 < 90 and \
            70 < abs(angle3) and abs(angle3) < 100:
            return "向上選取"

    def check_right(self, angle1, angle2, angle3):
        if -20 < angle1 and angle1 < 20 and \
            -15 < angle2 and angle2 < 10 and \
            -200 < angle3 and angle3 < -145:
            return "向左選取"

    def check_left(self, angle1, angle2, angle3):
        if 145 < abs(angle1) and abs(angle1) < 200 and \
            -150 < angle2 and angle2 < -70 and \
            -20 < angle3 and angle3 < 20:
            return "向右選取"

    def check_down(self, angle1, angle2, angle3):
        if (-60 < angle1 and angle1 < -30) and \
            -60 < angle2 and angle2 < -30 and \
            130 < angle3 and angle3 < 160:
            return "向下選取"

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
