import os
import cv2
import glob
import argparse
import matplotlib
import numpy as np
import tensorflow as tf

from PIL import Image
from keras.models import load_model
from matplotlib import pyplot as plt
from layers import BilinearUpSampling2D
from utils import predict, load_images, display_images

# os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'

parser = argparse.ArgumentParser(
    description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='nyu.h5', type=str,
                    help='Trained Keras model file.')
parser.add_argument('--input', default='examples/*.png',
                    type=str, help='Input filename or folder.')
args = parser.parse_args()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True
sess = tf.Session(config=config)

physical_devices = tf.config.experimental.list_physical_devices("GPU")
print("Num of GPUs", physical_devices)
if len(physical_devices):
    tf.config.experimental.set_memory_growth(physical_devices[0], True)

custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D,
                  'depth_loss_function': None}
model = load_model(args.model, custom_objects=custom_objects, compile=False)

cap = cv2.VideoCapture(0)

while(cap.isOpened()):
    ret, frame = cap.read()

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (480, 960))
    frame = np.clip(np.asarray(frame, dtype=float) / 255, 0, 1)
    inputs = frame.reshape(1, frame.shape[0], frame.shape[1], frame.shape[2])

    outputs = predict(model, inputs)

    _, result = display_images(
        outputs.copy(), inputs.copy(), is_colormap=False)

    cv2.imshow("result", result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
