from utils.counter import Counter
from behavior.both_production import Behavior


class Clicked(Behavior):
    def __init__(self, state, behavior):
        super().__init__(state)
        self.behavior = behavior

    def __call__(self, img, points, face, history):
        self.history = history

        self.state.behavior = self.behavior
        self.behavior = ""

        if self.is_drop_the_hands(points):
            self.state.analysis.change_both_state(
                BothClose(self.state.analysis))


class Outside(Behavior):
    def __init__(self, state):
        super().__init__(state)

    def __call__(self, img, points, face, history):
        self.history = history

        if self.is_left_point_in_thres(img, points, face) and \
                self.is_right_point_in_thres(img, points, face):
            self.state.change(Inside(self.state))

        if self.is_drop_the_hands(points):
            self.state.analysis.change_both_state(
                BothClose(self.state.analysis))


class Inside(Behavior):
    def __init__(self, state):
        super().__init__(state)
        self.counter = Counter()
        self.time = 0.3

    def __call__(self, img, points, face, history):
        self.history = history

        if not (self.is_left_point_in_thres(img, points, face) and
                self.is_right_point_in_thres(img, points, face)):
            self.state.change(Outside(self.state))

        if not (self.check_left_length() and self.check_right_length()):
            self.counter.start()
            if self.counter.result() > self.time:
                self.behavior = "雙手彎舉"
                self.state.change(Clicked(self.state, self.behavior))
        else:
            self.counter.reset()


class Open(Behavior):
    def __init__(self, analysis):
        self.analysis = analysis
        self.history = {}
        self.state = None
        self.valid_width = 20
        self.valid_height = 5
        self.behavior = ""
        self.left_wrist = []

    def __call__(self, img, points, face):
        self.append(points, face)
        if self.state is None:
            if self.is_left_point_in_thres(img, points, face) and \
                    self.is_right_point_in_thres(img, points, face):
                self.state = Inside(self)
        else:
            self.state(img, points, face, self.history)

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


class BothClose(object):
    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, img, points, face):
        if self.is_left_upper_than_line(points) and \
                self.is_right_upper_than_line(points):
            self.analysis.change_both_state(Open(self.analysis))
        return ""

    def is_left_upper_than_line(self, points):
        y = points["left_wrist_y"]
        thres = self.analysis.calc_left_thres(points, 2)
        return y < thres

    def is_right_upper_than_line(self, points):
        y = points["right_wrist_y"]
        thres = self.analysis.calc_right_thres(points, 2)
        return y < thres
