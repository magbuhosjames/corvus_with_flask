import pyttsx3

def speak(texttosay):
    engine = pyttsx3.init()
    engine.say(texttosay)
    engine.runAndWait()