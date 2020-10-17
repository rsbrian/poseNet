from courses.template.alert import ALERTS


class PrepareTemp(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain

    def __call__(self, check_list):
        print("Preparing")
        self.counter.start()
        for error in check_list:
            if self.check(error):
                return

        if self.is_ready_to_start():
            self.course.api.course_action["start"] = True
            self.brain.reset_temp_points()
            # self.course.change(
            #     Action(self.course, self.brain))

    def check(self, error):
        if self.brain.is_pose(ALERTS[error]):
            self.course.api.course_action["tip"]["note"] = [error]
            self.counter.reset()
            return True
        return False

    def is_ready_to_start(self):
        self.course.api.course_action["tip"]["note"] = [
            f"很好請保持"]
        self.course.set_time("lastTime")
        self.course.set_time("startPoint")
        return self.counter.result() > 3
