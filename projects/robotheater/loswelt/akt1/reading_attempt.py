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
        try:
            self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
            self.posture.goToPosture("Stand", 0.8)  # Используем "Stand" для прямой позы
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def follow_bluebot(self):
        """Робот следит за движением Bluebot."""
        try:
            self.logger.info("MyClass", "Робот начинает следить за Bluebot.")
            self.motion.setAngles("HeadYaw", -0.5, 0.2)  # Поворот вправо
            self.motion.setAngles("HeadPitch", 0.3, 0.1)  # Наклон головы вниз
            time.sleep(2)

            self.motion.setAngles("HeadYaw", 0.0, 0.05)  # Возврат головы в центр
            time.sleep(4)

            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возвращение головы в прямое положение
            time.sleep(1)

            self.logger.info("MyClass", "Робот завершил слежение за Bluebot.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при слежении за Bluebot: " + str(e))

    def read_word(self):
        """Робот пытается прочитать слово."""
        try:
            self.logger.info("MyClass", "Робот делает вид, что читает слово.")
            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Лёгкий наклон вниз
            self.motion.setAngles("HeadYaw", -0.1, 0.1)  # Легкий поворот головы влево
            time.sleep(1.0)

            self.speech.say("\\rspd=50\\ \\vct=70\\ a... ")
            time.sleep(1.0)
            self.speech.say("\\rspd=30\\ \\vct=70\\ hmm... ")
            time.sleep(1.0)
            self.speech.say("\\rspd=40\\ \\vct=70\\ ehh... ")
            time.sleep(1.5)

            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возврат головы в центр
            self.motion.setAngles("HeadYaw", 0.0, 0.1)
            time.sleep(1.0)

            self.logger.info("MyClass", "Робот завершил попытку прочитать слово.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при попытке прочитать слово: " + str(e))

    def address_audience(self):
        """Робот обращается к зрителям."""
        try:
            self.logger.info("MyClass", "Робот обращается к зрителям.")

            # Указание на табличку ладонью вверх
            self.motion.angleInterpolationWithSpeed(
                ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"],
                [0.5, 0.0, 1.5, 0.0, 1.57],  # Положение руки и запястья, чтобы ладонь смотрела вверх
                0.2
            )
            self.motion.openHand("RHand")  # Открыть ладонь
            time.sleep(2)  # Задержка для фиксации на табличке
            self.motion.closeHand("RHand")  # Закрыть ладонь

            # Одобрительные кивки
            self.motion.setAngles("HeadPitch", -0.2, 0.1)  # Наклон вниз
            time.sleep(1.5)

            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Подъем головы
            time.sleep(1.0)

            self.motion.setAngles("HeadPitch", 0.3, 0.1)  # Поднятие головы
            time.sleep(0.3)
            self.motion.setAngles("HeadPitch", 0.1, 0.1)  # Небольшой наклон вниз
            time.sleep(0.3)

            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Поднятие головы
            time.sleep(1.0)

            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возвращение в нейтральное положение
            self.logger.info("MyClass", "Робот завершил обращение к зрителям.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при обращении к зрителям: " + str(e))



    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")

            # Устанавливаем начальную позу
            self.reset_to_initial_pose()

            # Выполнение последовательности действий
            self.follow_bluebot()
            self.read_word()
            self.address_audience()

            self.reset_to_initial_pose()

            self.onStopped()  # Сигнал завершения
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.motion.rest()  # Перевод всех моторов в состояние покоя
        self.onStopped()