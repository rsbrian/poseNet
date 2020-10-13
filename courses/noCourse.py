from api.socket import Api


class NoCourse(object):
    def __init__(self, brain, view):
        self.api = Api()
        self.brain = brain
        self.view = view
        self.stored_api = []
        self.action = None

    def __call__(self):
        # if self.is_body_in_box():
        self.choose_action()
        return self

    def is_body_in_box(self):
        return self.brain.human.points != {} and self.view.calibrate_human_body()

    def choose_action(self):
        if self.brain.is_pose("cancel"):
            self.set_api("最後動作", "雙手交叉")
        elif self.brain.is_pose("click"):
            self.set_api("最後動作", "雙手彎舉")
        elif self.brain.is_pose("next"):
            self.set_api("最後動作", "右手彎舉")
        elif self.brain.is_pose("back"):
            self.set_api("最後動作", "左手彎舉")
        else:
            self.set_api("最後動作", "")

    def filtered(self, api):
        temp = api.copy()
        self.stored_api.append(temp)
        if len(self.stored_api) > 3:
            self.stored_api = self.stored_api[1:]
            if self.stored_api[0]["最後動作"] == "雙手彎舉" and self.stored_api[2]["最後動作"] == "雙手彎舉":
                self.stored_api[1]["最後動作"] = "雙手彎舉"
        check = all([action["最後動作"] for action in self.stored_api[:2]])
        if not check:
            self.action = None
            api["最後動作"] = ""
        elif self.action is None:
            self.action = ""
        else:
            api["最後動作"] = ""
        return api

    def get_api(self):
        return self.filtered(self.api.behavior)

    def set_api(self, column_name, behavior_name):
        self.api.behavior[column_name] = behavior_name
