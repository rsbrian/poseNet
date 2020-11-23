import os
import shutil
from mkdir import mkdir

def rmdir():
    os.chdir("C:\\Users\\iiids\\Documents\\openPose\\openpose\\build\\examples\\openpose_mirror")
    cs = os.listdir("videos")
    for c in cs:
        if "test" in c:
            continue
        name = os.path.join(os.getcwd(), os.path.join("videos", c))
        shutil.rmtree(name)
