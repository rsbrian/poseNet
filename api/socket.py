class Api(object):
    def __init__(self):
        self._course = {"name": ""}
        self._course_action = {
            "function": "getExercise",
            "tip": {"note": [""], "duration": 0},
            "action": {
                "alert": [""],
                "alertLastTime": "",
                "startPoint": "",
                "startPointLastTime": "",
                "lastTime": "",
                "times": 0,
                "stop": False,
                "quit": False,
                "score": 0
            },
            "start": False,
        }
        self._end = {"break": False}
        self._behavior = {
            'function': 'exercise_status',
            '最後動作': ''
        }
        self._qrcode = {
            "function": "qrcode"
            "content": ""
        }

    @property
    def course(self):
        return self._course

    @course.setter
    def course(self, key, value):
        self._course[key] = value

    @property
    def course_action(self):
        return self._course_action

    @course_action.setter
    def course_action(self, key, value):
        self._course_action[key] = value

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, key, value):
        self._end[key] = value

    @property
    def behavior(self):
        return self._behavior

    @behavior.setter
    def behavior(self, key, value):
        self._behavior[key] = value

    @property
    def qrcode(self):
        return self._qrcode

    @qrcode.setter
    def qrcode(self, key, value):
        self._qrcode[key] = value
