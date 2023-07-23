import gradio as gr
import pyttsx3
import speech_recognition as sr
from llama_index import GPTVectorStoreIndex, LLMPredictor, PromptHelper, SimpleDirectoryReader, StorageContext, load_index_from_storage
from langchain import OpenAI
import os
import openai
# from speech_to_text import speech_to_text 
# from text_to_speech import text_to_speech
import threading

# from transformers import pipeline

# p = pipeline("automatic-speech-recognition")

# def transcribe(audio):
#     text = p(audio)["text"]
#     return text

# gr.Interface(
#     fn=transcribe, 
#     inputs=gr.Audio(source="microphone", type="filepath"), 
#     outputs="text").launch()



# ================================================
# below is the second code
# ================================================

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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"

def text_to_speech(mytext):
    engine = pyttsx3.init()
    engine.setProperty("rate", 187) # Integer speech rate in words per minute. Defaults to 200 word per minute.
    engine.say(mytext)
    return engine.runAndWait()

def createVectorIndex():
    max_input = 4096 # set the maximum input size 
    tokens = 256 # set number of output tokens
    max_chunk_overlap = 20 # set maximum chunk overlap
    chunk_size = 600 # set the maximum chunk size
    prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)
    #define LLM
    llmPredictor = LLMPredictor(llm=OpenAI(
        temperature=0.3,
        model_name="text-davinci-003",
        max_tokens=tokens
    ))
    documents = SimpleDirectoryReader('D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data').load_data()
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=documents, llm_predictors=llmPredictor, prompt_helper=prompt_helper)
    vectorIndex.set_index_id("vector_index")
    return vectorIndex

def answerMe(vectorIndex, prompt):
    storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
    vIndex = load_index_from_storage(storage_context, index_id="vector_index")
    # while True:
    #     prompt = input ('Please ask: ')
    prompt = speech_to_text(timeout=20)  # Uses speech_to_text function to get prompt
    print(f"Recognized speech: {prompt} \n")
    query_engine = vIndex.as_query_engine()
    response = query_engine.query(prompt)
    text_to_speech(response)
    print(f"Query: {prompt} \n")
    print(f"Response: {response} \n")
    # return response

# Voice trigger function
def listen_for_trigger():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Listening for trigger...")
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        trigger = recognizer.recognize_google(audio).lower()
        if "hello assistant" in trigger:
            print("Trigger detected. Please speak your query.")
            return True
        else:
            print("Trigger not detected.")
            return False
    except sr.UnknownValueError:
        print("Could not understand audio. Please try again.")
        return False
    except sr.RequestError:
        print("Sorry, speech recognition service is currently unavailable.")
        return False

# def main():
#     vectorIndex = createVectorIndex()
#     while True:
#         if listen_for_trigger():
#             prompt = speech_to_text(timeout=10)
#             # print(f"Recognized speech: {prompt}\n")
#             response = answerMe(vectorIndex, prompt)
#             # text_to_speech(response)
#             print(f"Query: {prompt}\n")
#             print(f"Response: {response}\n")

def voice_assistant_interface(trigger_phrase="hello assistant"):
    response_text = gr.outputs.Textbox()
    trigger_input = gr.inputs.Textbox(placeholder="Say the trigger phrase to start: " + trigger_phrase)

    interface = gr.Interface(
        fn=answerMe,
        inputs=[trigger_input, gr.inputs.Textbox(placeholder="Ask your query...")],
        outputs=response_text,
        live=True
    )
    def trigger_listener():
        while True:
            trigger = listen_for_trigger()
            if trigger:
                interface.update([trigger_phrase, ""])
                interface.process_input()

    # Start the voice trigger listener in a separate thread
    trigger_thread = threading.Thread(target=trigger_listener)
    trigger_thread.daemon = True
    trigger_thread.start()

    # Start the Gradio interface
    interface.launch()

if __name__ == "__main__":
    vectorIndex = createVectorIndex()
    voice_assistant_interface()


if __name__ == "__main__":
    main()


# =======================================
# below is the very first code test
# ========================================
# title = "Custom chatbot"

# #app 1
# def user_greeting(name):
#     return "Hi! " + name + " Welcome to your first Gradio application!😎"

# #app 2
# def user_help(do):
#     return "So today we will do " + do + " using Gradio. Great choice!"

# # with gr.Blocks(theme=gr.themes.Glass()):

# #interface 1
# app1 =  gr.Interface(fn = user_greeting,
#                         inputs=gr.inputs.Textbox(placeholder="Hello! how can I help you?"), 
#                         outputs="text")
# #interface 2

# app2 =  gr.Interface(fn = user_help, inputs="text", outputs="text")

# demo = gr.TabbedInterface([app1, app2], ["Welcome", "What to do"])

# demo.launch()