import time


class Counter(object):
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.logs = {}

    def record(self, name):
        self.logs[name] = self.result()

    def get_logs(self):
        return self.logs

    def start(self):
        if self.start_time is None:
            self.start_time = time.time()
        self.end_time = time.time()

    def reset(self):
        self.__init__()
        self.start()

    def result(self):
        self.end_time = time.time()
        return round(self.end_time - self.start_time, 2)
