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

    def perform_side_chest_pose(self):
        """Робот выполняет позу 'Side Chest'."""
        try:
            self.logger.info("MyClass", "Робот выполняет позу 'Side Chest'.")

            # Поворот корпуса слегка вбок
            self.motion.setAngles("TorsoYaw", 0.4, 0.2)  # Разворот вправо
            time.sleep(0.5)

            # Поднятие правой руки
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RElbowYaw", "RElbowRoll"],
                [0.0, 1.5, 0.3],  # Рука вверх и слегка согнута
                0.2
            )

            # Сгиб левой руки
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "LElbowYaw", "LElbowRoll"],
                [1.0, -1.5, -0.5],  # Локоть согнут, рука перед корпусом
                0.2
            )

            time.sleep(3)  # Удержание позы

            # Возврат корпуса в центр
            self.motion.setAngles("TorsoYaw", 0.0, 0.2)
            self.logger.info("MyClass", "Робот завершил позу 'Side Chest'.")
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
            self.perform_side_chest_pose()

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
