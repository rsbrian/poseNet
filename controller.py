import cv2
import json
import copy
import posenet
import numpy as np

from utils.view import View
from utils.brain import Brain
from utils.server import Server


class Controller(object):
    def __init__(self, args):
        self.args = args
        self.brain = Brain(args)
        self.view = View(args)
        self.my_server = Server()
        self.camera = None

    def loading(self, points, face):
        if len(points) == 0:
            return
        angles = self.calculate_angles(points)
        if not self.is_angles_none(angles):
            self.brain.reset_state(points, angles)
            self.brain.add_median_filter()
            self.brain.face = face

    def add_video_writer(self, camera):
        self.camera = camera

    def calculate_angles(self, points):
        return posenet.computeangle.calculateangle_all_body(points)

    def is_angles_none(self, angles):
        if len(angles) == 2:
            return True
        hi, wi = angles.shape
        for h in range(hi):
            for w in range(wi):
                if angles[h, w] is None:
                    return True
        return False

    def update_server(self, api):
        self.my_server.set_api(api)

    def server_default(self):
        self.my_server.default()

    def choose_course(self):
        return self.my_server.get_route(self.brain, self.camera)

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

    def send_qrcode(self, server, api):
        if self.args.socket and api["content"] != "":
            print(f"QRCode: {api}")
            server.send_message_to_all(
                json.dumps(api, ensure_ascii=False))