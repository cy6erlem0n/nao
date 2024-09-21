from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.receivedIP = None
        self.receivedPort = None

    # Прием IP
    def onInput_IP(self, ip):
        self.receivedIP = ip
        print("Получен IP:", self.receivedIP)

    # Прием порта
    def onInput_port(self, port):
        self.receivedPort = port
        print("Получен порт:", self.receivedPort)

    # Сигнал для начала работы
    def onStart(self):
        if self.receivedIP and self.receivedPort:
            print("Инициализация работы с IP и портом")
            try:
                # Тут можно делать любые операции с IP и портом
                print("Работаем с IP:", self.receivedIP)
                print("Работаем с портом:", self.receivedPort)
                
                # Дополнительные действия (например, подключение к роботу)
                # proxy = ALProxy("SomeService", self.receivedIP, self.receivedPort)
                
                # Логируем успешное завершение работы блока
                self.onStopped()  # Завершение блока
            except Exception as e:
                print("Ошибка при работе с IP и портом:", e)
        else:
            print("IP или порт не были получены!")
