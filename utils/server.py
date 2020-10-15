from urllib.parse import unquote

from courses.barbellOverheadSquat import BarbellOverheadSquat
from courses.bentRow import BentRow
from courses.bentLaterRaise import BentLaterRaise
from courses.bentLegPushHip import BentLegPushHip
from courses.noCourse import NoCourse
from courses.laterRaise import LaterRaise
from courses.bicepsCurl import BicepsCurl
from courses.shoulderPress import ShoulderPress
from courses.turnBicepsCurl import TurnBicepsCurl
from courses.sumoDeadlift import SumoDeadlift
from courses.sideLunge import SideLunge
from courses.shoulderPressSit import ShoulderPressSit
from courses.frontRaise import FrontRaise
from courses.gobletSquat import GobletSquat
from courses.hammerCurl import HammerCurl
from courses.recumbentbird import Recumbentbird
from courses.recumbentChestPress import RecumbentChestPress

class Server(object):
    def __init__(self):
        self.course_template = {
            "首頁": NoCourse,
            "啞鈴彎舉": BicepsCurl,
            "二頭彎曲": TurnBicepsCurl,
            "啞鈴肩推": ShoulderPress,
            "站姿側平舉": LaterRaise,
            "俯身啞鈴後划船": BentRow,
            "俯身啞鈴反向飛鳥": BentLaterRaise,
            "曲腿挺髖": BentLegPushHip,
            "單臂啞鈴過頂深蹲": BarbellOverheadSquat,
            "斜躺啞鈴胸推": RecumbentChestPress,
            "斜躺啞鈴飛鳥": Recumbentbird,
            "錘式彎曲啞鈴": HammerCurl,
            "相撲硬拉深蹲": SumoDeadlift,
            "啞鈴側弓步蹲": SideLunge,
            "坐立肩推上提": ShoulderPressSit,
            "高腳杯寬腿深蹲": GobletSquat,
            "雙手交替前舉": FrontRaise
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
            print('course_name: ', self.course_name)
            print('course_template: ', self.course_template)

            if "高腳杯寬腿深蹲" in self.course_name:
                self.course_name = "高腳杯寬腿深蹲"

            self.course_name_cache = self.course_name
            self.course = self.course_template[self.course_name](brain, view)

        return self.course

    def set_api(self, msg):
        self.function = msg["function"]

        if self.function == "endExercise":
            self.default()

        elif self.function == "uploadCourse":
            self.course_name = unquote(msg["name"])
