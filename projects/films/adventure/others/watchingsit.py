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
            self.logger.info("LookAround", "Script loaded and ready.")
        except Exception as e:
            self.logger.error("LookAround", "Error during initialization: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("LookAround", "Script is already running.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("LookAround", "Starting head movement.")

            # Проверка, что робот сидит
            if self.posture.getPosture() not in ["Sit", "SitRelax"]:
                self.logger.info("LookAround", "Switching to SitRelax posture.")
                self.posture.goToPosture("SitRelax", 0.7)
                time.sleep(1)

            # Плавные движения головой по сторонам
            head_movements = [
                (["HeadYaw"], [-0.5], 0.2),  # Смотрит влево
                (["HeadYaw"], [0.5], 0.2),   # Смотрит вправо
                (["HeadYaw"], [0.0], 0.2),   # Смотрит прямо
                (["HeadPitch"], [0.3], 0.2), # Смотрит немного вниз
                (["HeadPitch"], [-0.3], 0.2),# Смотрит немного вверх
                (["HeadPitch", "HeadYaw"], [0.0, 0.0], 0.2) # Возвращается к центру
            ]

            for joints, angles, speed in head_movements:
                self.motion.angleInterpolationWithSpeed(joints, angles, speed)
                time.sleep(0.5)

            self.logger.info("LookAround", "Head movement completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("LookAround", "Error during execution: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("LookAround", "Stopping head movement.")
        self.bIsRunning = False
        self.onStopped()