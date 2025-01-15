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

            # Настройка начальной стойки с увеличением ширины ног
            self.motion.angleInterpolationWithSpeed(["LHipYawPitch", "RHipYawPitch"], [0.15, -0.15], 0.1)
            self.motion.angleInterpolationWithSpeed(["LHipRoll", "RHipRoll"], [0.1, -0.1], 0.1)
            time.sleep(0.5)

            # Включить стабильность шага
            self.motion.moveInit()
            self.motion.setWalkArmsEnabled(True, True)  # Включить движение рук для баланса
            self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])  # Контроль контакта стоп

            # Настройка первого шага для плавного старта
            self.motion.setMotionConfig([
                ["MaxStepX", 0.02],  # Маленький шаг вперед
                ["MaxStepY", 0.05],  # Широкий шаг для предотвращения столкновений ног
                ["MaxStepFrequency", 0.2],  # Замедленный первый шаг
                ["StepHeight", 0.015],  # Низкий подъем ноги
                ["TorsoWx", 0.0]
            ])

            # Первый шаг вперед
            self.motion.moveTo(0.1, 0.02, 0.0)  # Добавлена небольшая ширина для устойчивости
            time.sleep(1)

            # Восстановление нормальных параметров для дальнейших шагов
            self.motion.setMotionConfig([
                ["MaxStepX", 0.04],
                ["MaxStepY", 0.03],
                ["MaxStepFrequency", 0.4],
                ["StepHeight", 0.02],
                ["TorsoWx", 0.0]
            ])

            # Два шага вперед
            for _ in range(2):
                self.motion.moveTo(0.2, 0.0, 0.0)  # Шаг вперед
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
