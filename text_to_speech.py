import pyttsx3

"""
This function is used to convert the text response into speech by the chatbot. 

(c) Anne-Sophia LIM, 2023
"""

def text_to_speech(mytext):
    engine = pyttsx3.init()

    # Customize voice male or female, or other languages
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 

    # Integer speech rate in words per minute. Defaults to 200 word per minute.
    engine.setProperty("rate", 187) 
    engine.say(mytext)
    
    return engine.runAndWait()