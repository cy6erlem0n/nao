import time
import random
import threading

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self, False)
        self.motion = None
        self.tts = None
        self.bIsRunning = False
        self.thread = None

    def onLoad(self):
        try:
            # Инициализация сервисов
            self.motion = self.session().service("ALMotion")
            self.tts = self.session().service("ALAnimatedSpeech")
            
            # Перевод в начальную позу StandInit
            self.motion.wakeUp()
            self.motion.setBreathEnabled("Arms", True)
        except Exception as e:
            print("[ERROR] Ошибка инициализации сервисов: {}".format(e))

    def onUnload(self):
        # Остановка движений и завершение потока
        self.bIsRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        try:
            self.motion.rest()
        except Exception as e:
            print("[ERROR] Ошибка возврата в режим отдыха: {}".format(e))

    def onInput_onStart(self):
        if self.bIsRunning:
            print("[WARNING] Режим уже запущен.")
            return

        # Запускаем поток
        self.bIsRunning = True
        self.thread = threading.Thread(target=self.active_fun_mode_loop)
        self.thread.start()

    def onInput_onStop(self):
        self.bIsRunning = False
        if self.thread and self.thread.is_alive():
            self.thread.join()

        try:
            self.motion.rest()
        except Exception as e:
            print("[ERROR] Ошибка возврата в режим отдыха при остановке: {}".format(e))

        # Передача флага об остановке
        self.output_onStopped(True)

    def active_fun_mode_loop(self):
        # Список фраз для пения и шуточных выкриков
        phrases = [
            "Ich liebe es, Spaß zu haben!",  # Я люблю веселиться!
            "La la la! Das Leben ist schön!",  # Ла ла ла! Жизнь прекрасна!
            "Wer will mit mir singen?",  # Кто хочет петь со мной?
            "Yeah! Tanzen wir!",  # Танцуем!
            "Das ist super!",  # Это круто!
            "Lass uns Party machen!",  # Давайте устроим вечеринку!
            "Ich bin der beste Roboter!",  # Я лучший робот!
            "Bum bum tschik! Party!",  # Бум бум чик! Вечеринка!
            "Let's rock!",  # Давайте зажжём!
            "Seid ihr bereit für Action?",  # Готовы к экшену?
            "Ich bin bereit, los geht’s!",  # Я готов, поехали!
        ]

        # Цикл для выполнения действий
        while self.bIsRunning:
            # Задержка между действиями
            time.sleep(random.randint(5, 15))

            if not self.bIsRunning:
                break

            # Выбор случайного действия или комбинации
            action = random.choice([self.say_phrase, self.combo_actions])
            action(random.choice(phrases) if action == self.say_phrase else None)

        # Когда цикл завершится, передаем флаг
        self.output_onStopped(True)

    def say_phrase(self, phrase):
        print("[INFO] Говорит: {}".format(phrase))
        # Используем анимированную речь для большего эффекта
        config = {"bodyLanguageMode": "contextual"}
        self.tts.say(phrase, config)

    def wave_hand(self, _):
        print("[INFO] Выполняется махание рукой.")
        self.motion.setAngles("RShoulderPitch", 0.5, 0.6)
        time.sleep(0.5)
        self.motion.setAngles("RShoulderPitch", 1.0, 0.6)

    def head_bob(self, _):
        print("[INFO] Выполняется кивание головой.")
        self.motion.setAngles("HeadPitch", 0.3, 0.4)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", -0.3, 0.4)
        time.sleep(0.5)
        self.motion.setAngles("HeadPitch", 0.0, 0.4)

    def raise_both_hands(self, _):
        print("[INFO] Выполняется поднимание обеих рук.")
        self.motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [0.3, 0.3], 0.6)
        time.sleep(0.5)
        self.motion.setAngles(["LShoulderPitch", "RShoulderPitch"], [1.0, 1.0], 0.6)

    def dance_move(self, _):
        print("[INFO] Танцевальное движение.")
        self.motion.setAngles("HipRoll", random.uniform(-0.5, 0.5), 0.6)
        time.sleep(1)
        self.motion.setAngles("HipRoll", 0.0, 0.6)

    def spin_around(self, _):
        print("[INFO] Выполняется поворот вокруг оси.")
        self.motion.moveTo(0, 0, 1.57)  # Поворот на 90 градусов
        time.sleep(1)
        self.motion.moveTo(0, 0, -1.57)  # Поворот назад

    def squat_and_jump(self, _):
        print("[INFO] Выполняется приседание и прыжок.")
        self.motion.setAngles("KneePitch", 0.5, 0.6)
        time.sleep(0.5)
        self.motion.setAngles("KneePitch", 1.0, 0.6)

    def combo_actions(self, _):
        print("[INFO] Выполняется комбинация движений.")
        actions = [self.wave_hand, self.head_bob, self.raise_both_hands, self.dance_move, self.spin_around, self.squat_and_jump]
        for action in random.sample(actions, 3):  # Выбираем 3 случайных действия
            action(None)
