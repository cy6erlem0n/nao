from naoqi import ALProxy
import logging
import time 

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        logging.basicConfig(level=logging.DEBUG)

    def onInput_onStart(self):
        # Получаем IP и порт из параметров (Edit Box в Choregraphe)
        robotIP = self.getParameter("robotIP")
        port = self.getParameter("port")

        # Проверяем, что параметры не пустые
        if robotIP and port:
            # Логируем перед отправкой сигналов
            logging.debug("Отправляем IP: %s", robotIP)
            logging.debug("Отправляем порт: %d", port)
            
            # Отправляем IP и порт в другие блоки через выходные сигналы
            self.output_IP(robotIP)  # Отправляем IP
            self.output_port(port)   # Отправляем порт           
            # Завершаем работу блока
            self.onStopped()
        else:
            logging.debug("IP или порт пустые, сигналы не отправляются")
            self.onStopped()  # Завершаем блок, даже если параметры не корректны