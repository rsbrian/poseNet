import cv2
import imutils
import numpy as np


class Camera(object):
    def __init__(self, args):
        self.args = args

    def preprocessing(self, img):
        h, w, c = img.shape

        if h < w:
            img = imutils.rotate_bound(img, self.args.rotate)
            # for c in range(img.shape[2]):
            #     img[:, :, c] = cv2.equalizeHist(img[:, :, c])

        img = cv2.resize(img, (self.args.cam_width, self.args.cam_height))

        return img

    def get_multi_skeleton_from(self, img, third_party):
        return third_party.get_multi_skeleton(img, self.args)

    def multi_person_filter(self, img, points):
        result = []
        minmimum = np.inf
        center = self.args.cam_width // 2
        for i in range(len(points)):
            face_points = points[i][1]

            x = np.mean([point[0] for point in face_points])
            y = np.mean([point[1] for point in face_points])
            r = np.mean([point[2] for point in face_points])

            try:
                cv2.circle(img, (int(x), int(y)), int(r), (255, 255, 0), -1)

                if abs(x - center) < minmimum:
                    result = points[i][0].copy()
                    minmimum = abs(x - center)

            except Exception as e:
                print(x, y, r, e)

        return img, result
