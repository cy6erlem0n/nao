from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.logger = None

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.logger = self.session().service("ALLogger")
        self.logger.info("NAO Look Around", "Behavior loaded.")

    def onInput_onStart(self):
        try:
            self.logger.info("NAO Look Around", "Starting behavior.")

            # В начальную позу
            self.posture.goToPosture("StandInit", 0.6)
            time.sleep(1)

            # Смотрит влево
            self.motion.setStiffnesses("Head", 1.0)
            self.motion.angleInterpolationWithSpeed("HeadYaw", 0.8, 0.2)
            time.sleep(1)

            # Смотрит вправо
            self.motion.angleInterpolationWithSpeed("HeadYaw", -0.8, 0.2)
            time.sleep(1)

            # Смотрит прямо
            self.motion.angleInterpolationWithSpeed("HeadYaw", 0.0, 0.2)
            time.sleep(1)

            self.logger.info("NAO Look Around", "Behavior completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("NAO Look Around", "Error during execution: {}".format(e))

    def onInput_onStop(self):
        self.logger.info("NAO Look Around", "Stopping behavior.")
        self.motion.setStiffnesses("Head", 0.0)
        self.onStopped()
