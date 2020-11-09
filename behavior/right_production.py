import cv2
import numpy as np


class Behavior(object):
    def __init__(self, state):
        self.state = state
        self.state.behavior = ""
        self.moving = 4
        self.valid_width = 20
        self.valid_height = 5
        self.behavior_map = ["向右選取", "向左選取", "向上選取", "向下選取"]

    def check_length(self):
        lsx = self.history["right_shoulder_x"]
        lsy = self.history["right_shoulder_y"]
        lhx = self.history["right_hip_x"]
        lhy = self.history["right_hip_y"]
        lex = self.history["right_elbow_x"]
        ley = self.history["right_elbow_y"]
        lwx = self.history["right_wrist_x"]
        lwy = self.history["right_wrist_y"]
        total = len(lsx)
        wrong = 0
        for i in range(total):
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
            thres = dist / 8
            if d1 < thres or d2 < thres:
                wrong += 1
        wrong_acc = (wrong / total)
        if wrong_acc > 0.4:
            return True
        return False

    def predict_behavior(self):
        rwx = self.history["right_wrist_x"][-1]
        rwy = self.history["right_wrist_y"][-1]
        rsx = self.history["right_shoulder_x"][-1]
        rsy = self.history["right_shoulder_y"][-1]
        fx = self.history["face_x"][-1]
        fy = self.history["face_y"][-1]
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        if self.check_length():
            return ""
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
        left_bound = rsx - (right_bound - rsx)
        upper_bound = fy - self.valid_height
        lower_bound = rsy + (rsy - upper_bound) - 20
        return (right_bound, left_bound, upper_bound, lower_bound)

    def compare_boundary(self, rwx, rwy, boundary):
        thres = 20
        right_bound = boundary[0]
        left_bound = boundary[1]
        upper_bound = boundary[2]
        lower_bound = boundary[3]
        c1 = rwx < (right_bound + thres)
        c2 = rwx > (left_bound - thres)
        c3 = rwy > (upper_bound - thres)
        c4 = rwy < (lower_bound + thres)
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

    def is_point_in_thres(self, points, face):
        rwx = points["right_wrist_x"]
        rwy = points["right_wrist_y"]
        rsx = points["right_shoulder_x"]
        rsy = points["right_shoulder_y"]
        fx = face[0]
        fy = face[1]
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        return all(check_list)

    def is_drop_the_hands(self, points):
        y = points["right_wrist_y"]
        _, thres = self.state.analysis.calc_right_thres(points, 10)
        return y > thres
