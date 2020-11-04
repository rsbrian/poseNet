import cv2
import numpy as np


class View(object):
    def __init__(self):
        self._img = None

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
