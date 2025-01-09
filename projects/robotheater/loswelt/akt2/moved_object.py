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
            self.posture.goToPosture("Stand", 0.8)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def manipulate_object(self):
        """NAO берет объект и перемещает его."""
        try:
            self.logger.info("MyClass", "Начало манипуляции с объектом.")

            # Берем объект (куб или шар)
            self.logger.info("MyClass", "Поднимаем объект.")
            self.motion.angleInterpolationWithSpeed(["LShoulderPitch", "LElbowYaw", "LElbowRoll"], [0.5, -1.0, -0.5], 0.1)
            time.sleep(1)

            # Поворачиваем туловище вправо для перемещения объекта
            self.logger.info("MyClass", "Перемещаем объект вправо.")
            self.motion.angleInterpolationWithSpeed(["LShoulderRoll", "LElbowYaw"], [-0.3, -1.5], 0.1)
            time.sleep(1)

            # Возвращаем руки в исходное положение
            self.logger.info("MyClass", "Опускаем объект и возвращаем руки в исходное положение.")
            self.motion.angleInterpolationWithSpeed(["LShoulderPitch", "LElbowYaw", "LElbowRoll", "LShoulderRoll"], [1.5, 0.0, -0.3, 0.0], 0.1)
            time.sleep(1)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при манипуляции с объектом: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск манипуляции с объектом.")
            self.reset_to_initial_pose()
            self.manipulate_object()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
