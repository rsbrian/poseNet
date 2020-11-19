import sys
import cv2
import os
from sys import platform
import argparse
from camera import Camera

def wxfopenpose():
    try:
        # Import Openpose (Windows/Ubuntu/OSX)
        dir_path = os.path.dirname(os.path.realpath(__file__))
        try:
            # Windows Import
            if platform == "win32":
                sys.path.append(dir_path + '/../../python/openpose/Release');
                os.environ['PATH']  = os.environ['PATH'] + ';' + dir_path + '/../../x64/Release;' +  dir_path + '/../../bin;'
                import pyopenpose as op
            else:
                sys.path.append('../../python');
                from openpose import pyopenpose as op
        except ImportError as e:
            print('Error: OpenPose library could not be found. Did you enable `BUILD_PYTHON` in CMake and have this Python script in the right folder?')
            raise e

        parser = argparse.ArgumentParser()
        args = parser.parse_known_args()
        params = dict()
        params["model_folder"] = "../../../models/"
    
        # Add others in path?
        for i in range(0, len(args[1])):
            curr_item = args[1][i]
            if i != len(args[1])-1: next_item = args[1][i+1]
            else: next_item = "1"
            if "--" in curr_item and "--" in next_item:
                key = curr_item.replace('-','')
                if key not in params:  params[key] = "1"
            elif "--" in curr_item and "--" not in next_item:
                key = curr_item.replace('-','')
                if key not in params: params[key] = next_item
        # Starting OpenPose
        opWrapper = op.WrapperPython()
        opWrapper.configure(params)
        opWrapper.start()
        cap = cv2.VideoCapture(1)
        while(True):
            ret, frame = cap.read()
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE) 
            datum = op.Datum()
            datum.cvInputData = frame
            opWrapper.emplaceAndPop(op.VectorDatum([datum]))
            print("Body keypoints: \n" + str(datum.poseKeypoints))
            cv2.imshow('frame', datum.cvOutputData)
            if cv2.waitKey(1) == ord('q'):
                break

    except Exception as e:
        print(e)
        sys.exit(-1)
    return datum.poseKeypoints


if __name__ == "__main__":
    a = wxfopenpose()