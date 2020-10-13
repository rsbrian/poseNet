# !/home/iiidsi/anaconda3/bin/python
# -*- coding: utf-8 -*-
import cv2
import copy
import json
import time
import posenet
import datetime
import argparse
import threading
import numpy as np
import tensorflow as tf

from websocket_server import WebsocketServer

from api import Api
from config import *
from homePage import *

parser = argparse.ArgumentParser()
parser.add_argument('--show', type=int, default=1)
parser.add_argument('--model', type=int, default=101)
parser.add_argument('--rotate', type=int, default=0)
parser.add_argument('--cam_id', type=int, default=0)
parser.add_argument('--cam_width', type=int, default=960)
parser.add_argument('--cam_height', type=int, default=540)
parser.add_argument('--scale_factor', type=float, default=0.7125)
parser.add_argument('--file', type=str, default=None,
                    help="Optionally use a video file instead of a live camera")
args = parser.parse_args()

physical_devices = tf.config.experimental.list_physical_devices("GPU")
print("Num of GPUs", physical_devices)
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

api = Api()
cap = cv2.VideoCapture("video.MOV")
cap.set(3, args.cam_width)
cap.set(4, args.cam_height)


def upPage(points, up_angle, param, overlay_image):
    starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y = param
    # left_shoulder_ankle, right_shoulder_ankle
    if abs(points[0][1][0] - points[4][1][0]) > 50 or abs(points[5][1][0] - points[9][1][0]) > 50:
        api.arm["tip"]["note"] = ["雙腳請與肩同寬"]
        frame = 0
        #   overlay_image = cv2.putText(overlay_image, api.arm["message"], (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    # left_hip_wrist, right_hip_wrist
    elif left_shoulder_point_y == 0 and (abs(points[0][1][1] - points[1][0][1]) > 40 or abs(points[5][1][1] - points[6][0][1]) > 40):
        api.arm["tip"]["note"] = ["手肘請與肩平行"]
        frame = 0
        #   overlay_image = cv2.putText(overlay_image, api.arm["message"], (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    # left_hip_wrist, right_hip_wrist
    elif left_shoulder_point_y == 0 and (abs(points[2][1][0] - points[1][0][0]) > 40 or abs(points[7][1][0] - points[6][0][0]) > 40):
        api.arm["tip"]["note"] = ["前臂請與手臂垂直"]
        frame = 0
    else:
        frame += 1
        api.arm["tip"]["note"] = ["很好！請繼續保持!"]
    if frame > 60 and frame < 120:
        api.arm["tip"]["note"] = [""]
    #   overlay_image = cv2.putText(overlay_image, api.arm["message"], (60,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    if frame == 60:
        if api.arm["start"] == False:
            timestamp = datetime.datetime.now()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
        api.arm["start"] = True
        left_shoulder_point_y = points[0][1][1]
        left_shoulder_point_x = points[0][1][0]
        right_shoulder_point_y = points[5][1][1]
        right_shoulder_point_x = points[5][1][0]
        left_wrist_point_y = points[2][1][1]
        # left_wrist_point_x = points[2][1][0]
        right_wrist_point_y = points[7][1][1]
        # right_wrist_point_x = points[7][1][0]
    if left_shoulder_point_y != 0 and (abs(points[0][1][1]-left_shoulder_point_y) > 100 or abs(points[0][1][0]-left_shoulder_point_x) > 100):
        api.arm["action"]["alert"] = ["左肩膀移動了，請回到預備動作重新開始!"]
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        cv2.putText(overlay_image, "左肩膀移動了, 請回到預備動作重新開始 ", (140, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    elif left_shoulder_point_y != 0 and (abs(points[5][1][1]-right_shoulder_point_y) > 100 or abs(points[5][1][0]-right_shoulder_point_x) > 100):
        api.arm["action"]["alert"] = ["右肩膀移動了, 請回到預備動作!"]
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        cv2.putText(overlay_image, "右肩膀移動了, 請回到預備動作重新開始 ", (160, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    if left_shoulder_point_y != 0 and abs(points[0][1][1]-left_shoulder_point_y) < 100 and abs(points[0][1][0]-left_shoulder_point_x) < 100 and abs(points[5][1][1]-right_shoulder_point_y) < 100 and abs(points[5][1][0]-right_shoulder_point_x) < 100:
        if points[2][1][1] < left_wrist_point_y - param and points[7][1][1] < right_wrist_point_y - param and zz == 1:
            timestamp = datetime.datetime.now()
            print("hahaha", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            starttime = time.time()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            zz = 0
        if up_angle[1][1] > 120 and up_angle[3][1] > 120:  # right left
            turningpoint += 1
            one_time_start = time.time()

        # and abs(points[2][0][0]-points[2][1][0])<50 and abs(points[7][0][0]-points[7][1][0])<50:
        if abs(points[7][1][1] - right_wrist_point_y) < 90 and turningpoint > 3 and abs(points[2][1][1] - left_wrist_point_y) < 90:
            startpoint += 1
        elif abs(points[2][0][0]-points[2][1][0]) > 40 or abs(points[7][0][0]-points[7][1][0]) > 40:
            api.arm["action"]["alert"] = ["手的角度請盡量保持90度，請回到預備動作重新開始!"]  # 請重新開始
            timestamp = datetime.datetime.now()
            api.arm["action"]["alertLastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            cv2.putText(overlay_image, "手的角度請盡量保持90度，請回到預備動作重新開始 ",
                        (160, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            startpoint = 15
            turningpoint = 15
            api.arm["action"]["stop"] = True
        elif points[1][0][1]-points[1][1][1] > 60 or points[6][0][1]-points[6][1][1] > 60:
            api.arm["action"]["alert"] = ["手臂請與肩膀平行，不要太下去!"]  # 請重新開始
            timestamp = datetime.datetime.now()
            api.arm["action"]["alertLastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            cv2.putText(overlay_image, "手臂請與肩膀平行，不要太下去!", (160, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            startpoint = 15
            turningpoint = 15
            api.arm["action"]["stop"] = True
        else:
            startpoint = 0
        if startpoint > 3:
            one_time_end = time.time()
            pass_time = one_time_end - one_time_start
            pass_time = round(pass_time, 2)
            startpoint = 0
            turningpoint = 0
            left_wrist_temp = points[2][1][1]
            right_wrist_temp = points[7][1][1]
            tt = 1
        if left_wrist_temp != -1 and right_wrist_temp != -1:
            if points[2][1][1] < left_wrist_temp - param and points[7][1][1] < right_wrist_temp - param and tt == 1:
                tt = 0
                timestamp = datetime.datetime.now()
                starttime = time.time()
                api.arm["action"]["startPoint"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
                api.arm["action"]["lastTime"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
                print("hahaha", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
        if up_angle[1][1] > 170 and up_angle[3][1] > 170:
            api.arm["action"]["alert"] = ["手臂請不要打直，請回到預備動作重新開始!"]
            timestamp = datetime.datetime.now()
            api.arm["action"]["alertLastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            cv2.putText(overlay_image, "手臂請不要打直，請回到預備動作重新開始 ", (160, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            startpoint = 15
            turningpoint = 15
            api.arm["action"]["stop"] = True
            # cv2.putText(overlay_image, "pass time:", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            # cv2.putText(overlay_image, str(ppp), (140, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    if pass_time != 0:
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        api.arm["action"]["startPointLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        print("aa", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
        endtime = time.time()
        diff = endtime - starttime
        pass_time = 0
        print(diff)
        if api.arm["action"]["stop"] == False:
            if diff > 2.5:
                api.arm["action"]["alert"] = ["太慢了, 請加快速度!"]
            elif diff < 2.5 and diff > 1.7:
                api.arm["action"]["alert"] = ["完美!"]
            elif diff < 1.7 and diff != 0:
                api.arm["action"]["alert"] = ["太快了, 請放慢速度!"]
            times = times + 1
            api.arm["action"]["times"] = times
        else:
            api.arm["action"]["stop"] = False
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y]


def slidePage(points, up_angle, param, overlay_image):
    starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y = param
    # left_shoulder_ankle, right_shoulder_ankle
    if abs(points[0][1][0] - points[4][1][0]) > 50 or abs(points[5][1][0] - points[9][1][0]) > 50:
        api.arm["tip"]["note"] = ["雙腳請與肩同寬"]
        frame = 0
        # overlay_image = cv2.putText(overlay_image, api.arm["message"], (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    # left_hip_wrist, right_hip_wrist
    elif left_shoulder_point_y == 0 and (abs(points[0][0][1] - points[2][1][1]) > 40 or abs(points[5][0][1] - points[7][1][1]) > 40):
        api.arm["tip"]["note"] = ["請將手自然垂放"]
        frame = 0
        #   overlay_image = cv2.putText(overlay_image, api.arm["message"], (40,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    else:
        frame += 1
        api.arm["tip"]["note"] = ["很好！請繼續保持!"]
    if frame > 60 and frame < 120:
        api.arm["tip"]["note"] = ["很好！請繼續保持!"]
        #   overlay_image = cv2.putText(overlay_image, api.arm["message"], (60,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    if frame == 60:
        if api.arm["start"] == False:
            timestamp = datetime.datetime.now()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
        api.arm["start"] = True
        left_shoulder_point_y = points[0][1][1]
        left_shoulder_point_x = points[0][1][0]
        right_shoulder_point_y = points[5][1][1]
        right_shoulder_point_x = points[5][1][0]
        left_wrist_point_y = points[2][1][1]
        # left_wrist_point_x = points[2][1][0]
        right_wrist_point_y = points[7][1][1]
        # right_wrist_point_x = points[7][1][0]
    if left_shoulder_point_y != 0 and (abs(points[0][1][1]-left_shoulder_point_y) > 80 or abs(points[0][1][0]-left_shoulder_point_x) > 40):
        api.arm["action"]["alert"] = ["左肩膀移動了，請回到預備動作重新開始!"]
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        cv2.putText(overlay_image, "左肩膀移動了, 請回到預備動作重新開始 ", (140, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    elif left_shoulder_point_y != 0 and (abs(points[5][1][1]-right_shoulder_point_y) > 80 or abs(points[5][1][0]-right_shoulder_point_x) > 40):
        api.arm["action"]["alert"] = ["右肩膀移動了, 請回到預備動作重新開始!"]
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        cv2.putText(overlay_image, "右肩膀移動了, 請回到預備動作重新開始 ", (160, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    if left_shoulder_point_y != 0 and abs(points[0][1][1]-left_shoulder_point_y) < 80 and abs(points[0][1][0]-left_shoulder_point_x) < 40 and abs(points[5][1][1]-right_shoulder_point_y) < 80 and abs(points[5][1][0]-right_shoulder_point_x) < 40:
        if points[2][1][1] < left_wrist_point_y - param and points[7][1][1] < right_wrist_point_y - param and zz == 1:
            timestamp = datetime.datetime.now()
            print("hahaha", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            starttime = time.time()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            zz = 0
        if up_angle[0][1] > 70 and up_angle[2][1] > 70:  # right left
            turningpoint += 1
            one_time_start = time.time()
        if abs(points[7][1][1] - right_wrist_point_y) < 50 and turningpoint > 10 and abs(points[2][1][1] - left_wrist_point_y) < 50:
            startpoint += 1
        else:
            startpoint = 0
        if startpoint > 3:
            one_time_end = time.time()
            pass_time = one_time_end - one_time_start
            pass_time = round(pass_time, 2)
            startpoint = 0
            turningpoint = 0
            left_wrist_temp = points[2][1][1]
            right_wrist_temp = points[7][1][1]
            tt = 1
        if left_wrist_temp != -1 and right_wrist_temp != -1:
            if points[2][1][1] < left_wrist_temp - param and points[7][1][1] < right_wrist_temp - param and tt == 1:
                tt = 0
                timestamp = datetime.datetime.now()
                starttime = time.time()
                api.arm["action"]["startPoint"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
                api.arm["action"]["lastTime"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
                print("hahaha", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
        if up_angle[0][1] > 110 or up_angle[2][1] > 110:
            api.arm["action"]["alert"] = ["手臂請不要舉太高，請回到預備動作重新開始!"]
            timestamp = datetime.datetime.now()
            api.arm["action"]["alertLastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            cv2.putText(overlay_image, "手臂請不要舉太高，請回到預備動作重新開始 ", (160, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
            startpoint = 15
            turningpoint = 15
            api.arm["action"]["stop"] = True
        # show frame
        cv2.putText(overlay_image, "pass time:", (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        cv2.putText(overlay_image, str(ppp), (140, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
    if pass_time != 0:
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        api.arm["action"]["startPointLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        print("aa", timestamp.strftime("%Y/%m/%d %H:%M:%S.%f"))
        endtime = time.time()
        diff = endtime - starttime
        pass_time = 0
        print(diff)
        if api.arm["action"]["stop"] == False:
            if diff > 2.5:
                api.arm["action"]["alert"] = ["太慢了, 請加快速度!"]
            elif diff < 2.5 and diff > 1.7:
                api.arm["action"]["alert"] = ["完美!"]
            elif diff < 1.7 and diff != 0:
                api.arm["action"]["alert"] = ["太快了, 請放慢速度!"]
            times = times + 1
            api.arm["action"]["times"] = times
        else:
            api.arm["action"]["stop"] = False
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y]


def armPage(points, param, overlay_image):
    print("Arm Page")
    starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_elbow_point_y, left_elbow_point_x, right_elbow_point_y, right_elbow_point_x, left_wrist_point_y, right_wrist_point_y = param
    if abs(points[0][1][0] - points[4][1][0]) > 50 or abs(points[5][1][0] - points[9][1][0]) > 50:
        api.arm["tip"]["note"] = ["雙腳請與肩同寬"]
        frame = 0
        cv2.putText(overlay_image, '雙腳請與肩同寬', (20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    elif left_elbow_point_y == 0 and (abs(points[0][0][1] - points[2][1][1]) > 40 or abs(points[5][0][1] - points[7][1][1]) > 40):
        api.arm["tip"]["note"] = ["請將手自然垂放"]
        frame = 0
        cv2.putText(overlay_image, '請將手自然垂放', (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
    else:
        frame += 1
        api.arm["tip"]["note"] = ["很好！請繼續保持!"]
    if frame > 60 and frame < 120:
        api.arm["tip"]["note"] = ["很好！請繼續保持!"]
    if frame == 60:
        if api.arm["start"] == False:
            timestamp = datetime.datetime.now()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
        api.arm["start"] = True
        left_elbow_point_y = points[2][0][1]
        left_elbow_point_x = points[2][0][0]
        right_elbow_point_y = points[6][0][1]
        right_elbow_point_x = points[6][0][0]
        left_wrist_point_y = points[2][1][1]
        right_wrist_point_y = points[7][1][1]

    if left_elbow_point_y != 0 and (abs(points[2][0][1]-left_elbow_point_y) > 40 or abs(points[2][0][0]-left_elbow_point_x) > 40):
        api.arm["action"]["alert"] = ["左手肘移動了，請回到預備動作重新開始!"]
        cv2.putText(overlay_image, '左手肘移動了，請回到預備動作重新開始', (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    elif left_elbow_point_y != 0 and (abs(points[6][0][1]-right_elbow_point_y) > 40 or abs(points[6][0][0]-right_elbow_point_x) > 40):
        api.arm["action"]["alert"] = ["右手肘移動了，請回到預備動作重新開始"]
        cv2.putText(overlay_image, '右手肘移動了，請回到預備動作重新開始', (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (84, 46, 8), 1, cv2.LINE_AA)
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        startpoint = 15
        turningpoint = 15
        api.arm["action"]["stop"] = True

    if left_elbow_point_y != 0 and abs(points[2][0][1]-left_elbow_point_y) < 40 and abs(points[2][0][0]-left_elbow_point_x) < 40 and abs(points[6][0][1]-right_elbow_point_y) < 40 and abs(points[6][0][0]-right_elbow_point_x) < 40:
        if points[2][1][1] < left_wrist_point_y - param and points[7][1][1] < right_wrist_point_y - param and zz == 1:
            timestamp = datetime.datetime.now()
            api.arm["action"]["startPoint"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            starttime = time.time()
            api.arm["action"]["lastTime"] = timestamp.strftime(
                "%Y/%m/%d %H:%M:%S.%f")
            zz = 0
        if abs(points[5][1][1] - points[7][1][1]) < 60 and abs(points[0][1][1] - points[2][1][1]) < 60:  # right left
            turningpoint += 1
            one_time_start = time.time()
        if abs(points[7][1][1] - right_wrist_point_y) < 50 and turningpoint > 10 and abs(points[2][1][1] - left_wrist_point_y) < 50:
            startpoint += 1
        else:
            startpoint = 0
        if startpoint > 3:
            one_time_end = time.time()
            pass_time = one_time_end - one_time_start
            pass_time = round(pass_time, 2)
            startpoint = 0
            turningpoint = 0
            left_wrist_temp = points[2][1][1]
            right_wrist_temp = points[7][1][1]
            tt = 1
        if left_wrist_temp != -1 and right_wrist_temp != -1:
            if points[2][1][1] < left_wrist_temp - param and points[7][1][1] < right_wrist_temp - param and tt == 1:
                tt = 0
                timestamp = datetime.datetime.now()
                starttime = time.time()
                api.arm["action"]["startPoint"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
                api.arm["action"]["lastTime"] = timestamp.strftime(
                    "%Y/%m/%d %H:%M:%S.%f")
        # show frame
        cv2.putText(overlay_image, "pass time:", (20, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
        cv2.putText(overlay_image, str(ppp), (140, 120),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)

    if pass_time != 0:
        timestamp = datetime.datetime.now()
        api.arm["action"]["alertLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        api.arm["action"]["startPointLastTime"] = timestamp.strftime(
            "%Y/%m/%d %H:%M:%S.%f")
        endtime = time.time()
        diff = endtime - starttime
        pass_time = 0
        if api.arm["action"]["stop"] == False:
            if diff > 2.5:
                api.arm["action"]["alert"] = ["太慢了, 請加快速度!"]
            elif diff < 2.5 and diff > 1.7:
                api.arm["action"]["alert"] = ["完美!"]
            elif diff < 1.7 and diff != 0:
                api.arm["action"]["alert"] = ["太快了, 請放慢速度!"]
            times = times + 1
            api.arm["action"]["times"] = times
        else:
            api.arm["action"]["stop"] = False
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_elbow_point_y, left_elbow_point_x, right_elbow_point_y, right_elbow_point_x, left_wrist_point_y, right_wrist_point_y]


def home(points, homeInfo, up_angle, server):
    homeInfo.settingHumanBodyFromPoints(points)
    if homeInfo.calibrateHumanBody():
        api.home["最後動作"], api.home["最後動作時間"] = homeInfo.chooseAction(
            api.home, up_angle)
        server.send_message_to_all(api.home)


def checkAngle(up_angle):
    angle = 30
    left_elbow_angle = up_angle[1][1]
    right_elbow_angle = up_angle[3][1]
    return left_elbow_angle < angle and right_elbow_angle < angle


def main():
    with tf.Session() as sess:
        global overlay_image
        global server
        model_cfg, model_outputs = posenet.load_model(args.model, sess)
        output_stride = model_cfg['output_stride']
        armParam = getArmParameters()
        upParam = getUpParamters()
        slideParam = getSlideParamters()
        homeInfo = HomeObject(args.cam_width, args.cam_height)
        while True:
            input_image, display_image, output_scale = posenet.read_cap(
                cap, args.rotate, scale_factor=args.scale_factor, output_stride=output_stride)
            heatmaps_result, offsets_result, displacement_fwd_result, displacement_bwd_result = sess.run(
                model_outputs,
                feed_dict={'image:0': input_image})
            pose_scores, keypoint_scores, keypoint_coords = posenet.decode_multi.decode_multiple_poses(
                heatmaps_result.squeeze(axis=0),
                offsets_result.squeeze(axis=0),
                displacement_fwd_result.squeeze(axis=0),
                displacement_bwd_result.squeeze(axis=0),
                output_stride=output_stride,
                max_pose_detections=10,
                min_pose_score=0.15)
            keypoint_coords *= output_scale
            overlay_image, points, up_angle, down_angle = posenet.draw_skel_and_kp(
                display_image, pose_scores, keypoint_scores, keypoint_coords,
                min_pose_score=0.4, min_part_score=0.4)

            if points == []:
                continue

            if api.start["name"] == "啞鈴彎舉":
                setArmAPI(api)
                armParam = armPage(points, armParam, overlay_image)
                server.send_message_to_all(api.arm)
                if api.end["break"]:
                    count = 0
                    resetAPI(api)
                    armParam = getArmParameters()

            elif api.start["name"] == "啞鈴肩推":
                setArmAPI(api)
                upParam = upPage(points, up_angle, upParam, overlay_image)
                server.send_message_to_all(api.arm)
                if api.end["break"]:
                    count = 0
                    resetAPI(api)
                    upParam = getUpParamters()

            elif api.start["name"] == "啞鈴側平舉":
                setArmAPI(api)
                slideParam = slidePage(
                    points, up_angle, slideParam, overlay_image)
                server.send_message_to_all(api.arm)
                if api.end["break"]:
                    count = 0
                    resetAPI(api)
                    slideParam = getSlideParamters()

            home(points, homeInfo, up_angle, server)
            if api.start["name"] == "啞鈴彎舉" or api.start["name"] == "啞鈴肩推" or api.start["name"] == "啞鈴側平舉":
                if api.home["最後動作"] == "雙手交叉":
                    count += 1
                else:
                    count = 0
                if count > 25:
                    api.arm["action"]["alert"] = [""]
                    api.arm["action"]["quit"] = True
            else:
                count = 0
                api.arm["action"]["quit"] = False

            if args.show:
                homeInfo.show(overlay_image)
                cv2.imshow('posenet', overlay_image)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        if args.show:
            cv2.destroyAllWindows()
        cap.release()


def new_client(client, server):
    server.send_message_to_all(api.home)


def client_left(client, server):
    print("Client(%d) disconnected" % client["id"])


def message_received(client, server, message):
    if len(message) > 200:
        message = message[:200] + ".."
    print("Client(%d) said: %s" % (client["id"], message))


def main_thread():
    global t
    t = threading.Thread(target=main, args=())
    t.start()


def main_thread_close():
    t.join()


PORT = 5500
server = WebsocketServer(PORT)

main_thread()

server.set_fn_new_client(new_client)
server.set_fn_client_left(client_left)
server.set_fn_message_received(message_received)
server.run_forever()

main_thread_close()
