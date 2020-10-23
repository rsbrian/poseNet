import numpy as np
from utils.counter import Counter


class Template(object):
    def __init__(self, analysis):
        self.analysis = analysis
        self.counter = Counter()
        self.history = {}
        self.center = ()
        self.reset_center()

    def reset_center(self):
        self.center_x = []
        self.center_y = []

    def start(self, points):
        cx = points["right_shoulder_x"]
        cy = points["right_shoulder_y"]
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        pivot_x = self.history["right_wrist_x"][self.start_pivot]
        pivot_y = self.history["right_wrist_y"][self.start_pivot]
        dist = self.norm(cx, cy, x, y)
        pivot_dist = self.norm(cx, cy, pivot_x, pivot_y)
        return dist < pivot_dist

    def stop(self, points):
        c1 = self.is_stop_for_a_while(points, 0.5)
        return c1

    def is_return_to_center(self):
        history_x = self.history["right_wrist_x"][self.start_pivot:]
        history_y = self.history["right_wrist_y"][self.start_pivot:]

    def is_stop_for_a_while(self, points, time):
        past_pivot = len(self.history["right_wrist_x"]) - 2
        past_x = self.history["right_wrist_x"][past_pivot]
        past_y = self.history["right_wrist_y"][past_pivot]

        now_x = points["right_wrist_x"]
        now_y = points["right_wrist_y"]
        dist = self.norm(now_x, now_y, past_x, past_y)
        if dist < 10:
            self.counter.start()
            if self.stop_pivot is None:
                self.stop_pivot = len(self.history["right_wrist_x"]) - 1
        else:
            self.counter.reset()
            self.stop_pivot = None

        return self.counter.result() > time

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_inside_the_circle(self, points):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        return self.analysis.is_inside_the_circle(x, y)

    def is_upper_than_line(self, points):
        y = points["right_wrist_y"]
        thres = self.calc_thres(points, 2)
        return y < thres

    def is_drop_the_hands(self, points):
        y = points["right_wrist_y"]
        thres = self.calc_thres(points, 4)
        return y > thres

    def append(self, points):
        for name, value in points.items():
            try:
                self.history[name].append(value)
            except Exception:
                self.history[name] = [value]

    def draw_thres(self, img, points):
        h, w, c = img.shape
        hip_y = points["right_hip_y"]
        shoulder_y = points["right_shoulder_y"]
        y = hip_y - (hip_y - shoulder_y) / 4
        cv2.line(img, (0, int(y)), (w, int(y)), (0, 200, 200), 3)

        y = hip_y - (hip_y - shoulder_y) / 2
        cv2.line(img, (0, int(y)), (w, int(y)), (0, 200, 200), 3)
