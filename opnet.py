# !/home/iiidsi/anaconda3/bin/python
# -*- coding: utf-8 -*-
# 2020/10/26 16:30
import os
import cv2
import json
import time
import copy
import pickle
import posenet
import openpose_information
import datetime
import argparse
import threading
import numpy as np
import tensorflow as tf
import sys
from sys import platform

from api.socket import Api
from pyzbar import pyzbar
from camera import Camera
from controller import Controller
from third_party import ThirdParty
from websocket_server import WebsocketServer

parser = argparse.ArgumentParser()
# parser.add_argument('--net_resolution', type=str, default="320x176")
parser.add_argument('--show', type=int, default=1)
parser.add_argument('--save', type=int, default=1)
parser.add_argument('--cam_id', type=int, default=1)
parser.add_argument('--socket', type=int, default=1)
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--rotate', type=int, default=-90)
parser.add_argument('--cam_width', type=int, default=160)
parser.add_argument('--cam_height', type=int, default=320)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None,
                    help="Optionally use a video file instead of a live camera")
args = parser.parse_args()

print(type(args))
print(args)

physical_devices = tf.config.experimental.list_physical_devices("GPU")
print("Num of GPUs", physical_devices)
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

saved_folder = "videos"
if not os.path.isdir(saved_folder):
    os.mkdir(saved_folder)
videos = os.listdir(saved_folder)
camera = Camera(args, videos)
control = Controller(args)
third_party = ThirdParty(args)
member = Api()


def extract_qrcode(img):
    bars = pyzbar.decode(img, symbols=[64])
    member.qrcode["content"] = ""
    for bar in bars:
        barcodeData = bar.data.decode("utf-8")
        member.qrcode["content"] = barcodeData


def main():
    global server
    with tf.Session() as sess:
        third_party.load_model(args.model, sess)
        while (camera.isOpened()):
            po = []
            fa = []
            res, img = camera.read()
            if not res:
                print("Camera Failed")
                break

            img = camera.preprocessing(img)
            camera.store(img)
            extract_qrcode(img)
            
            posenet_img = copy.deepcopy(img)
            multi_points = third_party.get_multi_skeleton_from(posenet_img)
            print(len(multi_points))

            if len(multi_points):
                datum = op.Datum()
                datum.cvInputData = img
                opWrapper.emplaceAndPop(op.VectorDatum([datum]))

                img = datum.cvOutputData
                if datum.poseKeypoints is not None and not member.take_a_rest["take_a_break"]:
                    multi_points = openpose_information.get_multipoints(datum.poseKeypoints)
                    points, face, all_faces = camera.one_person_filter(multi_points)
                    for i in range(len(points)):
                        a = int(points[i][0])
                        b = int(points[i][1])
                        c = int(points[i][2])
                        po.append([a, b, c])
                        
                    aa = int(face[0])
                    bb = int(face[1])
                    cc = int(face[2])
                    fa.append([aa, bb, cc])

                    points = po
                    face = fa[0]
                    control.loading(points, face)
                    control.add_video_writer(camera)
                    course = control.choose_course()
                    api = course().get_api()
                    control.send(server, api)
                    control.send_qrcode(server, member.qrcode)

                    bounding_box = course.get_bounding_box()

                    control.update(img)
                    control.show(points, (200, 200, 0), 3)
                    control.show(face, (200, 200, 0), -1)
                    control.show(bounding_box, (0, 200, 0), 3)

            cv2.imshow("img", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

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
    if msg.get("take_a_break") is not None:
        member.take_a_rest["take_a_break"] = msg.get("take_a_break")

def main_thread():
    global t
    t = threading.Thread(target=main, args=())
    t.start()


def main_thread_close():
    t.join()

try:
    # Import Openpose (Windows/Ubuntu/OSX)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    try:
        # Windows Import
        if platform == "win32":
            sys.path.append(dir_path + '/../../python/openpose/Release');
            os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
            import pyopenpose as op
        else:
            sys.path.append('../../python');
            from openpose import pyopenpose as op
    except ImportError as e:
        print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
        raise e

    parser1 = argparse.ArgumentParser()
    args1 = parser1.parse_known_args()
    params = dict()
    params["model_folder"] = "../../../models/"

    # Add others in path?
    for i in range(0, len(args1[1])):
        curr_item = args1[1][i]
        if i != len(args1[1])-1: next_item = args1[1][i+1]
        else: next_item = "1"
        if "--" in curr_item and "--" in next_item:
            key = curr_item.replace('-','')
            if key not in params:  params[key] = "1"
        elif "--" in curr_item and "--" not in next_item:
            key = curr_item.replace('-','')
            if key not in params: params[key] = next_item
    # Starting OpenPose
    opWrapper = op.WrapperPython()
    opWrapper.configure(params)
    opWrapper.start()
except Exception as e:
    print(e)
    sys.exit(-1)

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
