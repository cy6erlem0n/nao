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
        """Произносит текст с дружественным тоном."""
        try:
            self.logger.info("MyClass", "Начато произнесение текста: " + text)
            # Обёртываем текст в параметры тона и скорости
            formatted_text = "\\rspd=90\\ \\vct=75\\ " + text
            self.speech.say(formatted_text)
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
                    "text": "Früher war diese Welt voller Klänge... \\pau=500\\ Lachen, Stimmen, Musik – all das war ein Teil des Lebens.",
                    "motions": {
                        "joints": ["LShoulderPitch", "RShoulderPitch"],
                        "angles": [0.4, 0.4],
                        "speed": 0.15
                    }
                },
                {
                    "text": "Doch eines Tages änderte sich alles. \\pau=500\\ Die Klänge verschwanden und hinterließen nichts als Stille.",
                    "motions": {
                        "joints": ["HeadPitch"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "Niemand weiß, \\pau=300\\ was der Grund für diesen Verlust war.",
                    "motions": {
                        "joints": ["RShoulderRoll"],
                        "angles": [-0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "Die Menschen versuchten, das Verlorene wiederherzustellen, \\pau=500\\ aber ohne Erfolg.",
                    "motions": {
                        "joints": ["LShoulderRoll"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "Doch es heißt, \\pau=300\\ es gibt einen Weg, die Klänge zurückzubringen.",
                    "motions": {
                        "joints": ["HeadYaw"],
                        "angles": [0.3],
                        "speed": 0.1
                    }
                },
                {
                    "text": "Heute beginnt eine Reise. \\pau=500\\ Wir müssen die Klänge sammeln und das wiederherstellen, \\pau=300\\ was verloren gegangen ist.",
                    "motions": {
                        "joints": ["RShoulderPitch"],
                        "angles": [0.5],
                        "speed": 0.15
                    }
                },
                {
                    "text": "Taucht ein in die Stille... \\pau=700\\ und seid bereit, der Welt ihre Stimme zurückzugeben.",
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
