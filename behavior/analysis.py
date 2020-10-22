import cv2
import copy
import numpy as np

from behavior.state import Close


class Analysis(object):
    def __init__(self, brain):
        self.brain = brain
        self.single_circle = (0, 0, 0, (200, 200, 200), 3)
        self.state = Close(self)

    def predict(self):
        face = self.brain.face
        points = self.brain.human.points
        x = points["right_shoulder_x"]
        y = points["right_shoulder_y"]
        r = 100
        self.set_circle(x, y, r)
        behavior = self.state(points, face)
        return ""

    def is_upper_than_line(self, points):
        return abs(points["right_shoulder_y"] + points["right_hip_y"]) / 2

    def is_inside_the_circle(self, x1, y1):
        x2, y2, r, _, _ = self.single_circle
        dist = self.norm(x1, y1, x2, y2)
        return dist < r

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def set_circle(self, x, y, r, clr=(0, 200, 200), t=3):
        self.single_circle = (
            x, y, r,
            clr, t
        )

    def get_circle(self):
        return self.single_circle

    def change(self, new_state):
        self.state = new_state
