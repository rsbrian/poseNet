import os

def mkdir():
    os.chdir("/home/iiidsimirror/Documents/poseNet")
    cs = os.listdir("courses")
    for c in cs:
        if not os.path.isdir(os.path.join(os.getcwd(), os.path.join("courses", c))):
            name, _ = c.split(".")
            if "noCourse" in name:
                continue
            name = os.path.join(os.getcwd(), os.path.join("videos", name.lower()))
            os.mkdir(name)
