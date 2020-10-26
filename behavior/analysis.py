import cv2
import copy
import numpy as np

from behavior.state import RightClose
from behavior.left_state import LeftClose


class Analysis(object):
    def __init__(self, brain):
        self.brain = brain
        self.single_circle = (0, 0, 0, (200, 200, 200), 3)
        self.right_state = RightClose(self)
        self.left_state = LeftClose(self)

    def predict(self, img):
        face = self.brain.face
        points = self.brain.human.points
        right_behavior = ""
        # right_behavior = self.right_state(img, points, face)
        left_behavior = self.left_state(img, points, face)
        return right_behavior

    def change_right_state(self, new_right_state):
        self.right_state = new_right_state

    def change_left_state(self, new_left_state):
        self.left_state = new_left_state

    def calc_right_thres(self, points, param):
        hip_y = points["right_hip_y"]
        shoulder_y = points["right_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return y

    def calc_left_thres(self, points, param):
        hip_y = points["left_hip_y"]
        shoulder_y = points["left_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return y
