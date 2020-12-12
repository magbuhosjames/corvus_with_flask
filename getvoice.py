import speech_recognition as sr
import say

class getvoice:
    def get_audio():
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Corvus is listening...")
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
            query = ""
            try:
                print("Recognizing...")
                query = r.recognize_google(audio)
                query = query.lower()
                print("You said: ", query)
            except Exception as e:
                print("Exception:", str(e))
                say.speak("I don't hear you.")

        return query