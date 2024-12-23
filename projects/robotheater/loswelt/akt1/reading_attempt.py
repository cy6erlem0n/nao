from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALTextToSpeech")
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
        self.posture.goToPosture("Stand", 0.8)
        time.sleep(0.5)

    def perform_motion(self, joints, angles, speed):
        """Выполняет движение робота."""
        try:
            self.logger.info("MyClass", "Выполняем движение: Joints={}, Angles={}, Speed={}".format(joints, angles, speed))
            self.motion.angleInterpolationWithSpeed(joints, angles, speed)
            time.sleep(0.5)
            self.logger.info("MyClass", "Движение завершено.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в движении: " + str(e))

    def attempt_speak(self):
        """Робот делает попытку говорить, но выдаёт неразборчивые звуки."""
        try:
            self.logger.info("MyClass", "Робот пытается говорить.")
            self.speech.say("\\rspd=50\\ \\vct=60\\ мммм... эээ... ааа...")
            self.logger.info("MyClass", "Попытка говорения завершена.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в попытке говорения: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")
            self.reset_to_initial_pose()

            # Следит за BlueBot справа
            self.perform_motion(["HeadYaw"], [-0.3], 0.2)  # Поворачивает голову вправо
            self.perform_motion(["HeadPitch"], [0.2], 0.2)  # Слегка опускает голову

            # Пытается что-то сказать, но издаёт неразборчивые звуки
            self.attempt_speak()

            # Обращается к зрителям жестами, указывая на табличку
            self.perform_motion(["HeadYaw"], [0.0], 0.2)  # Возвращает голову прямо
            self.perform_motion(["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], 0.2)  # Поднимает обе руки вверх
            self.perform_motion(["RShoulderRoll", "LShoulderRoll"], [-0.3, 0.3], 0.2)  # Разводит руки в стороны

            self.logger.info("MyClass", "Блок завершён.")
            self.onStopped()

        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onUnload()
        self.onStopped()
