from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.motion = None
        self.posture = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.logger = self.session().service("ALLogger")
            self.logger.info("LookAroundStanding", "Script loaded and ready.")
        except Exception as e:
            self.logger.error("LookAroundStanding", "Error during initialization: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("LookAroundStanding", "Script is already running.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("LookAroundStanding", "Starting head movement.")
            
            # Проверка, что робот стоит
            if self.posture.getPosture() not in ["Stand", "StandInit", "StandZero"]:
                self.logger.info("LookAroundStanding", "Switching to StandInit posture.")
                self.posture.goToPosture("StandInit", 0.7)
                time.sleep(1)

            # Плавные движения головой по сторонам
            head_movements = [
                (["HeadYaw"], [-0.6], 0.2),  # Смотрит влево
                (["HeadYaw"], [0.6], 0.2),   # Смотрит вправо
                (["HeadYaw"], [0.0], 0.2),   # Смотрит прямо
                (["HeadPitch"], [0.2], 0.2), # Смотрит немного вниз
                (["HeadPitch"], [-0.2], 0.2),# Смотрит немного вверх
                (["HeadPitch", "HeadYaw"], [0.0, 0.0], 0.2) # Возвращается к центру
            ]

            for joints, angles, speed in head_movements:
                self.motion.angleInterpolationWithSpeed(joints, angles, speed)
                time.sleep(0.5)

            self.logger.info("LookAroundStanding", "Head movement completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("LookAroundStanding", "Error during execution: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("LookAroundStanding", "Stopping head movement.")
        self.bIsRunning = False
        self.onStopped()
