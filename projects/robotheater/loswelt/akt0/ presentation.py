from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.bIsRunning = False  # Булевый флаг выполнения

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.speech = self.session().service("ALAnimatedSpeech")
        self.logger = self.session().service("ALLogger")  # Создаём сервис логирования
        self.logger.info("MyClass", "Блок загружен и готов к работе.")

    def onUnload(self):
        if self.bIsRunning:
            self.motion.stopMove()
            self.logger.info("MyClass", "Движение остановлено.")
        self.bIsRunning = False
        self.logger.info("MyClass", "Блок выгружен.")

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")
            # Начальная поза
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(1)

            # Вступление - наклон головы вниз
            self.speech.say(" \RSPD=90\ \VCT=80\ Wann hatte dieser Welt viele Geräusche...")
            self.motion.angleInterpolationWithSpeed("HeadPitch", 0.3, 0.1)
            time.sleep(1)

            # Поднимаем голову и руки
            self.logger.info("MyClass", "Поднимаем голову и руки.")
            self.motion.angleInterpolationWithSpeed(
                ["HeadPitch", "LShoulderPitch", "RShoulderPitch"],
                [0.0, 0.5, 0.5], 
                0.1
            )
            time.sleep(2)

            # Завершение блока
            self.logger.info("MyClass", "Блок завершён.")
            self.onStopped()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка во время выполнения: {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onUnload()
        self.onStopped()
