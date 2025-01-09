from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.is_virtual = False  # Флаг для проверки виртуального робота

    def onLoad(self):
        try:
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")

            # Проверяем наличие сервиса ALMotion
            try:
                self.motion = self.session().service("ALMotion")
                self.posture = self.session().service("ALRobotPosture")
                self.speech = self.session().service("ALTextToSpeech")
            except Exception as e:
                self.is_virtual = True  # Устанавливаем флаг виртуального робота
                self.logger.warning("MyClass", "Работа в виртуальной среде.")

        except Exception as e:
            if self.logger:
                self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        try:
            if not self.is_virtual:
                self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
                self.posture.goToPosture("Stand", 0.8)
                time.sleep(0.5)
            else:
                self.logger.info("MyClass", "Виртуальный робот: пропускаем возврат в позу Stand.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def say_or_log(self, text):
        """Произнести текст или вывести его в лог в зависимости от типа робота."""
        try:
            if not self.is_virtual:
                self.speech.say(text)
            else:
                self.logger.info("MyClass", "Виртуальный робот: {}".format(text))
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при воспроизведении текста: " + str(e))

    def first_word(self):
        """Робот читает первое слово."""
        try:
            self.logger.info("MyClass", "Робот читает первое слово.")

            self.say_or_log("\\rspd=30\\ \\vct=50\\ d... ")
            self.say_or_log("\\rspd=30\\ \\vct=50\\ die ")
            time.sleep(1.0)

            if not self.is_virtual:
                self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Лёгкий наклон вниз
                self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возврат головы в центр

            self.say_or_log("\\rspd=30\\ \\vct=50\\ die St... ")
            self.say_or_log("\\rspd=30\\ \\vct=50\\ die Stimm ")
            self.say_or_log("\\rspd=30\\ \\vct=50\\ die Stimmen ")
            time.sleep(1.0)

            self.logger.info("MyClass", "Робот завершил читать фразу")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при попытке прочитать слово: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск блока.")
            self.reset_to_initial_pose()
            self.first_word()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при запуске: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
