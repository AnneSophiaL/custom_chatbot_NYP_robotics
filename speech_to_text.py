import speech_recognition as sr

"""
This function converts the user's speaking to a text. The language set is English, but can be changed. 
The code that is commented can listen 3 times to the user if it does not understand before stopping the listening.
I remove this part when inserting the code into the app.py file because it creates conflicts with the front end but still can be used to do some tests. 

(c) Anne-Sophia LIM, 2023
"""

# OPENAI_API_KEY = "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"
def speech_to_text(timeout):
    # Initialize recognizer instance (for recognizing the speech)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout= timeout)
        try:
            # Store the result in a variable
            # text = recognizer.recognize_whisper_api(audio, api_key=OPENAI_API_KEY) 
            text = recognizer.recognize_google(audio, language="en-US") 
            return text
        except sr.UnknownValueError:
            print("Sorry, I did not understand")
        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))
    return None 


# real code below


# def speech_to_text(timeout):
#     # Initialize recognizer class (for recognizing the speech)
#     recognizer = sr.Recognizer()

#     for i in range(3): # will retry 3 times
#         # Record Audio
#         with sr.Microphone() as source:
#             print("Say something!")
#             # Optionally, can add this line to adjust for ambient noise
#             # recognizer.adjust_for_ambient_noise(source) #listen for 1 second to calibrate the energy threshold for ambient noise levels
#             # Listening to the microphone
#             audio = recognizer.listen(source, timeout= timeout)
#             try:
#                 # Store the result in a variable
#                 text = recognizer.recognize_google(audio, language='en-US') # en-US
#                 return text # if speech recognition was successful, return the recognized text
#             except sr.UnknownValueError:
#                 print("Sorry, I did not understand, can you repeat please?")
#             except sr.RequestError as e:
#                 print("Request Failed; {0}".format(e))
    
#     print("Sorry, I still did not understand what you said.")
#     return None 

# speech_to_text()
