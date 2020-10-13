from urllib.parse import unquote

from courses.barbellOverheadSquat import BarbellOverheadSquat
from courses.bentRow import BentRow
from courses.bentLaterRaise import BentLaterRaise
from courses.bentLegPushHip import BentLegPushHip

from courses.noCourse import NoCourse
from courses.laterRaise import LaterRaise
from courses.bicepsCurl import BicepsCurl
from courses.shoulderPress import ShoulderPress


class Server(object):
    def __init__(self):
        self.course_template = {
            "首頁": NoCourse,
            "啞鈴彎舉": BicepsCurl,
            "啞鈴肩推": ShoulderPress,
            "站姿側平舉": LaterRaise,
            "俯身啞鈴後划船": BentRow,
            "俯身啞鈴反向飛鳥": BentLaterRaise,
            "曲腿挺髖": BentLegPushHip,
            "單臂啞鈴過頂深蹲": BarbellOverheadSquat
        }
        self.default()
        self.course_name_cache = None

    def default(self):
        self.function = "home"
        self.course_name = "首頁"

    def is_course_need_to_change(self):
        return self.course_name_cache != self.course_name

    def get_route(self, brain, view):
        if self.is_course_need_to_change():
            self.course_name_cache = self.course_name
            self.course = self.course_template[self.course_name](brain, view)

        return self.course

    def set_api(self, msg):
        print(msg)
        self.function = msg["function"]

        if self.function == "endExercise":
            self.default()

        elif self.function == "uploadCourse":
            self.course_name = unquote(msg["name"])
