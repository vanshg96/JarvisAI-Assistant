import speech_recognition as sr
from gtts import gTTS
import pygame
import time
import os
import datetime
import webbrowser
import requests
import openai
import yt_dlp
import vlc
import wikipedia
from dotenv import load_dotenv

load_dotenv(".env")  # load from .env file
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

#Save data
MEMORY_FILE = "memory.txt"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"name": None, "recent": []}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    memory = {"name": None, "recent": []}
    for line in lines:
        if line.startswith("name:"):
            memory["name"] = line.split(":", 1)[1].strip()
        elif line.startswith("chat:"):
            memory["recent"].append(line.split(":", 1)[1].strip())
    return memory

def save_memory(memory):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        if memory["name"]:
            f.write(f"name:{memory['name']}\n")
        for chat in memory["recent"][-10:]:  # keep only last 10 chats
            f.write(f"chat:{chat}\n")

memory = load_memory()

#Speak
def say(text):
    print(f"Jarvis: {text}")
    tts = gTTS(text=text, lang="en")
    filename = "voice.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    pygame.mixer.quit()
    os.remove(filename)

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception:
            return ""

#FEATURES 
def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")

def get_date():
    return datetime.datetime.now().strftime("%A, %d %B %Y")

def get_weather(city="Delhi"):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {desc}"
    return "Sorry, I couldn't fetch the weather."

def get_news():
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
    response = requests.get(url).json()
    articles = response.get("articles", [])
    if not articles:
        return "Sorry, no news available."
    headlines = [a["title"] for a in articles[:5]]
    return "Here are the top news headlines: " + ", ".join(headlines)

def chat_with_ai(prompt):
    if not OPENAI_API_KEY:
        return "AI chat is disabled. Please add your OpenAI API key."
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are Jarvis, a helpful AI assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response.choices[0].message["content"]

player = None  # global VLC player

def play_youtube_song(query):
    global player
    search_url = f"ytsearch1:{query}"
    ydl_opts = {"format": "bestaudio/best"}
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search_url, download=False)
        url = info['entries'][0]['url']

        # Stop previous song if playing
        if player:
            player.stop()

        player = vlc.MediaPlayer(url)
        player.play()
        return f"Playing {query} from YouTube 🎵"

def stop_song():
    global player
    if player:
        player.stop()
        player = None
        say("Song stopped.")
    else:
        say("No song is playing right now.")

def pause_song():
    global player
    if player:
        player.pause()
        say("Song paused.")
    else:
        say("No song is playing right now.")

def resume_song():
    global player
    if player:
        player.play()
        say("Resuming song.")
    else:
        say("No song is playing right now.")

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except:
        return "Sorry, I couldn't find anything on Wikipedia."


if __name__ == '__main__':
    if memory["name"]:
        say(f"Welcome back {memory['name']}, I am Jarvis.")
    else:
        say("Hello, I am Jarvis, your AI assistant.")

    while True:
        query = takeCommand()

        if not query:
            continue

        memory["recent"].append(query)
        save_memory(memory)

        # Name setting
        if "my name is" in query:
            memory["name"] = query.replace("my name is", "").strip().title()
            save_memory(memory)
            say(f"Nice to meet you, {memory['name']}")

        elif "what is my name" in query:
            if memory["name"]:
                say(f"Your name is {memory['name']}")
            else:
                say("I don't know your name yet. Please tell me.")

        elif "what did i say earlier" in query:
            if memory["recent"]:
                say(f"You said: {memory['recent'][-2]}")
            else:
                say("I don’t remember anything yet.")

        # Websites
        elif "open youtube" in query:
            say("Opening YouTube")
            webbrowser.open("https://www.youtube.com")
        elif "open google" in query:
            say("Opening Google")
            webbrowser.open("https://www.google.com")
        elif "open wikipedia" in query:
            say("Opening Wikipedia")
            webbrowser.open("https://www.wikipedia.org")

        # Music commands
        elif "play" in query:
            song = query.replace("play", "").strip()
            if song:
                response = play_youtube_song(song)
                say(response)
            else:
                say("Please tell me the song name.")
        elif "stop song" in query:
            stop_song()
        elif "pause song" in query:
            pause_song()
        elif "resume song" in query:
            resume_song()

        # Time & Date
        elif "time" in query:
            say(f"Sir, the time is {get_time()}")
        elif "date" in query:
            say(f"Today is {get_date()}")

        # Weather
        elif "weather" in query:
            say(get_weather("Delhi"))  # change city if needed

        # News
        elif "news" in query:
            say(get_news())

        # Wikipedia
        elif "search" in query or "who is" in query or "what is" in query:
            topic = query.replace("search", "").replace("who is", "").replace("what is", "").strip()
            if topic:
                result = search_wikipedia(topic)
                say(result)
            else:
                say("Please tell me what to search on Wikipedia.")

        # Small Talk
        elif "how are you" in query:
            say("I am doing great, thank you for asking. How about you?")
        elif "joke" in query:
            say("Why don't programmers like nature? Because it has too many bugs!")

        # AI Q&A
        elif "question" in query or "jarvis" in query or "chat" in query:
            response = chat_with_ai(query)
            say(response)

        # Exit
        elif "exit" in query or "bye" in query or "quit" in query:
            say("Goodbye sir, shutting down.")
            break

        else:
            say("I did not understand that. Would you like me to search it online?")
