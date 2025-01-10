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

            # Приседание для захвата объекта
            self.logger.info("MyClass", "Робот приседает для захвата объекта.")
            self.motion.angleInterpolationWithSpeed(["KneePitch", "HipPitch"], [1.2, -0.8], 0.2)
            time.sleep(1)

            # Разжимание пальцев для захвата
            self.logger.info("MyClass", "Разжимание пальцев для захвата.")
            self.motion.openHand("LHand")
            self.motion.openHand("RHand")
            time.sleep(1)

            # Подготовка рук к захвату
            self.logger.info("MyClass", "Подготовка рук к захвату.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderPitch", "RShoulderPitch", "LShoulderRoll", "RShoulderRoll"
            ], [0.8, 0.8, 0.1, -0.1], 0.2)
            time.sleep(1)

            # Сведение рук ближе друг к другу для захвата объекта
            self.logger.info("MyClass", "Сведение рук для захвата объекта.")
            self.motion.angleInterpolationWithSpeed([
                "LElbowYaw", "RElbowYaw", "LElbowRoll", "RElbowRoll"
            ], [-1.5, 1.5, -1.7, 1.7], 0.2)
            time.sleep(1)

            # Сжимание пальцев для захвата объекта
            self.logger.info("MyClass", "Сжимание пальцев для захвата объекта.")
            self.motion.closeHand("LHand")
            self.motion.closeHand("RHand")
            time.sleep(1)

            # Поднятие объекта
            self.logger.info("MyClass", "Поднятие объекта.")
            self.motion.angleInterpolationWithSpeed(["KneePitch", "HipPitch"], [0.6, -0.2], 0.2)
            time.sleep(1)

            # Поворот туловища влево для перемещения объекта
            self.logger.info("MyClass", "Разворот туловища влево для перемещения объекта.")
            self.motion.angleInterpolationWithSpeed([
                "LShoulderRoll", "RShoulderRoll", "TorsoYaw"
            ], [0.0, 0.0, 0.785], 0.2)  # Поворот на 45 градусов
            time.sleep(1)

            # Опускание объекта
            self.logger.info("MyClass", "Опускание объекта.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch"
            ], [1.2, -0.8], 0.2)
            time.sleep(1)

            # Разжимание пальцев для отпускания объекта
            self.logger.info("MyClass", "Разжимание пальцев для отпускания объекта.")
            self.motion.openHand("LHand")
            self.motion.openHand("RHand")
            time.sleep(1)

            # Возврат в исходное положение
            self.logger.info("MyClass", "Возврат в исходное положение.")
            self.motion.angleInterpolationWithSpeed([
                "KneePitch", "HipPitch", "TorsoYaw"
            ], [0.0, 0.0, 0.0], 0.2)
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
