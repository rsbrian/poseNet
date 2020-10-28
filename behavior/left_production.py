import cv2
import numpy as np


class Behavior(object):
    def __init__(self, state):
        self.state = state
        self.moving = 4
        self.valid_width = 20
        self.valid_height = 5

    def calcAngles(self, listed_x, listed_y):
        angles = []
        px = listed_x[0]
        py = listed_y[0]
        for i in range(1, len(listed_x)):
            x = listed_x[i]
            y = listed_y[i]
            dx = (x - px)
            dy = (y - py)
            angle = np.arctan2(dy, dx) / np.pi * 180
            angles.append(angle)
            px = x
            py = y
        temp = []
        i = 0
        step = 3
        while i < (len(angles) - (step - 1)):
            angles[i] = np.mean(angles[i:i+step])
            i += 1
        return angles

    def check_length(self):
        lsx = self.history["left_shoulder_x"]
        lsy = self.history["left_shoulder_y"]
        lhx = self.history["left_hip_x"]
        lhy = self.history["left_hip_y"]
        lex = self.history["left_elbow_x"]
        ley = self.history["left_elbow_y"]
        lwx = self.history["left_wrist_x"]
        lwy = self.history["left_wrist_y"]
        for i in range(len(lsx)):
            x1 = lsx[i]
            y1 = lsy[i]
            x2 = lhx[i]
            y2 = lhy[i]
            x3 = lex[i]
            y3 = ley[i]
            x4 = lwx[i]
            y4 = lwy[i]
            dist = self.norm(x1, y1, x2, y2)
            d1 = self.norm(x1, y1, x3, y3)
            d2 = self.norm(x3, y3, x4, y4)
            if (d1 + d2) < (dist / 4):
                return True
        return False

    def predict_behavior(self):
        rwx = self.history["left_wrist_x"][-1]
        rwy = self.history["left_wrist_y"][-1]

        angles = self.calcAngles(
            self.history["left_wrist_x"], self.history["left_wrist_y"])
        mean_angles = np.mean(angles)

        if self.check_length():
            return ""

        return "Cancel" if mean_angles > -10 and mean_angles < 45 else ""

    def find_closest_point_and_cut(self):
        temp = {}
        minimum = np.inf
        for i in range(len(self.history["left_wrist_x"])):
            rwx = self.history["left_wrist_x"][i]
            rwy = self.history["left_wrist_y"][i]
            rsx = self.history["left_shoulder_x"][i]
            rsy = self.history["left_shoulder_y"][i]
            fx = self.history["face_x"][i]
            fy = self.history["face_y"][i]
            dist = self.norm(rwx, rwy, rsx, rsy)
            if dist < minimum and self.point_in_thres(rwx, rwy, rsx, rsy, fx, fy):
                temp = self.cut_history_by_index(i)
                minimum = dist
        if temp == {}:
            self.cut_history_to_start(param=-2)
        else:
            self.history = temp.copy()

    def cut_history_by_index(self, i):
        temp = self.history.copy()
        for name, value in temp.items():
            temp[name] = value[i:]
        return temp

    def cut_history_to_start(self, param=-1):
        for name, listed in self.history.items():
            self.history[name] = self.history[name][param:].copy()

    def get_boundary(self, rsx, rsy, fx, fy):
        left_bound = fx - self.valid_width
        right_bound = rsx + (rsx - fx)
        upper_bound = fy - self.valid_height
        lower_bound = rsy + (rsy - fy)
        return [right_bound, left_bound, upper_bound, lower_bound]

    def compare_boundary(self, rwx, rwy, boundary):
        right_bound = boundary[0]
        left_bound = boundary[1]
        upper_bound = boundary[2]
        lower_bound = boundary[3]
        c1 = rwx < right_bound
        c2 = rwx > left_bound
        c3 = rwy > upper_bound
        c4 = rwy < lower_bound
        return [c1, c2, c3, c4]

    def point_in_thres(self, rwx, rwy, rsx, rsy, fx, fy):
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        return all(check_list)

    def move(self, points):
        if len(self.history["left_wrist_x"]) > 2:
            past_x = self.history["left_wrist_x"][-2]
            past_y = self.history["left_wrist_y"][-2]
            now_x = points["left_wrist_x"]
            now_y = points["left_wrist_y"]
            dist = self.norm(now_x, now_y, past_x, past_y)
            return dist > self.moving
        return False

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_point_in_thres(self, img, points, face):
        rwx = points["left_wrist_x"]
        rwy = points["left_wrist_y"]
        rsx = points["left_shoulder_x"]
        rsy = points["left_shoulder_y"]
        fx = face[0]
        fy = face[1]
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)

        right_bound = boundary[0]
        left_bound = boundary[1]
        upper_bound = boundary[2]
        lower_bound = boundary[3]
        h, w, c = img.shape
        cv2.line(
            img,
            (int(left_bound), 0), (int(left_bound), h), (0, 200, 200), 3)
        cv2.line(
            img,
            (0, int(upper_bound)), (w, int(upper_bound)), (0, 200, 200), 3)
        cv2.line(
            img,
            (int(right_bound), 0), (int(right_bound), h), (0, 200, 200), 3)
        cv2.line(
            img,
            (0, int(lower_bound)), (w, int(lower_bound)), (0, 200, 200), 3)
        return all(check_list)

    def is_drop_the_hands(self, points):
        y = points["left_wrist_y"]
        thres = self.state.analysis.calc_left_thres(points, 4)
        return y > thres
