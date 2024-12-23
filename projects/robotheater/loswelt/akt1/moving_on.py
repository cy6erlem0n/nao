from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.logger = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.logger = self.session().service("ALLogger")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
        self.motion.wakeUp()
        time.sleep(0.5)

    def perform_motion(self, joints, angles, speed):
        """Выполняет движение робота."""
        try:
            self.logger.info("MyClass", f"Выполняем движение: Joints={joints}, Angles={angles}, Speed={speed}")
            self.motion.angleInterpolationWithSpeed(joints, angles, speed)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", f"Ошибка в движении: {str(e)}")

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск третьего скрипта акта.")
            self.reset_to_initial_pose()

            # NAO смотрит по сторонам
            self.perform_motion(["HeadYaw"], [0.5], 0.2)  # Поворот головы вправо
            self.perform_motion(["HeadYaw"], [-0.5], 0.2)  # Поворот головы влево
            self.perform_motion(["HeadYaw"], [0.0], 0.2)  # Возвращение головы прямо

            # Наклоны головы вниз
            self.perform_motion(["HeadPitch"], [0.2], 0.15)  # Голова вниз
            self.perform_motion(["HeadPitch"], [-0.2], 0.15)  # Голова вверх
            self.perform_motion(["HeadPitch"], [0.0], 0.15)  # Возвращение в центр

            # Эффект "пошатывания"
            self.perform_motion(["LHipRoll", "RHipRoll"], [0.1, -0.1], 0.1)  # Лёгкий наклон влево
            self.perform_motion(["LHipRoll", "RHipRoll"], [-0.1, 0.1], 0.1)  # Лёгкий наклон вправо

            # Установка на месте, взгляд вперед
            self.perform_motion(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.2)  # Стабилизация головы

            self.logger.info("MyClass", "Третий скрипт акта завершён.")
            self.onStopped()

        except Exception as e:
            self.logger.error("MyClass", f"Ошибка при выполнении: {str(e)}")
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()
