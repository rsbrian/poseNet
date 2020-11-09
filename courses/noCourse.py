from api.socket import Api
from behavior.analysis import Analysis


class NoCourse(object):
    def __init__(self, brain, camera):
        self.api = Api()
        self.brain = brain
        self.camera = camera
        self.analysis = Analysis(brain)
        self.bounding_box = self.brain.setting_calibrate_box()

    def __call__(self):
        self.analysis.thres = None
        self.set_api("最後動作", "")
        if self.is_body_in_box():
            self.camera.save(self.camera.original_img, "only_in_box")
            behavior = self.analysis.predict()
            self.set_api("最後動作", behavior)
        return self

    def is_body_in_box(self):
        c = self.brain.human.points != {}
        c1 = self.brain.calibrate_human_body(self.bounding_box)
        return c and c1

    def get_thres(self):
        return self.analysis.get_thres()

    def get_bounding_box(self):
        return self.bounding_box

    def get_api(self):
        return self.api.behavior

    def set_api(self, column_name, behavior_name):
        self.api.behavior[column_name] = behavior_name
