import cv2
import imutils
import numpy as np


class Camera(object):
    def __init__(self, args, video_name, saved_names):
        self.args = args
        self.outs = {}
        self.original_img = None

        if self.args.cam_id != -1:
            self.cap = cv2.VideoCapture(self.args.cam_id)
            self.add_writers(saved_names)
        else:
            self.cap = cv2.VideoCapture(video_name)
            self.args.save = 0

    def add_writers(self, saved_names):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        fps = 20.0
        shape = (self.args.cam_width, self.args.cam_height)
        for name in saved_names:
            file_name, format_name = name.split('.')
            self.outs[file_name] = cv2.VideoWriter(name, fourcc, fps, shape)

    def isOpened(self):
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def save(self, img, name):
        if self.args.save:
            self.outs[name].write(img)

    def release(self):
        if self.args.save:
            for k, out in self.outs.items():
                out.release()
        self.cap.release()

    def get_original_img(self):
        return self.original_img

    def preprocessing(self, img):
        h, w, c = img.shape

        if h < w:
            img = imutils.rotate_bound(img, self.args.rotate)
            # for c in range(img.shape[2]):
            #     img[:, :, c] = cv2.equalizeHist(img[:, :, c])

        img = cv2.resize(img, (self.args.cam_width, self.args.cam_height))
        self.original_img = img.copy()
        return img

    def get_multi_skeleton_from(self, img, third_party):
        return third_party.get_multi_skeleton(img, self.args)

    def multi_person_filter(self, img, points):
        result = []
        minmimum = np.inf
        center = self.args.cam_width // 2
        (x, y, r) = (None, None, None)
        for i in range(len(points)):
            face_points = points[i][1]

            x = np.mean([point[0] for point in face_points])
            y = np.mean([point[1] for point in face_points])
            r = np.mean([point[2] for point in face_points])

            try:
                cv2.circle(img, (int(x), int(y)), int(r), (255, 255, 0), -1)
                diff = abs(x - center)
                if diff < minmimum:
                    result = points[i][0].copy()
                    x = np.mean([point[0] for point in points[i][1]])
                    y = np.mean([point[1] for point in points[i][1]])
                    r = np.mean([point[2] for point in points[i][1]])
                    minmimum = diff

            except Exception as e:
                print(x, y, r, e)

        return img, result, (x, y, r)
