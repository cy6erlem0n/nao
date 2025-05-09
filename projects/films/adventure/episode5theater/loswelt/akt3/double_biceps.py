from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу StandInit."""
        try:
            self.logger.info("MyClass", "Возвращаем робота в позу StandInit.")
            self.posture.goToPosture("StandInit", 0.8)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу StandInit: " + str(e))

    def perform_double_biceps_pose(self):
        """Робот выполняет позу 'Double Biceps'."""
        try:
            self.logger.info("MyClass", "Робот выполняет позу 'Double Biceps'.")

            # Поднятие рук вверх
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll"],
                [-1.0, -1.0, -0.5, 0.5],  # Углы для поднятия рук
                0.2
            )

            # Лёгкий наклон корпуса
            self.motion.setAngles("TorsoYaw", 0.3, 0.2)  # Разворот корпуса
            time.sleep(3)  # Удержание позы

            self.logger.info("MyClass", "Робот завершил позу 'Double Biceps'.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении позы: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")

            # Устанавливаем начальную позу
            self.reset_to_initial_pose()

            # Выполнение позы бодибилдера
            self.perform_double_biceps_pose()

            # Возвращение в начальную позу
            self.reset_to_initial_pose()

            self.onStopped()  # Сигнал завершения
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.motion.rest()  # Перевод моторов в состояние покоя
        self.onStopped()
