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
            self.posture.goToPosture("Stand", 0.8)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def interact_with_dash(self):
        """NAO взаимодействует с Dash."""
        try:
            self.logger.info("MyClass", "Начало взаимодействия с Dash.")

            # Поворачиваемся к Dash
            self.logger.info("MyClass", "Разворачиваемся влево для взаимодействия.")
            self.motion.moveTo(0.0, 0.0, -1.57)  # Поворот на 90 градусов влево
            time.sleep(1)

            # Dash показывает слово
            text = "Мир звук восстановлен."
            self.logger.info("MyClass", "Dash показывает слово.")
            self.speech.say(text)
            self.logger.info("MyClass", "Прочитанное слово: " + text)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при взаимодействии с Dash: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск взаимодействия с Dash.")
            self.reset_to_initial_pose()
            self.interact_with_dash()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
