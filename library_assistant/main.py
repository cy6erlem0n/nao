from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        robotIP = self.getParameter("robotIP")  # Получаем IP из Edit Box
        PORT = self.getParameter("port")  # Получаем порт из Edit Box

        self.ask_for_age(robotIP, PORT)  # Запрашиваем возраст

    def ask_for_age(self, robotIP, PORT):
        try:
            # Приветствие и настройка для прослушивания возраста
            tts = ALProxy("ALTextToSpeech", robotIP, int(PORT))
            asr = ALProxy("ALSpeechRecognition", robotIP, int(PORT))
            memory = ALProxy("ALMemory", robotIP, int(PORT))

            tts.say("Please tell me your age or your age group, like child, teenager, or adult.")
            time.sleep(2)  # Пауза, чтобы NAO не слышал свою речь

            asr.setLanguage("English")
            vocabulary = ["10", "20", "30", "40", "50", "teenager", "child", "adult"]
            asr.setVocabulary(vocabulary, False)
            asr.subscribe("AgeListener")

            time.sleep(5)  # Ожидание ответа
            data = memory.getData("WordRecognized")
            asr.unsubscribe("AgeListener")

            if data and len(data) > 0:
                age_group = data[0]
                self.route_based_on_age(age_group)  # Передаем возрастную группу
            else:
                tts.say("I couldn't recognize your age, please repeat.")
                self.ask_for_age(robotIP, PORT)  # Повторяем запрос, если возраст не распознан
        except Exception as e:
            print("Error occurred: ", e)

    def route_based_on_age(self, age_group):
        # Отправка IP и порта в другие блоки
        self.output_IP(self.getParameter("robotIP"))
        self.output_port(self.getParameter("port"))
        
        # Убедимся, что параметры переданы, добавив паузу
        time.sleep(1)
        
        # Логика маршрутизации по возрастным группам
        if age_group in ["child", "10"]:
            print("Routing to child block")
            self.output_child()  # Переход в блок для детей
        elif age_group in ["teenager", "20"]:
            print("Routing to teenager block")
            self.output_teenager()  # Переход в блок для подростков
        elif age_group in ["adult", "30", "40", "50"]:
            print("Routing to adult block")
            self.output_adult()  # Переход в блок для взрослых
        else:
            print("Couldn't recognize the age group, asking again.")
            self.ask_for_age(self.getParameter("robotIP"), self.getParameter("port"))  # Переспрашиваем, если возраст не распознан
