from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.speech = self.session().service("ALTextToSpeech")
        self.logger = self.session().service("ALLogger")
        self.logger.info("NAO Invite Basteln", "Behavior loaded.")

    def onInput_onStart(self):
        try:
            self.logger.info("NAO Invite Basteln", "Starting behavior.")

            # Переводим NAO в стандартную позу StandInit
            self.logger.info("NAO Invite Basteln", "Moving to StandInit posture.")
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(1)

            # Манящие движения руками (2 раза)
            self.logger.info("NAO Invite Basteln", "Inviting with hand gestures.")
            for _ in range(2):
                self.motion.angleInterpolationWithSpeed(
                    ["RShoulderPitch", "LShoulderPitch", "RElbowRoll", "LElbowRoll"],
                    [0.8, 0.8, 1.2, -1.2],  # Поднимаем руки и сгибаем локти
                    0.3
                )
                time.sleep(0.3)
                self.motion.angleInterpolationWithSpeed(
                    ["RElbowRoll", "LElbowRoll"],
                    [0.3, -0.3],  # Опускаем локти ближе к телу
                    0.3
                )
                time.sleep(0.3)

            # Говорит приглашение (замените текст на ваш)
            self.logger.info("NAO Invite Basteln", "Speaking invitation.")
            self.speech.say("\\rspd=85\\ \\vct=70\\ Kommt her! Wir basteln zusammen und haben viel Spaß!")

            # Махает рукой (правой)
            self.logger.info("NAO Invite Basteln", "Waving hand.")
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw"],
                [-1.0, 0.1, 0.0, -1.57],  # Поднимает руку
                0.3
            )
            self.motion.openHand("RHand")  # Открываем ладонь
            time.sleep(0.5)

            for _ in range(3):
                self.motion.angleInterpolationWithSpeed(["RWristYaw"], [-1.2], 0.3)  # Мах вправо
                self.motion.angleInterpolationWithSpeed(["RWristYaw"], [-1.9], 0.3)  # Мах влево

            self.motion.closeHand("RHand")  # Закрываем ладонь

            # Возвращаем руку в исходное положение
            self.logger.info("NAO Invite Basteln", "Returning hand to initial position.")
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RWristYaw"],
                [1.4, 0.0, 0.0, 0.0],
                0.2
            )

            # Возвращаем NAO в позу StandInit
            self.logger.info("NAO Invite Basteln", "Returning to StandInit posture.")
            self.posture.goToPosture("StandInit", 0.7)

            self.logger.info("NAO Invite Basteln", "Behavior completed.")
            self.onStopped()

        except Exception as e:
            self.logger.error("NAO Invite Basteln", "Error during execution: {}".format(e))

    def onInput_onStop(self):
        self.logger.info("NAO Invite Basteln", "Stopping behavior.")
        self.motion.stopMove()
        self.posture.goToPosture("StandInit", 0.7)
        self.onStopped()
