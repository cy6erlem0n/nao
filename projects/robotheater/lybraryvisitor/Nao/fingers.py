class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.bIsRunning = False  # Флаг выполнения

    def onLoad(self):
        self.motion = self.session().service("ALMotion")

    def onUnload(self):
        if self.bIsRunning:
            self.motion.stopMove()

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Движение уже выполняется")
            return

        self.bIsRunning = True
        try:
            # Положение указания вниз влево
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"],
                [0.5, 0.3, -1.5, -0.5],  # Значения углов в радианах
                0.2  # Скорость выполнения
            )
            time.sleep(1)

            # Возврат в нейтральное положение
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"],
                [1.5, 0.0, -1.0, -0.1],
                0.2
            )
            time.sleep(1)

            # Положение указания вниз вправо
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"],
                [0.5, -0.3, 1.5, 0.5],
                0.2
            )
            time.sleep(1)

            # Возврат в нейтральное положение
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll"],
                [1.5, 0.0, 1.0, 0.1],
                0.2
            )
            time.sleep(1)

            self.onStopped()  # Завершение блока
        except Exception as e:
            print("[ERROR] Ошибка во время выполнения: {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.onUnload()
