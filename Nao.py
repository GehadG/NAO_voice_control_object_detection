import math

from controller import Robot, Motion


class Nao(Robot):
    PHALANX_MAX = 8
    RED = [1.0, 0.0, 0.0]
    GREEN = [0.0, 1.0, 0.0]
    BLUE = [0.0, 0.0, 1.0]

    # load motion files
    def loadMotionFiles(self):
        self.handWave = Motion('motions/HandWave.motion')
        self.forwardsxl = Motion('motions/Forwards50.motion')
        self.forwards = Motion('motions/Forwards.motion')
        self.backwards = Motion('motions/Backwards.motion')
        self.sideStepLeft = Motion('motions/SideStepLeft.motion')
        self.sideStepRight = Motion('motions/SideStepRight.motion')
        self.turnLeft_xl = Motion('motions/TurnLeft60.motion')
        self.turnRight_xl = Motion('motions/TurnRight60.motion')
        self.turnLeft_l = Motion('motions/TurnLeft40.motion')
        self.turnRight_l = Motion('motions/TurnRight40.motion')
        self.turnLeft_m = Motion('motions/TurnLeft20.motion')
        self.turnRight_m = Motion('motions/TurnRight20.motion')
        self.turnLeft_s = Motion('motions/TurnLeft10.motion')
        self.turnRight_s = Motion('motions/TurnRight10.motion')

    def startMotion(self, motion):
        # interrupt current motion
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()
        motion.play()
        self.currentlyPlaying = motion

    def findAndEnableDevices(self):
        self.timeStep = int(self.getBasicTimeStep())
        # camera
        self.cameraTop = self.getDevice("CameraTop")
        self.cameraBottom = self.getDevice("CameraBottom")
        self.cameraTop.enable(4 * self.timeStep)
        self.cameraBottom.enable(4 * self.timeStep)
        self.cameraTop.recognitionEnable(4 * self.timeStep)
        self.cameraBottom.recognitionEnable(4 * self.timeStep)

        # sonars
        self.sonar_right = self.getDevice('Sonar/Right')
        self.sonar_left = self.getDevice('Sonar/Left')
        self.sonar_right.enable(4 * self.timeStep)
        self.sonar_left.enable(4 * self.timeStep)

        # bumpers
        self.right_foot_right_bumper = self.getDevice('RFoot/Bumper/Right')
        self.right_foot_left_bumper = self.getDevice('RFoot/Bumper/Left')
        self.left_foot_right_bumper = self.getDevice('LFoot/Bumper/Right')
        self.left_foot_left_bumper = self.getDevice('LFoot/Bumper/Left')
        self.right_foot_right_bumper.enable(4 * self.timeStep)
        self.right_foot_left_bumper.enable(4 * self.timeStep)
        self.left_foot_right_bumper.enable(4 * self.timeStep)
        self.left_foot_left_bumper.enable(4 * self.timeStep)

        # accelerometer
        self.accel = self.getDevice('accelerometer')
        self.accel.enable(4 * self.timeStep)

        # gyro
        self.gyro = self.getDevice('gyro')
        self.gyro.enable(4 * self.timeStep)

    def __init__(self):
        Robot.__init__(self)
        self.currentlyPlaying = False
        self.findAndEnableDevices()
        self.loadMotionFiles()

    def perform_motion(self, motion):
        motion.play()
        while not motion.isOver():
            self.step(self.timeStep)

    def handle_callback(self, inference):
        if inference.is_understood:
            for k, v in inference.slots.items():
                if inference.intent == 'locate':
                    self.handleLocate(v)
                elif inference.intent == 'goto':
                    self.handeNavigate(v)
                elif inference.intent == 'move':
                    self.handleMove(v)
                elif inference.intent == 'turn':
                    self.handleTurn(v)
        else:
            print("Command not understood")

    def handleLocate(self, v):
        print("Finding an object with the color " + v)
        counter = 0
        detection_color = []
        if v == 'red':
            detection_color = self.RED
        elif v == 'green':
            detection_color = self.GREEN
        elif v == 'blue':
            detection_color = self.BLUE
        else:
            print("Color not preconfigured")
        color_found = False
        detected_object = {}
        while not color_found:
            self.perform_motion(self.turnRight_xl)
            objects = self.cameraTop.getRecognitionObjects()
            if objects:
                for object in objects:
                    if object.get_colors() == detection_color:
                        color_found = True
                        print("Object found!")
                        detected_object = object
            counter = counter + 1
            if counter == 6:
                print("Object with color " + v + " not found within the room")
        if color_found:
            id = detected_object.get_id()
            x, y, distance, angle = self.getObjectDetails(detected_object)
            if abs(angle) > 0.1:
                print("Getting Object to be centered in camera")
                if angle < 0:
                    self.moveLeftToCenterObject(id)
                    return id, True
                else:
                    self.moveRightToCenterObject(id)
                    return id, False

    def handeNavigate(self, v):
        id, was_left = self.handleLocate(v)
        self.navigateToObject(id, was_left)

    def handleMove(self, v):
        if v == 'forward':
            self.perform_motion(self.forwards)
        elif v == 'backward':
            self.perform_motion(self.backwards)
        elif v == 'left':
            self.perform_motion(self.sideStepLeft)
        elif v == 'right':
            self.perform_motion(self.sideStepRight)

    def handleTurn(self, v):
        if v == 'left':
            self.perform_motion(self.turnLeft_xl)
        elif v == 'right':
            self.perform_motion(self.turnRight_xl)

    def moveLeftToCenterObject(self, id):
        while True:
            self.perform_motion(self.turnLeft_s)
            objects = self.cameraTop.getRecognitionObjects()
            if objects:
                for object in objects:
                    if object.get_id() == id:
                        x, y, distance, currentAngle = self.getObjectDetails(object)
            if currentAngle >= 0:
                break

    def getObjectDetails(self, objectToParse):
        x = objectToParse.get_position()[0]
        y = objectToParse.get_position()[1]
        currentAngle = math.atan2(x, y)
        distance = math.sqrt(math.pow(x, 2) + math.pow(y, 2))
        return x, y, distance, currentAngle

    def moveRightToCenterObject(self, id):
        currentAngle = 0
        while True:
            self.perform_motion(self.turnLeft_s)
            objects = self.cameraTop.getRecognitionObjects()
            if objects:
                for object in objects:
                    if object.get_id() == id:
                        x, y, distance, currentAngle = self.getObjectDetails(object)
            if currentAngle <= 0:
                break

    def navigateToObject(self, id, was_left):
        print("Started Walking towards object")
        reached_object = False
        distance = 999
        old_distance = 999
        currentAngle = -9
        while not reached_object:
            if distance < 0.4:
                self.perform_motion(self.forwards)
            else:
                self.perform_motion(self.forwardsxl)
            objects = self.cameraTop.getRecognitionObjects()
            if objects:
                for object in objects:
                    if object.get_id() == id:
                        x, y, distance, currentAngle = self.getObjectDetails(object)
                        if (distance <= 0.25):
                            reached_object = True
            if distance == old_distance:
                print("Lost Sight of object, recalculating object position")
                was_left = self.refind_object(id, currentAngle)
            else:
                old_distance = distance
            if currentAngle < 0 and was_left:
                self.moveLeftToCenterObject(id)
            elif currentAngle > 0 and not was_left:
                self.moveRightToCenterObject(id)

    def refind_object(self, id, currentAngle):
        motion = self.turnLeft_xl
        object_found = False
        if currentAngle > 0:
            motion = self.turnRight_xl
        while not object_found:
            self.perform_motion(motion)
            objects = self.cameraTop.getRecognitionObjects()
            if objects:
                for object in objects:
                    if object.get_id() == id:
                        x, y, distance, angle = self.getObjectDetails(object)
                        if angle < 0:
                            return True
                        else:
                            return False
