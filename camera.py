import cv2
import imutils
import numpy as np
import datetime


class Camera(object):
    def __init__(self, args, videos):
        self.args = args
        self.outs = {}

        if self.args.cam_id != -1:
            self.cap = cv2.VideoCapture(self.args.cam_id)
        else:
            video_name = f"videos/test/{sorted(videos)[-1]}"
            self.cap = cv2.VideoCapture(video_name)
            self.args.save = 0

    def tuple_to_str(self, shape):
        x1, x2 = shape
        return f"{str(x1)}x{str(x2)}"

    def add_writers(self, resolutions, folder_name):
        if self.args.save:
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            fps = 20.0
            time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
            for shape in resolutions:
                name = self.tuple_to_str(shape)
                file_name = f"videos/{folder_name}/{time}_{name}"
                self.outs[name] = cv2.VideoWriter(f"{file_name}.avi", fourcc, fps, shape)

    def isOpened(self):
        if not self.cap.isOpened():
            raise "Please Check the camera id."
        return self.cap.isOpened()

    def read(self):
        return self.cap.read()

    def save(self, resolutions):
        if len(self.outs) == 0: return
        for resolution in resolutions:
            img = cv2.resize(self.original_img, resolution)
            self.outs[self.tuple_to_str(resolution)].write(img)

    def store(self, img):
        self.original_img = img.copy()

    def writer_release(self):
        for name, out in self.outs.items():
            out.release()

    def release(self):
        self.cap.release()

    def preprocessing(self, img):
        h, w, c = img.shape

        if h < w:
            img = imutils.rotate_bound(img, self.args.rotate)

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
                #x = np.mean([point[0] for point in face_points])
                #y = np.mean([point[1] for point in face_points])
                #r = np.mean([point[2] for point in face_points])
                x = np.mean(face_points[0])
                y = np.mean(face_points[1])
                r = np.mean(face_points[2])
                all_faces.append((x, y, r))

                diff = abs(x - center)
                if diff < minmimum:
                    points = multi_points[i][0].copy()
                    face = (x, y, r)
                    minmimum = diff

        return points, face, all_faces

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
