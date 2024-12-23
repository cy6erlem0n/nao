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
        self.logger.info("NAO Wave Hand", "Behavior loaded.")

    def onInput_onStart(self):
        try:
            self.logger.info("NAO Wave Hand", "Starting behavior.")

            # Переводим робота в стандартную позу StandInit
            self.logger.info("NAO Wave Hand", "Moving to StandInit posture.")
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(1)

            # Поднимаем руку и корректируем запястье
            self.logger.info("NAO Wave Hand", "Lifting right hand and adjusting wrist.")
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw"],
                [-1.0, 0.1, 0.0, -1.57],  # Запястье вперед
                0.2
            )

            # Разгибаем пальцы
            self.logger.info("NAO Wave Hand", "Opening hand.")
            self.motion.openHand("RHand")
            time.sleep(0.5)

            # Мах рукой (3 раза)
            self.logger.info("NAO Wave Hand", "Waving hand.")
            for _ in range(3):
                self.motion.angleInterpolationWithSpeed(
                    ["RWristYaw"],
                    [-1.2],  # Мах вправо (от исходного положения)
                    0.3
                )
                self.motion.angleInterpolationWithSpeed(
                    ["RWristYaw"],
                    [-1.9],  # Мах влево (от исходного положения)
                    0.3
                )

            # Закрываем пальцы
            self.logger.info("NAO Wave Hand", "Closing hand.")
            self.motion.closeHand("RHand")

            # Возвращаем руку в исходное положение
            self.logger.info("NAO Wave Hand", "Returning hand to initial position.")
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw"],
                [1.4, 0.0, 0.0, 0.0],
                0.2
            )

            # Возвращаемся в позу StandInit
            self.logger.info("NAO Wave Hand", "Returning to StandInit posture.")
            self.posture.goToPosture("StandInit", 0.7)
            
            self.logger.info("NAO Wave Hand", "Behavior completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("NAO Wave Hand", "Error during execution: {}".format(e))

    def onInput_onStop(self):
        self.logger.info("NAO Wave Hand", "Stopping behavior.")
        self.motion.stopMove()
        self.posture.goToPosture("StandInit", 0.7)
        self.onStopped()
