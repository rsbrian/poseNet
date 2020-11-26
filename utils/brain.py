import copy
from api.human import Human


class Brain(object):
    def __init__(self, args):
        self.args = args
        self.human = Human()

        self.stored_points = []
        self.stored_angles = []

        self.count_next = 0
        self.count_back = 0

    def get_points(self, name):
        return self.human.points[name]

    def reset_temp_points(self):
        self.human.temp_points = self.human.points

    def reset_state(self, points, angles):
        self.human.points = points
        self.human.angles = angles

    def add_median_filter(self):
        self.stored_points.append(copy.deepcopy(self.human.points))
        self.stored_angles.append(copy.deepcopy(self.human.angles))

        if len(self.stored_points) > 8:
            self.stored_points = self.stored_points[1:]
            self.stored_angles = self.stored_angles[1:]
            self.median_filter(self.stored_points, self.human.points)
            self.median_filter(self.stored_angles, self.human.angles)

    def median_filter(self, listed_points, new_list):
        median = len(listed_points) // 2
        for key in listed_points[0].keys():
            if "temp" in key:
                continue
            newlist = sorted(listed_points, key=lambda x: x[key])
            value = newlist[median].get(key)
            new_list[key] = value

    def compare(self, name, ops, param):
        try:
            if ops == ">":
                return self.human.points[name] > param
            elif ops == "<":
                return self.human.points[name] < param
            else:
                return self.human.points[name] == param
        except Exception as e:
            pass

    def noabs_compare(self, nameA, nameB, ops, param, buff=0):
        try:
            if ops == ">":
                return self.human.points[nameA] - self.human.points[nameB] > (param - buff)
            elif ops == "<":
                return self.human.points[nameA] - self.human.points[nameB] < (param - buff)
            else:
                return self.human.points[nameA] - self.human.points[nameB] == (param - buff)
        except Exception as e:
            pass

    def abs_compare(self, nameA, nameB, ops, param, buff=0):
        try:
            if ops == ">":
                return abs(self.human.points[nameA] - self.human.points[nameB]) > (param - buff)
            elif ops == "<":
                return abs(self.human.points[nameA] - self.human.points[nameB]) < (param - buff)
            else:
                return abs(self.human.points[nameA] - self.human.points[nameB]) == (param - buff)
        except Exception as e:
            pass

    def setting_calibrate_box(self):
        if self.args.cam_height < self.args.cam_width:
            segment_width = self.args.cam_height // 3
            segment_height = self.args.cam_width // 6
        else:
            segment_width = self.args.cam_width // 3
            segment_height = self.args.cam_height // 6

        x1 = segment_width * 1 + 10  # 1
        x2 = segment_width * 2 - 10  # 2
        y1 = segment_height * 4 + 50  # 4
        y2 = segment_height * 5 + 100  # 5
        return (x1, x2, y1, y2)

    def setting_calibrate_box_leg(self):
        x1, x2, y1, y2 = self.setting_calibrate_box()
        x1 = x1 - 80
        x2 = x2 + 80
        return (x1, x2, y1, y2)

    def calibrate_human_body(self, coor):
        x1, x2, y1, y2 = coor
        c1 = self.compare("left_ankle_x", ">", x1) and \
            self.compare("left_ankle_x", "<", x2)
        c2 = self.compare("right_ankle_x", ">", x1) and \
            self.compare("right_ankle_x", "<", x2)
        c3 = self.compare("left_ankle_y", ">", y1) and \
            self.compare("left_ankle_y", "<", y2)
        c4 = self.compare("left_ankle_y", ">", y1) and \
            self.compare("left_ankle_y", "<", y2)
        return c1 and c2 and c3 and c4

    def is_pose(self, name):
        return self.pose_template()[name]()

    def pose_template(self):
        return {
            "prepare_action": self.prepare_action,
            "shoulder_width_apart": self.shoulder_width_apart,
            "drop_hand_natrually": self.drop_hand_natrually,
            "drop_hand_natrually_right": self.drop_hand_natrually_right,
            "drop_hand_natrually_left": self.drop_hand_natrually_left,
            "front_left_feet": self.front_left_feet,
            "front_right_feet": self.front_right_feet,
            "left_hand_feet": self.left_hand_feet,
            "right_hand_feet": self.right_hand_feet,
            "hands_over_shoulder": self.hands_over_shoulder,
            "hands_over_shoulder_front": self.hands_over_shoulder_front,
            "lying_down": self.lying_down,
            "hold_dumbbel_shoulder": self.hold_dumbbel_shoulder,
            "raised_with_one_hand": self.raised_with_one_hand,
            "raised_with_one_hand_simple": self.raised_with_one_hand_simple,
            "hold_dumbbells_on_chest": self.hold_dumbbells_on_chest,
            "hold_dumbbells_on_abdomen": self.hold_dumbbells_on_abdomen,
            "hold_dumbbells_on_shoulder": self.hold_dumbbells_on_shoulder,
            "hold_dumbbells_on_brain": self.hold_dumbbells_on_brain,
            "hold_rightfeet_on_step": self.hold_rightfeet_on_step,
            "hold_leftfeet_on_step": self.hold_leftfeet_on_step,
            "keep_body_stable": self.keep_body_stable,
            "spread_feet": self.spread_feet,
            "hand_to_knee": self.hand_to_knee,
            "sit_down": self.sit_down,
            "left_elbow_expansion": self.left_elbow_expansion,
            "right_elbow_expansion": self.right_elbow_expansion,
            "hand_too_straight": self.hand_too_straight,
            "left_elbow_moved": self.left_elbow_moved,
            "right_elbow_moved": self.right_elbow_moved,
            "knee_to_toe": self.knee_to_toe,
            "hands_lower_than_shoulder": self.hands_lower_than_shoulder,
            "heands_track_is_wrong": self.heands_track_is_wrong,
            "hands_up": self.hands_up,
            "hands_up_down": self.hands_up_down,
            "hands_up_left": self.hands_up_left,
            "hands_up_right": self.hands_up_right,
            "hands_up_downleft": self.hands_up_downleft,
            "hands_up_downright": self.hands_up_downright,
            "hands_up_left_feet": self.hands_up_left_feet,
            "hands_up_right_feet": self.hands_up_right_feet,
            "hands_down": self.hands_down,
            "hands_down_left": self.hands_down_left,
            "hands_down_right": self.hands_down_right,
            "hands_down_downleft": self.hands_down_downleft,
            "hands_down_downright": self.hands_down_downright,
            "hands_down_front": self.hands_down_front,
            "hands_down_frontleft": self.hands_down_frontleft,
            "hands_down_frontright": self.hands_down_frontright,
            "hands_down_boat": self.hands_down_boat,
            "hands_down_boat_left": self.hands_down_boat_left,
            "hands_down_boat_right": self.hands_down_boat_right,
            "hands_down_laterraise": self.hands_down_laterraise,
            "hands_down_shoulderpress": self.hands_down_shoulderpress,
            "hands_down_bent": self.hands_down_bent,
            "hands_down_overheadsquat": self.hands_down_overheadsquat,
            "hands_down_thruster": self.hands_down_thruster,
            "hands_down_pushpress": self.hands_down_pushpress,
            "hands_down_left_feet": self.hands_down_left_feet,
            "hands_down_right_feet": self.hands_down_right_feet,
            "hands_down_lift_left": self.hands_down_lift_left,
            "hands_down_lift_right": self.hands_down_lift_right,
            "hands_down_extension": self.hands_down_extension,
            "hands_down_step": self.hands_down_step,

            "ending": self.ending,
            "ending_left": self.ending_left,
            "ending_right": self.ending_right,
            "ending_down": self.ending_down,
            "ending_downleft": self.ending_downleft,
            "ending_downright": self.ending_downright,
            "ending_left_feet": self. ending_left_feet,
            "ending_right_feet": self. ending_right_feet

        }

    def prepare_action(self):  # 與預備動作差異太大
        return self.abs_compare("left_shoulder_x", "left_shoulder_x_temp", ">", 30) or \
            self.abs_compare("right_shoulder_x", "right_shoulder_x_temp", ">", 30) or \
            self.abs_compare("right_knee_x", "right_knee_x_temp", ">", 30) or \
            self.abs_compare(
                "left_knee_x", "left_knee_x_temp", ">", 30)  # or \
        # self.abs_compare("left_shoulder_y", "left_shoulder_y_temp", ">", 30) or \
        # self.abs_compare("right_shoulder_y", "right_shoulder_y_temp", ">", 30) or \
        # self.abs_compare("right_knee_y", "right_knee_y_temp", ">" , 30) or \
        #self.abs_compare("left_knee_y", "left_knee_y_temp", ">", 30)

    def shoulder_width_apart(self):
        return self.abs_compare("left_shoulder_x", "left_knee_x", ">", 70) or \
            self.abs_compare("right_shoulder_x", "right_knee_x", ">", 70)

    def drop_hand_natrually(self):
        return self.abs_compare("left_hip_y", "left_wrist_y", ">", 40) or \
            self.abs_compare("right_hip_y", "right_wrist_y", ">", 40)

    def drop_hand_natrually_right(self):
        return self.abs_compare("right_hip_y", "right_wrist_y", ">", 40)

    def drop_hand_natrually_left(self):
        return self.abs_compare("left_hip_y", "left_wrist_y", ">", 40) 

    def front_left_feet(self):
        return self.noabs_compare("left_ankle_y", "right_ankle_y", "<", 40)

    def front_right_feet(self):
        return self.noabs_compare("right_ankle_y", "left_ankle_y", "<", 40)

    def left_hand_feet(self):
        result = True
        if self.abs_compare("left_knee_x", "left_wrist_x", "<", 30) and \
        self.abs_compare("left_hip_x", "left_wrist_x", "<", 30):
            result = False
        return result

    def right_hand_feet(self):
        result = True
        if self.abs_compare("right_knee_x", "right_wrist_x", "<", 30) and \
        self.abs_compare("right_hip_x", "right_wrist_x", "<", 30):
            result = False
        return result

    def lying_down(self):  # 斜躺
        return self.abs_compare("right_hip_y", "right_knee_y", ">", 100) or \
            self.abs_compare("left_hip_y", "left_knee_y", ">", 100)

    def hands_over_shoulder(self):  # 手不要舉過肩膀
        return self.noabs_compare("left_shoulder_y", "left_wrist_y", ">", 60) or \
            self.noabs_compare("right_shoulder_y", "right_wrist_y", ">", 60)

    def hands_over_shoulder_front(self):
        return self.noabs_compare("left_shoulder_y", "left_elbow_y", ">", 80) or \
            self.noabs_compare("right_shoulder_y", "right_elbow_y", ">", 80)

    def left_elbow_expansion(self):  # 左手肘外擴
        return self.abs_compare("left_elbow_x", "left_elbow_x_temp", ">", 40)

    def right_elbow_expansion(self):  # 右手肘外擴
        return self.abs_compare("right_elbow_x", "right_elbow_x_temp", ">", 40)

    def hand_too_straight(self):  # 手打太直了
        return self.human.angles["right_elbow_angle"] > 170

    def hands_lower_than_shoulder(self):
        return self.noabs_compare("right_elbow_y", "right_shoulder", ">", 30) or \
            self.noabs_compare("left_elbow_y", "left_shoulder", ">", 30)

    def heands_track_is_wrong(self):
        return self.abs_compare("right_wrist_x", "right_shoulder_x", ">", 100) or \
            self.abs_compare("left_wrist_x", "left_shoulder_x", ">", 100)

    def left_elbow_moved(self):
        return self.abs_compare("left_elbow_y", "left_elbow_y_temp", ">", 40) or \
            self.abs_compare("left_elbow_x", "left_elbow_x_temp", ">", 40)

    def right_elbow_moved(self):
        return self.abs_compare("right_elbow_y", "right_elbow_y_temp", ">", 40) or \
            self.abs_compare("right_elbow_x", "right_elbow_x_temp", ">", 40)

    def knee_to_toe(self):  # 膝蓋請對其腳尖
        return self.noabs_compare("right_knee_x", "right_ankle_x", ">", 20) or \
            self.noabs_compare("left_knee_x", "left_ankle_x", "<", -20)

    def hold_dumbbel_shoulder(self):  # 雙手持啞鈴於肩膀兩側
        return self.abs_compare("right_shoulder_y", "right_wrist_y", ">", 60) or \
            self.abs_compare("left_shoulder_y", "left_wrist_y", ">", 60)
            #self.abs_compare("right_elbow_x", "right_wrist_x", ">", 50) or \
            #self.abs_compare("left_elbow_x", "left_wrist_x", ">", 50)

    def raised_with_one_hand(self):  # 持啞鈴手舉起並貼緊耳朵
        return self.human.angles["right_shoulder_angle"] < 120 and \
            self.human.angles["left_shoulder_angle"] < 120

    def raised_with_one_hand_simple(self):
        return self.noabs_compare("left_wrist_y", "left_shoulder_y", ">", -50) and \
            self.noabs_compare("right_wrist_y", "right_shoulder_y", ">", -50)

    def hold_dumbbells_on_chest(self):  # 持啞鈴於胸口
        c1 = self.abs_compare("left_wrist_x", "right_wrist_x", ">", 100)
        #c2 = self.human.angles["left_elbow_angle"] > 60
        #c3 = self.human.angles["right_elbow_angle"] > 60
        c4 = self.abs_compare("left_wrist_y", "left_shoulder_y", ">", 50)
        c5 = self.abs_compare("right_wrist_y", "right_shoulder_y", ">", 50)
        return c1 or c4 or c5

    def hold_dumbbells_on_abdomen(self):  # 持啞鈴於腹前
        c1 = self.abs_compare("left_wrist_x", "right_wrist_x", ">", 100)
        #c2 = self.human.angles["left_elbow_angle"] > 60
        #c3 = self.human.angles["right_elbow_angle"] > 60
        c4 = self.abs_compare("left_wrist_y", "left_hip_y", ">", 50)
        c5 = self.abs_compare("right_wrist_y", "right_hip_y", ">", 50)
        return c1 or c4 or c5

    def hold_dumbbells_on_shoulder(self): #將啞鈴放置於肩膀之上
        return self.human.angles["left_elbow_angle"] > 30 or \
            self.human.angles["right_elbow_angle"] > 30 or \
            self.abs_compare("left_wrist_y", "left_shoulder_y", ">", 30) or \
            self.abs_compare("right_wrist_y", "right_shoulder_y", ">", 30) 
    
    def hold_dumbbells_on_brain(self):
        return self.abs_compare("left_elbow_y", "brain_y", ">", 40) or \
            self.abs_compare("right_elbow_y", "brain_y", ">", 40) 
            #self.abs_compare("left_wrist_y", "brain_y", ">", 30) or \
            #self.abs_compare("right_wrist_y", "brain_y", ">", 30)

    def hold_rightfeet_on_step(self):
        return self.abs_compare("right_knee_y", "right_hip_y", ">", 80)

    def hold_leftfeet_on_step(self):
        return self.abs_compare("left_knee_y", "left_hip_y", ">", 80)

    def keep_body_stable(self):
        return self.abs_compare("left_hip_x", "left_hip_x_temp", ">", 30) or \
            self.abs_compare("left_knee_x", "left_knee_x_trmp", ">", 30) or \
            self.abs_compare("right_hip_x", "right_hip_x_temp", ">", 30) or \
            self.abs_compare("right_knee_x", "right_knee_x_temp", ">", 30)


    def spread_feet(self):  # 雙腳略張開
        return self.noabs_compare("right_ankle_x", "right_shoulder_x", ">", -20) or \
            self.noabs_compare("left_ankle_x", "left_shoulder_x", "<", 20)

    def hand_to_knee(self):  # 手脘放到膝蓋旁
        return self.abs_compare("right_wrist_y", "right_knee_y", ">", 70) or \
            self.abs_compare("left_wrist_y", "left_knee_y", ">", 70)

    def sit_down(self):  # 坐姿
        return self.abs_compare("right_knee_x", "right_ankle_x", ">", 30) or \
            self.abs_compare("left_knee_x", "left_ankle_x", ">", 30) or \
            self.abs_compare("right_hip_y", "right_knee_y", ">", 120) or \
            self.abs_compare("left_hip_y", "left_knee_y", ">", 120)

    # TODO: Calculate Velocity instead
    def hands_up(self, param=30):  # 動作往上開始
        return self.human.points["left_wrist_y"] < self.human.points["left_wrist_y_temp"] - param and \
            self.human.points["right_wrist_y"] < self.human.points["right_wrist_y_temp"] - param

    def hands_up_down(self, param=30):  # 動作往下開始
        return self.human.points["left_wrist_y"] > self.human.points["left_wrist_y_temp"] + param and \
            self.human.points["right_wrist_y"] > self.human.points["right_wrist_y_temp"] + param

    def hands_up_left(self, param=30):  # 動作由左手開始
        return self.human.points["left_wrist_y"] < self.human.points["left_wrist_y_temp"] - param

    def hands_up_right(self, param=30):  # 動作由右手開始
        return self.human.points["right_wrist_y"] < self.human.points["right_wrist_y_temp"] - param

    def hands_up_downleft(self, param=30):  # 動作由左腳往下開始
        return self.human.points["left_hip_y"] > self.human.points["left_hip_y_temp"] + param

    def hands_up_downright(self, param=30):
        return self.human.points["right_hip_y"] > self.human.points["right_hip_y_temp"] + param

    def hands_up_left_feet(self, param=30):
        return self.human.points["left_knee_y"] < self.human.points["left_knee_y_temp"] - param

    def hands_up_right_feet(self, param=30):
        return self.human.points["right_knee_y"] < self.human.points["right_knee_y_temp"] - param

    def hands_down(self):
        param = 100
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param and \
            self.human.points["right_wrist_y"] < self.human.points["right_shoulder_y"] + param

    def hands_down_left(self):
        param = 50
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param

    def hands_down_right(self):
        param = 50
        return self.human.points["right_wrist_y"] < self.human.points["right_shoulder_y"] + param

    def hands_down_downleft(self):
        return self.abs_compare("left_knee_x", "left_ankle_x", "<", 50) and \
            self.abs_compare("right_ankle_x", "right_hip_x", ">", 100)

    def hands_down_downright(self):
        return self.abs_compare("right_knee_x", "right_ankle_x", "<", 50) and \
            self.abs_compare("left_ankle_x", "left_hip_x", ">", 100)

    def hands_down_front(self): #雙手前舉
        param_left = 55
        param_right = 30
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param_left and \
            self.human.points["left_elbow_y"] < self.human.points["left_shoulder_y"] + param_left and \
            self.human.points["left_wrist_x"] < self.human.points["left_shoulder_x"] + param_left and \
            self.human.points["left_elbow_x"] < self.human.points["left_shoulder_x"] + param_left and \
            self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param_right and \
            self.human.points["left_elbow_y"] < self.human.points["left_shoulder_y"] + param_right and \
            self.human.points["left_wrist_x"] < self.human.points["left_shoulder_x"] + param_right and \
            self.human.points["left_elbow_x"] < self.human.points["left_shoulder_x"] + param_right

    def hands_down_frontleft(self):  # 左手前舉
        param = 55
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param and \
            self.human.points["left_elbow_y"] < self.human.points["left_shoulder_y"] + param and \
            self.human.points["left_wrist_x"] < self.human.points["left_shoulder_x"] + param and \
            self.human.points["left_elbow_x"] < self.human.points["left_shoulder_x"] + param

    def hands_down_frontright(self):  # 右手前舉
        param = 30
        return self.human.points["right_wrist_y"] < self.human.points["right_shoulder_y"] + param and \
            self.human.points["right_elbow_y"] < self.human.points["right_shoulder_y"] + param and \
            self.human.points["right_wrist_x"] < self.human.points["right_shoulder_x"] + param and \
            self.human.points["right_elbow_x"] < self.human.points["right_shoulder_x"] + param

    def hands_down_boat(self):  # 划船動作折返點，手腕與屁股同高
        param = 30
        return self.human.points["left_wrist_y"] < self.human.points["left_hip_y"] + param and \
            self.human.points["right_wrist_y"] < self.human.points["right_hip_y"] + param

    def hands_down_boat_left(self):  # 划船動作折返點，手腕與屁股同高
        param = 30
        return self.human.points["left_wrist_y"] < self.human.points["left_hip_y"] + param
    
    def hands_down_boat_right(self):  # 划船動作折返點，手腕與屁股同高
        param = 30
        return self.human.points["right_wrist_y"] < self.human.points["right_hip_y"] + param

    def hands_down_laterraise(self):
        param = 90
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"] + param and \
            self.human.points["right_wrist_y"] < self.human.points["right_shoulder_y"] + param and \
            self.human.points["left_elbow_y"] < self.human.points["left_shoulder_y"] + param and \
            self.human.points["right_elbow_y"] < self.human.points["right_shoulder_y"] + param

    def hands_down_shoulderpress(self):  # 肩推動作折返點，手舉高高
        param = 30
        param = -30
        #print("left_wrist_y:", self.human.points["left_wrist_y"])
        #print("right_wrist_y", self.human.points["right_wrist_y"])
        return self.human.points["left_wrist_y"] < self.human.points["left_shoulder_y"]  and \
            self.human.points["right_wrist_y"] < self.human.points["right_shoulder_y"]
        """
        self.human.points["left_wrist_x"] < self.human.points["left_shoulder_x"] + param and \
            self.human.points["right_wrist_x"] < self.human.points["right_shoulder_x"] + param and \
        """
    def hands_down_bent(self):  # 曲腿挺髖
        param_y = 50
        #param_x = 50
        return self.abs_compare("right_shoulder_y", "right_hip_y_temp", "<", param_y) and \
            self.abs_compare("left_shoulder_y", "left_hip_y_temp", "<", param_y) and \
            self.abs_compare("right_wrist_y", "right_knee_y_temp", "<", param_y) and \
            self.abs_compare("left_wrist_y", "left_knee_y_temp", "<", param_y)
        # and \
        # self.abs_compare("right_shoulder_x", "right_hip_x_temp", ">", param_x) and \
        # self.abs_compare("left_shoulder_x", "left_hip_x_temp", ">", param_x) and \
        # self.abs_compare("right_elbow_x", "right_knee_x_temp", ">", param_x) and \
        # self.abs_compare("left_elbow_x", "left_knee_x_temp", ">", param_x)

    def hands_down_overheadsquat(self):
        return self.human.angles["right_knee_angle"] < 150 and self.human.angles["left_knee_angle"] < 150
    
    def hands_down_thruster(self):
        param = 100
        return self.abs_compare("left_knee_y", "left_hip_y", "<", param) and \
            self.abs_compare("right_knee_y", "right_hip_y", "<", param)

    def hands_down_pushpress(self):
        param = 20
        return self.abs_compare("left_knee_y", "left_knee_y_temp", ">", param) and \
            self.abs_compare("right_knee_y", "right_knee_y_temp", ">", param)

    def hands_down_left_feet(self):
        return self.abs_compare("left_hip_y", "left_knee_y", "<", 150) #and \
            #self.abs_compare("right_ankle_y", "right_knee_y", "<", 30)
    
    def hands_down_right_feet(self):
        print("right_hip_y",self.human.points["right_hip_y"])
        print("right_knee_y",self.human.points["right_knee_y"])
        return self.abs_compare("right_hip_y", "right_knee_y", "<", 150)# and \
            #self.abs_compare("left_ankle_y", "left_knee_y", "<", 70)

    def hands_down_lift_left(self):
        return self.noabs_compare("right_wrist_x", "left_shoulder_x", ">", 70) and \
            self.noabs_compare("left_wrist_x", "left_shoulder_x", ">", 70) and \
            self.noabs_compare("right_wrist_y", "left_shoulder_y", "<", -20) and \
            self.noabs_compare("left_wrist_y", "left_shoulder_y", "<", -20)
    
    def hands_down_lift_right(self):
        return self.noabs_compare("right_wrist_x", "right_shoulder_x", "<", -70) and \
            self.noabs_compare("left_wrist_x", "right_shoulder_x", "<", -70) and \
            self.noabs_compare("right_wrist_y", "right_shoulder_y", "<", -20) and \
            self.noabs_compare("left_wrist_y", "right_shoulder_y", "<", -20)

    def hands_down_extension(self):
        return self.noabs_compare("right_wrist_y", "brain_y", "<", -30) and \
            self.noabs_compare("left_wrist_y", "brain_y", "<", -30) 

    def hands_down_step(self):
        return self.abs_compare("right_knee_y", "left_knee_y", "<", 20) and \
            self.abs_compare("right_hip_y", "left_hip_y", "<", 20)

    def ending(self):
        return not self.hands_up(param=15)

    def ending_left(self):
        return not self.hands_up_left(param=15)

    def ending_right(self):
        return not self.hands_up_right(param=15)

    def ending_down(self):
        return not self.hands_up_down(param=15)

    def ending_downleft(self):
        return not self.hands_up_downleft(param=15)

    def ending_downright(self):
        return not self.hands_up_downright(param=15)
    
    def ending_left_feet(self):
        return not self.hands_up_left_feet(param=15)

    def ending_right_feet(self):
        return not self.hands_up_right_feet(param=15)
