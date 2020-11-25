import random


class EvaluationTemplate(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter

    def __call__(self):
        print("Evaluation")
        total_time = self.counter.get_logs()["total"]

        if total_time < 1.2:
            self.course.api.course_action["action"]["alert"] = ["不錯"]
        elif total_time < 2.5:
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            self.course.api.course_action["action"]["alert"] = ["不錯"]

        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")
        self.course.api.course_action["action"]["times"] += 1
        self.course.api.course_action["action"]["score"] = round(
            self.course.api.course_action["action"]["times"] /\
            (self.course.api.course_action["action"]["times"] + \
            self.course.try_total_times) * 100, 1
        )
