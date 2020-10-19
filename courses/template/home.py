from operator import getitem
from functools import reduce
from api.socket import Api


class Home(object):
    def __init__(self, brain, view):
        self.brain = brain
        self.view = view
        self.error = 0
        self.number = -1
        self.total_score = 0
        self.state = None
        self.api = Api()
        self.api.course_action["tip"]["duration"] = 2

    def __call__(self, leg=None):
        if self.is_body_in_box(leg):
            self.state()
            print(self.api.course_action["action"]["score"])
            points = self.brain.get_test_points()
            behavior = self.analysis.predict(points, self.brain.face)
            self.set_api("最後動作", behavior)
        return self

    def is_body_in_box(self, leg):
        c = self.brain.human.points != {}
        c1 = self.view.calibrate_human_body_leg() and c
        c2 = self.view.calibrate_human_body() and c
        if leg is None:
            return c2
        else:
            return c1

    def change(self, new_state):
        self.state = new_state

    def set_start_time(self):
        self.set_time("lastTime")
        self.set_time("startPoint")

    def set_prepare_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_start_time()

    def set_alert_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_time("alertLastTime")
        self.set_time("startPointLastTime")

    def set_api(self, mapList, val):
        reduce(
            getitem, mapList[:-1],
            self.api.course_action)[mapList[-1]] = val
        return self.api.course_action

    def get_api(self):
        return self.api.course_action

    def set_time(self, name):
        time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S.%f")
        self.set_api(["action", name], time)
