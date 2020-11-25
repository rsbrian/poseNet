import time
import datetime

from utils.counter import Counter

from courses.template.home import Home
from courses.template.prepare import PrepareTemp
from courses.template.evaluation import EvaluationTemplate
from courses.template.error_handleing import ErrorHandleingTemplate

# 單(右)手划船


class OneArmDubbleRowRight(Home):
    def __init__(self, brain, camera):
        super().__init__(brain, camera)
        self.state = Prepare(self, self.brain)
        self.bounding_box = self.brain.setting_calibrate_box_leg()

    def __call__(self):
        self.camera.save(self.resolutions)
        self.state()
        behavior = self.analysis.predict()
        if behavior == "取消":
            self.api.course_action["action"]["quit"] = True
        return self


class Prepare(PrepareTemp):
    prepare_notes = {
        "請將左腳往前踏右腳向後伸​": "front_left_feet",
        #"請將左手至於大腿上並將身體向前傾": "left_hand_feet",
        "將右手自然垂放": "drop_hand_natrually_right"
    }

    def __init__(self, course, brain):
        super().__init__(course, brain, self.prepare_notes)

    def __call__(self):
        print("Preparing")
        super().__call__(Action)


class Action(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self):
        print("Action")

        if self.brain.is_pose("front_left_feet"):
            # print("請將左腳往前踏右腳向後伸")
            self.course.api.course_action["action"]["alert"] = ["請將左腳往前踏右腳向後伸"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))
        elif self.brain.is_pose("right_elbow_expansion"):
            print("右手肘外擴了，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "右手肘外擴了，請回到預備動作重新開始"]
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
        elif self.brain.is_pose("hands_up_right"):
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
        if self.brain.is_pose("ending_right"):
            if self.is_time_small_than(0.8):
                print("你沒有要開始就不要亂動")
            self.course.api.course_action["action"]["alert"] = ["舉的不夠高不列入次數"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(Action(self.course, self.brain))

        elif self.brain.is_pose("front_left_feet"):
            # print("請將左腳往前踏右腳向後伸")
            self.course.api.course_action["action"]["alert"] = ["請將左腳往前踏右腳向後伸"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("right_elbow_expansion"):
            # print("右手肘外擴了，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "右手肘外擴了，請回到預備動作重新開始"]
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

        elif self.brain.is_pose("hands_down_boat_right"):
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
        if self.brain.is_pose("ending_right"):
            # print("Bar2 Close", self.counter.result())
            self.brain.reset_temp_points()
            self.counter.record("total")
            self.course.change(
                EvaluationScore(self.course, self.brain, self.counter))

        elif self.brain.is_pose("front_left_feet"):
            # print("請將左腳往前踏右腳向後伸")
            self.course.api.course_action["action"]["alert"] = ["請將左腳往前踏右腳向後伸"]
            self.course.set_time("alertLastTime")
            self.course.set_time("startPointLastTime")
            self.course.change(
                ErrorHandleing(self.course, self.brain))

        elif self.brain.is_pose("right_elbow_expansion"):
            # print("右手肘外擴了，請回到預備動作重新開始")
            self.course.api.course_action["action"]["alert"] = [
                "右手肘外擴了，請回到預備動作重新開始"]
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
            self.course.api.course_action["action"]["alert"] = ["不錯"]
        elif total_time < 2.5:
            # print("完美")
            self.course.api.course_action["action"]["alert"] = ["完美"]
        else:
            # print("太慢了，請加快速度")
            self.course.api.course_action["action"]["alert"] = ["不錯"]

        self.course.api.course_action["action"]["times"] += 1

        self.course.change(
            Action(self.course, self.brain))


class ErrorHandleing(ErrorHandleingTemplate):
    def __init__(self, course, brain):
        super().__init__(course, brain)
        self.check_list = ["ending_right"]

    def __call__(self):
        if super().__call__(self.check_list):
            self.course.change(PrepareTest(self.course, self.brain))


class EvaluationScore(EvaluationTemplate):
    def __init__(self, course, brain, counter):
        super().__init__(course, brain, counter)

    def __call__(self):
        super().__call__()
        self.course.change(Action(self.course, self.brain))
