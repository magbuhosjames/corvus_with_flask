import speech_recognition as sr

class getvoice:
    def getvoice():
        r = sr.Recognizer()

        with sr.Microphone() as source:
            print("Listening...")
            audio = r.listen(source)

        said = r.recognize_google(audio)
        said = said.lower()
        print(said)

        return said
