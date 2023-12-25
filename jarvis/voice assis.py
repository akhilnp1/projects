import speech_recognition as sr
import webbrowser
import datetime
import pyttsx3
import pyjokes
import os

def sptext():
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Say something...")

        try:
            audio = recognizer.listen(source)
            text = recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()  # Convert recognized text to lowercase and return
        except sr.UnknownValueError:
            print("Sorry, could not understand the audio.")
            return None  # Return None in case of unknown value/error
        except sr.RequestError as e:
            print(f"Error: {e}")
            return None  # Return None in case of request error

def speechtx(x):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    rate = engine.getProperty('rate')
    engine.setProperty("rate", 150)
    engine.say(x)
    engine.runAndWait()

if __name__ == "__main__":
    while True:
            data1 = sptext()
            if data1 is not None:
                if "your name" in data1:
                    name = "my name is Peter"
                    speechtx(name)

                elif "your age" in data1:
                    age = "my age is 25"
                    speechtx(age)   

                elif 'time' in data1:
                    time=datetime.datetime.now().strftime("%I%M%p")
                    speechtx(time)
                elif "youtube" in data1 or "yotube" in data1:
                            webbrowser.open("https://www.youtube.com/")

                elif "google" in data1 or "gugle" in data1:
                            webbrowser.open("https://www.google.com/")  

                elif "joke" in data1:
                    joke_1= pyjokes.get_joke(language="en",category="neutral")
                    print(joke_1)
                    speechtx(joke_1)  

                elif 'play song' in data1:
                    add="D:\songs"
                    listsongs=os.listdir(add)
                    print(listsongs)
                    os.startfile(os.path.join(add,listsongs[0]))

                elif "exit" in data1 or "axit" in data1:
                                     print("Exiting the program...")
                                     speechtx("Thank you")
                                     break
                else:
                 print("Your voice data is not mentioned.")
else:
    print("No speech recognized or encountered an error.")