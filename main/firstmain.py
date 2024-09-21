from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def listen_for_age(self, robotIP, PORT=9559):
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)
        asr = ALProxy("ALSpeechRecognition", robotIP, PORT)
        memory = ALProxy("ALMemory", robotIP, PORT)

        # Подготовка к прослушиванию возраста
        asr.setLanguage("English")
        vocabulary = ["10", "20", "30", "40", "50", "teenager", "child", "adult"]
        asr.setVocabulary(vocabulary, False)
        asr.subscribe("AgeListener")

        # NAO задает вопрос
        tts.say("Hello! Please tell me your age or your age group like child, teenager, or adult.")

        # Слушаем ответ
        time.sleep(5)  # Слушаем 5 секунд
        data = memory.getData("WordRecognized")
        print("Recognized:", data)
        asr.unsubscribe("AgeListener")

        if data:
            return data[0]  # Возвращаем распознанное слово (возраст или группа)

        return None

    def suggest_books(self, age_group, robotIP, PORT=9559):
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)

        if age_group in ["child", "10"]:
            tts.say("For children, I recommend checking out our fairy tales and adventure books.")
        elif age_group in ["teenager", "20"]:
            tts.say("For teenagers, we have a great selection of science fiction and fantasy novels.")
        elif age_group in ["adult", "30", "40", "50"]:
            tts.say("For adults, we offer a wide range of fiction, non-fiction, and self-help books.")
        else:
            tts.say("I'm sorry, I didn't understand your age. Could you repeat it?")
        
        # Углубление в детали, если пользователь хочет
        tts.say("Would you like to hear more details about one of these categories? Just ask me!")

    def onInput_onStart(self):
        robotIP = "169.254.205.101"  # IP-адрес твоего NAO
        PORT = 9559

        try:
            # NAO начинает разговор
            age_group = self.listen_for_age(robotIP, PORT)
            if age_group:
                self.suggest_books(age_group, robotIP, PORT)
            else:
                print("I couldn't recognize the age group.")
        except Exception as e:
            print("Error occurred: ", e)

        self.onStopped()  # Завершение выполнения блока

    def onInput_onStop(self):
        self.onStopped()  # Завершение выполнения блока
