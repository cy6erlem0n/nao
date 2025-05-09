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
            # Убедиться, что робот стоит ровно
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(1)

            # Включить стабильность шага
            self.motion.moveInit()
            self.motion.setWalkArmsEnabled(True, True)  # Включить движение рук для баланса
            self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])  # Контроль контакта стоп

            # Делает шаг вперед с настройкой параметров
            for _ in range(1):
                self.motion.moveTo(0.3, 0.0, 0.0)  # Шаг вперед на 30 см
                time.sleep(1)

            # Передача булевого флага после трех шагов
            self.onStopped()  # Сигнализируем завершение первой части действий

            # Поднимает руки вверх
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch"],  # Только плечи
                [-0.5, -0.5],  # Поднимаем вверх
                0.3
            )
            time.sleep(1)

            # Разводит руки в стороны
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderRoll", "RShoulderRoll"],  # Только роллы плеч
                [0.5, -0.5],  # Разведение рук
                0.3
            )
            time.sleep(2)

            # Возврат рук в исходное положение
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"],
                [1.5, 1.5, 0.0, 0.0],  # Возврат к исходной позе
                0.3
            )
            time.sleep(1)

        except Exception as e:
            print("[ERROR] Ошибка во время выполнения: {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.onUnload()
