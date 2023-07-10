# Link :
# https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

# pip install pyaudio
# pip install SpeechRecognition

import speech_recognition as sr

# Initialize recognizer class (for recognizing the speech)
recognizer = sr.Recognizer()

# Record Audio
with sr.Microphone() as source:
    print("Say something!")
    # Optionally, can add this line to adjust for ambient noise
    # recognizer.adjust_for_ambient_noise(source)
    # Listening to the microphone
    audio = recognizer.listen(source, timeout=10)

# Try to recognize the listened audio with Google Speech Recognition
print("You said: " + recognizer.recognize_google(audio, language='fr-FR'))
# Store the result in a variable
text = recognizer.recognize_google(audio, language='fr-FR')
print("Stored in variable text: " + text)
