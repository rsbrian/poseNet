# !/home/iiidsi/anaconda3/bin/python
# -*- coding: utf-8 -*-
# 2020/10/20 12:30
import cv2
import json
import time
import posenet
import datetime
import argparse
import threading
import numpy as np
import tensorflow as tf

from camera import Camera
from controller import Controller
from third_party import ThirdParty
from websocket_server import WebsocketServer

import pickle

parser = argparse.ArgumentParser()
parser.add_argument('--show', type=int, default=1)
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--rotate', type=int, default=-90)
parser.add_argument('--socket', type=int, default=1)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=540)
parser.add_argument('--cam_height', type=int, default=960)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None,
                    help="Optionally use a video file instead of a live camera")
args = parser.parse_args()

physical_devices = tf.config.experimental.list_physical_devices("GPU")
print("Num of GPUs", physical_devices)
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

camera = Camera(args)
control = Controller(args)
third_party = ThirdParty()

video_name = "videos/behavior.MOV"
cap = cv2.VideoCapture(0)


def main():
    with tf.Session() as sess:
        global server
        third_party.load_model(args.model, sess)
        while True:
            res, img = cap.read()
            if not res:
                print("Camera Failed")
                break

            img = camera.preprocessing(img)

            img, multi_points = camera.get_multi_skeleton_from(
                img, third_party)
            img, points, face = camera.multi_person_filter(img, multi_points)

            control.update_model(img, points)

            control.test_loading(face)

            course = control.choose_course()
            api = course().get_api()
            control.send(server, api)

            control.show(img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # print(len(points))
        # pickle_out = open('points.pickle', "wb")
        # pickle.dump(points, pickle_out)
        # pickle_out.close()

        control.destroy()
        cap.release()


def new_client(client, server):
    print("Connecting")
    control.server_default()


def client_left(client, server):
    print("Client(%d) disconnected" % client["id"])


def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + ".."

    msg = json.loads(message, encoding="utf-8")
    control.update_server(msg)


def main_thread():
    global t
    t = threading.Thread(target=main, args=())
    t.start()


def main_thread_close():
    t.join()


if args.socket:
    PORT = 5500
    server = WebsocketServer(PORT)
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    main_thread()
    server.set_fn_message_received(message_received)
    server.run_forever()
    main_thread_close()
else:
    main()
