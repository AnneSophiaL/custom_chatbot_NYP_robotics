from langchain import OpenAI
from llama_index import LLMPredictor, PromptHelper, SimpleDirectoryReader, GPTVectorStoreIndex
import os 
import openai

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

    # load documents
    documents = SimpleDirectoryReader('D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data').load_data()
    vectorIndex = GPTVectorStoreIndex.from_documents(documents=documents, llm_predictors=llmPredictor, prompt_helper=prompt_helper)

    # save index to the folder: "vectorIndex"
    vectorIndex.set_index_id("vector_index")
    vectorIndex.storage_context.persist('vectorIndex')

    return vectorIndex

createVectorIndex()