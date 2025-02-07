from naoqi import ALProxy
import time
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
        self.memory = None
        self.touch_event = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.speech = self.session().service("ALAnimatedSpeech")
        self.life = self.session().service("ALAutonomousLife")
        self.memory = self.session().service("ALMemory")
        self.logger = self.session().service("ALLogger")

        # Подписываемся на событие нажатия кнопки
        self.memory.subscribeToEvent(
            self.touch_event,
            "onHeadTouchDetected",
            "onTouchDetected"
        )
        self.logger.info("Storytelling", "Behavior loaded and event subscribed.")

    def get_stories(self):
        return [
            {
                "title": "Die kleine Glühwürmchen",
                "text": "\\rspd=90\\ \\vct=85\\ ^start(animations/Stand/Gestures/Explain_1) In einem dunklen Wald lebte ein kleines Glühwürmchen namens Lumi..."
            }
        ]

    def select_random_story(self):
        stories = self.get_stories()
        if not stories:
            return None, None
        story = random.choice(stories)
        return story["title"], story["text"]

    def onInput_onStart(self):
        if self.running:
            return
        self.running = True

        try:
            self.logger.info("Storytelling", "Starting storytelling mode.")
            self.life.setState("solitary")
            self.posture.goToPosture("Stand", 0.5)
            time.sleep(1)

            while self.running:
                title, text = self.select_random_story()
                if title and text:
                    self.logger.info("Storytelling", "Telling story: " + title)
                    self.speech.say(text)

                wait_time = random.randint(8, 12) * 60
                self.logger.info("Storytelling", "Waiting {} minutes before next story.".format(wait_time // 60))

                for _ in range(wait_time // 10):
                    if not self.running:
                        break
                    time.sleep(10)

            self.logger.info("Storytelling", "Exiting storytelling mode.")
            self.onStopped()

        except Exception as e:
            self.logger.error("Storytelling", "Error: " + str(e))
        finally:
            self.running = False

    def onInput_onStop(self):
        self.logger.info("Storytelling", "Forced stop.")
        self.running = False
        self.memory.unsubscribeToEvent(self.touch_event, "onTouchDetected")
        self.life.setState("interactive")
        self.onStopped()

    def onHeadTouchDetected(self, *_args):
        """Обработчик события нажатия на голову."""
        self.logger.info("Storytelling", "Head button pressed. Stopping the script.")
        self.running = False
