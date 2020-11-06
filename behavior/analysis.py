import cv2
import copy
import numpy as np

from behavior.left_state import LeftClose
from behavior.right_state import RightClose
from behavior.both_state import BothClose


class Analysis(object):
    def __init__(self, brain):
        self.brain = brain
        self.right_state = RightClose(self)
        self.left_state = LeftClose(self)
        self.both_state = BothClose(self)
        self.thres = None

    def predict(self):
        face = self.brain.face
        points = self.brain.human.points
        both_behavior = self.both_state(points, face)
        if both_behavior != "":
            return both_behavior
        left_behavior = self.left_state(points, face)
        if left_behavior != "":
            return left_behavior
        right_behavior = self.right_state(points, face)
        return right_behavior

    def get_thres(self):
        return self.thres

    def change_both_state(self, new_both_state):
        self.both_state = new_both_state

    def change_right_state(self, new_right_state):
        self.right_state = new_right_state

    def change_left_state(self, new_left_state):
        self.left_state = new_left_state

    def calc_right_thres(self, points, param):
        hip_y = points["right_hip_y"]
        shoulder_y = points["right_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return (0, y)

    def calc_left_thres(self, points, param):
        hip_y = points["left_hip_y"]
        shoulder_y = points["left_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return (0, y)
