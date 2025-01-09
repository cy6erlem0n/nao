from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None

    def onLoad(self):
        try:
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")

            # Инициализация сервисов
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALTextToSpeech")
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

    def move_and_turn(self):
        """Скрипт для движения NAO вправо и поворотов."""
        try:
            self.logger.info("MyClass", "Начало движения вправо и поворотов.")

            # Поворот направо
            self.motion.moveTo(0.0, 0.0, -1.57)  # Поворот на 90 градусов направо
            time.sleep(1)

            # Три шага вперед
            for _ in range(3):
                self.motion.moveTo(0.2, 0.0, 0.0)
                time.sleep(0.5)

            # Поворот налево
            self.motion.moveTo(0.0, 0.0, 1.57)  # Поворот на 90 градусов налево
            time.sleep(1)

            # Один шаг вперед
            self.motion.moveTo(0.2, 0.0, 0.0)
            time.sleep(0.5)

            self.logger.info("MyClass", "Движение завершено.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при движении: " + str(e))

    def onInput_onStart(self):
        try:
            self.logger.info("MyClass", "Запуск скрипта движения.")
            self.reset_to_initial_pose()
            self.move_and_turn()
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.onStopped()

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
