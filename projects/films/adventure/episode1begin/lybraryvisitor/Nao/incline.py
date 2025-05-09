from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.bIsRunning = False  # Флаг выполнения

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")

    def onUnload(self):
        if self.bIsRunning:
            self.motion.stopMove()

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Движение уже выполняется")
            return

        self.bIsRunning = True
        try:
            # Встать в начальную позицию
            self.posture.goToPosture("StandInit", 0.5)
            time.sleep(1)

            # Наклон корпуса вперед
            self.motion.angleInterpolationWithSpeed(
                ["HipPitch"],
                [0.3],  # Угол наклона вперед
                0.2
            )
            time.sleep(1)

            # Жест приглаживания левой рукой
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"],
                [0.5, 0.1, -1.0, -0.5, 0.0],  # Позиция руки
                0.3
            )
            time.sleep(1)

            # Движение рукой вниз и обратно, как приглаживание
            self.motion.angleInterpolationWithSpeed(
                ["LElbowRoll", "LWristYaw"],
                [-1.0, -0.5],  # Приглаживание вниз
                0.3
            )
            time.sleep(0.5)
            self.motion.angleInterpolationWithSpeed(
                ["LElbowRoll", "LWristYaw"],
                [-0.5, 0.0],  # Возврат назад
                0.3
            )
            time.sleep(0.5)

            # Возврат корпуса и руки в начальное положение
            self.motion.angleInterpolationWithSpeed(
                ["HipPitch", "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"],
                [0.0, 1.5, 0.0, -1.0, -0.5, 0.0],  # Начальная позиция
                0.3
            )
            time.sleep(1)

            self.onStopped()  # Завершение блока
        except Exception as e:
            print("[ERROR] Ошибка во время выполнения: {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.onUnload()
