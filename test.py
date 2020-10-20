import time
from utils.counter import Counter

TEMPLATES = {
    "雙腳請與肩同寬": "shoulder_width_apart",
    "請將手自然垂放": "drop_hand_natrually"
}


class Brain(object):
    def is_pose(self, name):
        # if name == "drop_hand_natrually":
        #     return True
        return False


class Basic(object):
    def __init__(self):
        self.state = None

    def __call__(self):
        self.state()

    def change(self, new_state):
        self.state = new_state


class BicepsCurl(Basic):
    def __init__(self):
        super().__init__()
        self.brain = Brain()
        self.state = Prepare(self.brain)

    def __call__(self):
        super().__call__()


class PrepareTemp(object):
    def __init__(self, brain):
        self.brain = brain

    def __call__(self, todos):
        self.counter.start()
        print("Prepare")
        for name in todos:
            if self.check_error(name):
                return
        if self.is_ready_to_start():
            print("START, RESET, CHANGE")

    def check_error(self, ch):
        if self.brain.is_pose(TEMPLATES[ch]):
            print("tip, note", ch)
            self.counter.reset()
            return True
        return False

    def is_ready_to_start(self):
        return self.counter.result() > 3


class Prepare(PrepareTemp):
    def __init__(self, brain):
        super().__init__(brain)
        self.counter = Counter()
        self.todo_list = [
            "雙腳請與肩同寬",
            "請將手自然垂放"
        ]

    def __call__(self):
        super().__call__(self.todo_list)


b = BicepsCurl()

for i in range(5):
    b()
    time.sleep(1)
