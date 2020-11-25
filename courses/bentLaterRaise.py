import time
import datetime

from utils.counter import Counter
from courses.template.home import Home
from courses.template.prepare import PrepareTemp
from courses.template.evaluation import EvaluationTemplate
from courses.template.error_handleing import ErrorHandleingTemplate

# 俯身啞鈴反向飛鳥


class BentLaterRaise(Home):
    def __init__(self, brain, camera):
        super().__init__(brain, camera)
        self.state = Prepare(self, self.brain)

    def __call__(self):
        return super().__call__()


class Prepare(PrepareTemp):
    prepare_notes = {
        "雙腳請與肩同寬": "shoulder_width_apart",
        "膝蓋微彎、身體前傾、將手垂放到膝蓋": "hand_to_knee"
    }

    def __init__(self, course, brain):
        super().__init__(course, brain, self.prepare_notes)

    def __call__(self):
        super().__call__(PrepareTest)


class PrepareTest(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self):
        print("Preparing")
        self.course.api.course_action["action"]["alert"] = ["請回到預備動作重新開始"]
        self.course.set_time("alertLastTime")
        self.course.set_time("startPointLastTime")
        if self.brain.is_pose("shoulder_width_apart"):
            print("雙腳請與肩同寬")
            self.course.api.course_action["action"]["alert"] = ["雙腳請與肩同寬"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")

        elif self.brain.is_pose("hand_to_knee"):
            print("膝蓋微彎、身體前傾、將手垂放到膝蓋")
            self.course.api.course_action["action"]["alert"] = [
                "膝蓋微彎、身體前傾、將手垂放到膝蓋"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")

        else:
            self.course.api.course_action["action"]["alert"] = ["很好，可以開始了"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.brain.reset_temp_points()
            self.course.change(
                Action(self.course, self.brain))


class Action(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self):
        print("Action")

        if self.brain.is_pose("shoulder_width_apart"):
            # print("雙腳請與肩同寬")
            self.course.api.course_action["action"]["alert"] = ["雙腳請與肩同寬"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("hands_over_shoulder"):
            print("手不要舉超過肩，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "手不要舉超過肩，請回到預備動作重新開始"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("prepare_action"):
            print("請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "請回到預備動作重新開始"]
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

        elif self.brain.is_pose("shoulder_width_apart"):
            # print("雙腳請與肩同寬")
            self.course.api.course_action["action"]["alert"] = ["雙腳請與肩同寬"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))
        elif self.brain.is_pose("prepare_action"):
            print("請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "請回到預備動作重新開始"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))
        elif self.brain.is_pose("hands_down_laterraise"):
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
            self.brain.reset_temp_points()
            self.counter.record("total")
            self.course.change(
                EvaluationScore(self.course, self.brain, self.counter))

        elif self.brain.is_pose("shoulder_width_apart"):
            # print("雙腳請與肩同寬")
            self.course.api.course_action["action"]["alert"] = ["雙腳請與肩同寬"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("hands_over_shoulder"):
            print("手不要舉超過肩，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "手不要舉超過肩，請回到預備動作重新開始"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))
        elif self.brain.is_pose("prepare_action"):
            print("請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "請回到預備動作重新開始"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))


class ErrorHandleing(ErrorHandleingTemplate):
    def __init__(self, course, brain):
        super().__init__(course, brain)
        self.check_list = ["ending"]

    def __call__(self):
        if super().__call__(self.check_list):
            self.course.change(PrepareTest(self.course, self.brain))


class EvaluationScore(EvaluationTemplate):
    def __init__(self, course, brain, counter):
        super().__init__(course, brain, counter)

    def __call__(self):
        super().__call__()
        self.course.change(Action(self.course, self.brain))
