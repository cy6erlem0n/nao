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

    def perform_front_lat_spread_pose(self):
        """Робот выполняет позу 'Front Lat Spread'."""
        try:
            self.logger.info("MyClass", "Робот выполняет позу 'Front Lat Spread'.")

            # Поднятие рук в стороны
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"],
                [0.5, 0.5, 0.5, -0.5],  # Руки чуть ниже уровня плеч
                0.2
            )

            # Легкий наклон корпуса вперед
            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Голова немного опущена
            self.motion.setAngles("TorsoYaw", 0.0, 0.2)  # Корпус без разворота

            time.sleep(3)  # Удержание позы

            # Возвращение корпуса и рук в начальное положение
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"],
                [1.5, 1.5, 0.0, 0.0],  # Руки опущены
                0.2
            )
            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Голова в нейтральном положении

            self.logger.info("MyClass", "Робот завершил позу 'Front Lat Spread'.")
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
            self.perform_front_lat_spread_pose()

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
