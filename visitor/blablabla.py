from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        
    def robot_reading_book(robotIP, PORT=9559):
        try:
            # Прокси для управления движениями и позами
            motionProxy = ALProxy("ALMotion", robotIP, PORT)
            postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)
            tts = ALProxy("ALTextToSpeech", robotIP, PORT)
    
            # Включение робота
            motionProxy.wakeUp()
    
            # Переход в сидячую позу, как будто робот читает книгу
            postureProxy.goToPosture("Sit", 1.0)
    
            # Поднимаем руки, как будто робот держит книгу
            names = ["RShoulderPitch", "LShoulderPitch", "RWristYaw", "LWristYaw"]
            angles = [-0.3, -0.3, 0.2, -0.2]  # Руки перед собой, как будто держит книгу
            times = [1.5, 1.5, 1.5, 1.5]
            motionProxy.angleInterpolation(names, angles, times, True)
    
            # Имитация чтения и бормотания
            for i in range(3):
                tts.say("Hmm, let's see... What do we have here...")
                time.sleep(2)  # Пауза между фразами, имитация чтения
                tts.say("Mmm... very interesting...")
    
            # Опускание рук после "чтения"
            names = ["RShoulderPitch", "LShoulderPitch"]
            angles = [1.0, 1.0]  # Опускаем руки
            times = [1.5, 1.5]
            motionProxy.angleInterpolation(names, angles, times, True)
    
            # Возвращение в исходную стойку
            postureProxy.goToPosture("StandInit", 1.0)
    
            # Отключение робота
            motionProxy.rest()
    
        except Exception as e:
            print("Error: ", e)

    def onUnload(self):
        #put clean-up code here
        pass

    def onInput_onStart(self):
        robotIP = "169.254.118.220"  # IP-адрес вашего NAO
        PORT = 9559
        robot_reading_book(robotIP, PORT)
        self.onStopped() #activate the output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #it is recommended to reuse the clean-up as the box is stopped
        self.onStopped() #activate the output of the box
