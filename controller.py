import cv2
import json
import copy
import posenet
import numpy as np

from utils.view import View
from utils.brain import Brain
from utils.server import Server
from utils.kalman import Kalman


class Controller(object):
    def __init__(self, args):
        self.args = args
        self.brain = Brain()
        self.view = View(self.brain)
        self.my_server = Server()
        self.kalman = Kalman()
        self.update_view(
            self.args.cam_width,
            self.args.cam_height,
            self.args.rotate)

    def loading(self, face):
        self.brain.face = face

    def update_view(self, width, height, rotate):
        self.view.width = width
        self.view.height = height
        self.view.rotate = rotate

    def update_model(self, points):
        if len(points) == 0:
            return False
        angles = self.calculate_angles(points)
        if not self.is_angles_none(angles):
            self.brain.reset_state(points, angles)
            self.brain.add_median_filter()
        return True

    def update_server(self, api):
        self.my_server.set_api(api)

    def server_default(self):
        self.my_server.default()

    def is_angles_none(self, angles):
        if len(angles) == 2:
            return True
        hi, wi = angles.shape
        for h in range(hi):
            for w in range(wi):
                if angles[h, w] is None:
                    return True
        return False

    def choose_course(self):
        return self.my_server.get_route(self.brain, self.view)

    def update(self, img):
        self.view.img = img

    def show(self, need_to_draw, clr, thickness):
        self.view.show(need_to_draw, clr, thickness)

    def destroy(self):
        self.view.destroy()

    def send(self, server, api):
        if self.args.socket:
            if api["function"] == "exercise_status" and api["最後動作"] != "":
                print(api["最後動作"])
                server.send_message_to_all(
                    json.dumps(api, ensure_ascii=False))
            elif api["function"] == "getExercise" or api["function"] == "endExercise":
                server.send_message_to_all(json.dumps(api, ensure_ascii=False))

    def is_body_in_box(self):
        return self.brain.human.points != {} and self.view.calibrate_human_body()

    def draw_skeleton(self, img, points, color, thickness):
        self.view.draw_skeleton(img, points, color, thickness)

    def calculate_angles(self, points):
        return posenet.computeangle.calculateangle_all_body(points)

    def draw_by_points(self, img, clr):
        new_points = [np.zeros((2, 2), dtype="int32") for i in range(12)]
        new_points[0][0][0] = self.brain.human.points["left_hip_x"]
        new_points[0][0][1] = self.brain.human.points["left_hip_y"]
        new_points[3][0][0] = self.brain.human.points["left_hip_x"]
        new_points[3][0][1] = self.brain.human.points["left_hip_y"]
        new_points[11][0][0] = self.brain.human.points["left_hip_x"]
        new_points[11][0][1] = self.brain.human.points["left_hip_y"]

        new_points[3][1][0] = self.brain.human.points["left_knee_x"]
        new_points[3][1][1] = self.brain.human.points["left_knee_y"]
        new_points[4][0][0] = self.brain.human.points["left_knee_x"]
        new_points[4][0][1] = self.brain.human.points["left_knee_y"]

        new_points[8][1][0] = self.brain.human.points["right_knee_x"]
        new_points[8][1][1] = self.brain.human.points["right_knee_y"]
        new_points[9][0][0] = self.brain.human.points["right_knee_x"]
        new_points[9][0][1] = self.brain.human.points["right_knee_y"]

        new_points[5][0][0] = self.brain.human.points["right_hip_x"]
        new_points[5][0][1] = self.brain.human.points["right_hip_y"]
        new_points[8][0][0] = self.brain.human.points["right_hip_x"]
        new_points[8][0][1] = self.brain.human.points["right_hip_y"]
        new_points[11][1][0] = self.brain.human.points["right_hip_x"]
        new_points[11][1][1] = self.brain.human.points["right_hip_y"]

        new_points[4][1][0] = self.brain.human.points["left_ankle_x"]
        new_points[4][1][1] = self.brain.human.points["left_ankle_y"]

        new_points[9][1][0] = self.brain.human.points["right_ankle_x"]
        new_points[9][1][1] = self.brain.human.points["right_ankle_y"]

        new_points[2][1][0] = self.brain.human.points["left_wrist_x"]
        new_points[2][1][1] = self.brain.human.points["left_wrist_y"]

        new_points[1][0][0] = self.brain.human.points["left_elbow_x"]
        new_points[1][0][1] = self.brain.human.points["left_elbow_y"]
        new_points[2][0][0] = self.brain.human.points["left_elbow_x"]
        new_points[2][0][1] = self.brain.human.points["left_elbow_y"]

        new_points[6][0][0] = self.brain.human.points["right_elbow_x"]
        new_points[6][0][1] = self.brain.human.points["right_elbow_y"]
        new_points[7][0][0] = self.brain.human.points["right_elbow_x"]
        new_points[7][0][1] = self.brain.human.points["right_elbow_y"]

        new_points[7][1][0] = self.brain.human.points["right_wrist_x"]
        new_points[7][1][1] = self.brain.human.points["right_wrist_y"]

        new_points[0][1][0] = self.brain.human.points["left_shoulder_x"]
        new_points[0][1][1] = self.brain.human.points["left_shoulder_y"]
        new_points[1][1][0] = self.brain.human.points["left_shoulder_x"]
        new_points[1][1][1] = self.brain.human.points["left_shoulder_y"]
        new_points[10][0][0] = self.brain.human.points["left_shoulder_x"]
        new_points[10][0][1] = self.brain.human.points["left_shoulder_y"]

        new_points[5][1][0] = self.brain.human.points["right_shoulder_x"]
        new_points[5][1][1] = self.brain.human.points["right_shoulder_y"]
        new_points[6][1][0] = self.brain.human.points["right_shoulder_x"]
        new_points[6][1][1] = self.brain.human.points["right_shoulder_y"]
        new_points[10][1][0] = self.brain.human.points["right_shoulder_x"]
        new_points[10][1][1] = self.brain.human.points["right_shoulder_y"]

        self.draw_skeleton(img, new_points, clr, 5)
