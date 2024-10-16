from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.bIsRunning = False  # Булевый флаг для отслеживания состояния работы

    def onLoad(self):
        # Инициализация сервисов через текущую сессию Choregraphe
        self.motion = self.session().service("ALMotion")
        self.posture = self.session().service("ALRobotPosture")

        # Отключаем Basic Awareness для 3D модели
        try:
            basic_awareness = self.session().service("ALBasicAwareness")
            basic_awareness.pauseAwareness()
        except Exception as e:
            print("[WARNING] Basic Awareness не поддерживается на 3D модели: {}".format(e))

    def onInput_onStart(self):
        # Проверяем флаг, чтобы не запускать блок повторно
        if self.bIsRunning:
            print("[WARNING] Блок уже выполняется")
            return

        self.bIsRunning = True  # Устанавливаем флаг перед выполнением

        # Переводим NAO в стартовую позу
        self.posture.goToPosture("StandInit", 0.5)

        # Выполняем движения: сначала влево, затем вправо
        self.raise_left_hand()
        time.sleep(3)  # Держим левую руку 3 секунды

        self.return_to_initial_position()
        time.sleep(2)  # Ожидаем возвращения в начальное состояние

        self.raise_right_hand()
        time.sleep(3)  # Держим правую руку 3 секунды

        self.return_to_initial_position()
        time.sleep(2)  # Ожидаем возвращения в начальное состояние

        # Сбрасываем флаг после завершения
        self.bIsRunning = False
        self.onStopped()  # Завершение блока

    def raise_left_hand(self):
        # Поднимаем левую руку для указания влево
        print("[INFO] Поднимаем левую руку")
        names = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll", "LWristYaw"]
        angles = [0.5, 0.5, -1.5, -0.5, 0.0]  # Угол для указания влево
        times = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.motion.angleInterpolation(names, angles, times, True)

    def raise_right_hand(self):
        # Поднимаем правую руку для указания вправо
        print("[INFO] Поднимаем правую руку")
        names = ["RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll", "RWristYaw"]
        angles = [0.5, -0.5, 1.5, 0.5, 0.0]  # Угол для указания вправо
        times = [1.0, 1.0, 1.0, 1.0, 1.0]
        self.motion.angleInterpolation(names, angles, times, True)

    def return_to_initial_position(self):
        # Возвращаемся в начальное положение
        print("[INFO] Возвращаемся в начальную позу")
        self.posture.goToPosture("StandInit", 0.5)

    def onInput_onStop(self):
        # Прекращаем выполнение и сбрасываем флаг
        if self.bIsRunning:
            print("[INFO] Остановка выполнения движений")
            self.bIsRunning = False
            self.motion.rest()
            self.onUnload()

    def onUnload(self):
        print("[INFO] Блок движений завершен")
        self.motion.rest()