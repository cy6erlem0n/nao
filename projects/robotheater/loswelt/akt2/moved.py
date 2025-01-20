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

    def set_custom_stand(self):
        """Устанавливает стартовую позицию с заданной шириной ног."""
        try:
            self.motion.angleInterpolationWithSpeed(
                ["LHipYawPitch", "RHipYawPitch"],  # Угол бедер
                [0.15, -0.15],  # Ширина ног
                0.2
            )
            self.motion.angleInterpolationWithSpeed(
                ["LHipRoll", "RHipRoll"],  # Роллы бедер
                [0.1, -0.1],  # Легкий наклон для устойчивости
                0.2
            )
            time.sleep(0.5)
        except Exception as e:
            print("[ERROR] Ошибка при настройке стартовой позиции: {}".format(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Движение уже выполняется")
            return

        self.bIsRunning = True
        try:
            # Переход в исходную позу StandInit
            self.posture.goToPosture("StandInit", 0.6)
            time.sleep(1)

            # Настройка стартовой позиции
            print("[INFO] Настройка стартовой позиции")
            self.set_custom_stand()

            # Включить стабильность шага
            self.motion.moveInit()
            self.motion.setWalkArmsEnabled(True, True)  # Включить движение рук для баланса
            self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])  # Контроль контакта стоп

            # Настройка первого шага для плавного старта
            self.motion.setMotionConfig([
                ["MaxStepX", 0.02],  # Маленький шаг вперед
                ["MaxStepY", 0.05],  # Широкий шаг
                ["MaxStepFrequency", 0.2],  # Замедленный первый шаг
                ["StepHeight", 0.015],  # Низкий подъем ноги
                ["TorsoWx", 0.0]
            ])

            # Первый шаг вперед
            self.motion.moveTo(0.1, 0.02, 0.0)
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
                self.motion.moveTo(0.3, 0.0, 0.0)
                time.sleep(1)

            # Плавный поворот налево
            self.motion.moveTo(0.0, 0.0, 0.785)  # Половина поворота
            time.sleep(1)
            self.motion.moveTo(0.0, 0.0, 0.785)  # Оставшаяся половина поворота
            time.sleep(1)

            # Два шага вперед
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
