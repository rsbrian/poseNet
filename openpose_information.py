import cv2
import numpy as np
import numpy.linalg as la

def get_multipoints(points):
    adjacent_keypoints = []
  
    for i in range(len(points)):
        new_keypoints = points[i]
        face_points = points[i][0]
        adjacent_keypoints.append([new_keypoints, face_points])
    return adjacent_keypoints        
    
def calculateangle_all_body(keypoints):
    left_shoulder_startpoint, left_shoulder_angle = startpoint_twovector(
        keypoints[5], keypoints[1], keypoints[6])
    left_elbow_startpoint, left_elbow_angle = startpoint_twovector(
        keypoints[6], keypoints[5], keypoints[7])
    right_shoulder_startpoint, right_shoulder_angle = startpoint_twovector(
        keypoints[2], keypoints[1], keypoints[3])
    right_elbow_startpoint, right_elbow_angle = startpoint_twovector(
        keypoints[3], keypoints[2], keypoints[4])
    left_hip_startpoint, left_hip_angle = startpoint_twovector(
        keypoints[12], keypoints[8], keypoints[3])
    left_knee_startpoint, left_knee_angle = startpoint_twovector(
        keypoints[13], keypoints[12], keypoints[14])
    right_hip_startpoint, right_hip_angle = startpoint_twovector(
        keypoints[9], keypoints[8], keypoints[10])
    right_knee_startpoint, right_knee_angle = startpoint_twovector(
        keypoints[10], keypoints[9], keypoints[11])
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

def startpoint_twovector(point, point2, point3):
    vec1 = np.zeros(2, dtype=int)
    vec2 = np.zeros(2, dtype=int)
    startpoint = [point[0], point[1]]
    vec1[0] = point2[0] - point[0]
    vec1[1] = point2[1] - point[1]
    vec2[0] = point3[0] - point[0]
    vec2[1] = point3[1] - point[1] 
    try:
        cosine_angle = np.dot(vec1, vec2) / (la.norm(vec1) * la.norm(vec2))
        cosine_angle = clip_cosine(cosine_angle)
        angle = np.arccos(cosine_angle)
        degree = round(np.degrees(angle))
        return startpoint, degree
    except Exception as e:
        return startpoint, None



def clip_cosine(angle):
    if angle < -1:
        return -1
    elif angle > 1:
        return 1
    return angle