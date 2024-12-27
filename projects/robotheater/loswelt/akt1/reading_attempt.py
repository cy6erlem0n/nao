from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.speech = None
        self.logger = None
        self.motion = None
        self.bIsRunning = False

    def onLoad(self):
        try:
            self.speech = self.session().service("ALTextToSpeech")
            self.logger = self.session().service("ALLogger")
            self.motion = self.session().service("ALMotion")
            self.logger.info("MyClass", "Блок загружен и готов к работе.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при загрузке: " + str(e))

    def follow_bluebot(self):
        """Робот следит за движением Bluebot и смотрит вниз при повороте головы."""
        try:
            self.logger.info("MyClass", "Робот начинает следить за Bluebot.")
            
            # Поворачиваем голову вправо
            self.motion.setAngles("HeadYaw", -0.5, 0.2)  # Поворот вправо
            # Наклоняем голову вниз
            self.motion.setAngles("HeadPitch", 0.3, 0.1)  # Наклон головы вниз (угол 0.3, скорость 0.1)
            time.sleep(2)
    
            # Возвращаем голову в центр
            self.motion.setAngles("HeadYaw", 0.0, 0.05)  # Центр
            time.sleep(4)
    
            # Возвращаем голову в исходное положение (прямо)
            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возвращение головы в исходное положение
            time.sleep(1)
    
            self.logger.info("MyClass", "Робот завершил слежение за Bluebot.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при слежении за Bluebot: " + str(e))


    def read_word(self):
        """Робот пытается прочитать слово с имитацией размышлений и трудностей в чтении."""
        try:
            self.logger.info("MyClass", "Робот делает вид, что читает слово.")
            
            # Робот наклоняет голову вниз, как бы сосредотачиваясь
            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Лёгкий наклон вниз
            self.motion.setAngles("HeadYaw", -0.1, 0.1)  # Легкий поворот головы влево для сосредоточения
            time.sleep(1.0)  # Короткая задержка для придания времени на сосредоточение
    
            # Робот издаёт звуки, как будто пытается прочитать слово
            self.speech.say("\\rspd=30\\ \\vct=50\\ a... ")  # Медленная речь с паузами
            time.sleep(1.0)  # Добавление паузы между звуками
            self.speech.say("\\rspd=30\\ \\vct=50\\ hmm... ")  # Медленная речь с паузами
            time.sleep(1.0)
            # Еще раз пытается, но с неуверенностью
            self.speech.say("\\rspd=40\\ \\vct=55\\ ehh... ")  # Сомневающаяся речь
            time.sleep(1.5)  # Немного дольше, создаём паузу для реакции
    
            # После "чтения" робот возвращает голову в нормальное положение
            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возврат головы в исходное положение
            self.motion.setAngles("HeadYaw", 0.0, 0.1)  # Возврат головы в центр
            time.sleep(1.0)
    
            self.logger.info("MyClass", "Робот завершил попытку прочитать слово.")
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при попытке прочитать слово: " + str(e))


    def address_audience(self):
        """Робот обращается к зрителям с помощью движений головы, чтобы привлечь внимание."""
        try:
            self.logger.info("MyClass", "Робот обращается к зрителям с помощью движений головы.")
            
            # Робот немного наклоняет голову вниз, как будто он собирается что-то сказать или спросить
            self.motion.setAngles("HeadPitch", -0.2, 0.1)  # Лёгкий наклон головы вниз
            time.sleep(1.5)
    
            # Робот поднимает голову, привлекая внимание зрителей
            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Подъем головы
            time.sleep(1.0)
    
            # Далее робот может выполнить несколько движений, как будто просит внимание
            # Легкий кивок головы, чтобы показать согласие или просьбу
            self.motion.setAngles("HeadPitch", 0.3, 0.1)  # Поднятие головы
            time.sleep(0.3)  # Пауза
            self.motion.setAngles("HeadPitch", 0.1, 0.1)  # Небольшой наклон вниз
            time.sleep(0.3)  # Пауза
    
            # Робот снова поднимает голову, как бы подтверждая просьбу
            self.motion.setAngles("HeadPitch", 0.2, 0.1)  # Легкий наклон вверх
            time.sleep(1.0)  # Пауза, как будто ожидание реакции
    
            # Робот завершает жесты, возвращая голову в исходное положение
            self.motion.setAngles("HeadPitch", 0.0, 0.1)  # Возвращаем голову в нейтральное положение
            self.logger.info("MyClass", "Робот завершил обращение к зрителям.")
            
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при обращении к зрителям: " + str(e))


    def onInput_onStart(self):
        if self.bIsRunning:
            self.logger.warning("MyClass", "Блок уже выполняется.")
            return

        self.bIsRunning = True
        try:
            self.logger.info("MyClass", "Запуск блока.")

            # Выполнение последовательности действий
            self.follow_bluebot()
            self.read_word()
            self.address_audience()

            self.onStopped()  # Сигнал завершения
        except Exception as e:
            self.logger.error("MyClass", "Ошибка при выполнении: " + str(e))
        finally:
            self.bIsRunning = False

    def onInput_onStop(self):
        self.logger.info("MyClass", "Принудительная остановка блока.")
        self.motion.rest()  # Переводит все моторы в состояние покоя
        self.onStopped()
