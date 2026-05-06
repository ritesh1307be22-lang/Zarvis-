import streamlit as st
import speech_recognition as sr
import webbrowser
import requests
import pygame
from gtts import gTTS
import os
import time
import musiclibrary 

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
    # Integration with locally hosted Phi-3 model via API [cite: 35, 47]
    url = "http://localhost:11434/api/generate"
    payload = {"model": "phi3", "prompt": command, "stream": False}
    try:
        response = requests.post(url, json=payload, timeout=10)
        return response.json()["response"]
    except Exception:
        return "I am having trouble reaching the local AI model. Please check Ollama."

# --- UI Setup ---
st.set_page_config(page_title="Jarvis OS", layout="centered")
st.title("🤖 Jarvis Virtual Assistant")
st.info("Status: System Online. Click 'Initialize' to start background listening.")

if st.button("Initialize Jarvis"):
    speak("Initializing Jarvis") # [cite: 92]
    
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    
    placeholder = st.empty()
    while True:
        with placeholder.container():
            st.write("🔍 Listening for 'Jarvis'...") # Wake-word detection phase [cite: 30]
        
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
            
            word = r.recognize_google(audio)
            
            if "jarvis" in word.lower():
                speak("Yes sir") 
                
                with sr.Microphone() as source:
                    st.write("🚀 Jarvis Active. Speak Command...")
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio = r.listen(source, timeout=5, phrase_time_limit=5)
                
                command = r.recognize_google(audio)
                st.write(f"**You said:** {command}")
                
                c = command.lower()
                
                # --- Task Automation Module [cite: 55] ---
                if "open google" in c:
                    webbrowser.open("https://google.com")
                    speak("Opening Google")
                elif "open youtube" in c:
                    webbrowser.open("https://youtube.com")
                    speak("Opening Youtube")
                elif "open facebook" in c:
                    webbrowser.open("https://facebook.com")
                    speak("Opening Facebook")
                elif "open linkedin" in c:
                    webbrowser.open("https://linkedin.com")
                    speak("Opening LinkedIn")
                
                # --- News Retrieval Module [cite: 59] ---
                elif "news" in c:
                    speak("Fetching latest news")
                    url = "https://newsdata.io/api/1/news"
                    params = {
                        "apikey": "pub_76def525ee164a3e9aa06b1222c47994",
                        "country": "in",
                        "language": "en"
                    }
                    try:
                        res = requests.get(url, params=params, timeout=5)
                        data = res.json()
                        articles = data.get("results", [])
                        for article in articles[:3]: # Reads top 3 headlines [cite: 59]
                            headline = article.get("title")
                            st.write(f"📰 {headline}")
                            speak(headline)
                            time.sleep(1)
                    except:
                        speak("I could not retrieve the news at this time.")

                elif c.startswith("play"):
                    try:
                        song = c.split(" ")[1]
                        link = musiclibrary.music[song]
                        webbrowser.open(link)
                        speak(f"Playing {song}")
                    except:
                        speak("Song not found.")
                
                # --- Local AI for Novel Queries [cite: 61] ---
                else:
                    output = aiProcess(command)
                    speak(output)
                    
        except Exception:
            continue