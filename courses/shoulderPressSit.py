import time
import datetime

from api.socket import Api
from utils.counter import Counter
# 坐立肩推上提


class ShoulderPressSit(object):
    def __init__(self, brain, view):
        self.api = Api()
        self.brain = brain
        self.view = view
        self.state = Prepare(self, self.brain)
        self.api.course_action["tip"]["duration"] = 2
        self.error = 0
        self.total_score = 0

    def __call__(self):
        if self.is_body_in_box():
            self.state()
        return self

    def is_body_in_box(self):
        return self.brain.human.points != {} and self.view.calibrate_human_body()

    def change(self, new_state):
        self.state = new_state

    def get_api(self):
        return self.api.course_action

    def set_time(self, name):
        self.api.course_action["action"][name] = datetime.datetime.now().strftime(
            "%Y/%m/%d %H:%M:%S.%f")


class Prepare(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain
        self.counter = Counter()

    def __call__(self):
        print("Preparing")
        self.counter.start()
        if self.brain.is_pose("sit_down"):
            # print("坐姿，腹部收緊")
            self.course.api.course_action["tip"]["note"] = ["坐姿，腹部收緊"]
            self.counter.reset()

        elif self.brain.is_pose("hold_dumbbel_shoulder"):
            # print("雙手持啞鈴於肩膀兩側")
            self.course.api.course_action["tip"]["note"] = ["雙手持啞鈴於肩膀兩側"]
            self.counter.reset()

        elif self.is_ready_to_start():
            self.course.api.course_action["start"] = True
            self.brain.reset_temp_points()
            self.course.change(
                Action(self.course, self.brain))

    def is_ready_to_start(self):
        # print("很好請保持", self.counter.result())
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

        if self.brain.is_pose("sit_down"):
            # print("坐姿，腹部收緊")
            self.course.api.course_action["action"]["alert"] = ["坐姿，腹部收緊"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("hands_up"):
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
        if self.brain.is_pose("ending"):
            if self.is_time_small_than(0.8):
                print("你沒有要開始就不要亂動")
            self.course.api.course_action["action"]["alert"] = ["舉的不夠高不列入次數"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(Action(self.course, self.brain))

        elif self.brain.is_pose("sit_down"):
            # print("坐姿，腹部收緊")
            self.course.api.course_action["action"]["alert"] = ["坐姿，腹部收緊"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("hands_down_shoulderpress"):
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
        if self.brain.is_pose("ending"):
            # print("Bar2 Close", self.counter.result())
            self.counter.record("total")
            self.course.change(
                EvaluationScore(self.course, self.brain, self.counter))

        elif self.brain.is_pose("hand_too_straight"):
            print("手打太直了，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "手打太直了，請回到預備動作重新開始"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("sit_down"):
            # print("坐姿，腹部收緊")
            self.course.api.course_action["action"]["alert"] = ["坐姿，腹部收緊"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))


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


class ErrorHandleing(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self):
        if self.brain.is_pose("ending"):
            self.course.error += 1
            self.brain.reset_temp_points()
            self.course.change(Action(self.course, self.brain))


class EvaluationScore(object):
    def __init__(self, course, brain, counter):
        self.course = course
        self.brain = brain
        self.counter = counter

        self.weights = [2, 6, 4]
        self.history = {
            "fast": 0,
            "perfect": 0,
            "slow": 0,
        }

    def __call__(self):
        print("Evaluation")
        total_time = self.counter.get_logs()["total"]

        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")

        if total_time < 1.2:
            self.history["fast"] += 1
            self.course.api.course_action["action"]["alert"] = ["太快了，請放慢速度"]
        elif total_time < 2.5:
            self.history["perfect"] += 1
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            self.history["slow"] += 1
            self.course.api.course_action["action"]["alert"] = ["太慢了，請加快速度"]

        self.course.api.course_action["action"]["times"] += 1

        if self.finished:
            self.calcScore()

        self.course.change(
            Action(self.course, self.brain))

    def finished(self):
        return self.course.api.course_action["action"]["times"] == 6

    def calcScore(self):
        total_score = 0
        for i, (key, value) in enumerate(self.history.items()):
            self.course.total_score += self.weights[i] * value

        print(self.course.total_score)
        print(self.course.error)
        print(self.course.total_score - self.course.error)
