import cv2
import numpy as np


class View(object):
    def __init__(self, brain):
        self.brain = brain
        self._height = None
        self._width = None
        self._rotate = None
        self._img = None

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, new_height):
        self._height = new_height

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, new_width):
        self._width = new_width

    @property
    def rotate(self):
        return self._rotate

    @rotate.setter
    def rotate(self, new_rotate):
        self._rotate = new_rotate

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, new_img):
        self._img = new_img

    def setting_calibrate_box(self):
        if self.height < self.width:
            segment_width = self.height // 3
            segment_height = self.width // 6
        else:
            segment_width = self.width // 3
            segment_height = self.height // 6

        x1 = segment_width * 1 + 10  # 1
        x2 = segment_width * 2 - 10  # 2
        y1 = segment_height * 4 + 50  # 4
        y2 = segment_height * 5 + 100  # 5
        return x1, x2, y1, y2

    def calibrate_human_body(self):
        x1, x2, y1, y2 = self.setting_calibrate_box()
        c1 = self.brain.compare("left_ankle_x", ">", x1) and \
            self.brain.compare("left_ankle_x", "<", x2)
        c2 = self.brain.compare("right_ankle_x", ">", x1) and \
            self.brain.compare("right_ankle_x", "<", x2)
        c3 = self.brain.compare("left_ankle_y", ">", y1) and \
            self.brain.compare("left_ankle_y", "<", y2)
        c4 = self.brain.compare("left_ankle_y", ">", y1) and \
            self.brain.compare("left_ankle_y", "<", y2)
        return c1 and c2 and c3 and c4

    def calibrate_human_body_leg(self):
        x1, x2, y1, y2 = self.setting_calibrate_box()
        x1 = x1 - 80
        x2 = x2 + 80
        c1 = self.brain.compare("left_ankle_x", ">", x1) and \
            self.brain.compare("left_ankle_x", "<", x2)
        c2 = self.brain.compare("right_ankle_x", ">", x1) and \
            self.brain.compare("right_ankle_x", "<", x2)
        c3 = self.brain.compare("left_ankle_y", ">", y1) and \
            self.brain.compare("left_ankle_y", "<", y2)
        c4 = self.brain.compare("left_ankle_y", ">", y1) and \
            self.brain.compare("left_ankle_y", "<", y2)
        return c1 and c2 and c3 and c4

    def draw_skeleton(self, points, clr, thickness):
        cv2.polylines(
            self.img, points,
            isClosed=False, color=clr, thickness=thickness)

    def draw_circle(self, circle, clr, thickness):
        x, y, r = circle
        cv2.circle(
            self.img, (int(x), int(y)), int(r * 10),
            color=clr, thickness=thickness)

    def draw_list(self, need_to_draw, clr, thickness):
        temp = need_to_draw[0]
        if isinstance(temp, tuple):
            for draw in need_to_draw:
                self.draw_circle(draw, clr, thickness)
        elif type(temp).__module__ == np.__name__:
            self.draw_skeleton(need_to_draw, clr, thickness)

    def show(self, need_to_draw, clr, thickness):
        if len(need_to_draw) == 0:
            return
        if isinstance(need_to_draw, list):
            self.draw_list(need_to_draw, clr, thickness)
        elif isinstance(need_to_draw, tuple):
            self.draw_circle(need_to_draw, clr, thickness)

    def destroy(self):
        cv2.destroyAllWindows()
