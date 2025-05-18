from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.motion = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.logger = self.session().service("ALLogger")
            self.logger.info("HeadNod", "Script loaded and ready.")
        except Exception as e:
            self.logger.error("HeadNod", "Error during initialization: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("HeadNod", "Script is already running.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("HeadNod", "Starting head nod motion.")

            # Кивок головой (вниз-вверх)
            self.motion.angleInterpolationWithSpeed("HeadPitch", 0.4, 0.3)  # Вниз
            time.sleep(0.3)
            self.motion.angleInterpolationWithSpeed("HeadPitch", -0.2, 0.3) # Вверх
            time.sleep(0.3)
            self.motion.angleInterpolationWithSpeed("HeadPitch", 0.0, 0.2)  # Возвращение в нейтральное положение

            self.logger.info("HeadNod", "Head nod completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("HeadNod", "Error during execution: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("HeadNod", "Stopping head nod.")
        self.bIsRunning = False
        self.onStopped()
