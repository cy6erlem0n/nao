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
        try:
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")

            # Инициализация сервисов
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALTextToSpeech")
        except Exception as e:
            if self.logger:
                self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        try:
            self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
            self.posture.goToPosture("Stand", 0.5)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def track_dash(self):
        """Скрипт для следящего взгляда NAO за Dash."""
        try:
            self.logger.info("MyClass", "Начало слежения за Dash.")

            # NAO смотрит направо вниз
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [-0.5, 0.3], 0.1)
            time.sleep(2)

            # Следящий взгляд влево
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.1, 0.3], 0.05)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.2, 0.3], 0.05)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.3, 0.2], 0.05)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.4, 0.2], 0.05)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.5, 0.1], 0.05)
            time.sleep(26.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.5, -0.3], 0.1)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.5, 0.3], 0.1)
            time.sleep(0.5)
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.5, 0.1], 0.1)
            time.sleep(1)
            # Возвращение головы в центр
            self.motion.setAngles(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.1)
            self.logger.info("MyClass", "Слежение завершено.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при слежении за Dash: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск скрипта слежения за Dash.")
            self.reset_to_initial_pose()
            self.track_dash()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()