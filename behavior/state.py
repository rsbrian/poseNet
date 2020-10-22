from behavior.template import Template


class Open(Template):
    def __init__(self, analysis):
        super().__init__(analysis)

    def __call__(self, points, face):
        print("Open")
        self.append(points)

        if not self.is_inside_the_circle(points):
            self.analysis.change(Close(self.analysis))


class Close(Template):
    def __init__(self, analysis):
        super().__init__(analysis)

    def __call__(self, points, face):
        print("Close")
        if self.is_inside_the_circle(points):
            self.analysis.change(Open(self.analysis))
