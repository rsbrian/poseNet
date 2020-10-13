import cv2
import datetime

class HomeObject():
    def __init__(self, width, height):
        self.width = height
        self.height = width
        self.humanBody = {}

        self.calibrateRangeX = 10
        self.calibrateRangeY = 30
        self.clickBuffer = 30

        self.bicepsCurlAngle1 = 45
        self.bicepsCurlAngle2 = 30

        self.holding = 3
        # FPS 大約 9~16

        self.leftHand = 0
        self.rightHand = 0
        self.bdumbbellLateral = 0

    def settingHumanBodyFromPoints(self, points):
        self.humanBody["leftHipX"] = points[0][0][0]
        self.humanBody["leftHipY"] = points[0][0][1]
        self.humanBody["rightHipX"] = points[5][0][0]
        self.humanBody["rightHipY"] = points[5][0][1]
        self.humanBody["leftAnkleX"] = points[4][1][0]
        self.humanBody["leftAnkleY"] = points[4][1][1]
        self.humanBody["rightAnkleX"] = points[9][1][0]
        self.humanBody["rightAnkleY"] = points[9][1][1]
        self.humanBody["leftWristX"] = points[2][1][0]
        self.humanBody["leftWristY"] = points[2][1][1]
        self.humanBody["leftElbowX"] = points[1][0][0]
        self.humanBody["leftElbowY"] = points[1][0][1]
        self.humanBody["rightWristX"] = points[7][1][0]
        self.humanBody["rightWristY"] = points[7][1][1]
        self.humanBody["leftShoulderX"] = points[0][1][0]
        self.humanBody["leftShoulderY"] = points[0][1][1]
        self.humanBody["rightShoulderX"] = points[6][1][0]
        self.humanBody["rightShoulderY"] = points[6][1][1]

    def settingCalibrateAxis(self):
        segment_width = self.width // 3
        segment_height = self.height // 6
        x1 = segment_width * 1 + self.calibrateRangeX
        x2 = segment_width * 2 - self.calibrateRangeX
        y1 = segment_height * 4 - self.calibrateRangeY
        y2 = segment_height * 5 + self.calibrateRangeY
        return x1, x2, y1, y2

    def calibrateHumanBody(self):
        x1, x2, y1, y2 = self.settingCalibrateAxis()
        c1 = x1 < self.humanBody["leftAnkleX"] and self.humanBody["leftAnkleX"] < x2
        c2 = x1 < self.humanBody["rightAnkleX"] and self.humanBody["rightAnkleX"] < x2
        c3 = y1 < self.humanBody["leftAnkleY"] and self.humanBody["leftAnkleY"] < y2
        c4 = y1 < self.humanBody["rightAnkleY"] and self.humanBody["rightAnkleY"] < y2
        return c1 and c2 and c3 and c4
        
    def chooseAction(self, homeAPI, up_angle):
        c = self.checkBicepsCurl(up_angle)
        if c == 1:
            return self.settingAction('雙手彎舉')
        elif c == 2:
            return self.settingAction('雙手交叉')
        elif self.checkRightHandCurl():
            return self.settingAction('右手彎舉')
        elif self.checkLeftHandCurl():
            return self.settingAction('左手彎舉')
        return homeAPI["最後動作"], homeAPI["最後動作時間"]

    def settingAction(self, name):
        timestamp = datetime.datetime.now()
        return name, timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")

    def checkRightHandCurl(self): # 右手彎舉
        if self.isAHigherThanB("rightWristY", "rightShoulderY"): self.rightHand += 1
        else: self.rightHand = 0
        return self.rightHand > self.holding

    def checkLeftHandCurl(self): # 左手彎舉
        if self.isAHigherThanB("leftWristY", "leftShoulderY"): self.leftHand += 1
        else: self.leftHand = 0
        return self.leftHand > self.holding

    def checkBicepsCurl(self, up_angle): # 雙手彎舉
        left_elbow_angle = up_angle[1][1]
        right_elbow_angle = up_angle[3][1]

        c1 = abs(self.humanBody["leftWristX"] - self.humanBody["rightWristX"]) < 100
        c2 = left_elbow_angle < self.bicepsCurlAngle1
        c3 = right_elbow_angle < self.bicepsCurlAngle1

        c4 = left_elbow_angle < self.bicepsCurlAngle2
        c5 = right_elbow_angle < self.bicepsCurlAngle2

        if c1 and c2 and c3: return 2
        elif c4 and c5: return 1

    def checkBdumbbellLateral(self): # 側平舉
        if self.isAHigherThanB("leftWristY", "leftShoulderY") and (self.humanBody["leftWristX"] - self.humanBody["leftElbowX"]) > 50:
            self.bdumbbellLateral += 1
        else:
            self.bdumbbellLateral = 0
        return self.bdumbbellLateral > self.holding

    def isAHigherThanB(self, A, B):
        return self.humanBody[A] < (self.humanBody[B] + self.clickBuffer)

    def show(self, image):
        x1, x2, y1, y2 = self.settingCalibrateAxis()
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 3)
