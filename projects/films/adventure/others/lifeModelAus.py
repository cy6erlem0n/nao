
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.life = None
        self.logger = None

    def onLoad(self):
        self.life = self.session().service("ALAutonomousLife")
        self.logger = self.session().service("ALLogger")
        self.logger.info("DisableLife", "Life block loaded")

    def onUnload(self):
        pass

    def onInput_onStart(self):
        try:
            self.logger.info("DisableLife", "Disabling Life mode...")
            self.life.setState("disabled")
            self.logger.info("DisableLife", "Life mode is now: disabled")
        except Exception as e:
            self.logger.error("DisableLife", "Error disabling Life mode: " + str(e))
        self.onStopped()

    def onInput_onStop(self):
        self.onStopped()
