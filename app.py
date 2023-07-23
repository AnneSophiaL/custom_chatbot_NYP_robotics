import streamlit as st
import pyttsx3
import speech_recognition as sr
from llama_index import GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader, StorageContext, load_index_from_storage
from langchain import OpenAI
import os
import openai
from speech_to_text import speech_to_text
from text_to_speech import text_to_speech

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

def createVectorIndex():
    max_input = 4096 # set the maximum input size 
    tokens = 256 # set number of output tokens
    max_chunk_overlap = 20 # set maximum chunk overlap
    chunk_size = 600 # set the maximum chunk size

    prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)

    #define LLM
    llmPredictor = LLMPredictor(llm=OpenAI(
        temperature=0.2,
        model_name="text-davinci-003",
        max_tokens=tokens
    ))

    documents = SimpleDirectoryReader('D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data - Copie').load_data()
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=documents, llm_predictors=llmPredictor, prompt_helper=prompt_helper)

    # save index to the folder: "vector_index"
    vectorIndex.set_index_id("vector_index")
    vectorIndex.storage_context.persist('vectorIndex')

    return vectorIndex

def answerMe(prompt):
    # storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
    storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
    vIndex = load_index_from_storage(storage_context, index_id="vector_index")
    query_engine = vIndex.as_query_engine()
    response = query_engine.query(prompt)
    return(response)
    # text_to_speech(response)
    # print(f"Query: {prompt} \n")
    # print(f"Response: {response} \n")

# Voice trigger function
def listen_for_trigger():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    trigger_phrase=["hey assistant", "thank you"]
    print("Listening for trigger...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

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
    # with open('style.css') as f:
    #     custom_css = f.read()
    # st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)

    # vectorIndex = createVectorIndex()
    # st.write('The indexes are created.')
    # if st.button("create Vector index"):
    #     st.write('I am creating your vector indexes')
    # else:
    #     st.write('Goodbye')
    # vectorIndex = createVectorIndex()
    trigger_phrase = ["hey assistant", "thank you"]
    st.title("Voice Assistant with Streamlit")

    start_listening = st.button("Start Listening")
    stop_listening = st.button("Stop Listening")

    # if vectorIndex: print("vectors ok")
    if start_listening:
        st.write("Listening for trigger...")
        while True:
            if listen_for_trigger() == trigger_phrase[0]:
                text_to_speech("how can I help you?")
                st.write("Trigger detected. What is your question?")
                prompt = speech_to_text(timeout=30)
                st.write(f"Question: {prompt}")
                response = answerMe(prompt)
                st.write(f"Response: {response}")
                text_to_speech(response)
                st.write("========================================================================================")
            if listen_for_trigger() == trigger_phrase[1]:
                text_to_speech("You're welcome!")
                break
            if stop_listening:
                break

if __name__ == "__main__":
    main()