class ErrorHandleingTemplate(object):
    def __init__(self, course, brain):
        self.course = course
        self.brain = brain
        self.error_weight = 1

    def __call__(self, check_list):
        for i, check in enumerate(check_list):
            c = self.brain.is_pose(check)
            if self.course.number != -1:
                c = c and (self.course.number == i)
            if c:
                self.course.api.course_action["action"]["score"] -= self.error_weight
                self.brain.reset_temp_points()
                return True
        return False
