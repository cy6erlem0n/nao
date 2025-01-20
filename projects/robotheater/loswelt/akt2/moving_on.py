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
            self.posture = self.session().service("ALRobotPosture")

            # Проверка наличия сервиса ALMotion
            try:
                self.motion = self.session().service("ALMotion")
            except Exception as e:
                self.logger.warning("MyClass", "Сервис ALMotion недоступен. Работа в виртуальной среде.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def reset_to_initial_pose(self):
        """Возвращаем NAO в начальную позу Stand."""
        try:
            self.logger.info("MyClass", "Возвращаем робота в позу Stand.")
            self.posture.goToPosture("Stand", 0.6)  # Используем "Stand" для прямой позы
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при возврате в позу Stand: " + str(e))

    def perform_motion(self, joints, angles, speed):
        """Выполняет движение робота."""
        if not self.motion:
            self.logger.warning("MyClass", "ALMotion недоступен. Пропускаем движение: Joints={}, Angles={}.".format(joints, angles))
            return

        try:
            self.logger.info("MyClass", "Выполняем движение: Joints={}, Angles={}, Speed={}".format(joints, angles, speed))
            self.motion.angleInterpolationWithSpeed(joints, angles, speed)
            time.sleep(0.5)
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в движении: {}".format(str(e)))

    def perform_swaying_effect(self):
        """Эффект пошатывания робота с поочередными движениями ног."""
        try:
            self.logger.info("MyClass", "Начинаем эффект пошатывания.")
    
            # Шаг 1: Лёгкий присест на левую ногу
            self.perform_motion(["LHipPitch"], [0.1], 0.2)  # Сгибаем левую ногу
            self.perform_motion(["RHipPitch"], [-0.05], 0.2)  # Чуть выпрямляем правую
            self.perform_motion(["LHipRoll"], [0.05], 0.2)  # Смещаем вес на левую
            time.sleep(0.4)  # Пауза для фиксации
    
            # Возврат в центр
            self.perform_motion(["LHipPitch", "RHipPitch", "LHipRoll"], [0.0, 0.0, 0.0], 0.2)
            time.sleep(0.3)
    
            # Шаг 2: Лёгкий присест на правую ногу
            self.perform_motion(["RHipPitch"], [0.1], 0.2)  # Сгибаем правую ногу
            self.perform_motion(["LHipPitch"], [-0.05], 0.2)  # Чуть выпрямляем левую
            self.perform_motion(["RHipRoll"], [0.05], 0.2)  # Смещаем вес на правую
            time.sleep(0.4)  # Пауза для фиксации
    
            # Возврат в центр
            self.perform_motion(["LHipPitch", "RHipPitch", "RHipRoll"], [0.0, 0.0, 0.0], 0.2)
            time.sleep(0.3)
    
            self.logger.info("MyClass", "Эффект пошатывания завершён.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка в эффекте пошатывания: " + str(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск третьего скрипта акта.")
            self.reset_to_initial_pose()

            # Проверяем, доступен ли сервис движения
            if not self.motion:
                self.logger.warning("MyClass", "Сервис ALMotion отсутствует. Выполнение ограничено.")
                self.onStopped()
                return

            # NAO смотрит по сторонам
            self.perform_motion(["HeadYaw"], [0.5], 0.2)  # Поворот головы вправо
            self.perform_motion(["HeadYaw"], [-0.5], 0.2)  # Поворот головы влево
            self.perform_motion(["HeadYaw"], [0.0], 0.2)  # Возвращение головы прямо

            # Наклоны головы вниз
            self.perform_motion(["HeadPitch"], [0.2], 0.15)  # Голова вниз
            self.perform_motion(["HeadPitch"], [-0.2], 0.15)  # Голова вверх
            self.perform_motion(["HeadPitch"], [0.0], 0.15)  # Возвращение в центр

            # Эффект "пошатывания"
            self.perform_swaying_effect()
            # Установка на месте, взгляд вперед
            self.perform_motion(["HeadYaw", "HeadPitch"], [0.0, 0.0], 0.2)  # Стабилизация головы

            self.logger.info("MyClass", "Третий скрипт акта завершён.")
            self.onStopped()

        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: {}".format(str(e)))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.onStopped()