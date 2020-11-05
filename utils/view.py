import cv2
import numpy as np


class View(object):
    def __init__(self, args):
        self._img = None
        self.args = args

    @property
    def img(self):
        return self._img

    @img.setter
    def img(self, new_img):
        self._img = new_img

    def draw_skeleton(self, points, clr, thickness):
        cv2.polylines(
            self.img, points,
            isClosed=False, color=clr, thickness=thickness)

    def draw_line(self, line, clr, thickness):
        x, y = line
        x = x or self.args.cam_width
        y = y or self.args.cam_height
        cv2.line(
            self.img, (0, int(y)), (int(x), int(y)),
            color=clr, thickness=thickness)

    def draw_circle(self, circle, clr, thickness):
        x, y, r = circle
        cv2.circle(
            self.img, (int(x), int(y)), int(r * 10),
            color=clr, thickness=thickness)

    def draw_rectangle(self, coor, clr, thickness):
        x1, x2, y1, y2 = coor
        cv2.rectangle(
            self.img, (int(x1), int(y1)), (int(x2), int(y2)),
            color=clr, thickness=thickness)

    def draw_list(self, need_to_draw, clr, thickness):
        temp = need_to_draw[0]
        if isinstance(temp, tuple):
            for draw in need_to_draw:
                self.draw_circle(draw, clr, thickness)
        elif type(temp).__module__ == np.__name__:
            self.draw_skeleton(need_to_draw, clr, thickness)

    def show(self, need_to_draw, clr, thickness):
        if need_to_draw is None or len(need_to_draw) == 0:
            return
        if isinstance(need_to_draw, list):
            self.draw_list(need_to_draw, clr, thickness)
        elif isinstance(need_to_draw, tuple):
            if len(need_to_draw) == 2:
                self.draw_line(need_to_draw, clr, thickness)
            elif len(need_to_draw) == 3:
                self.draw_circle(need_to_draw, clr, thickness)
            elif len(need_to_draw) == 4:
                self.draw_rectangle(need_to_draw, clr, thickness)

    def destroy(self):
        cv2.destroyAllWindows()
