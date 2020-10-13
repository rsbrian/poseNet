import time
"""
def draw_skel_and_kp(
        img, instance_scores, keypoint_scores, keypoint_coords,
        min_pose_score=0.5, min_part_score=0.5):
    out_img = img
    adjacent_keypoints = []
    cv_keypoints = []
    for ii, score in enumerate(instance_scores):
        if score < min_pose_score:
            continue
        # if ii == 0:
        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_score)
        adjacent_keypoints.extend(new_keypoints)

        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_score:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10. * ks))

        new_keypoints = get_adjacent_keypoints(
            keypoint_scores[ii, :], keypoint_coords[ii, :, :], min_part_score)
        adjacent_keypoints.extend(new_keypoints)

        for ks, kc in zip(keypoint_scores[ii, :], keypoint_coords[ii, :, :]):
            if ks < min_part_score:
                continue
            cv_keypoints.append(cv2.KeyPoint(kc[1], kc[0], 10. * ks))
    out_img = cv2.drawKeypoints(
        out_img, cv_keypoints, outImage=np.array([]), color=(255, 255, 0),
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    out_img = cv2.polylines(out_img, adjacent_keypoints,
                            isClosed=False, color=(255, 255, 0), thickness=3)

    if len(adjacent_keypoints) == 12:
        upper_startpoint_angle = posenet.computeangle.calculateangle_upper_body(
            adjacent_keypoints)
        down_startpoint_angle = posenet.computeangle.calculateangle_down_body(
            adjacent_keypoints)
        # for i in range(4):
        #     out_img = cv2.putText(out_img, str(upper_startpoint_angle[i][1]), tuple(
        #         upper_startpoint_angle[i][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (84, 46, 8), 1, cv2.LINE_AA)
        #     out_img = cv2.putText(out_img, str(down_startpoint_angle[i][1]), tuple(
        #         down_startpoint_angle[i][0]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (84, 46, 8), 1, cv2.LINE_AA)
    else:
        upper_startpoint_angle = np.zeros(2)
        down_startpoint_angle = np.zeros(2)
    return out_img, adjacent_keypoints, upper_startpoint_angle, down_startpoint_angle

"""


def setArmAPI(api):
    api.arm["tip"]["duration"] = 2


def resetAPI(api):
    api.start["name"] = ""
    api.end["break"] = False
    api.arm["action"]["quit"] = False

    api.arm["tip"]["note"] = ""
    api.arm["tip"]["duration"] = 0
    api.arm["action"]["alert"] = ""
    api.arm["action"]["alertLastTime"] = ""
    api.arm["action"]["startPoint"] = ""
    api.arm["action"]["startPointLastTime"] = ""
    api.arm["action"]["lastTime"] = ""
    api.arm["action"]["times"] = 0
    api.arm["action"]["stop"] = False
    api.arm["start"] = False


def getArmParameters():
    aa = 0
    tt = 0
    zz = 1
    ppp = 0
    frame = 0
    times = 0
    param = 30
    end_frame = 0
    pass_time = 0
    startpoint = 0
    frame_count = 0
    turningpoint = 0
    left_wrist_temp = -1
    right_wrist_temp = -1
    left_elbow_point_y = 0
    left_elbow_point_x = 0
    right_elbow_point_y = 0
    right_elbow_point_x = 0
    left_wrist_point_y = 0
    right_wrist_point_y = 0
    start = time.time()
    one_time_start = 0
    starttime = 0
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_elbow_point_y, left_elbow_point_x, right_elbow_point_y, right_elbow_point_x, left_wrist_point_y, right_wrist_point_y]


def getUpParamters():
    aa = 0
    tt = 0
    zz = 1
    ppp = 0
    frame = 0
    times = 0
    param = 30
    end_frame = 0
    pass_time = 0
    startpoint = 0
    frame_count = 0
    turningpoint = 0
    left_wrist_temp = -1
    right_wrist_temp = -1
    left_shoulder_point_y = 0
    left_shoulder_point_x = 0
    right_shoulder_point_y = 0
    right_shoulder_point_x = 0
    left_wrist_point_y = 0
    right_wrist_point_y = 0
    start = time.time()
    one_time_start = 0
    starttime = time.time()
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y]


def getSlideParamters():
    aa = 0
    tt = 0
    zz = 1
    ppp = 0
    frame = 0
    times = 0
    param = 30
    end_frame = 0
    pass_time = 0
    startpoint = 0
    frame_count = 0
    turningpoint = 0
    left_wrist_temp = -1
    right_wrist_temp = -1
    left_shoulder_point_y = 0
    left_shoulder_point_x = 0
    right_shoulder_point_y = 0
    right_shoulder_point_x = 0
    left_wrist_point_y = 0
    right_wrist_point_y = 0
    start = time.time()
    one_time_start = 0
    starttime = 0
    return [starttime, one_time_start, start, aa, tt, zz, ppp, frame, times, param, end_frame, pass_time, startpoint, frame_count, turningpoint, left_wrist_temp, right_wrist_temp, left_shoulder_point_y, left_shoulder_point_x, right_shoulder_point_y, right_shoulder_point_x, left_wrist_point_y, right_wrist_point_y]
