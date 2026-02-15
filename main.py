import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclib
import feedparser
import pyjokes


r = sr.Recognizer()
api_key = " c7c7680dda394a8d89e7836994ebca6a"

r.pause_threshold = 1.2   # slight pauses in speech

def speak(text):
    print("Jarvis:", text)

    engine = pyttsx3.init('sapi5')   # fresh engine every time
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 170)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

def jokes():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)


def get_news():
    try:
        speak("Fetching the latest news")

        feed = feedparser.parse("https://timesofindia.indiatimes.com/rssfeedstopstories.cms")

        articles = feed.entries

        if not articles:
            speak("No news available right now")
            return

        speak("Here are the latest headlines from India")

        for i in range(3):
            headline = articles[i].title
            print(f"Headline {i+1}: {headline}")
            speak(headline)

        speak("That is all for now")

    except Exception as e:
        print("Error:", e)
        speak("There was an error fetching the news")


def processcommand(c):
    c = c.lower()

    if "open google" in c:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "open github" in c:
        speak("Opening GitHub")
        webbrowser.open("https://github.com")

    elif "open youtube" in c:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "open instagram" in c:
        speak("Opening Instagram")
        webbrowser.open("https://instagram.com")

    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link=musiclib.music[song]
        webbrowser.open(link)

    elif "news" in c:
        get_news()

    elif "joke" in c:
        jokes()
        speak("hehehehehehe")


        


if __name__ == "__main__":
    speak("   Initializing Jarvis   ")

    # Calibrate mic once
    with sr.Microphone() as source:
        print("Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=2)

    while True:
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source)

            word = r.recognize_google(audio)
            print("Heard:", word)

            if "jarvis" in word.lower():
                print("jarvis is just coming...")
                speak("yes my lord")
                # time.sleep(1.5)

                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source, timeout=5,phrase_time_limit=6)

                command = r.recognize_google(audio)
                print("Command:", command)
                processcommand(command)

                time.sleep(1)  # avoid rapid loop restart

        except Exception as e:
            print("Error:", e)
