import streamlit as st
import speech_recognition as sr
from llama_index import  StorageContext, load_index_from_storage
import os
import openai
from speech_to_text import speech_to_text
from text_to_speech import text_to_speech
# from create_vector_index import createVectorIndex

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

def answerMe(prompt):
    storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
    vIndex = load_index_from_storage(storage_context, index_id="vector_index")
    query_engine = vIndex.as_query_engine()
    response = query_engine.query(prompt)
    return(response)

# Voice trigger function
def listen_for_trigger():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    trigger_phrase=["hey assistant", "thank you"]
    print("Listening for trigger...")
    with mic as source:
        while True:
            audio = recognizer.listen(source)
            try:
                trigger = recognizer.recognize_google(audio).lower()
                if trigger_phrase[0] in trigger:
                    print("Trigger detected.")
                    return trigger_phrase[0]
                if trigger_phrase[1] in trigger:
                    print("You're welcome, bye!")
                    return trigger_phrase[1]
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Sorry, speech recognition service is currently unavailable.")
                break

def main():
    trigger_phrase = ["hey assistant", "thank you"]
    st.title("Voice Assistant with Streamlit")
    start_listening = st.button("Start Listening")
    stop_listening = st.button("Stop Listening")

    if start_listening:
        
        st.write("Listening for trigger...")
        while True:
            if listen_for_trigger() == trigger_phrase[0]:
                text_to_speech("How can I help you?")
                st.write("Trigger detected. What is your question?")
                try:
                    prompt = speech_to_text(timeout=30)
                    st.write(f"Question: {prompt}")
                    st.write("Please wait, I will look into my data...")
                    response = answerMe(prompt)
                    st.write(f"Response: {response}")
                    text_to_speech(response)
                except:
                    text_to_speech("I cannot hear you")
                    st.write("I cannot hear you.")
            
            elif listen_for_trigger() == trigger_phrase[1]:
                text_to_speech("You're welcome!")
                st.write("You're welcome!")
                break
            if stop_listening:
                break

if __name__ == "__main__":
    main()