import cv2
import numpy as np

from utils.counter import Counter
from behavior.right_production import Behavior


class Outside(Behavior):
    def __init__(self, state, behavior):
        super().__init__(state)
        self.behavior = behavior
        self.count = 0

    def __call__(self, points, face, history):
        self.history = history

        if self.is_point_in_thres(points, face) and not self.move(points):
            self.state.change(InsideNotMove(self.state))

        elif self.is_point_in_thres(points, face) and self.move(points):
            self.state.change(InsideMovingNoCenter(self.state))

        if self.behavior == "向下選取" and not self.is_drop_the_hands(points):
            if self.count > 4:
                self.state.behavior = self.behavior
                self.behavior = ""
            self.count += 1

        elif self.behavior == "向下選取" and self.count < 4:
            # print("我只是想把手放下")
            self.state.behavior = ""
            self.state.analysis.change_right_state(
                RightClose(self.state.analysis))

        elif self.is_drop_the_hands(points):
            self.state.analysis.change_right_state(
                RightClose(self.state.analysis))

        else:
            self.state.behavior = self.behavior
            self.behavior = ""


class InsideMovingNoCenter(Behavior):
    def __init__(self, state):
        super().__init__(state)

    def __call__(self, points, face, history):
        self.history = history
        self.find_closest_point_and_cut()
        if not self.is_point_in_thres(points, face):
            behavior = self.predict_behavior()
            self.state.history = {}
            self.state.change(Outside(self.state, behavior))

        elif not self.move(points):
            self.state.change(InsideNotMove(self.state))


class InsideMovingHaveCenter(Behavior):
    def __init__(self, state):
        super().__init__(state)

    def __call__(self, points, face, history):
        self.history = history

        if not self.is_point_in_thres(points, face):
            behavior = self.predict_behavior()
            self.state.history = {}
            self.state.change(Outside(self.state, behavior))

        elif not self.move(points):
            self.state.change(InsideNotMove(self.state))


class InsideNotMove(Behavior):
    def __init__(self, state):
        super().__init__(state)
        self.counter = Counter()
        self.center = None
        self.time = 0.6

    def __call__(self, points, face, history):
        self.history = history

        if self.move(points) and self.center is None:
            self.counter.reset()
            self.state.change(InsideMovingNoCenter(self.state))

        elif self.move(points):
            self.counter.reset()
            self.state.change(InsideMovingHaveCenter(self.state))

        elif self.center is None:
            self.counter.start()
            if self.counter.result() > self.time:
                self.cut_history_to_start(-2)
                self.center = (
                    self.history["right_wrist_x"][-1],
                    self.history["right_wrist_y"][-1]
                )
        else:
            self.cut_history_to_start(-2)
            self.center = (
                self.history["right_wrist_x"][-1],
                self.history["right_wrist_y"][-1]
            )


class Open(Behavior):
    def __init__(self, analysis):
        self.analysis = analysis
        self.history = {}
        self.state = None
        self.valid_width = 20
        self.valid_height = 5
        self.behavior = ""

    def __call__(self, points, face):
        self.append(points, face)

        if self.state is None:
            if not self.is_point_in_thres(points, face):
                self.state = Outside(self, self.behavior)

            elif not self.move(points):
                self.state = InsideNotMove(self)

            else:
                self.state = InsideMovingNoCenter(self)

        else:
            rsx = points["right_shoulder_x"]
            rsy = points["right_shoulder_y"]
            fx = face[0]
            fy = face[1]
            boundary = self.state.get_boundary(rsx, rsy, fx, fy)
            right_bound = boundary[0]
            left_bound = boundary[1]
            upper_bound = boundary[2]
            lower_bound = boundary[3]
            self.analysis.thres = (
                left_bound, right_bound, upper_bound, lower_bound)
            self.state(points, face, self.history)

        return self.behavior

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

    def change(self, new_state):
        self.state = new_state


class RightClose(Behavior):
    def __init__(self, analysis):
        self.analysis = analysis
        self.valid_width = 20
        self.valid_height = 5

    def __call__(self, points, face):
        rsx = points["right_shoulder_x"]
        rsy = points["right_shoulder_y"]
        fx = face[0]
        fy = face[1]
        boundary = self.get_boundary(rsx, rsy, fx, fy)
        right_bound = boundary[0]
        left_bound = boundary[1]
        upper_bound = boundary[2]
        lower_bound = boundary[3]
        self.analysis.thres = (
            left_bound, right_bound, upper_bound, lower_bound)
        if self.is_point_in_thres(points, face):
            self.analysis.change_right_state(Open(self.analysis))
        return ""

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
