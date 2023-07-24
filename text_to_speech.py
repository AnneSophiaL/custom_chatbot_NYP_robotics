# from gtts import gTTS

import pyttsx3

def text_to_speech(mytext):
    engine = pyttsx3.init()
    # Customize voice male or female, or other languages
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id) 
    # Integer speech rate in words per minute. Defaults to 200 word per minute.
    engine.setProperty("rate", 187) 
    engine.say(mytext)
    
    return engine.runAndWait()

# Save the spoken text to an audio file
# engine.save_to_file(text, 'output.mp3')

# text_to_speech("hello this is a custom chatbot")

# to get the different types of voices
    # voices = engine.getProperty('voices')
    # # engine.setProperty('voice', voice.id=='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') Zira en US
    # for voice in voices:
    #     print(voice)
    #     engine.setProperty('voice', voice.id) # 4 choices, print(voice) to see them 


# def text_to_speech_saved(mytext):
#     tts = gTTS(text=mytext, lang='en') # convert my text to an audio file
#     tts.save("speech.mp3") #save it to my local directory
#     os.system("mpg321 speech.mp3") # play the audio by the operating system