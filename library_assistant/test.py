from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.receivedIP = None
        self.receivedPort = None
        self.bIsRunning = False  # Флаг состояния работы

    # Прием IP
    def onInput_IP(self, ip):
        self.receivedIP = ip
        print("[DEBUG] Получен IP: {}".format(self.receivedIP))
        if not self.receivedIP:
            print("[ERROR] IP не был корректно получен или пуст.")

    # Прием порта
    def onInput_port(self, port):
        self.receivedPort = port
        print("[DEBUG] Получен порт: {}".format(self.receivedPort))
        if not self.receivedPort:
            print("[ERROR] Порт не был корректно получен или пуст.")

    # Сигнал для начала работы
    def onInput_onStart(self):
        print("[INFO] Запуск onInput_onStart")
        
        if self.bIsRunning:
            print("[WARNING] Блок уже работает")
            return

        if self.receivedIP and self.receivedPort:
            print("[INFO] Инициализация работы с IP и портом")
            self.bIsRunning = True
            try:
                print("[INFO] Работаем с IP: {}".format(self.receivedIP))
                print("[INFO] Работаем с портом: {}".format(self.receivedPort))

                # Пример создания прокси (расскомментируй и настрой под свой сервис)
                # proxy = ALProxy("SomeService", self.receivedIP, self.receivedPort)

                self.onStopped()  # Завершение блока
                print("[INFO] Завершение работы блока")
            except Exception as e:
                print("[ERROR] Ошибка при работе с IP и портом: {}".format(e))
            finally:
                self.bIsRunning = False  # Сбрасываем флаг после завершения работы
                print("[INFO] Сброс состояния bIsRunning")
        else:
            print("[ERROR] IP или порт не были получены! IP: {}, Порт: {}".format(self.receivedIP, self.receivedPort))

    def onInput_onStop(self):
        print("[INFO] Остановка блока")
        if self.bIsRunning:
            print("[INFO] Остановка текущей работы")
            self.bIsRunning = False
            self.onUnload()

    def onUnload(self):
        print("[INFO] Разгрузка блока")
