from naoqi import ALProxy
import time
import almath

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.bIsRunning = False

    def onLoad(self):
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")

    def onUnload(self):
        if self.bIsRunning:
            self.motion.stopMove()

    def set_custom_stand(self):
        try:
            self.motion.angleInterpolationWithSpeed(
                ["LHipYawPitch", "RHipYawPitch"], [0.15, -0.15], 0.2)
            self.motion.angleInterpolationWithSpeed(
                ["LHipRoll", "RHipRoll"], [0.1, -0.1], 0.2)
            time.sleep(0.3)
        except Exception as e:
            print("[ERROR] Ошибка при установке позиции: {}".format(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Уже выполняется")
            return

        self.bIsRunning = True
        try:
            x = self.getParameter("Distance X (m)")
            y = self.getParameter("Distance Y (m)")
            theta_deg = self.getParameter("Theta (deg)")
            theta = theta_deg * almath.PI / 180
            enable_arms = self.getParameter("Arms movement enabled")

            self.posture.goToPosture("StandInit", 0.6)
            time.sleep(1)
            self.set_custom_stand()

            self.motion.moveInit()
            self.motion.setWalkArmsEnabled(enable_arms, enable_arms)
            self.motion.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

            # Настройка первого шага для плавного старта
            self.motion.setMotionConfig([
                ["MaxStepX", 0.02],
                ["MaxStepY", 0.05],
                ["MaxStepFrequency", 0.2],
                ["StepHeight", 0.015],
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

            # Основной шаг, заданный пользователем
            self.motion.moveTo(x, y, theta)

            self.onStopped()

        except Exception as e:
            print("[ERROR] {}".format(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()
