from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.speech = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.speech = self.session().service("ALTextToSpeech")
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def repeat_phrase(self, phrase):
        """Робот повторяет услышанное слово или фразу."""
        try:
            self.logger.info("MyClass", f"Робот повторяет фразу: {phrase}")
            self.speech.say("\\rspd=90\\ \\vct=100\\ " + phrase)
            self.logger.info("MyClass", "Фраза произнесена.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при повторении фразы: " + str(e))

    def onInput_onStart(self, phrase):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")
            if phrase:
                self.logger.info("MyClass", f"Получена фраза для повторения: {phrase}")
                self.repeat_phrase(phrase)
            else:
                self.logger.warning("MyClass", "Фраза для повторения отсутствует.")
            
            self.onStopped()  # Сигнал завершения
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
