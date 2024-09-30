from naoqi import ALProxy
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def listen_for_age(self, robotIP, PORT=9559):
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)
        asr = ALProxy("ALSpeechRecognition", robotIP, PORT)
        memory = ALProxy("ALMemory", robotIP, PORT)

        # Подготовка к прослушиванию возраста
        asr.setLanguage("German") 
        vocabulary = ["eins", "zwei", "drei", "vier", "fünf", "sechs", "sieben", "acht", "neun", "zehn", "elf", "zwölf", 
                      "dreizehn", "vierzehn", "fünfzehn", "sechzehn", "siebzehn", "achtzehn", "neunzehn", 
                      "zwanzig", "einundzwanzig", "zweiundzwanzig", "dreißig", "vierzig", "fünfzig"]
        asr.setVocabulary(vocabulary, False)
        asr.subscribe("AgeListener")

        tts.say("Hallo! Bitte sage mir dein genaues Alter.")

        # Слушаем ответ
        time.sleep(5)  
        data = memory.getData("WordRecognized")
        print("Erkannt:", data)
        asr.unsubscribe("AgeListener")

        if data:
            recognized_age = data[0]
            return self.map_age_to_group(recognized_age)

        return None

    def map_age_to_group(self, recognized_age):
        """Классификация возраста по группам"""
        age_mapping = {
            "eins": 1, "zwei": 2, "drei": 3, "vier": 4, "fünf": 5, "sechs": 6, "sieben": 7, "acht": 8, "neun": 9, "zehn": 10,
            "elf": 11, "zwölf": 12, "dreizehn": 13, "vierzehn": 14, "fünfzehn": 15, "sechzehn": 16, "siebzehn": 17,
            "achtzehn": 18, "neunzehn": 19, "zwanzig": 20, "einundzwanzig": 21, "zweiundzwanzig": 22, 
            "dreißig": 30, "vierzig": 40, "fünfzig": 50
        }

        age = age_mapping.get(recognized_age, None)
        
        if age is not None:
            if age <= 12:
                return "Kind"
            elif 13 <= age <= 17:
                return "Jugendlicher"
            elif age >= 18:
                return "Erwachsener"
        return None

    def suggest_books(self, age_group, robotIP, PORT=9559):
        tts = ALProxy("ALTextToSpeech", robotIP, PORT)

        if age_group == "Kind":
            tts.say("Für Kinder unter 12 Jahren empfehle ich Märchen, Abenteuergeschichten, und natürlich eine große Auswahl an Nintendo- oder PlayStation-Spielen. Es gibt auch tolle Brettspiele und CDs für Kinder.")
        elif age_group == "Jugendlicher":
            tts.say("Für Jugendliche zwischen 13 und 17 Jahren empfehle ich Science-Fiction und Fantasy-Bücher. Außerdem bieten wir Spiele für PlayStation und Nintendo an. Du könntest auch VR-Brillen ausprobieren oder 3D-Drucker für kreative Projekte nutzen.")
        elif age_group == "Erwachsener":
            tts.say("Für Erwachsene ab 18 Jahren bieten wir eine breite Auswahl an Belletristik, Sachbüchern und Selbsthilfe-Büchern. Für technikinteressierte gibt es 3D-Drucker, VR-Brillen und viele verschiedene Brettspiele oder CD-Sammlungen.")
        else:
            tts.say("Entschuldigung, ich habe dein Alter nicht verstanden.")

        tts.say("Möchtest du mehr Details zu einer dieser Kategorien hören? Frag mich einfach!")

    def onInput_onStart(self):
        robotIP = "169.254.205.101"  # IP-адрес твоего NAO
        PORT = 9559

        try:
            # NAO начинает разговор
            age_group = self.listen_for_age(robotIP, PORT)
            if age_group:
                self.suggest_books(age_group, robotIP, PORT)
            else:
                tts = ALProxy("ALTextToSpeech", robotIP, PORT)
                tts.say("Entschuldigung, ich konnte dein Alter nicht erkennen.")
        except Exception as e:
            print("Es ist ein Fehler aufgetreten: ", e)

        self.onStopped()  

    def onInput_onStop(self):
        self.onStopped()  
