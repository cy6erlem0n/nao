from naoqi import ALProxy
import time

def main(robotIP, PORT=9559):
    try:
        # Прокси для управления движениями
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

        # Включение робота
        motionProxy.wakeUp()

        # Установим начальную стойку (StandInit)
        postureProxy.goToPosture("StandInit", 1.0)

        # Переход в планку (наклон вперёд, вытягивание рук)
        # Поднимаем руки вперёд и наклоняем корпус
        names = ["RShoulderPitch", "LShoulderPitch", "HipPitch", "RKneePitch", "LKneePitch"]
        angles = [-1.5, -1.5, -0.5, 0.5, 0.5]  # Руки вперёд, корпус наклонён, колени согнуты
        times = [2.0, 2.0, 2.0, 2.0, 2.0]
        motionProxy.angleInterpolation(names, angles, times, True)

        # Удержание позиции планки
        time.sleep(3)  # Удерживаем планку 3 секунды

        # Возвращение в начальную стойку (StandInit)
        postureProxy.goToPosture("StandInit", 1.5)

        # Отключение робота
        motionProxy.rest()

    except Exception as e:
        print("Ошибка: ", e)

if __name__ == "__main__":
    robotIP = "127.0.0.1"  # IP-адрес твоего NAO
    PORT = 9559
    main(robotIP, PORT)
