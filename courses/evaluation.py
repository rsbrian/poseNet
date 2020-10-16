class EvaluationTemplate(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter
        self.weights = [2, 6, 4]

    def __call__(self):
        print("Evaluation")
        total_time = self.counter.get_logs()["total"]

        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")

        if total_time < 1.2:
            self.course.history["fast"] += 1
            self.course.api.course_action["action"]["alert"] = ["太快了，請放慢速度"]
        elif total_time < 2.5:
            self.course.history["perfect"] += 1
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            self.course.history["slow"] += 1
            self.course.api.course_action["action"]["alert"] = ["太慢了，請加快速度"]

        self.course.api.course_action["action"]["times"] += 1
        self.calcScore()
        # self.course.change(
        #     Action(self.course, self.brain))

    def calcScore(self):
        for i, (key, value) in enumerate(self.course.history.items()):
            self.course.api.course_action["action"]["score"] += self.weights[i] * value
