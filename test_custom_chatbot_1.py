from llama_index import GPTVectorStoreIndex, LLMPredictor, PromptHelper, BeautifulSoupWebReader, SimpleDirectoryReader, load_index_from_storage, StorageContext
from langchain import OpenAI
import sys
import os
import openai
import time
from retrying import RetryError, retry
from datasets import load_dataset, load_from_disk
from 
from llama_index import Document
import speech_recognition as sr

os.environ["OPENAI_API_KEY"] = "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"
openai.api_key = "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" # key de judith

def createVectorIndex():
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)

    #define LLM
    llmPredictor = LLMPredictor(llm=OpenAI(
        temperature=0.5,
        model_name="text-davinci-003",
        max_tokens=tokens
    ))

    # with open('test_json.json', 'r') as file:
    #     text = file.read()

    documents = SimpleDirectoryReader('D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data').load_data()

    vectorIndex = GPTVectorStoreIndex.from_documents(documents=documents, llm_predictors=llmPredictor, prompt_helper=prompt_helper)

    vectorIndex.set_index_id("vector_index")
    vectorIndex.storage_context.persist('vectorIndex')
    return vectorIndex

# def answerMe(vectorIndex): #ma fonction de base
  
#     # rebuild storage context
#     storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
#     # load index
#     vIndex = load_index_from_storage(storage_context, index_id="vector_index")

#     while True:
#         prompt = input ('Please ask: ')
#         query_engine = vIndex.as_query_engine()
#         response = query_engine.query(prompt)
#         # print(f"Query: {prompt} \n")
#         print(f"Response: {response} \n")
    

def answerMe(vectorIndex, question): # nouvelle fonction
  
    # rebuild storage context
    storage_context = StorageContext.from_defaults(persist_dir='vectorIndex')
    # load index
    vIndex = load_index_from_storage(storage_context, index_id="vector_index")

    # Use the question variable as the input instead of reading from terminal
    query_engine = vIndex.as_query_engine()
    response = query_engine.query(question)
    print(f"Response: {response} \n")



# This function listens to your speech and converts it to text
# question = listen_and_convert_to_text()

# Initialize vectorIndex before the loop
vectorIndex = createVectorIndex()
# answerMe('vectorIndex')


# Infinite loop to continuously ask questions
while True:
    # This function listens to your speech and converts it to text
    question = listen_and_convert_to_text()

    # If the speech was 'stop', exit the loop
    if question == "stop":
        break

    # If the speech was recognized, call the answerMe function with the question as input
    elif question:
        answerMe(vectorIndex, question)