class Test(object):
    def __init__(self, analysis):
        self.analysis = analysis
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
