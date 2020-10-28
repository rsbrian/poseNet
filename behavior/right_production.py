import cv2
import numpy as np


class Behavior(object):
    def __init__(self, state):
        self.state = state
        self.moving = 4
        self.valid_width = 20
        self.valid_height = 5
        self.behavior_map = ["向左選取", "向右選取", "向上選取", "向下選取"]

    def predict_behavior(self):
        rwx = self.history["right_wrist_x"][-1]
        rwy = self.history["right_wrist_y"][-1]
        rsx = self.history["right_shoulder_x"][-1]
        rsy = self.history["right_shoulder_y"][-1]
        fx = self.history["face_x"][-1]
        fy = self.history["face_y"][-1]
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        return self.behavior_filter(check_list)

    def behavior_filter(self, check_list):
        for i, check in enumerate(check_list):
            if not check:
                return self.behavior_map[i]
        return ""

    def find_closest_point_and_cut(self):
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
        right_bound = fx + self.valid_width
        left_bound = rsx - (fx - rsx)
        upper_bound = fy - self.valid_height
        lower_bound = rsy + (rsy - fy) - 20
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
        if len(self.history["right_wrist_x"]) > 2:
            past_x = self.history["right_wrist_x"][-2]
            past_y = self.history["right_wrist_y"][-2]
            now_x = points["right_wrist_x"]
            now_y = points["right_wrist_y"]
            dist = self.norm(now_x, now_y, past_x, past_y)
            return dist > self.moving
        return False

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_point_in_thres(self, img, points, face):
        rwx = points["right_wrist_x"]
        rwy = points["right_wrist_y"]
        rsx = points["right_shoulder_x"]
        rsy = points["right_shoulder_y"]
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
        y = points["right_wrist_y"]
        thres = self.state.analysis.calc_right_thres(points, 4)
        return y > thres
