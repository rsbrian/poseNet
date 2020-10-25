import cv2
import numpy as np
from utils.counter import Counter


class Test(object):
    def __init__(self, analysis):
        self.analysis = analysis
        self.counter = Counter()
        self.history = {}
        self.time = 0.5
        self.valid_width = 20
        self.valid_height = 20
        self.moving = 4

    def predict_by_angles(self, history):
        angles = []
        right_wrist_x = history["right_wrist_x"].copy()
        right_wrist_y = history["right_wrist_y"].copy()
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

        i = 0
        step = 3
        while i < len(angles) - (step - 1):
            angles[i] = np.mean(angles[i:i+step])
            i += 1
        return angles

    def predict_by_gradients(self, history):
        right_wrist_x = history["right_wrist_x"]
        right_wrist_y = history["right_wrist_y"]
        print(len(right_wrist_x))
        dx = 0
        dy = 0
        dxs = []
        dys = []
        px = right_wrist_x[0]
        py = right_wrist_y[0]
        for i in range(1, len(right_wrist_x)):
            x = right_wrist_x[i]
            y = right_wrist_y[i]
            diffx = x - px
            diffy = y - py
            dxs.append(diffx)
            dys.append(diffy)
            dx += abs(diffx)
            dy += abs(diffy)
        print(dx, dy)
        if (dx - dy) > 50 and self.calc_scope(dxs) == "先負再正":
            print("往左滑")
        elif (dx - dy) > 50 and self.calc_scope(dxs) == "先正再負":
            print("往右滑")
        elif (dy - dx) > 50 and self.calc_scope(dxs) == "先負再正":
            print("往上滑")
        elif (dy - dx) > 50 and self.calc_scope(dxs) == "先正再負":
            print("往下滑")

    def calc_scope(self, gradients):
        s = 0
        p = gradients[0]
        for gradient in gradients[1:]:
            s += (gradient - p)
            p = gradient
        if s > 0:
            return "先負再正"
        else:
            return "先正再負"

    def cut_start_history(self):
        temp = {}
        minimum = np.inf
        for i in range(len(self.history["right_wrist_x"])):
            rwx = self.history["right_wrist_x"][i]
            rwy = self.history["right_wrist_y"][i]
            rsx = self.history["right_shoulder_x"][i]
            rsy = self.history["right_shoulder_y"][i]
            fx = self.history["face_x"][i]
            fy = self.history["face_y"][i]
            dist = self.norm(rwx, rwy, rsx, rsy)
            if dist < minimum and self.point_is_thres(rwx, rwy, rsx, rsy, fx, fy):
                temp = self.cut_history_by_index(i)
                minimum = dist
        return temp

    def cut_history_by_index(self, i):
        temp = self.history.copy()
        for name, value in temp.items():
            temp[name] = value[i:]
        return temp

    def point_is_thres(self, rwx, rwy, rsx, rsy, fx, fy):
        right_bound = fx
        left_bound = rsx - (fx - rsx)
        upper_bound = fy
        lower_bound = rsy - (fy - rsy)
        c1 = rwx < right_bound
        c2 = rwx > left_bound
        c3 = rwy > upper_bound
        c4 = rwy < lower_bound
        return c1 and c2 and c3 and c4

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

    def append(self, points, face):
        for name, value in points.items():
            try:
                self.history[name].append(value)
            except Exception:
                self.history[name] = [value]
        try:
            self.history["face_x"].append(face[0])
            self.history["face_y"].append(face[1])
        except Exception:
            self.history["face_x"] = [face[0]]
            self.history["face_y"] = [face[1]]

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
