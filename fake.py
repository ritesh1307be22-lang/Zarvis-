import streamlit as st
import speech_recognition as sr
import webbrowser
import requests
import pygame
from gtts import gTTS
import os
import time
import musiclibrary 
import psutil     
import pyautogui 
import pywhatkit
import cv2

# --- Core Logic ---
def speak(text):
    st.write(f"**Jarvis:** {text}") 
    tts = gTTS(text)
    tts.save('temp.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load("temp.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    # Integration with locally hosted Phi-3 model via API
    # Updated to use 127.0.0.1 for better connection stability
    url = "http://127.0.0.1:11434/api/generate"
    payload = {"model": "phi3:latest", "prompt": command, "stream": False}
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json()["response"]
    except Exception:
        return "I am having trouble reaching the local AI model. Please check Ollama."

# --- UI Setup ---
st.set_page_config(page_title="Jarvis OS", layout="wide") # Changed to wide for sidebar

# FEATURE 1: SYSTEM HEALTH SIDEBAR
with st.sidebar:
    st.title("🛰️ System Vitals")
    st.divider()
    cpu_usage = psutil.cpu_percent(interval=1)
    st.subheader("Performance")
    st.progress(cpu_usage / 100, text=f"CPU: {cpu_usage}%")
    
    battery = psutil.sensors_battery()
    if battery:
        st.progress(battery.percent / 100, text=f"Battery: {battery.percent}%")
    
    st.divider()
    st.write("🟢 **Status:** System Online")
    st.write("🟢 **AI Core:** Phi-3 (Local)")
    st.write("🟢 **Env:** Virtual Environment")

st.title("🤖 Jarvis Virtual Assistant")

# FEATURE 2: SESSION HISTORY INITIALIZATION
if "history" not in st.session_state:
    st.session_state.history = []

st.info("Click 'Initialize' to start the voice interaction system.")

if st.button("Initialize Jarvis"):
    st.toast("Booting Jarvis Core...", icon="⚡")
    speak("Initializing Jarvis") 
    
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    
    placeholder = st.empty()
    while True:
        with placeholder.container():
            st.write("🔍 Listening for 'Jarvis'...") 
        
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            word = r.recognize_google(audio)
            
            if "jarvis" in word.lower():
                st.toast("Jarvis Awakened!", icon="🔥")
                speak("Yes sir") 
                
                with sr.Microphone() as source:
                    st.write("🚀 Jarvis Active. Speak Command...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    
                    # FEATURE 3: VISUAL SPINNER DURING LISTENING
                    with st.spinner("Intercepting Audio Command..."):
                        audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
                command = r.recognize_google(audio)
                st.write(f"**You said:** {command}")
                c = command.lower()
                
                output = "" # Variable to store AI/Task response for the log

                # --- TASK AUTOMATION ---
                if "open google" in c:
                    webbrowser.open("https://google.com")
                    output = "Opening Google"
                    speak(output)
                elif "open youtube" in c:
                    webbrowser.open("https://youtube.com")
                    output = "Opening Youtube"
                    speak(output)
                elif "open facebook" in c:
                    webbrowser.open("https://facebook.com")
                    output = "Opening Facebook"
                    speak(output)
                elif "open linkedin" in c:
                    webbrowser.open("https://linkedin.com")
                    output = "Opening LinkedIn"
                    speak(output)

                elif "stop work" in c or "close chrome" in c:
                    os.system("taskkill /f /im chrome.exe")
                    output = "Closing Chrome and clearing your workspace, sir."
                    speak(output)

                elif "send a message" in c:
                    pywhatkit.sendwhatmsg_instantly("+91XXXXXXXXXX", "Hello from Jarvis!")
                    output = "Message has been queued and sent, sir."
                    speak(output)

                elif "weather" in c:
                    city = "Delhi" 
                    url = f"http://wttr.in/{city}?format=%t+%C"
                    response = requests.get(url)
                    weather_data = response.text
                    output = f"The current temperature and condition in {city} is {weather_data}"
                    speak(output)

                elif "photo" in c or "camera" in c:
                    speak("Initializing camera, sir.")
                    cam = cv2.VideoCapture(0)
                    result, image = cam.read()
                    if result:
                        cv2.imwrite("jarvis_camera.png", image)
                        output = "Photo captured and saved."
                        speak(output)
                    else:
                        output = "I cannot access the camera hardware."
                        speak(output)
                    cam.release()

                elif "system status" in c or "battery" in c:
                    usage = psutil.cpu_percent()
                    bat = psutil.sensors_battery().percent
                    output = f"Sir, CPU usage is at {usage} percent and battery is at {bat} percent."
                    speak(output)

                elif "screenshot" in c:
                    pyautogui.screenshot("jarvis_shot.png")
                    output = "Screenshot taken and saved to your folder, sir."
                    speak(output)

                elif "news" in c:
                    speak("Fetching latest news")
                    url = "https://newsdata.io/api/1/news?apikey=pub_76def525ee164a3e9aa06b1222c47994&country=in&language=en"
                    try:
                        res = requests.get(url, timeout=5)
                        data = res.json()
                        articles = data.get("results", [])
                        news_titles = []
                        for article in articles[:3]: 
                            headline = article.get("title")
                            st.write(f"📰 {headline}")
                            news_titles.append(headline)
                            speak(headline)
                        output = f"Read {len(news_titles)} news headlines."
                    except:
                        output = "I could not retrieve the news."
                        speak(output)

                elif c.startswith("play"):
                    song = c.replace("play", "").strip()
                    try:
                        link = musiclibrary.music[song]
                        webbrowser.open(link)
                        output = f"Playing {song}"
                        speak(output)
                    except KeyError:
                        output = "That song isn't in your library, sir."
                        speak(output)

                elif "goodbye" in c or "exit" in c:
                    speak("System going offline. Goodbye, sir.")
                    os._exit(0)
                
                # --- LOCAL AI ---
                else:
                    output = aiProcess(command)
                    speak(output)
                
                # UPDATE SESSION LOG
                st.session_state.history.append({"user": command, "jarvis": output})
                    
        except Exception:
            continue

# FEATURE 2 (CONTINUED): RENDER LOG AT BOTTOM
if st.session_state.history:
    with st.expander("📝 Session Interaction Log", expanded=False):
        for chat in reversed(st.session_state.history):
            st.write(f"👤: {chat['user']}")
            st.write(f"🤖: {chat['jarvis']}")
            st.divider()