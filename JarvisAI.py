import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import pyautogui
import pyjokes
import openai


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning")
    elif hour >= 12 and hour <= 16:
        speak("Good Afternoon")
    else:
        speak(" Good Evening")

    speak("I am Jarvis Sir. Please tell me how may I help you")


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"Afnan: {query}\n")

    except Exception as e:
        print("Say that again please... ")
        return "Sorry Unable to recognize Say that again please"
    return query

def ai(prompt):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        text = f"OpenAI response for prompt: {prompt}\n ********************\n\n"
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text += response["choices"][0]["text"]
        if not os.path.exists("OpenAI"):
            os.mkdir("OpenAI")

        with open(f"OpenAI/{''.join(prompt.split('intelligence')[1:30]).strip()}.txt", 'w') as f:
            f.write(text)
        speak(f"sir the prompt {''.join(prompt.split('intelligence')[1:30]).strip()} is been written in text file")
        print(f"{''.join(prompt.split('intelligence')[1:30]).strip()}")

    except Exception as e:
        speak("Sorry Some error occured")

chatStr = ""
def chat(query):

    try:
        global chatStr
        chatStr += f"Afnan: {query}\n Jarvis: "
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=chatStr,
            temperature=1,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]

    except Exception as e:
        return "Sorry Some error occured"

if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower()

        if 'wikipedia' in query:
            try:
                speak('Searching Wikipedia...')
                query = query.replace('wikipedia', "")
                results = wikipedia.summary(query, sentences=2)
                speak("According to Wikipedia")
                print(results)
                speak(results)
            except Exception as e:
                print("Sorry Unable to recognize")
                speak("Sorry Unable to recognize")

        # elif 'how are you' in query:
        #     msg = ["I'm fine, thanks. How about you?", "Good, thanks. And you?", "I'm good. And yourself?",
        #            "Not bad. How are you?", "Fine, and you?", "I'm doing well, and you?", "Good, how about you?"]
        #     reply = random.choice(msg)
        #     print(reply)
        #     speak(reply)
        #     greet = takeCommand()
        #     if 'good' in greet or 'fine' in greet or 'happy' in greet or 'okey' in greet:
        #         speak('Great to hear from you')
        #     elif 'not' in greet or 'upset' in greet or 'sad' in greet:
        #         speak("oh sorry")



        elif 'open youtube' in query:
            webbrowser.open("youtube.com")
            break

        elif 'open google' in query:
            webbrowser.open("google.com")
            break

        elif 'open stack overflow' in query:
            webbrowser.open("stackoverflow.com")
            break

        elif 'open chat gpt' in query:
            webbrowser.open("chat.openai.com")
            break

        elif 'open linkedin' in query:
            webbrowser.open("linkedin.com")
            break

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            print(f"sir,the time is {strTime}")
            speak(f"sir,the time is {strTime}")

        elif 'open code' in query:
            codePath = "C:\\Users\\syeda\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'quit' in query:
            speak('Thank you sir for interacting with me...')
            break

        elif 'screenshot' in query:
            path = "C:\\Users\\syeda\\OneDrive\\Pictures\\Screenshots\\Jarvis"
            speak("Sir please enter the name for the screenshot file")
            name = input("Enter the File name")
            screenshot = pyautogui.screenshot()
            screenshot.save(f"{path}\\{name}.png")
            speak("screenshot saved")

        elif 'joke' in query:
            joke = pyjokes.get_joke()
            print(joke)
            speak(joke)
            speak("hahahahah hahahahah")

        elif "using artificial intelligence" in query:
            ai(prompt=query)

        else:
            q = chat(query)
            print(f"Jarvis:{q}")
            speak(q)


