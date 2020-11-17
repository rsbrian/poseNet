from operator import getitem
from functools import reduce
from api.socket import Api
from behavior_static.analysis import Analysis
import datetime
import time


class Home(object):
    def __init__(self, brain, camera):
        self.brain = brain
        self.camera = camera
        self.resolutions = [(540, 960), (360, 540)]
        self.class_name = self.__class__.__name__.lower()
        self.camera.add_writers(self.resolutions, self.class_name)
        self.error = 0
        self.number = -1
        self.try_total_times = 0
        self.state = None
        self.api = Api()
        self.analysis = Analysis(brain)
        self.api.course_action["tip"]["duration"] = 2
        self.bounding_box = self.brain.setting_calibrate_box()

    def __call__(self, leg=None):
        self.camera.save(self.resolutions)
        if self.is_body_in_box():
            self.state()
            behavior = self.analysis.predict()
            if behavior == "取消":
                self.api.course_action["action"]["quit"] = True
        else:
            try:
                self.state.reset()
            except Exception as e:
                pass
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

    def default_prepare(self, check_list):
        items = []
        for note, check_pose in check_list.items():
            item = {}
            item["name"] = note
            item["check"] = False
            items.append(item)
        return items

    def check_prepare(self, check_list, func):
        items = []
        for note, check_pose in check_list.items():
            pose_error = self.brain.is_pose(check_pose)
            item = {}
            item["name"] = note
            item["check"] = bool(not pose_error)
            if pose_error:
                func()
            items.append(item)
        return items

    def set_time(self, name):
        self.set_api(["action", name], self.get_time())

    def set_prepare_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_start_time()

    def set_start_time(self):
        time = self.get_time()
        self.set_api(["action", "startPointLastTime"], time)

    def set_alert_msg(self, mapList, val):
        self.set_api(mapList, val)
        self.set_alert_time()

    def set_alert_time(self):
        time = self.get_time()
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
