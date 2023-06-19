import time
import pyttsx3
import speech_recognition as sr
import googlesearch
import datetime
import wikipedia
import webbrowser as wb
import AppOpener
import os
import requests
from bs4 import BeautifulSoup

# getting initial values of user
file = open("profile.txt", "r")
data = file.readlines()

MASTER = data[0][data[0].find(":")+2::]
loc = data[1][data[1].find(":")+2::]
chrome_path = data[2][data[2].find(":")+2::]

file.close()
#---------------

# setting values of assistant
engine = pyttsx3.init('sapi5')
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)
engine.setProperty("rate", 178)
#---------------


# This function will pronounce the string passed to it
def speak(text):
    engine.say(text)
    engine.runAndWait()

# This function will wish us according to the current time
def wishMe():
    hour = int(datetime.datetime.now().hour) # hour would be string by default
    if hour >= 0 and hour < 12:
        print("Good Morning " + MASTER)
        speak("Good Morning " + MASTER)
    elif hour >= 12 and hour < 16:
        print("Good Afternoon " + MASTER)
        speak("Good Afternoon " + MASTER)
    else:
        print("Good Evening " + MASTER)
        speak("Good Evening " + MASTER)

def resetData():
    speak("Are you sure you want to reset your profile?")
    choice = takeCommand()
    if choice == "yes":
        speak("As you wish")
        speak("Your previous data has been successfully erased. Please enter new details to proceed")
        speak("Please enter your name")
        name = input("ENTER YOUR NAME: ")
        speak("Enter your location")
        location = input("ENTER YOUR LOCATION: ")
        speak("Input your chrome path")
        path = input("ENTER YOUR CHROME PATH HERE: ")

        file = open("profile.txt", "w")
        file.write(f"Name: {name}\nLocation: {location}\nChrome Path: {path}\n")
        file.close()
        speak("Your new profile has been successfully set")

    else:
        speak("Your details won't be reset")

# This function will listen to the audio, recognise it and then return it
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = str(r.recognize_google(audio, language = "en-in"))
        print(f"You said: {query}")
        return query.lower()

    except Exception as e:
        print("Could you please repeat that again")
        speak("Could you please repeat that again")
        return takeCommand()

def daily_update():
    current_date = str(datetime.datetime.now().date())
    current_hour = str(datetime.datetime.now().hour)
    current_minutes = str(datetime.datetime.now().minute)
    current_day = datetime.datetime.now().strftime("%A")

    print("The current time is " + current_hour + " " + current_minutes)
    speak("The current time is " + current_hour + " " + current_minutes)
    print("The date is "+current_date+ " and it's " + current_day+ " today")
    speak("The date is "+current_date+ " and it's " + current_day+ " today")

    search = "weather in " + loc
    url = f"https://www.google.com/search?q={search}"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    region = soup.find("span", class_="BNeawe tAd8D AP7Wnd")
    temp = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
    day = soup.find("div", class_="BNeawe tAd8D AP7Wnd")
    w = day.text.split("m", 1)
    temperature = temp.text.split("C", 1)
    s = f"Its Currently" + w[1] + " and " + temperature[0] + " Celsius in " + loc
    print(s)
    speak(s)

speak("Karen activated")
wishMe()
query1 = "None"

# Driver code
while True:
    query = takeCommand()

    if query == "no" or "go to sleep" in query:
        break

    elif "reset my profile" in query or "reset my data" in query:
        resetData()

    elif "today's updates" in query or "how is the day today" in query:
        daily_update()

    elif "wikipedia" in query:
        speak("Searching for results in wikipedia...")
        query = query.lower().replace("wikipedia", "")
        results = wikipedia.summary(query, sentences = 2)
        print(results)
        speak(results)

    elif "open youtube" in query:
        url = "youtube.com"
        wb.get(chrome_path).open(url)

    elif "open google" in query:
        url = "google.com"
        wb.get(chrome_path).open(url)

    elif "open instagram" in query:
        url = "instagram.com"
        wb.get(chrome_path).open(url)

    elif "open reddit" in query:
        url = "reddit.com"
        wb.get(chrome_path).open(url)

    elif "play music" in query:
        songs_dir = "D:\\Music"
        songs = os.listdir(songs_dir)
        os.startfile(os.path.join(songs_dir, songs[0]))

    elif "open " in query:
        try:
            app = query[query.find("open ")+5::]
            speak("OPENING " + app)
            AppOpener.run(app)
        except:
            speak(f"I'm sorry I couldn't find any application named {query} in here")

    else:
        speak("Looking for results online")
        speak("Here are the top ten results")
        for j in googlesearch.search(query, tld = "co.in", num = 10, stop=10, pause=2, country="in"):
            print(j)

    time.sleep(5)
    speak("Is there anything else you want me to do Sir?")

speak(f"As you wish sir")
print("Have a nice day")
speak("Have a nice day ")
speak("Karen shutting down")
