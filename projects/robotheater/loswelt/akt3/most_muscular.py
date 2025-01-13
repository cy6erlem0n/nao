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

    def perform_most_muscular_pose(self):
        """Робот выполняет позу 'Most Muscular'."""
        try:
            self.logger.info("MyClass", "Робот выполняет позу 'Most Muscular'.")

            # Сгибание рук перед собой
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll", "LShoulderRoll", "RShoulderRoll"],
                [0.5, 0.5, -1.0, 1.0, -0.3, 0.3],  # Руки перед корпусом, локти согнуты
                0.2
            )

            # Легкий наклон корпуса вперед
            self.motion.setAngles("HeadPitch", 0.3, 0.1)  # Голова слегка наклонена вниз
            self.motion.setAngles("TorsoYaw", 0.0, 0.2)  # Корпус без поворота

            time.sleep(3)  # Удержание позы

            # Возвращение корпуса и рук в начальное положение
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LElbowRoll", "RElbowRoll", "LShoulderRoll", "RShoulderRoll"],
                [1.5, 1.5, 0.0, 0.0, 0.0, 0.0],  # Руки опущены
                0.2
            )
            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Голова в нейтральном положении

            self.logger.info("MyClass", "Робот завершил позу 'Most Muscular'.")
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
            self.perform_most_muscular_pose()

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
