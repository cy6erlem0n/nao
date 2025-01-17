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
            self.posture.goToPosture("StandInit", 0.7)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def push_object(self):
        """NAO выполняет толчок руками."""
        try:
            self.logger.info("MyClass", "Начало манипуляции с предметом.")

            # Приседание для сближения с объектом
            self.logger.info("MyClass", "Робот приседает.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch", "AnklePitch"
            ], [1.0, -0.5, 0.3], 0.2)  # Приседание
            time.sleep(1)

            # Подготовка рук для толчка
            self.logger.info("MyClass", "Подготовка рук.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"
            ], [0.4, 0.4, 0.1, -0.1], 0.2)  # Руки перед собой
            time.sleep(0.5)

            # Разжимание пальцев
            self.logger.info("MyClass", "Разжимание пальцев.")
            self.motion.openHand("LHand")
            self.motion.openHand("RHand")
            time.sleep(0.5)

            # Толчок двумя руками вперед
            self.logger.info("MyClass", "Толчок руками.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch"
            ], [0.2, 0.2], 0.3)  # Толчок
            time.sleep(1)

            # Сжатие пальцев после толчка
            self.logger.info("MyClass", "Сжатие пальцев.")
            self.motion.closeHand("LHand")
            self.motion.closeHand("RHand")
            time.sleep(0.5)

            # Возвращение рук в исходное положение
            self.logger.info("MyClass", "Возвращение рук в исходное положение.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"
            ], [1.5, 1.5, 0.0, 0.0], 0.3)
            time.sleep(0.5)

            # Возвращение в стоячее положение
            self.logger.info("MyClass", "Возвращение в стоячее положение.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch", "AnklePitch"
            ], [0.0, 0.0, 0.0], 0.2)
            time.sleep(1)

        except Exception as e:
            self.logger.error("MyClass", "Ошибка при манипуляции с предметом: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск манипуляции с предметом.")
            self.reset_to_initial_pose()
            self.push_object()
            self.reset_to_initial_pose()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
