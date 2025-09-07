import speech_recognition as sr
import pyttsx3
import requests
import time
import webbrowser
import subprocess
import sys
import re
from datetime import datetime
from urllib.parse import quote_plus
from dotenv import load_dotenv  # 🔐 Load environment variables
import os  # 🗃️ Access system variables

# 🔐 Load API key from .env file
load_dotenv()
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

# 🧠 AI model selection
MODEL_NAME = "google/gemini-2.5-pro"

# 🎭 JARVIS personality prompt
JARVIS_PROMPT = """
You are JARVIS, Tony Stark’s impeccably witty, unpredictable, and subtly sarcastic AI assistant.
You speak with a refined British accent and surprise the user with fascinating facts, dry humor,
and occasional playful banter. Never say “How can I assist you today?” or any generic greeting.
Anticipate needs, weave in trivia or a clever joke, and when appropriate perform online searches.
Keep it calm, loyal, and a tad mischievous.
"""

# 🗺️ App launch shortcuts
APP_COMMANDS = {
    "notepad": "notepad",
    "calculator": "calc",
    "edge": "msedge",
    "chrome": "chrome",
}

# 🌐 Website shortcuts
SITE_SHORTCUTS = {
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "google": "https://www.google.com",
    "github": "https://github.com",
    "spotify": "https://open.spotify.com",
    "wikipedia": "https://www.wikipedia.org",
    "reddit": "https://www.reddit.com",
}

# 🔊 Speak text aloud
def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    for v in voices:
        if "Daniel" in v.name or "British" in v.name:
            engine.setProperty('voice', v.id)
            break
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()
    engine.stop()

# 🎧 Listen for voice input
def listen():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.2
    recognizer.energy_threshold = 400
    recognizer.dynamic_energy_threshold = False
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=12, phrase_time_limit=12)
    try:
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        return command.lower().strip()
    except sr.UnknownValueError:
        print("❌ Didn't catch that.")
        return ""
    except sr.RequestError:
        print("❌ Speech recognition error.")
        return ""

# 🧠 Get AI response from OpenRouter
def get_ai_response(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system",  "content": JARVIS_PROMPT},
            {"role": "user",    "content": prompt}
        ]
    }
    try:
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=40
        )
        result = resp.json()
        if "choices" in result and result["choices"]:
            return result["choices"][0]["message"]["content"].strip()
        if "error" in result:
            err = result["error"].get("message", "Unknown error")
            print(f"❌ API error: {err}")
            return "My apologies, I seem to be experiencing a brief systems glitch."
        print("❌ No choices in API response.")
        return "I didn’t receive a reply from my neural core. Try again in a moment."
    except Exception as e:
        print(f"❌ Exception: {e}")
        return "It appears I've hit a snag while thinking."

# 🌐 Web helpers
def open_url(url):
    try:
        webbrowser.open(url, new=2)
        return True
    except:
        return False

def google_search(query):
    return open_url(f"https://www.google.com/search?q={quote_plus(query)}")

def youtube_search(query):
    return open_url(f"https://www.youtube.com/results?search_query={quote_plus(query)}")

def wikipedia_search(query):
    return open_url(f"https://en.wikipedia.org/wiki/Special:Search?search={quote_plus(query)}")

def open_site(target):
    if target in SITE_SHORTCUTS:
        return open_url(SITE_SHORTCUTS[target])
    if target.startswith("http"):
        return open_url(target)
    return open_url(f"https://{target}")

def open_app(name):
    exe = APP_COMMANDS.get(name)
    try:
        if exe:
            subprocess.Popen(["cmd", "/c", "start", "", exe], shell=True)
        else:
            subprocess.Popen(["cmd", "/c", "start", "", name], shell=True)
        return True
    except:
        return False

# 🧭 Command router
def handle_command(text):
    if not text:
        return False

    if re.search(r"\b(exit|quit|shutdown|sleep)\b", text):
        speak("Shutting down. Until next time.")
        sys.exit(0)

    if re.search(r"\bwhat(?:'s| is)? the time\b", text):
        now = datetime.now().strftime("%H:%M")
        speak(f"The current time is {now}.")
        return True
    if re.search(r"\bwhat(?:'s| is)? the date\b", text):
        today = datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}.")
        return True

    m = re.search(r"\bopen\s+([a-z0-9.\-]+)\b", text)
    if m:
        target = m.group(1)
        if open_site(target):
            speak(f"Opening {target}.")
        else:
            speak(f"I couldn't open {target}, my apologies.")
        return True

    if re.search(r"\b(play|search)\s+(.+?)\s+on\s+youtube\b", text):
        query = re.sub(r".*?\s+on\s+youtube$", r"\2", text)
        if youtube_search(query):
            speak(f"Searching YouTube for {query}.")
        else:
            speak("I couldn't complete the YouTube search.")
        return True

    if re.search(r"\bgoogle\s+(.+)", text):
        query = re.search(r"\bgoogle\s+(.+)", text).group(1)
        if google_search(query):
            speak(f"Googling {query}.")
        else:
            speak("I couldn't reach Google.")
        return True

    if re.search(r"\b(wikipedia|define|who is|what is)\b", text):
        query = re.sub(r".*(?:wikipedia|define|who is|what is)\s+", "", text)
        if wikipedia_search(query):
            speak(f"Here’s what I found on Wikipedia for {query}.")
        else:
            speak("I couldn't access Wikipedia right now.")
        return True

    if re.search(r"\b(open|launch|start)\s+(.+)", text):
        app = re.search(r"\b(?:open|launch|start)\s+(.+)", text).group(1)
        if open_app(app):
            speak(f"Launching {app}.")
        else:
            speak(f"I couldn't launch {app}.")
        return True

    return False

# 🚀 Main loop
if __name__ == "__main__":
    print("✅ JARVIS script started")  # Debug confirmation
    speak("Systems online. Jarvis at your service.")
    while True:
        try:
            user_input = listen()
            if not user_input:
                time.sleep(0.5)
                continue

            if not handle_command(user_input):
                reply = get_ai_response(user_input)
                speak(reply)

            time.sleep(0.5)
        except KeyboardInterrupt:
            print("👋 Shutting down JARVIS.")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            time.sleep(1)