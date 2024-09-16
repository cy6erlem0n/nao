from naoqi import ALProxy
import time

def main(robotIP, PORT=9559):
    try:
        # Прокси для управления движениями
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

        # Включение робота
        motionProxy.wakeUp()

        # Установка в начальную стойку
        postureProxy.goToPosture("StandInit", 0.5)

        # 1. Переход в положение, имитирующее планку
        names = ["RShoulderPitch", "LShoulderPitch", "RKneePitch", "LKneePitch"]
        angles = [-1.5, -1.5, 0.9, 0.9]  # Руки вытянуты вперед, ноги согнуты
        times = [1.0, 1.0, 1.0, 1.0]
        motionProxy.angleInterpolation(names, angles, times, True)

        time.sleep(1)  # Пауза

        # 2. Имитация опускания в отжимании (сгибание рук)
        names = ["RElbowYaw", "LElbowYaw"]
        angles = [-1.0, 1.0]  # Сгибание локтей
        times = [1.5, 1.5]
        motionProxy.angleInterpolation(names, angles, times, True)

        time.sleep(1)

        # 3. Возвращение в исходное положение отжимания (разгибание рук)
        names = ["RElbowYaw", "LElbowYaw"]
        angles = [0.0, 0.0]  # Разгибание локтей
        times = [1.5, 1.5]
        motionProxy.angleInterpolation(names, angles, times, True)

        time.sleep(1)

        # Возвращение в стойку
        postureProxy.goToPosture("StandInit", 1.0)

        # Отключение робота
        motionProxy.rest()

    except Exception as e:
        print("Ошибка: ", e)

if __name__ == "__main__":
    robotIP = "169.254.205.101"  # IP-адрес твоего NAO
    main(robotIP)
