# !/home/iiidsi/anaconda3/bin/python
# -*- coding: utf-8 -*-
# 2020/10/26 16:30
import cv2
import json
import time
import copy
import pickle
import posenet
import datetime
import argparse
import threading
import numpy as np
import tensorflow as tf

from pyzbar import pyzbar
from camera import Camera
from controller import Controller
from third_party import ThirdParty
from websocket_server import WebsocketServer


parser = argparse.ArgumentParser()
parser.add_argument('--show', type=int, default=1)
parser.add_argument('--save', type=int, default=0)
parser.add_argument('--cam_id', type=int, default=-1)
parser.add_argument('--socket', type=int, default=1)
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--rotate', type=int, default=-90)
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

video_name = "videos/test_video.avi"
saved_names = ["all.avi", "only_in_box.avi"]
camera = Camera(args, video_name, saved_names)
control = Controller(args)
third_party = ThirdParty(args)


def extract_qrcode(img):
    bars = pyzbar.decode(img)
    for bar in bars:
        barcodeData = bar.data.decode("utf-8")
        print(f"QR code: {barcodeData}")


def main():
    with tf.Session() as sess:
        global server
        third_party.load_model(args.model, sess)
        while (camera.isOpened()):
            res, img = camera.read()
            if not res:
                print("Camera Failed")
                break

            img = camera.preprocessing(img)
            # camera.save(original_img, "all")
            extract_qrcode(img)

            multi_points = third_party.get_multi_skeleton_from(img)
            points, face, all_faces = camera.one_person_filter(multi_points)

            control.loading(points, face)

            course = control.choose_course()
            api = course().get_api()
            control.send(server, api)

            thres = course.get_thres()
            bounding_box = course.get_bounding_box()

            control.update(img)
            control.show(bounding_box, (0, 200, 0), 3)
            control.show(all_faces, (0, 100, 100), -1)
            control.show(points, (200, 200, 0), 3)
            control.show(face, (200, 200, 0), -1)
            control.show(thres, (0, 200, 200), 3)
            cv2.imshow("img", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # print(len(points))
        # pickle_out = open('points.pickle', "wb")
        # pickle.dump(points, pickle_out)
        # pickle_out.close()

        camera.release()
        control.destroy()


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


PORT = 5500
server = WebsocketServer(PORT)
if args.socket:
    server.set_fn_new_client(new_client)
    server.set_fn_client_left(client_left)
    main_thread()
    server.set_fn_message_received(message_received)
    server.run_forever()
    main_thread_close()
else:
    main()
