from operator import getitem
from functools import reduce
from api.socket import Api
from behavior.analysis import Analysis
import datetime
import time


class Canceling(object):
    def __init__(self, home, brain, analysis):
        self.home = home
        self.brain = brain
        self.analysis = analysis
        self.start_time = time.time()
        self.end_time = None

    def __call__(self):
        self.end_time = time.time()
        processing_time = self.result()
        behavior = self.analysis.predict()
        if self.analysis.both_hand_move():
            self.home.change_cancel_state(
                NotCancel(self.home, self.brain, self.analysis))

        if processing_time > 2.5:
            self.home.api.course_action["action"]["quit"] = True

    def result(self):
        return self.end_time - self.start_time


class NotCancel(object):
    def __init__(self, home, analysis):
        self.home = home
        self.analysis = analysis

    def __call__(self):
        behavior = self.analysis.predict()
        if behavior == "取消":
            self.home.api.course_action["action"]["quit"] = True

class Home(object):
    def __init__(self, brain, camera):
        self.brain = brain
        self.camera = camera
        self.error = 0
        self.number = -1
        self.try_total_times = 0
        self.state = None
        self.api = Api()
        self.analysis = Analysis(brain)
        self.api.course_action["tip"]["duration"] = 2
        self.bounding_box = self.brain.setting_calibrate_box()
        self.cancel_state = NotCancel(self, self.analysis)

    def __call__(self, leg=None):
        if self.is_body_in_box():
            self.state()
            self.camera.save(self.camera.original_img, "only_in_box")
            print(self.api.course_action["action"]["score"])
            self.cancel_state()
        return self

    def change_cancel_state(self, new_state):
        self.cancel_state = new_state

    def is_body_in_box(self):
        c = self.brain.human.points != {}
        c1 = self.brain.calibrate_human_body(self.bounding_box)
        return c and c1

    def get_bounding_box(self):
        return self.bounding_box

    def change(self, new_state):
        self.state = new_state

    def set_prepare_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_start_time()

    def set_start_time(self):
        time = self.get_time()
        self.set_api(["tip", "lastTime"], time)
        self.set_api(["tip", "startPoint"], time)

    def set_alert_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_alert_time()

    def set_alert_time(self):
        time = self.get_time()
        self.set_api(["action", "alertLastTime"], time)
        self.set_api(["action", "startPointLastTime"], time)

    def set_api(self, mapList, val):
        reduce(
            getitem, mapList[:-1],
            self.api.course_action)[mapList[-1]] = val
        return self.api.course_action

    def get_api(self):
        return self.api.course_action

    def get_time(self):
        return datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")