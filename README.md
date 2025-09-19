JarvisAI Assistant

A Python-based voice-controlled AI assistant inspired by Jarvis. It recognizes speech, responds with text-to-speech, remembers user details, fetches weather and news, plays YouTube music, searches Wikipedia, and answers questions using OpenAI’s API.

Features:

Voice commands with Google Speech Recognition
Text-to-Speech using gTTS
Weather updates (OpenWeather API)
Latest news headlines (NewsAPI)
Play, pause, stop, and resume YouTube songs
Wikipedia search
AI Q&A powered by OpenAI
Memory system to store user details and recent chats

Installation:

Clone the repository:
git clone https://github.com/your-username/JarvisAI-Assistant.git
cd JarvisAI-Assistant

Install the dependencies:
pip install -r requirements.txt

Set up your environment variables:
Create a .env file in the project root and add the following:

WEATHER_API_KEY=your_openweather_api_key
NEWS_API_KEY=your_newsapi_key
OPENAI_API_KEY=your_openai_api_key


Usage:
Run the assistant with:
python JarvisAI.py


Then give voice commands such as:
"Play Despacito"
"What is the weather in Delhi"
"Search Albert Einstein"
"Tell me the news"
"What time is it"
"Chat with me"


Requirements:
See requirements.txt for the full list of dependencies.


Project Structure
JarvisAI-Assistant/
│── JarvisAI.py
│── requirements.txt
│── README.md
│── .env.example
│── .gitignore
│── LICENSE


Future Improvements:
Add a graphical user interface (GUI)
Add reminders and calendar integration
Enable offline speech recognition
Support more APIs and plugins


License:
This project is licensed under the MIT License. See the LICENSE file for details.
