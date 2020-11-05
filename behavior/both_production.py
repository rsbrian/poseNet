import cv2
import numpy as np


class Behavior(object):
    def __init__(self, state):
        self.state = state
        self.moving = 4
        self.valid_width = 20
        self.valid_height = 5
        self.thres = None

    def check_left_length(self):
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
            if (d1 + d2) < (dist / 3):
                return True
        return False

    def check_right_length(self):
        lsx = self.history["right_shoulder_x"]
        lsy = self.history["right_shoulder_y"]
        lhx = self.history["right_hip_x"]
        lhy = self.history["right_hip_y"]
        lex = self.history["right_elbow_x"]
        ley = self.history["right_elbow_y"]
        lwx = self.history["right_wrist_x"]
        lwy = self.history["right_wrist_y"]
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
            if (d1 + d2) < (dist / 3):
                return True
        return False

    def get_right_boundary(self, rsx, rsy, fx, fy):
        right_bound = fx + self.valid_width
        left_bound = rsx - (fx - rsx)
        upper_bound = fy - self.valid_height
        lower_bound = rsy + (rsy - fy)
        return [right_bound, left_bound, upper_bound, lower_bound]

    def get_left_boundary(self, rsx, rsy, fx, fy):
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

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

    def is_left_point_in_thres(self, points, face):
        rwx = points["left_wrist_x"]
        rwy = points["left_wrist_y"]
        rsx = points["left_shoulder_x"]
        rsy = points["left_shoulder_y"]
        fx = face[0]
        fy = face[1]
        boundary = self.get_left_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        return all(check_list)

    def is_right_point_in_thres(self, points, face):
        rwx = points["right_wrist_x"]
        rwy = points["right_wrist_y"]
        rsx = points["right_shoulder_x"]
        rsy = points["right_shoulder_y"]
        fx = face[0]
        fy = face[1]
        boundary = self.get_right_boundary(rsx, rsy, fx, fy)
        check_list = self.compare_boundary(rwx, rwy, boundary)
        return all(check_list)

    def is_drop_the_hands(self, points):
        y1 = points["left_wrist_y"]
        y2 = points["right_wrist_y"]
        _, thres = self.state.analysis.calc_left_thres(points, 10)
        return y1 > thres and y2 > thres
