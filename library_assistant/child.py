from naoqi import ALProxy

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.robotIP = None
        self.port = None

    def onInput_IP(self, value):
        self.robotIP = value

    def onInput_port(self, value):
        self.port = value

    def onInput_onSignal(self):
        if self.robotIP is None or self.port is None:
            print("IP or port not set in child block!")
            return

        try:
            tts = ALProxy("ALTextToSpeech", self.robotIP, self.port)
            tts.say("For children, I recommend checking out fairy tales and adventure books!")
        except Exception as e:
            print("Error in child block:", e)

        self.onStopped()
