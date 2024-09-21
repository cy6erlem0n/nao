from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def robot_sleep_sitting(self, robotIP, PORT=9559):
        try:
            # Прокси для управления движениями и позами
            motionProxy = ALProxy("ALMotion", robotIP, PORT)
            postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
            ledsProxy = ALProxy("ALLeds", robotIP, PORT)

            # Включение робота
            motionProxy.wakeUp()

            # Переход в сидячую позу
            postureProxy.goToPosture("Sit", 1.0)

            # Уменьшаем интенсивность "глаз", чтобы имитировать закрытие глаз
            ledsProxy.fadeRGB("FaceLeds", 0x000000, 1.0)  # Отключаем глаза, имитируя сон

            # Имитация сна (робот сидит с пониженной активностью)
            time.sleep(5)  # Удерживаем позу "сна" 5 секунд

            # Возвращаем глаза в исходное состояние (робот "просыпается")
            ledsProxy.fadeRGB("FaceLeds", 0xFFFFFF, 1.0)  # Включаем глаза снова

            # Возвращение в начальную стойку (StandInit)
            postureProxy.goToPosture("StandInit", 1.0)

            # Отключение робота
            motionProxy.rest()

        except Exception as e:
            print("Error: ", e)

    def onUnload(self):
        pass

    def onInput_onStart(self):
        robotIP = "169.254.118.220"  # IP-адрес вашего NAO
        PORT = 9559
        self.robot_sleep_sitting(robotIP, PORT)
        self.onStopped()  # Завершение выполнения блока

    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()  # Завершение выполнения блока
