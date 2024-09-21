from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onInput_onStart(self):
        robotIP = "169.254.205.101"  # IP-адрес NAO
        PORT = 9559

        try:
            tts = ALProxy("ALTextToSpeech", robotIP, PORT)
            tts.say("For adults, I recommend checking out fiction, non-fiction, and self-help books!")
        except Exception as e:
            print("Error occurred: ", e)

        self.onStopped()  # Завершение блока