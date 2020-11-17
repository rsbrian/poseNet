import os
import shutil
from mkdir import mkdir

def rmdir():
    os.chdir("/home/iiidsimirror/Documents/poseNet")
    cs = os.listdir("videos")
    for c in cs:
        if "test" in c:
            continue
        name = os.path.join(os.getcwd(), os.path.join("videos", c))
        shutil.rmtree(name)
