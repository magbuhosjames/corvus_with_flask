import win32com.client as wincl
import pythoncom
import time
from pywintypes import com_error


def say(texttosay):
    pythoncom.CoInitialize()
    speak = wincl.Dispatch("SAPI.SpVoice")
    try:
        speak.Speak(texttosay)
    except com_error:
        time.sleep(1)
        speak.Speak(texttosay)
        
        

