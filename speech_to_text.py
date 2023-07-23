import speech_recognition as sr

def speech_to_text(timeout):
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, timeout= timeout)
        try:
            # Store the result in a variable
            text = recognizer.recognize_google(audio, language='en-US') # en-US
            return text # if speech recognition was successful, return the recognized text
        except sr.UnknownValueError:
            print("Sorry, I did not understand, can you repeat please?")
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
