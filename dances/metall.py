import time
from naoqi import ALProxy

def main(robotIP, PORT=9559):
    try:
        # Прокси для управления движениями и позами
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

        # Включение робота
        motionProxy.wakeUp()

        # Установим начальную стойку
        postureProxy.goToPosture("StandInit", 0.5)

        # 1. Резкие движения руками в ритм музыки
        names = ["RShoulderPitch", "LShoulderPitch"]
        angles = [[-1.5, 1.5], [1.5, -1.5]]
        times = [[0.5, 1.0], [0.5, 1.0]]
        motionProxy.angleInterpolation(names, angles, times, True)

        # 2. Повороты головы влево и вправо
        motionProxy.angleInterpolation("HeadYaw", [-0.5, 0.5], [1.0, 1.0], True)

        # 3. Поднятие и опускание головы
        motionProxy.angleInterpolation("HeadPitch", [-0.5, 0.5], [1.0, 1.0], True)

        # 4. Повороты корпуса влево и вправо
        motionProxy.moveTo(0.0, 0.0, 1.57)  # Поворот на 90 градусов влево
        time.sleep(1)
        motionProxy.moveTo(0.0, 0.0, -1.57)  # Поворот на 90 градусов вправо

        # 5. Заключительные взмахи руками вверх
        names = ["RShoulderPitch", "LShoulderPitch"]
        angles = [-1.5, -1.5]  # Руки подняты вверх
        times = [1.0, 1.0]
        motionProxy.angleInterpolation(names, angles, times, True)

        # Возвращение в исходное положение
        postureProxy.goToPosture("StandInit", 2.0)

        # Отключение робота
        motionProxy.rest()

    except Exception as e:
        print("Ошибка: ", e)

if __name__ == "__main__":
    robotIP = "169.254.205.101"  # IP-адрес твоего робота
    main(robotIP)
