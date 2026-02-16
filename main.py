import speech_recognition as sr
import webbrowser
import pyttsx3
import time
import musiclib
import feedparser
import pyjokes
import datetime



r = sr.Recognizer()

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
    speak(joke)

def greet_user():
    hour = datetime.datetime.now().hour
    current_time = datetime.datetime.now().strftime("%I:%M %p")

    if 5 <= hour < 12:
        greeting = "Good Morning"
    elif 12 <= hour < 17:
        greeting = "Good Afternoon"
    elif 17 <= hour < 21:
        greeting = "Good Evening"
    else:
        greeting = "Good Night"

    speak(f" jai shree raam !. {greeting}. The current time is {current_time}")


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
            # print(f"Headline {i+1}: {headline}")
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

    elif "good morning" in c or "good evening" in c or "time" in c or "greet" in c:
        greet_user()

    elif "goodbye" in c or "bye" in c or "exit" in c or "stop" in c:
        speak("Are you sure you want to shut me down?")

        try:
            with sr.Microphone() as source:
                print("Waiting for confirmation...")
                audio = r.listen(source, timeout=5, phrase_time_limit=4)

            confirmation = r.recognize_google(audio)
            print("Confirmation:", confirmation)

            if "yes" or "han" in confirmation.lower():
                speak("Goodbye. Shutting down now.")
                exit()
            else:
                speak("Okay, I will continue working.")

        except Exception as e:
            print("Error during confirmation:", e)
            speak("I did not catch that. Continuing operation.")




        


if __name__ == "__main__":
    speak("   Initializing Jarvis   ")
    greet_user()


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
