import os

def mkdir(current_path):
    courses_path = os.path.join(current_path, "courses")
    courses_folder = os.listdir("courses")
    for c in courses_folder:
        target = os.path.join(os.path.join(current_path, "courses"), c)
        if not os.path.isdir(target):
            name, _ = c.split(".")
            if "noCourse" in name:
                continue
            result_path = os.path.join(os.path.join(current_path, "videos"), name)
            if not os.path.isdir(result_path):
                os.mkdir(result_path)
