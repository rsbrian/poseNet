import time
import datetime

from utils.counter import Counter

from courses.template.home import Home
from courses.template.evaluation import EvaluationTemplate
from courses.template.error_handleing import ErrorHandleingTemplate
# 單臂啞鈴過頂深蹲


class BarbellOverheadSquat(Home):
    def __init__(self, brain, view):
        super().__init__(brain, view)
        self.state = Prepare(self, self.brain)

    def __call__(self):
        return super().__call__(leg="leg")


class Prepare(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain
        self.counter = Counter()

    def __call__(self):
        print("Preparing")
        self.counter.start()
        if self.brain.is_pose("raised_with_one_hand"):
            # print("請將持啞鈴手舉起並貼緊耳朵")
            self.course.api.course_action["tip"]["note"] = ["請將持啞鈴手舉起並貼緊耳朵"]
            self.counter.reset()

        elif self.brain.is_pose("spread_feet"):
            # print("雙腳略張開")
            self.course.api.course_action["tip"]["note"] = ["雙腳略張開"]
            self.counter.reset()

        elif self.is_ready_to_start():
            self.course.api.course_action["start"] = True
            self.brain.reset_temp_points()
            self.course.change(
                Action(self.course, self.brain))

    def is_ready_to_start(self):
        self.course.api.course_action["tip"]["note"] = [
            f"很好請保持"]
        self.course.set_time("lastTime")
        self.course.set_time("startPoint")
        return self.counter.result() > 3


class Action(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self):
        print("Action")

        if self.brain.is_pose("hands_up_down"):
            # print("Bar1 Open")
            self.course.set_time("lastTime")
            self.course.set_time("startPoint")
            self.course.change(
                HandsUp(self.course, self.brain))
                

class HandsUp(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain
        self.counter = Counter()

    def __call__(self):
        print('HandsUp')

        self.counter.start()
        if self.brain.is_pose("ending_down"):
            if self.is_time_small_than(0.8):
                print("你沒有要開始就不要亂動")
            self.course.api.course_action["action"]["alert"] = ["蹲的不夠低不列入次數"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(Action(self.course, self.brain))

        elif self.brain.is_pose("hands_down_overheadsquat"):
            # print("Bar1 Close", self.counter.result())
            # print("Bar2 Open")
            self.counter.record("up")
            self.course.change(
                HandsDown(self.course, self.brain, self.counter))
       

    def is_time_small_than(self, time_threshold):
        time = self.counter.result()
        return time < time_threshold and time != 0.0


class HandsDown(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter

    def __call__(self):
        print("HandsDown")

        self.counter.start()
        if self.brain.is_pose("ending_down"):
            # print("Bar2 Close", self.counter.result())
            # self.brain.reset_temp_points()
            self.counter.record("total")
            self.course.change(
                EvaluationScore(self.course, self.brain, self.counter))
        
        
class Evaluation(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter

    def __call__(self):
        print("Evaluation")
        total_time = self.counter.get_logs()["total"]

        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")

        if total_time < 1.2:
            # print("太快了，請放慢速度")
            self.course.api.course_action["action"]["alert"] = ["太快了，請放慢速度"]
        elif total_time < 2.5:
            # print("完美")
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            # print("太慢了，請加快速度")
            self.course.api.course_action["action"]["alert"] = ["太慢了，請加快速度"]

        self.course.api.course_action["action"]["times"] += 1

        self.course.change(
            Action(self.course, self.brain))


class ErrorHandleing(ErrorHandleingTemplate):
    def __init__(self, course, brain):
        super().__init__(course, brain)
        self.check_list = ["ending_down"]

    def __call__(self):
        if super().__call__(self.check_list):
            self.course.change(Action(self.course, self.brain))


class EvaluationScore(EvaluationTemplate):
    def __init__(self, course, brain, counter):
        super().__init__(course, brain, counter)

    def __call__(self):
        super().__call__()
        self.course.change(Action(self.course, self.brain))
