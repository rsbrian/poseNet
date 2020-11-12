from utils.counter import Counter


class PrepareTemp(object):
    def __init__(self, course, brain, prepare_notes):
        self.course = course
        self.brain = brain
        self.prepare_notes = prepare_notes
        self.counter = Counter()
        self.course.set_prepare_msg(
            ["tip", "note"],
            self.course.default_prepare(self.prepare_notes))

    def __call__(self, action):
        self.counter.start()
        self.course.set_prepare_msg(
            ["tip", "note"],
            self.course.check_prepare(self.prepare_notes, self.counter.reset))
        if self.is_ready_to_start():
            self.course.api.course_action["start"] = True
            self.brain.reset_temp_points()
            self.course.change(
                action(self.course, self.brain))

    def is_ready_to_start(self):
        return self.counter.result() > 3

    def reset(self):
        self.counter.reset()
