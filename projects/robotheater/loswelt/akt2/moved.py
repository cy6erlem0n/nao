from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.bIsRunning = False  # Флаг выполнения

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")

    def onUnload(self):
        if self.bIsRunning:
            self.motion.stopMove()

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Движение уже выполняется")
            return

        self.bIsRunning = True
        try:
            # Убедиться, что робот стоит ровно
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(1)

            # Включить стабильность шага
            self.motion.moveInit()
            self.motion.setWalkArmsEnabled(True, True)  # Включить движение рук для баланса
            self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])  # Контроль контакта стоп

            # Делает два шага вперед
            for _ in range(2):
                self.motion.moveTo(0.3, 0.0, 0.0)  # Шаг вперед на 30 см
                time.sleep(1)

            # Поворот налево
            self.motion.moveTo(0.0, 0.0, 1.57)  # Поворот на 90 градусов налево
            time.sleep(1)

            # Делает ещё два шага вперед
            for _ in range(1):
                self.motion.moveTo(0.3, 0.0, 0.0)
                time.sleep(1)
            self.onStopped()
            
        except Exception as e:
            print("[ERROR] Ошибка во время выполнения: {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onUnload()
        self.onStopped()