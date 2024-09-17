from naoqi import ALProxy
import time

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

if __name__ == "__main__":
    robotIP = "169.254.205.101"  # IP-адрес вашего NAO
    PORT = 9559
    robot_reading_book(robotIP, PORT)
