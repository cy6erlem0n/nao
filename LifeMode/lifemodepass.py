import time
import random
import threading

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.motion = None
        self.posture = None
        self.bIsRunning = False
        self.thread = None

    def onLoad(self):
        try:
            # Инициализация сервисов
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            
            # Перевод в начальную позу StandInit
            self.posture.goToPosture("StandInit", 0.5)
        except Exception as e:
            print("[ERROR] Ошибка инициализации сервисов: {}".format(e))

    def onUnload(self):
        # Остановка движений и завершение потока
        self.bIsRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        try:
            self.posture.goToPosture("StandInit", 0.5)
        except Exception as e:
            print("[ERROR] Ошибка возврата в начальную позу: {}".format(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Режим уже запущен.")
            return

        # Запускаем поток
        self.bIsRunning = True
        self.thread = threading.Thread(target=self.life_mode_loop)
        self.thread.start()

    def onInput_onStop(self):
        self.bIsRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

        try:
            self.posture.goToPosture("StandInit", 0.5)
        except Exception as e:
            print("[ERROR] Ошибка возврата в начальную позу при остановке: {}".format(e))

        # Передача флага об остановке
        self.output_onStopped(True)

    def life_mode_loop(self):
        # Цикл для выполнения действий
        while self.bIsRunning:
            # Увеличиваем задержку между движениями
            time.sleep(random.randint(20, 40))

            if not self.bIsRunning:
                break

            # Выбор случайного действия
            action = random.choice([self.wave_hand, self.double_wave_hand, self.head_turn, self.lean_forward, self.lean_side, self.raise_hand])
            action()

        # Когда цикл завершится, передаем флаг
        self.output_onStopped(True)

    def wave_hand(self):
        print("[INFO] Выполняется махание одной рукой.")
        self.motion.setAngles("RShoulderPitch", 0.5, 0.2)
        time.sleep(1)
        self.motion.setAngles("RShoulderPitch", 1.0, 0.2)

    def double_wave_hand(self):
        print("[INFO] Выполняется махание двумя руками.")
        self.motion.setAngles(["RShoulderPitch", "LShoulderPitch"], [0.5, 0.5], 0.2)
        time.sleep(1)
        self.motion.setAngles(["RShoulderPitch", "LShoulderPitch"], [1.0, 1.0], 0.2)

    def head_turn(self):
        print("[INFO] Выполняется медленный поворот головы.")
        self.motion.setAngles("HeadYaw", random.uniform(-0.5, 0.5), 0.1)  # Медленный поворот
        time.sleep(2)
        self.motion.setAngles("HeadYaw", 0.0, 0.1)

    def lean_forward(self):
        print("[INFO] Выполняется наклон вперед.")
        self.motion.setAngles("HipPitch", random.uniform(0.1, 0.3), 0.15)  # Медленный наклон вперед
        time.sleep(2)
        self.motion.setAngles("HipPitch", 0.0, 0.15)

    def lean_side(self):
        print("[INFO] Выполняется наклон в сторону.")
        self.motion.setAngles("LShoulderRoll", random.uniform(-0.3, 0.3), 0.2)
        time.sleep(1)
        self.motion.setAngles("LShoulderRoll", 0.0, 0.2)

    def raise_hand(self):
        print("[INFO] Выполняется поднятие руки.")
        side = random.choice(["LShoulderPitch", "RShoulderPitch"])
        self.motion.setAngles(side, 0.3, 0.2)  # Поднимаем одну руку
        time.sleep(1)
        self.motion.setAngles(side, 1.0, 0.2)
