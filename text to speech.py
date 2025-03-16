import pyttsx3

def text_to_speech():
    engine = pyttsx3.init()
    while True:
        text = input("Enter the text you want to convert to speech: ")
        engine.say(text)
        engine.runAndWait()

# Use the function
text_to_speech()