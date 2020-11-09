from urllib.parse import unquote

from courses.bentRow import BentRow
from courses.noCourse import NoCourse
from courses.sideLunge import SideLunge
from courses.hammerCurl import HammerCurl
from courses.bicepsCurl import BicepsCurl
from courses.laterRaise import LaterRaise
from courses.frontRaise import FrontRaise
from courses.gobletSquat import GobletSquat
from courses.recumbentbird import Recumbentbird
from courses.sumoDeadlift import SumoDeadlift
from courses.shoulderPress import ShoulderPress
from courses.turnBicepsCurl import TurnBicepsCurl
from courses.bentLaterRaise import BentLaterRaise
from courses.bentLegPushHip import BentLegPushHip
from courses.shoulderPressSit import ShoulderPressSit
from courses.recumbentChestPress import RecumbentChestPress
from courses.barbellOverheadSquat import BarbellOverheadSquat


class Server(object):
    def __init__(self):
        self.course_template = {
            "首頁": NoCourse,
            "啞鈴彎舉": BicepsCurl,
            "站姿側平舉": LaterRaise,
            "俯身啞鈴後划船": BentRow,
            "啞鈴側弓步蹲": SideLunge,
            "啞鈴肩推": ShoulderPress,
            "雙手交替前舉": FrontRaise,
            "錘式彎曲啞鈴": HammerCurl,
            "二頭彎曲": TurnBicepsCurl,
            "曲腿挺髖": BentLegPushHip,
            "相撲硬拉深蹲": SumoDeadlift,
            "高腳杯寬腿深蹲": GobletSquat,
            "斜躺啞鈴飛鳥": Recumbentbird,
            "坐立肩推上提": ShoulderPressSit,
            "俯身啞鈴反向飛鳥": BentLaterRaise,
            "斜躺啞鈴胸推": RecumbentChestPress,
            "單臂啞鈴過頂深蹲": BarbellOverheadSquat,
        }
        self.default()
        self.course_name_cache = None

    def default(self):
        self.function = "home"
        self.course_name = "首頁"

    def is_course_need_to_change(self):
        return self.course_name_cache != self.course_name

    def get_route(self, brain, camera):
        if self.is_course_need_to_change():
            if "高腳杯寬腿深蹲" in self.course_name:
                self.course_name = "高腳杯寬腿深蹲"
            self.course_name_cache = self.course_name
            self.course = self.course_template[self.course_name](brain, camera)
        return self.course

    def set_api(self, msg):
        self.function = msg["function"]

        if self.function == "endExercise":
            self.default()

        elif self.function == "uploadCourse":
            self.course_name = unquote(msg["name"])
