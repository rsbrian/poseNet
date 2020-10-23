import cv2
import numpy as np

from behavior.test import Test


class Open(Test):
    def __init__(self, analysis):
        super().__init__(analysis)

    def __call__(self, img, points, face):
        print("Open")
        self.append(points)

        # self.find_center()
        # self.find_turning()

        # if self.is_stop_for_a_while():
        #     self.reset_center()

        right_wrist_y = self.history["right_wrist_y"]
        print(right_wrist_y)

        if self.is_drop_the_hands(points):
            self.analysis.change(Close(self.analysis))


class Close(object):
    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, img, points, face):
        if self.is_inside_the_circle(img, points):
            self.analysis.change(Open(self.analysis))

    def is_inside_the_circle(self, img, points):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        x1 = points["right_shoulder_x"]
        y1 = points["right_shoulder_y"]
        r = 75
        dist = self.norm(x, y, x1, y1)
        cv2.circle(img, (int(x1), int(y1)), r, (0, 200, 200), 3)
        return dist < r

    def is_upper_than_line(self, points):
        y = points["right_wrist_y"]
        thres = self.analysis.calc_thres(points, 2)
        return y < thres

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
