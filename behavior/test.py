import cv2
import numpy as np
from utils.counter import Counter


class Test(object):
    def __init__(self, analysis):
        self.analysis = analysis
        self.counter = Counter()
        self.history = {}
        self.time = 0.7
        self.valid_width = 20
        self.valid_height = 20
        self.moving = 4
        self.dists = []

    def is_any_turning_point(self, listed_name):
        angles = []
        right_wrist_x = self.history["right_wrist_x"].copy()
        right_wrist_y = self.history["right_wrist_y"].copy()
        px = right_wrist_x[0]
        py = right_wrist_y[0]
        for i in range(1, len(right_wrist_x)):
            x = right_wrist_x[i]
            y = right_wrist_y[i]
            dx = (x - px)
            dy = (y - py)
            angle = np.arctan2(dy, dx) / np.pi * 180
            angles.append(angle)
            px = x
            py = y
        print(angles)
        self.history = {}

    def is_drop_the_hands(self, points):
        y = points["right_wrist_y"]
        thres = self.analysis.calc_thres(points, 4)
        return y > thres

    def append(self, points):
        for name, value in points.items():
            try:
                self.history[name].append(value)
            except Exception:
                self.history[name] = [value]

    def find_closest_point(self, points):
        cx = points["right_shoulder_x"]
        cy = points["right_shoulder_y"]
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        pivot_x = self.open_state.history["right_wrist_x"][self.start_pivot]
        pivot_y = self.open_state.history["right_wrist_y"][self.start_pivot]
        dist = self.norm(cx, cy, x, y)
        pivot_dist = self.norm(cx, cy, pivot_x, pivot_y)
        if dist <= pivot_dist:
            self.start_pivot = len(
                self.open_state.history["right_wrist_x"]) - 1
            self.default_center = (
                points["right_wrist_x"],
                points["right_wrist_y"]
            )

    def reset_center(self):
        self.center = (
            np.mean(self.center_x),
            np.mean(self.center_y)
        )

    def move(self, points):
        if len(self.history["right_wrist_x"]) > 2:
            past_x = self.history["right_wrist_x"][-2]
            past_y = self.history["right_wrist_y"][-2]
            now_x = points["right_wrist_x"]
            now_y = points["right_wrist_y"]
            dist = self.norm(now_x, now_y, past_x, past_y)
            self.dists.append(dist)
            if len(self.dists) > 5:
                dist = np.mean(self.dists)
                self.dists = self.dists[1:]
                return dist < self.moving
        return False

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_point_in_thres(self, img, points, face):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        x1 = points["right_shoulder_x"]
        y1 = points["right_shoulder_y"]
        x2 = face[0]
        y2 = face[1]
        cx1 = x < x2
        cy1 = y > y2
        diff = (x2 - x1) + self.valid_width
        x3 = x1 - diff
        cx2 = x > x3
        diff = (y1 - y2) + self.valid_height
        y3 = y1 + diff
        cy2 = y < y3

        h, w, c = img.shape
        cv2.line(img, (int(x3), 0), (int(x3), h), (0, 200, 200), 3)
        cv2.line(img, (0, int(y2)), (w, int(y2)), (0, 200, 200), 3)
        cv2.line(img, (int(x2), 0), (int(x2), h), (0, 200, 200), 3)
        cv2.line(img, (0, int(y3)), (w, int(y3)), (0, 200, 200), 3)
        return cx1 and cy1 and cx2 and cy2
