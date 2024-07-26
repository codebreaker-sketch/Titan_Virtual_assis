import speech_recognition as sr
import webbrowser
import pyttsx3
import music_library
import requests

recognizer = sr.Recognizer()
engine = pyttsx3.init()
news_api = "72b16bdff07642a2b0bc434a44cf0920"

def speak(text):
    engine.say(text)
    engine.runAndWait()

def processCommand(c):
    try:
        if "open google" in c.lower():
            webbrowser.open("https://google.com")
        elif "open facebook" in c.lower():
            webbrowser.open("https://facebook.com")
        elif "open linkedin" in c.lower():
            webbrowser.open("https://linkedin.com")
        elif "open youtube" in c.lower():
            webbrowser.open("https://youtube.com")
        elif c.lower().startswith("play"):
            parts = c.lower().split(" ", 1)
            if len(parts) > 1:
                song = parts[1]
                if song in music_library.music:
                    link = music_library.music[song]
                    webbrowser.open(link)
                else:
                    speak(f"Sorry, I couldn't find the song {song} in your music library.")
            else:
                speak("Please specify a song to play.")
        elif "news" in c.lower():
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}")
            if r.status_code == 200:
                data = r.json()
                articles = data.get("articles", [])
                if articles:
                    for article in articles[:5]:  # Read only the first 5 articles for brevity
                        title = article.get('title', 'No Title')
                        print(title)
                        speak(title)
                else:
                    speak("I couldn't find any news articles.")
            else:
                speak(f"Failed to retrieve news, status code {r.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak(f"An error occurred: {e}")

if __name__ == "__main__":
    speak("Initializing Titan..")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                print("Listening for activation word...")
                audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
                word = recognizer.recognize_google(audio)
                print(f"Heard word: {word}")

                if word.lower() == "titan":
                    speak("Yes?")
                    print("Titan Active....")
                    audio = recognizer.listen(source, timeout=4, phrase_time_limit=2)
                    command = recognizer.recognize_google(audio)
                    print(f"Heard command: {command}")
                    processCommand(command)

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand the audio.")
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

