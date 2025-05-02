
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.life = None
        self.logger = None

    def onLoad(self):
        self.life = self.session().service("ALAutonomousLife")
        self.logger = self.session().service("ALLogger")
        self.logger.info("EnableLife", "Life block loaded")

    def onUnload(self):
        pass

    def onInput_onStart(self):
        try:
            self.logger.info("EnableLife", "Setting Life mode to interactive...")
            self.life.setState("interactive")
            self.logger.info("EnableLife", "Life mode is now: interactive")
        except Exception as e:
            self.logger.error("EnableLife", "Error setting Life mode: " + str(e))
        self.onStopped()

    def onInput_onStop(self):
        self.onStopped()
