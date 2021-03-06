import random


class EvaluationTemplate(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter
        self.normal = 100/36
        self.weights = {
            "fast": round(2 * self.normal),
            "slow": round(4 * self.normal),
            "perfect": round(6 * self.normal),
        }

    def __call__(self):
        print("Evaluation")
        total_time = self.counter.get_logs()["total"]

        if total_time < 1.2:
            self.course.api.course_action["action"]["score"] += self.weights["fast"]
            self.course.api.course_action["action"]["alert"] = ["太快了，請放慢速度"]
        elif total_time < 2.5:
            self.course.api.course_action["action"]["score"] += self.weights["perfect"]
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            self.course.api.course_action["action"]["score"] += self.weights["slow"]
            self.course.api.course_action["action"]["alert"] = ["太慢了，請加快速度"]

        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")
        self.course.api.course_action["action"]["times"] += 1

        if self.course.api.course_action["action"]["times"] == 6:
            if self.course.api.course_action["action"]["score"] < 0:
                self.course.api.course_action["action"]["score"] = round(random.random() * 20 + 30)
            elif self.course.api.course_action["action"]["score"] < 50:
                self.course.api.course_action["action"]["score"] += 15

        if self.course.api.course_action["action"]["score"] < 0:
            self.course.api.course_action["action"]["score"] = 0

        if self.course.api.course_action["action"]["score"] > 100:
            self.course.api.course_action["action"]["score"] = 100

