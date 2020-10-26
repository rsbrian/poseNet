from utils.counter import Counter
from behavior.both_production import Behavior


class Outside(Behavior):
    def __init__(self, state, behavior):
        super().__init__(state)
        self.behavior = behavior
        self.count = 0

    def __call__(self, img, points, face, history):
        self.history = history

        self.state.behavior = self.behavior
        self.behavior = ""

        if self.is_point_in_thres(img, points, face) and not self.move(points):
            self.state.change(InsideNotMove(self.state))

        elif self.is_point_in_thres(img, points, face) and self.move(points):
            self.state.change(InsideMovingNoCenter(self.state))

        if self.is_drop_the_hands(points):
            self.state.analysis.change_left_state(
                LeftClose(self.state.analysis))


class InsideNotMove(Behavior):
    def __init__(self, state):
        super().__init__(state)
        self.counter = Counter()
        self.center = None
        self.time = 0.6

    def __call__(self, img, points, face, history):
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
                    self.history["left_wrist_x"][-1],
                    self.history["left_wrist_y"][-1]
                )
        else:
            self.cut_history_to_start(-2)
            self.center = (
                self.history["left_wrist_x"][-1],
                self.history["left_wrist_y"][-1]
            )


class InsideMovingNoCenter(Behavior):
    def __init__(self, state):
        super().__init__(state)

    def __call__(self, img, points, face, history):
        self.history = history
        self.find_closest_point_and_cut()
        if not self.is_point_in_thres(img, points, face):
            behavior = self.predict_behavior()
            self.state.history = {}
            self.state.change(Outside(self.state, behavior))

        elif not self.move(points):
            self.state.change(InsideNotMove(self.state))


class InsideMovingHaveCenter(Behavior):
    def __init__(self, state):
        super().__init__(state)

    def __call__(self, img, points, face, history):
        self.history = history

        if not self.is_point_in_thres(img, points, face):
            behavior = self.predict_behavior()
            self.state.history = {}
            self.state.change(Outside(self.state, behavior))

        elif not self.move(points):
            self.state.change(InsideNotMove(self.state))


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
            if not self.is_point_in_thres(img, points, face):
                self.state = Outside(self, self.behavior)

            elif not self.move(points):
                self.state = InsideNotMove(self)

            else:
                self.state = InsideMovingNoCenter(self)

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
        if self.is_upper_than_line(points):
            self.analysis.change_left_state(Open(self.analysis))
        return ""

    def is_upper_than_line(self, points):
        y = points["left_wrist_y"]
        thres = self.analysis.calc_left_thres(points, 2)
        return y < thres
