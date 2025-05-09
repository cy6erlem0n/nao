from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.speech_recognition = None
        self.memory = None
        self.isListening = False
        self.last_spoken = None
        self.word_dict = {  # Словарь ключ-значение
            "hallo": "Hallo, wie geht es dir?",
            "danke": "Bitte schön.",
            "tschüss": "Auf Wiedersehen!",
            "bitte": "Kein Problem!",
            "nao": "Ja, das bin ich, Nao.",
            "wie geht's": "Mir geht es gut, danke!",
            "gut": "Das freut mich zu hören.",
            "schlecht": "Das tut mir leid zu hören.",
            "dumm" : "Ich bin total dumm"
        }

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALTextToSpeech")
            self.speech_recognition = self.session().service("ALSpeechRecognition")
            self.memory = self.session().service("ALMemory")

            # Установка языка и словаря
            self.speech.setLanguage("German")
            self.speech_recognition.setLanguage("German")
            vocabulary = list(self.word_dict.keys())
            self.speech_recognition.setVocabulary(vocabulary, False)

            # Параметры улучшения распознавания речи
            self.speech.setVolume(0.6)  # Уменьшение громкости
        except Exception as e:
            self.logger.error("Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        try:
            self.posture.goToPosture("Stand", 0.8)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("Ошибка при возврате в позу Stand: " + str(e))

    def simulate_listening(self):
        try:
            self.motion.setAngles("HeadYaw", 0.3, 0.1)  # Поворот головы вправо
            time.sleep(1)
            self.motion.setAngles("HeadYaw", -0.3, 0.1)  # Поворот головы влево
            time.sleep(1)
            self.motion.setAngles("HeadYaw", 0.0, 0.1)  # Возврат в центр
        except Exception as e:
            self.logger.error("Ошибка при движении головы: " + str(e))

    def listen_and_repeat(self):
        try:
            self.simulate_listening()
            self.speech.say("Hallo! Bitte sage etwas, und ich werde versuchen, es zu verstehen.")
            time.sleep(1)  # Пауза перед активацией слушания

            self.speech_recognition.subscribe("RepeatListener")
            time.sleep(5)  # Время прослушивания
            data = self.memory.getData("WordRecognized")
            self.speech_recognition.unsubscribe("RepeatListener")

            if data and len(data) > 0:
                recognized_word = data[0]
                confidence = data[1] if len(data) > 1 else 0.0

                if confidence > 0.3:
                    if recognized_word in self.word_dict:
                        self.speech.say(self.word_dict[recognized_word])
                    else:
                        self.speech.say("Entschuldigung, ich kenne dieses Wort nicht.")
                else:
                    self.speech.say("Entschuldigung, ich bin mir nicht sicher, was du gesagt hast.")
            else:
                self.speech.say("Entschuldigung, ich habe nichts gehört.")
        except Exception as e:
            self.logger.error("Ошибка при прослушивании и повторении: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("Запуск блока.")
            self.reset_to_initial_pose()
            self.listen_and_repeat()
        except Exception as e:
            self.logger.error("Ошибка при запуске: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        try:
            self.speech_recognition.unsubscribe("RepeatListener")
            self.logger.info("Распознавание отключено.")
        except Exception as e:
            self.logger.error("Ошибка при остановке: " + str(e))
        finally:
            self.onStopped()
