from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.logger = None

    def onLoad(self):
        try:
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")

            # Инициализация сервисов
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
        except Exception as e:
            if self.logger:
                self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        try:
            self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
            self.posture.goToPosture("StandInit", 0.6)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def knock_object(self):
        """NAO ударяет предмет перед собой."""
        try:
            self.logger.info("MyClass", "Начало манипуляции с предметом.")

            # Приседание для подготовки
            self.logger.info("MyClass", "Робот приседает.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch"
            ], [1.2, -0.4], 0.3)  # Приседание
            time.sleep(1)

            # Подготовка рук для удара (отведение назад)
            self.logger.info("MyClass", "Подготовка рук для удара.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll",
                "LElbowYaw", "RElbowYaw", "LElbowRoll", "RElbowRoll"
            ], [
                1.5, 1.5, 0.2, -0.2, -1.3, 1.3, -0.5, 0.5
            ], 0.2)
            time.sleep(0.5)

            # Удар вперед
            self.logger.info("MyClass", "Удар предмета.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll",
                "LElbowRoll", "RElbowRoll"
            ], [
                0.3, 0.3, 0.0, 0.0, -1.0, 1.0
            ], 0.3)  # Удар вперед
            time.sleep(1)

            # Возвращение рук в исходное положение
            self.logger.info("MyClass", "Возвращение рук в исходное положение.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll",
                "LElbowYaw", "RElbowYaw", "LElbowRoll", "RElbowRoll"
            ], [
                1.5, 1.5, 0.0, 0.0, 0.0, 0.0, -0.5, 0.5
            ], 0.2)
            time.sleep(0.5)

            # Возвращение в стоячее положение
            self.logger.info("MyClass", "Возвращение в стоячее положение.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch"
            ], [0.0, 0.0], 0.3)
            time.sleep(1)

        except Exception as e:
            self.logger.error("MyClass", "Ошибка при манипуляции с предметом: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск манипуляции с предметом.")
            self.reset_to_initial_pose()
            self.knock_object()
            self.reset_to_initial_pose()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
