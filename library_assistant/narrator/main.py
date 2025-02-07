from naoqi import ALProxy
import time
import json
import random

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.life = None
        self.running = False

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.speech = self.session().service("ALAnimatedSpeech")  # Используем ALAnimatedSpeech
        self.life = self.session().service("ALAutonomousLife")
        self.logger = self.session().service("ALLogger")
        self.logger.info("Storytelling", "Behavior loaded.")

    def load_stories(self):
        try:
            with open("stories.json", "r") as file:
                return json.load(file)
        except Exception as e:
            self.logger.error("Storytelling", "Ошибка загрузки сказок: " + str(e))
            return []

    def select_random_story(self):
        stories = self.load_stories()
        if not stories:
            return None, None
        story = random.choice(stories)
        return story["title"], story["text"]

    def onInput_onStart(self):
        if self.running:
            return
        self.running = True

        try:
            self.logger.info("Storytelling", "Запуск режима рассказывания сказок.")
            self.life.setState("solitary")  # Выключаем Life Mode, но не сажаем NAO
            self.posture.goToPosture("Stand", 0.5)
            time.sleep(1)

            while self.running:
                # Выбираем случайную сказку
                title, text = self.select_random_story()
                if title and text:
                    self.logger.info("Storytelling", "Рассказ сказки: " + title)
                    self.speech.say(text)  # Используем анимационный текст

                # Выбираем случайную паузу перед следующим рассказом (8-12 минут)
                wait_time = random.randint(8, 12) * 60
                self.logger.info("Storytelling", "Ожидание {} минут перед следующей сказкой.".format(wait_time // 60))
                
                for _ in range(wait_time // 10):  # Проверяем кнопку каждые 10 секунд
                    if not self.running:
                        break
                    time.sleep(10)

            self.logger.info("Storytelling", "Режим завершён.")
            self.onStopped()

        except Exception as e:
            self.logger.error("Storytelling", "Ошибка: " + str(e))

    def onInput_onStop(self):
        self.logger.info("Storytelling", "Принудительная остановка.")
        self.running = False
        self.life.setState("interactive")  # Включаем Life Mode обратно
        self.posture.goToPosture("Stand", 0.5)  # Возвращаем в нормальную позу
        self.onStopped()
