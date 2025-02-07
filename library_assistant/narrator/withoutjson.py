from naoqi import ALProxy
import time
import random

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.motion = None
        self.posture = None
        self.speech = None
        self.logger = None
        self.life = None
        self.memory = None
        self.running = False
        self.touch_event = "Device/SubDeviceList/Head/Touch/Middle/Sensor/Value"
        self.stories = [
            {
                "title": "Die kleine Glühwürmchen",
                "text": """In einem dunklen Wald lebte ein kleines Glühwürmchen namens Lumi. Lumi wollte genauso hell
                leuchten wie der große Mond. Jede Nacht flog es hoch in den Himmel und versuchte, den Mond zu erreichen. 
                Doch der Mond war immer zu weit entfernt, egal wie hoch Lumi flog.
                Eines Tages bemerkte die weise Eule Lumis Bemühungen und sagte: Lumi, du musst nicht so hoch fliegen, 
                um zu leuchten. Dein Licht ist bereits wunderschön und einzigartig.
                Lumi war überrascht. Es hatte sich immer mit dem Mond verglichen, 
                ohne zu merken, dass sein eigenes Licht den Wald erhellte und anderen Tieren half, ihren Weg zu finden.
                Von diesem Tag an genoss Lumi es, in der Nähe seiner Freunde zu bleiben und mit seinem sanften Licht die 
                Dunkelheit zu vertreiben. Es verstand, dass es nicht darauf ankommt, der größte oder hellste zu sein, 
                sondern darauf, wie man mit seinem Licht anderen helfen kann."""
            },
            {
                "title": "Der sprechende Baum",
                "text": """Tief im Herzen eines alten Waldes stand ein riesiger Baum, der sprechen konnte. Alle Tiere des 
                Waldes kamen zu ihm, wenn sie Rat brauchten.
                Eines Tages kam ein kleiner Hase zum Baum. Er sah besorgt aus und fragte: „Weiser Baum, wie kann ich mutiger 
                sein?“
                Der Baum bewegte leicht seine Äste im Wind und antwortete: „Mut bedeutet nicht, keine Angst zu haben, 
                sondern trotz der Angst weiterzumachen.“
                Der Hase dachte darüber nach und beschloss, das auszuprobieren. Als er am nächsten Tag einem großen 
                Schatten begegnete, wollte er zunächst weglaufen, doch dann erinnerte er sich an die Worte des Baumes. 
                Langsam trat er näher und erkannte, dass es nur ein umgestürzter Ast war.
                Von diesem Tag an wurde der kleine Hase für seinen Mut bekannt, weil er gelernt hatte, sich seinen 
                Ängsten zu stellen."""
            },
            {
                "title": "Das verlorene Wolkenschaf",
                "text": """Hoch oben am Himmel lebte eine Herde Wolkenschafe. 
                Sie trieben gemütlich mit dem Wind und spielten miteinander.
                Eines Tages wurde das kleinste Wolkenschaf, Fluff, von einem starken Windstoß weit weg von seiner Herde geweht. 
                Es hatte große Angst und wusste nicht, wie es zurückkehren konnte.
                Plötzlich erschienen Sonnenstrahlen und sagten: „Keine Sorge, Fluff. Wir helfen dir, deinen Weg zurückzufinden.“
                Zusammen mit dem Wind formten die Sonnenstrahlen kleine Zeichen im Himmel, die Fluff zur Herde führten. 
                Nach einer langen Reise fand Fluff endlich seine Familie wieder.
                Seit diesem Tag wusste Fluff, dass es immer Hilfe geben würde, selbst wenn es sich einmal verirren sollte."""
            },
            {
                "title": "Der kleine Stern, der leuchten wollte",
                "text": """Weit draußen im Universum gab es einen kleinen Stern namens Nova. 
                Er war noch jung und konnte nicht so hell leuchten wie die großen Sterne um ihn herum.
                „Ich will auch so strahlen wie ihr!“, rief Nova traurig. Doch die großen Sterne lachten nur: 
                „Du bist zu klein, um hell zu scheinen.“
                Eines Nachts fiel eine dunkle Schattenwolke über einen kleinen Planeten. 
                Die Menschen dort konnten den Himmel nicht mehr sehen. Nova sah das und beschloss, sein Licht zu nutzen, 
                so schwach es auch sein mochte.
                Er strahlte mit all seiner Kraft, und langsam durchbrach sein Licht die Dunkelheit. 
                Die Menschen auf dem Planeten konnten den Himmel wieder sehen und freuten sich.
                Die großen Sterne bemerkten das und sagten: „Nova, du hast etwas getan, was wir nicht konnten. 
                Du hast mit deinem Licht Hoffnung gebracht.“
                Von diesem Tag an wusste Nova, dass es nicht darauf ankommt, wie hell man scheint, sondern darauf, 
                dass man für andere leuchtet."""
            },
            {
                "title": "Die verschwundene Musik",
                "text": """In einer kleinen Stadt gab es ein magisches Glockenspiel, das die schönste Musik spielte. 
                Jedes Mal, wenn die Glocken erklangen, wurden die Menschen glücklich und vergaßen ihre Sorgen.
                Doch eines Tages verstummte das Glockenspiel. Die Menschen suchten überall nach einer Lösung, aber 
                niemand wusste, warum es nicht mehr spielte.
                Ein kleines Mädchen namens Mia entschied sich, die Ursache herauszufinden. 
                Sie kletterte auf den großen Glockenturm und fand eine kleine Nachtigall, die sich im 
                Mechanismus verfangen hatte.
                Behutsam half Mia dem Vogel, sich zu befreien. Dankbar sang die Nachtigall eine wunderschöne Melodie, 
                und in diesem Moment begann das Glockenspiel wieder zu läuten.
                Die Stadt war erfüllt von Musik und Freude. Die Menschen verstanden, dass es nicht nur das Glockenspiel war, 
                das ihnen Glück brachte, sondern auch die kleinen Wunder des Lebens. Mia wusste nun: Manchmal braucht 
                es nur eine helfende Hand, um die Melodie des Lebens wieder zum Erklingen zu bringen."""
            }
        ]

    def onLoad(self):
        try:
            self.motion = self.session().service("ALMotion")
            self.posture = self.session().service("ALRobotPosture")
            self.speech = self.session().service("ALAnimatedSpeech")
            self.life = self.session().service("ALAutonomousLife")
            self.memory = self.session().service("ALMemory")
            self.logger = self.session().service("ALLogger")

            self.memory.subscribeToEvent(self.touch_event, "onHeadTouchDetected", "onTouchDetected")
            self.logger.info("Storytelling", "Behavior loaded and event subscribed.")
        except Exception as e:
            self.logger.error("Storytelling", "Error during initialization: " + str(e))

    def select_random_story(self):
        """ Выбираем случайную сказку """
        if not self.stories:
            return None, None
        story = random.choice(self.stories)
        return story["title"], story["text"]

    def onInput_onStart(self):
        if self.running:
            return
        self.running = True

        try:
            self.logger.info("Storytelling", "Starting storytelling mode.")
            self.life.setState("solitary")  # Отключаем реакции
            self.posture.goToPosture("Stand", 0.5)  # Встаем в стартовую позу
            time.sleep(1)

            while self.running:
                title, text = self.select_random_story()
                if title and text:
                    self.logger.info("Storytelling", "Telling story: " + title)

                    # Запуск анимации речи
                    animated_text = "\\rspd=90\\ \\vct=85\\ " + text
                    self.speech.say(animated_text)

                # Ожидание перед следующей сказкой
                wait_time = random.randint(8, 12) * 60  # Минуты → секунды
                self.logger.info("Storytelling", "Waiting {} minutes before next story.".format(wait_time // 60))

                for _ in range(wait_time // 10):
                    if not self.running:
                        break
                    time.sleep(10)

            self.logger.info("Storytelling", "Exiting storytelling mode.")
            self.onStopped()

        except Exception as e:
            self.logger.error("Storytelling", "Error: " + str(e))
        finally:
            self.running = False

    def onInput_onStop(self):
        self.logger.info("Storytelling", "Forced stop.")
        self.running = False
        self.memory.unsubscribeToEvent(self.touch_event, "onTouchDetected")
        self.life.setState("interactive")  # Включаем обратно реакции
        self.onStopped()

    def onHeadTouchDetected(self, *_args):
        """ Обработчик события нажатия на голову """
        self.logger.info("Storytelling", "Head button pressed. Stopping the script.")
        self.running = False
