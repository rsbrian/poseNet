import cv2
import copy
import numpy as np

from behavior.state import Close


class Analysis(object):
    def __init__(self, brain):
        self.brain = brain
        self.single_circle = (0, 0, 0, (200, 200, 200), 3)
        self.state = Close(self)

    def predict(self, img):
        face = self.brain.face
        points = self.brain.human.points
        behavior = self.state(img, points, face)
        return behavior

    def change(self, new_state):
        self.state = new_state

    def calc_thres(self, points, param):
        hip_y = points["right_hip_y"]
        shoulder_y = points["right_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / param
        return y
