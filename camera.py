import cv2
import imutils
import numpy as np


class Camera(object):
    def __init__(self, args, video_name, saved_names):
        self.args = args
        self.outs = {}

        if self.args.cam_id != -1:
            self.cap = cv2.VideoCapture(self.args.cam_id)
            if self.args.save:
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

    def preprocessing(self, img):
        h, w, c = img.shape

        if h < w:
            img = imutils.rotate_bound(img, self.args.rotate)
            # for c in range(img.shape[2]):
            #     img[:, :, c] = cv2.equalizeHist(img[:, :, c])

        img = cv2.resize(img, (self.args.cam_width, self.args.cam_height))
        return img

    def one_person_filter(self, multi_points):
        face = ()
        points = []
        all_faces = []
        minmimum = np.inf
        center = self.args.cam_width // 2
        for i in range(len(multi_points)):
            face_points = multi_points[i][1].copy()

            if len(face_points) > 0:
                x = np.mean([point[0] for point in face_points])
                y = np.mean([point[1] for point in face_points])
                r = np.mean([point[2] for point in face_points])
                all_faces.append((x, y, r))

                diff = abs(x - center)
                if diff < minmimum:
                    points = multi_points[i][0].copy()
                    face = (x, y, r)
                    minmimum = diff

        return points, face, all_faces
