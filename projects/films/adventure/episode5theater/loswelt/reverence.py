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

    def perform_bow(self):
        """Робот выполняет поклон."""
        try:
            self.logger.info("MyClass", "Робот выполняет поклон.")

            # Легкий наклон корпуса вперед
            self.motion.angleInterpolationWithSpeed(
                ["HeadPitch", "HipPitch"],
                [0.3, 0.2],  # Голова наклонена, корпус слегка подан вперед
                0.2
            )

            # Поднятие рук в приветственном жесте
            self.motion.angleInterpolationWithSpeed(
                ["LShoulderPitch", "RShoulderPitch"],
                [1.0, 1.0],  # Руки слегка подняты вперед
                0.2
            )
            time.sleep(2)  # Удержание в позиции поклона

            # Возвращение в нейтральное положение
            self.motion.angleInterpolationWithSpeed(
                ["HeadPitch", "HipPitch", "LShoulderPitch", "RShoulderPitch"],
                [0.0, 0.0, 1.5, 1.5],  # Голова и корпус выпрямлены, руки опущены
                0.2
            )
            self.logger.info("MyClass", "Робот завершил поклон.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении поклона: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")

            # Устанавливаем начальную позу
            self.reset_to_initial_pose()

            # Выполнение поклона
            self.perform_bow()

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
