import cv2
import numpy as np

from behavior.test import Test


class Open(Test):
    def __init__(self, analysis):
        super().__init__(analysis)
        self.center = ()
        self.center_x = []
        self.center_y = []

    def __call__(self, img, points, face):
        print("Open")
        self.append(points, face)

        if self.is_point_in_thres(img, points, face):
            # if not self.move(points):
            #     self.counter.start()
            #     self.center_x.append(points["right_wrist_x"])
            #     self.center_y.append(points["right_wrist_y"])
            #     if len(self.center_x) > 3:
            #         self.center_x = self.center_x[1:]
            #         self.center_y = self.center_y[1:]
            #     if self.counter.result() > self.time:
            #         self.center = (
            #             np.mean(self.center_x),
            #             np.mean(self.center_y),
            #         )
            #         x, y = self.center
            #         cv2.circle(img, (int(x), int(y)), 3, (0, 200, 200), 3)
            # else:
            self.counter.reset()
            self.center_x = []
            self.center_y = []
            if self.center == ():
                self.history = self.cut_start_history()
                print(self.history)
                x = self.history["right_wrist_x"][0]
                y = self.history["right_wrist_y"][0]
                cv2.circle(img, (int(x), int(y)), 3, (0, 0, 200), 3)

        if self.is_drop_the_hands(points):
            self.analysis.change(Close(self.analysis))

    def change(self, new_state):
        self.state = new_state


class Close(object):
    def __init__(self, analysis):
        self.analysis = analysis

    def __call__(self, img, points, face):
        if self.is_upper_than_line(points):
            self.analysis.change(Open(self.analysis))

    def is_inside_the_circle(self, img, points):
        x = points["right_wrist_x"]
        y = points["right_wrist_y"]
        x1 = points["right_shoulder_x"]
        y1 = points["right_shoulder_y"]
        r = 75
        dist = self.norm(x, y, x1, y1)
        cv2.circle(img, (int(x1), int(y1)), r, (0, 200, 200), 3)
        return dist < r

    def is_upper_than_line(self, points):
        y = points["right_wrist_y"]
        thres = self.analysis.calc_thres(points, 2)
        return y < thres

    def norm(self, x1, y1, x2, y2):
        return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


""""
self.find_closest_point(points)
cv2.circle(
    img, (
        int(self.default_center[0]),
        int(self.default_center[1])
    ), 10, (0, 200, 200), -1)

if self.is_point_in_thres(img, points, face) and not self.move(points):
    self.center_x.append(points["right_wrist_x"])
    self.center_y.append(points["right_wrist_y"])
    self.counter.start()
    if self.counter.result() > self.time:
        self.reset_center()
        cv2.circle(
            img, (
                int(self.center[0]),
                int(self.center[1])
            ), 10, (0, 200, 200), -1)
    #     self.change(Moving(self.)
else:
    self.center = ()
    self.center_x = []
    self.center_y = []
    self.counter.reset()


        if self.center == ():
            if not self.move(points):
                self.counter.start()
                self.center_x.append(points["right_wrist_x"])
                self.center_y.append(points["right_wrist_y"])
                if self.counter.result() > self.time:
                    temp = self.cut_start_history()
                    if temp != {}:  # temp 的第一個值就是起點 -> 畫出來應該會在中間
                        x = temp["right_wrist_x"][0]
                        y = temp["right_wrist_y"][0]
                        cv2.circle(img, (int(x), int(y)), 3, (0, 200, 200), -1)
                        if not self.is_point_in_thres(img, points, face):
                            print("Calculate Angles")
                            angles = self.predict_by_angles(temp)
                            print(angles)
                            self.history = {}
                        else:
                            print("Calculate dx and dy")
                            predict = self.predict_by_gradients(temp)
                            if predict == "":
                                self.history = {}
                                self.center = (
                                    np.mean(self.center_x),
                                    np.mean(self.center_y),
                                )
                                self.center_x = []
                                self.center_y = []
                            else:
                                print(predict)
        else:
            x, y = self.center
            cv2.circle(img, (int(x), int(y)), 3, (0, 200, 200), 3)
            if not self.move(points):
                print(len(self.history["right_wrist_x"]))
                self.center = ()
                self.center_x = []
                self.center_y = []
                self.history = {}


"""
