from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALAnimatedSpeech")
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
        self.posture.goToPosture("Stand", 0.8)  # Используем "Stand" для более прямой позы
        time.sleep(0.5)

    def perform_motion(self, joints, angles, speed):
        """Выполняет движение робота."""
        try:
            self.logger.info("MyClass", "Выполняем движение: Joints={}, Angles={}, Speed={}".format(joints, angles, speed))
            self.motion.angleInterpolationWithSpeed(joints, angles, speed)
            time.sleep(0.5)
            self.logger.info("MyClass", "Движение завершено.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в движении: " + str(e))

    def speak(self, text):
        """Произносит текст."""
        try:
            self.logger.info("MyClass", "Начато произнесение текста: " + text)
            self.speech.say(text)
            self.logger.info("MyClass", "Текст завершён.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в речи: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")
            self.reset_to_initial_pose()

            # Полный текст и соответствующие движения
            sequences = [
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Früher war diese Welt voller Klänge... Lachen, Stimmen, Musik – all das war ein Teil des Lebens.",
                    "motions": {
                        "joints": ["LShoulderPitch", "RShoulderPitch"],
                        "angles": [0.4, 0.4],
                        "speed": 0.15
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Doch eines Tages änderte sich alles. Die Klänge verschwanden und hinterließen nichts als Stille.",
                    "motions": {
                        "joints": ["HeadPitch"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Niemand weiß, was der Grund für diesen Verlust war.",
                    "motions": {
                        "joints": ["RShoulderRoll"],
                        "angles": [-0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Die Menschen versuchten, das Verlorene wiederherzustellen, aber ohne Erfolg. Die Welt blieb stumm.",
                    "motions": {
                        "joints": ["LShoulderRoll"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Doch es heißt, es gibt einen Weg, die Klänge zurückzubringen.",
                    "motions": {
                        "joints": ["HeadYaw"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Heute beginnt eine Reise. Wir müssen die Klänge sammeln und das wiederherstellen, was verloren gegangen ist.",
                    "motions": {
                        "joints": ["RShoulderPitch"],
                        "angles": [0.5],
                        "speed": 0.15
                    }
                },
                {
                    "text": "\\rspd=80\\ \\vct=70\\ Taucht ein in die Stille... und seid bereit, der Welt ihre Stimme zurückzugeben.",
                    "motions": {
                        "joints": ["LShoulderPitch", "RShoulderPitch"],
                        "angles": [0.6, 0.6],
                        "speed": 0.15
                    }
                }
            ]

            for sequence in sequences:
                self.reset_to_initial_pose()
                self.speak(sequence["text"])
                self.perform_motion(
                    sequence["motions"]["joints"],
                    sequence["motions"]["angles"],
                    sequence["motions"]["speed"]
                )
                self.reset_to_initial_pose()

            self.logger.info("MyClass", "Блок завершён.")
            self.onStopped()

        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onUnload()
        self.onStopped()
