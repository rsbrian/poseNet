class Human:
    def __init__(self):
        self._angles = {}
        self._points = {}
        self._temp_points = {}

    @property
    def temp_points(self):
        return self._points

    @temp_points.setter
    def temp_points(self, new_points):
        self._points["left_hip_x_temp"] = self._points["left_hip_x"]
        self._points["left_hip_y_temp"] = self._points["left_hip_y"]
        self._points["left_knee_x_temp"] = self._points["left_knee_x"]
        self._points["left_knee_y_temp"] = self._points["left_knee_y"]
        self._points["right_knee_x_temp"] = self._points["right_knee_x"]
        self._points["right_knee_y_temp"] = self._points["right_knee_y"]
        self._points["right_hip_x_temp"] = self._points["right_hip_x"]
        self._points["right_hip_y_temp"] = self._points["right_hip_y"]
        self._points["left_ankle_x_temp"] = self._points["left_ankle_x"]
        self._points["left_ankle_y_temp"] = self._points["left_ankle_y"]
        self._points["right_ankle_x_temp"] = self._points["right_ankle_x"]
        self._points["right_ankle_y_temp"] = self._points["right_ankle_y"]
        self._points["left_wrist_x_temp"] = self._points["left_wrist_x"]
        self._points["left_wrist_y_temp"] = self._points["left_wrist_y"]
        self._points["left_elbow_x_temp"] = self._points["left_elbow_x"]
        self._points["left_elbow_y_temp"] = self._points["left_elbow_y"]
        self._points["right_elbow_x_temp"] = self._points["right_elbow_x"]
        self._points["right_elbow_y_temp"] = self._points["right_elbow_y"]
        self._points["right_wrist_x_temp"] = self._points["right_wrist_x"]
        self._points["right_wrist_y_temp"] = self._points["right_wrist_y"]
        self._points["left_shoulder_x_temp"] = self._points["left_shoulder_x"]
        self._points["left_shoulder_y_temp"] = self._points["left_shoulder_y"]
        self._points["right_shoulder_x_temp"] = self._points["right_shoulder_x"]
        self._points["right_shoulder_y_temp"] = self._points["right_shoulder_y"]

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, new_points):
        self._points["left_hip_x"] = new_points[0][0][0]
        self._points["left_hip_y"] = new_points[0][0][1]
        self._points["left_knee_x"] = new_points[4][0][0]
        self._points["left_knee_y"] = new_points[4][0][1]
        self._points["right_knee_x"] = new_points[8][1][0]
        self._points["right_knee_y"] = new_points[8][1][1]
        self._points["right_hip_x"] = new_points[5][0][0]
        self._points["right_hip_y"] = new_points[5][0][1]
        self._points["left_ankle_x"] = new_points[4][1][0]
        self._points["left_ankle_y"] = new_points[4][1][1]
        self._points["right_ankle_x"] = new_points[9][1][0]
        self._points["right_ankle_y"] = new_points[9][1][1]
        self._points["left_wrist_x"] = new_points[2][1][0]
        self._points["left_wrist_y"] = new_points[2][1][1]
        self._points["left_elbow_x"] = new_points[1][0][0]
        self._points["left_elbow_y"] = new_points[1][0][1]
        self._points["right_elbow_x"] = new_points[6][0][0]
        self._points["right_elbow_y"] = new_points[6][0][1]
        self._points["right_wrist_x"] = new_points[7][1][0]
        self._points["right_wrist_y"] = new_points[7][1][1]
        self._points["left_shoulder_x"] = new_points[0][1][0]
        self._points["left_shoulder_y"] = new_points[0][1][1]
        self._points["right_shoulder_x"] = new_points[6][1][0]
        self._points["right_shoulder_y"] = new_points[6][1][1]

    @property
    def angles(self):
        return self._angles

    @angles.setter
    def angles(self, new_angles):
        self._angles["left_shoulder_angle"] = new_angles[0][1]
        self._angles["right_shoulder_angle"] = new_angles[2][1]

        self._angles["left_elbow_angle"] = new_angles[1][1]
        self._angles["right_elbow_angle"] = new_angles[3][1]

        self._angles["left_knee_angle"] = new_angles[5][1]
        self._angles["right_knee_angle"] = new_angles[7][1]
