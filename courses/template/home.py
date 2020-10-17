from api.socket import Api


class Home(object):
    def __init__(self, brain, view):
        self.brain = brain
        self.view = view
        self.error = 0
        self.number = 0
        self.total_score = 0
        self.state = None
        self.api = Api()
        self.api.course_action["tip"]["duration"] = 2

    def __call__(self):
        if self.is_body_in_box():
            self.state()
        return self

    def is_body_in_box(self):
        return self.brain.human.points != {} and self.view.calibrate_human_body()

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
