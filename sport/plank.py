from naoqi import ALProxy
import time

def main(robotIP, PORT=9559):
    try:
        # Прокси для управления движениями
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
        postureProxy = ALProxy("ALRobotPosture", robotIP, PORT)

        # Включение робота
        motionProxy.wakeUp()

        # Переход в положение "планка"
        names = ["RShoulderPitch", "LShoulderPitch", "RKneePitch", "LKneePitch"]
        angles = [-1.5, -1.5, 0.9, 0.9]  # Руки вперед, ноги согнуты
        times = [1.0, 1.0, 1.0, 1.0]
        motionProxy.angleInterpolation(names, angles, times, True)

        # Удерживаем позицию 5 секунд
        time.sleep(5)

        # Возвращение в стойку
        postureProxy.goToPosture("StandInit", 1.0)

        # Отключение робота
        motionProxy.rest()

    except Exception as e:
        print("Ошибка: ", e)

if __name__ == "__main__":
    robotIP = "169.254.205.101"  # IP-адрес твоего NAO
    main(robotIP)
