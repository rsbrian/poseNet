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
from courses.thruster import Thruster
from courses.alternateShoulderPress import AlternateShoulderPress
from courses.oneArmDubbleRowRight import OneArmDubbleRowRight
from courses.oneArmDubbleRowLeft import OneArmDubbleRowLeft
from courses.splitSquatRight import SplitSquatRight
from courses.splitSquatLeft import SplitSquatLeft
from courses.doubleFrontRaise import DoubleFrontRaise
from courses.pushPress import PushPress
from courses.liftAndChopLeft import LiftAndChopLeft
from courses.liftAndChopRight import LiftAndChopRight
from courses.overheadTricepExtension import OverheadTricepExtension
from courses.stepRight import StepRight
from courses.stepLeft import StepLeft

class Server(object):
    def __init__(self):
        self.course_template = {
            "首頁": NoCourse,
            # Test
            "跳躍": LaterRaise,
            "滑雪": LaterRaise,
            "上斜伏地挺身": LaterRaise,

            # Shoulder
            "側平舉": LaterRaise,
            "雙手交替前舉": FrontRaise,
            "肩上交替推舉": AlternateShoulderPress, #ok
            "雙手前平舉": DoubleFrontRaise, #ok
            "借力推舉": PushPress, #ok
            # Arm
            "雙手錘式彎舉": BicepsCurl,
            "雙手彎舉": BicepsCurl,
            "雙手過頂伸展": OverheadTricepExtension, # ok
            # Chest
            "上斜臥推": RecumbentChestPress,
            # Back
            "單(右)手划船": OneArmDubbleRowRight, # wrong
            "單(左)手划船": OneArmDubbleRowLeft, # wrong
            # Hip
            "羅馬尼亞硬舉": BentLegPushHip, # 曲腿挺髖
            # Leg
            "分腿蹲(右)": SplitSquatRight, # ok
            "分腿蹲(左)": SplitSquatLeft, # ok
            "火箭推舉": Thruster, # ok
            "徒手登階(右)": StepRight,
            "徒手登階(左)": StepLeft,
            # 核心
            "伐木(左)": LiftAndChopLeft, #ok 
            "伐木(右)": LiftAndChopRight, #ok

            # No
            "相撲深蹲": SumoDeadlift, # 相撲硬拉深蹲
            "啞鈴肩推": ShoulderPress,
            "斜躺啞鈴飛鳥": Recumbentbird,
            "俯身啞鈴反向飛鳥": BentLaterRaise,
            "俯身啞鈴後划船": BentRow,
            "啞鈴側弓步蹲": SideLunge,
            "坐立肩推上提": ShoulderPressSit,#ShoulderPressSit, # 坐立肩推上提
            "二頭彎曲": TurnBicepsCurl,
            "高腳杯深蹲": GobletSquat,
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
            self.course_name_cache = self.course_name
            self.course = self.course_template[self.course_name](brain, camera)
        return self.course

    def set_api(self, msg):
        self.function = msg["function"]

        if self.function == "endExercise":
            self.default()

        elif self.function == "uploadCourse":
            self.course_name = unquote(msg["name"])
