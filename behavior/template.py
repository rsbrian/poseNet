class Template(object):
    def __init__(self, analysis):
        self.analysis = analysis
        self.history = {}

    def is_inside_the_circle(self, points):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        return self.analysis.is_inside_the_circle(x, y)

    def is_upper_than_line(self, points):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        return y < self.analysis.is_upper_than_line(points)

    def append(self, points):
        for name, value in points.items():
            try:
                self.history[name].append(value)
            except Exception:
                self.history[name] = [value]
