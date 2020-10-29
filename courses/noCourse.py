from api.socket import Api
from behavior.analysis import Analysis


class NoCourse(object):
    def __init__(self, brain, view):
        self.api = Api()
        self.brain = brain
        self.view = view
        self.analysis = Analysis(self.brain)

    def __call__(self):
        if self.is_body_in_box():
            behavior = self.analysis.predict()
            self.set_api("最後動作", behavior)
        return self

    def is_body_in_box(self):
        return self.view.calibrate_human_body()

    def get_api(self):
        return self.api.behavior

    def set_api(self, column_name, behavior_name):
        self.api.behavior[column_name] = behavior_name
