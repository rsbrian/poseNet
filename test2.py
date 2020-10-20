from operator import getitem
from functools import reduce
import copy
import time
import datetime
from utils.counter import Counter

TEMPLATES = {
    "雙腳請與肩同寬": "shoulder_width_apart",
    "請將手自然垂放": "drop_hand_natrually"
}


class Api(object):
    def __init__(self):
        self._course_action = {
            "function": "getExercise",
            "tip": {"note": [""], "duration": 0},
            "action": {
                "alert": [""],
                "alertLastTime": "",
                "startPoint": "",
                "startPointLastTime": "",
                "lastTime": "",
                "times": 0,
                "stop": False,
                "quit": False,
                "score": 0
            },
            "start": False,
        }

    @property
    def course_action(self):
        return self._course_action

    @course_action.setter
    def course_action(self, key, value):
        self._course_action[key] = value


class Basic(object):
    def __init__(self):
        self.api = Api()
        self.state = None

    def __call__(self):
        self.state()
        return self

    def change(self, new_state):
        self.state = new_state

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

    def set_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_time("lastTime")
        self.set_time("startPoint")


class BicepsCurl(Basic):
    def __init__(self):
        super().__init__()
        self.state = Prepare(self)

    def __call__(self):
        return super().__call__()


class Prepare(object):
    def __init__(self, course):
        self.course = course
        self.counter = Counter()

    def __call__(self):
        self.course.set_msg(["tip", "note"], "x")


b = BicepsCurl()
api = b.get_api()
print(api)
print()
b()
api = b.get_api()
print(api)
