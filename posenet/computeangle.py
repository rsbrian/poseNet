import cv2
import numpy as np
import numpy.linalg as la


def calculateangle(keypoints):
    for i in range(len(keypoints)):
        print(keypoints[i])
    startpoint, angle = startpoint_twovector(keypoints[0], keypoints[1])
    return angle, startpoint


def calculateangle_upper_body(keypoints):
    left_shoulder_startpoint, left_shoulder_angle = startpoint_twovector(
        keypoints[0], keypoints[1])
    left_elbow_startpoint, left_elbow_angle = startpoint_twovector(
        keypoints[1], keypoints[2])
    right_shoulder_startpoint, right_shoulder_angle = startpoint_twovector(
        keypoints[5], keypoints[6])
    right_elbow_startpoint, right_elbow_angle = startpoint_twovector(
        keypoints[6], keypoints[7])
    startpoint_and_angle = np.array([[left_shoulder_startpoint, left_shoulder_angle], [left_elbow_startpoint, left_elbow_angle], [
                                    right_shoulder_startpoint, right_shoulder_angle], [right_elbow_startpoint, right_elbow_angle]])
    return startpoint_and_angle


def calculateangle_down_body(keypoints):
    left_hip_startpoint, left_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[3])
    left_knee_startpoint, left_knee_angle = startpoint_twovector(
        keypoints[3], keypoints[4])
    right_hip_startpoint, right_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[8])
    right_knee_startpoint, right_knee_angle = startpoint_twovector(
        keypoints[8], keypoints[9])
    startpoint_and_angle = np.array([[left_hip_startpoint, left_hip_angle], [left_knee_startpoint, left_knee_angle], [
                                    right_hip_startpoint, right_hip_angle], [right_knee_startpoint, right_knee_angle]])
    return startpoint_and_angle


def calculateangle_all_body(keypoints):
    left_shoulder_startpoint, left_shoulder_angle = startpoint_twovector(
        keypoints[0], keypoints[1])
    left_elbow_startpoint, left_elbow_angle = startpoint_twovector(
        keypoints[1], keypoints[2])
    right_shoulder_startpoint, right_shoulder_angle = startpoint_twovector(
        keypoints[5], keypoints[6])
    right_elbow_startpoint, right_elbow_angle = startpoint_twovector(
        keypoints[6], keypoints[7])
    left_hip_startpoint, left_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[3])
    left_knee_startpoint, left_knee_angle = startpoint_twovector(
        keypoints[3], keypoints[4])
    right_hip_startpoint, right_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[8])
    right_knee_startpoint, right_knee_angle = startpoint_twovector(
        keypoints[8], keypoints[9])
    startpoint_and_angle = np.array([
        [left_shoulder_startpoint, left_shoulder_angle],
        [left_elbow_startpoint, left_elbow_angle],
        [right_shoulder_startpoint, right_shoulder_angle],
        [right_elbow_startpoint, right_elbow_angle],
        [left_hip_startpoint, left_hip_angle],
        [left_knee_startpoint, left_knee_angle],
        [right_hip_startpoint, right_hip_angle],
        [right_knee_startpoint, right_knee_angle]])
    return startpoint_and_angle


def calculateangle_left_body(keypoints):
    left_shoulder_startpoint, left_shoulder_angle = startpoint_twovector(
        keypoints[0], keypoints[1])
    left_elbow_startpoint, left_elbow_angle = startpoint_twovector(
        keypoints[1], keypoints[2])
    left_hip_startpoint, left_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[3])
    left_knee_startpoint, left_knee_angle = startpoint_twovector(
        keypoints[3], keypoints[4])
    startpoint_and_angle = np.array([[left_shoulder_startpoint, left_shoulder_angle], [left_elbow_startpoint, left_elbow_angle], [
                                    left_hip_startpoint, left_hip_angle], [left_knee_startpoint, left_knee_angle]])
    return startpoint_and_angle


def calculateangle_right_body(keypoints):
    right_shoulder_startpoint, right_shoulder_angle = startpoint_twovector(
        keypoints[5], keypoints[6])
    right_elbow_startpoint, right_elbow_angle = startpoint_twovector(
        keypoints[6], keypoints[7])
    right_hip_startpoint, right_hip_angle = startpoint_twovector(
        keypoints[11], keypoints[8])
    right_knee_startpoint, right_knee_angle = startpoint_twovector(
        keypoints[8], keypoints[9])
    startpoint_and_angle = np.array([[right_shoulder_startpoint, right_shoulder_angle], [right_elbow_startpoint, right_elbow_angle], [
                                    right_hip_startpoint, right_hip_angle], [right_knee_startpoint, right_knee_angle]])
    return startpoint_and_angle


def startpoint_twovector(line1, line2):
    vec1 = np.zeros(2, dtype=int)
    vec2 = np.zeros(2, dtype=int)
    for i in range(len(line1)):
        for j in range(len(line2)):
            if line1[i][0] == line2[j][0] and line1[i][1] == line2[j][1]:
                startpoint = line1[i]
    temp = startpoint
    for k1 in range(len(line1)):
        if line1[k1][0] != startpoint[0] or line1[k1][1] != startpoint[1]:
            vec1[0] = line1[k1][0] - startpoint[0]
            vec1[1] = line1[k1][1] - startpoint[1]
    startpoint = temp
    for k2 in range(len(line2)):
        if line2[k2][0] != startpoint[0] or line2[k2][1] != startpoint[1]:
            vec2[0] = line2[k2][0] - startpoint[0]
            vec2[1] = line2[k2][1] - startpoint[1]

    try:
        cosine_angle = np.dot(vec1, vec2) / (la.norm(vec1) * la.norm(vec2))
        cosine_angle = clip_cosine(cosine_angle)
        angle = np.arccos(cosine_angle)
        degree = round(np.degrees(angle))
        return startpoint, degree
    except Exception as e:
        return None, None


def angle_between_twolines(startpoint, vec1, vec2):
    cosine_angle = np.dot(vec1, vec2) / (la.norm(vec1) * la.norm(vec2))
    angle = np.arccos(cosine_angle)
    degree = np.degrees(angle)
    return degree


def clip_cosine(angle):
    if angle < -1:
        return -1
    elif angle > 1:
        return 1
    return angle
