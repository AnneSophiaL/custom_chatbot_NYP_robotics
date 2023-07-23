# from gtts import gTTS
import pyttsx3

def text_to_speech(mytext):
    # The text that you want to convert to audio
    engine = pyttsx3.init()
    # voices = engine.getProperty('voices')
    # engine.setProperty('voice', voice.id=='HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') Zira en US
    # for voice in voices:
    #     print(voice)
    #     engine.setProperty('voice', voice.id) # 4 choices, print(voice) to see them 
    engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0') 
    engine.setProperty("rate", 187) # Integer speech rate in words per minute. Defaults to 200 word per minute.
    engine.say(mytext)
    
    return engine.runAndWait()



# text_to_speech("hello this is a custom chatbot")



# def text_to_speech_saved(mytext):
#     tts = gTTS(text=mytext, lang='en') # convert my text to an audio file
#     tts.save("speech.mp3") #save it to my local directory
#     os.system("mpg321 speech.mp3") # play the audio by the operating system