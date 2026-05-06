import speech_recognition as sr
import pyttsx3
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Initialize speech engine
engine = pyttsx3.init(driverName='sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)
engine.setProperty('volume', 1.0)


def speak(text):
    engine.stop()
    engine.say(text)
    engine.runAndWait()


print("Jarvis test started...")

while True:
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)

        word = recognizer.recognize_google(audio)
        print("You said:", word)

        if "jarvis" in word.lower():
            print("Wake word detected")
            speak("Yes sir")
            time.sleep(1)

    except Exception as e:
        print("Error:", e)
