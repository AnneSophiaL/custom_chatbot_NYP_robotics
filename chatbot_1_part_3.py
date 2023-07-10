import os
import time
import openai
from retrying import RetryError, retry
from datasets import load_dataset, load_from_disk
from llama_index import (GPTVectorStoreIndex, LLMPredictor, PromptHelper,
                         BeautifulSoupWebReader, SimpleDirectoryReader,
                         load_index_from_storage, StorageContext, Document)
from langchain import OpenAI


def retry_if_error(exception):
    return isinstance(exception, RetryError)


@retry(retry_on_exception=retry_if_error, wait_fixed=1000, stop_max_attempt_number=3)
def create_vector_index():
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20

    prompt_helper = PromptHelper(
        max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)

    llm_predictor = LLMPredictor(llm=OpenAI(
        temperature=0.5,
        model_name="text-davinci-003",
        max_tokens=tokens
    ))

    documents = SimpleDirectoryReader(
        "D://ESIEE//VOYAGE SINGAP 2023//project_custom_chatbot_nyp//my_data").load_data()

    vector_index = GPTVectorStoreIndex.from_documents(
        documents=documents, llm_predictors=llm_predictor, prompt_helper=prompt_helper)
    
    vector_index.set_index_id("vector_index")
    vector_index.storage_context.persist('vectorIndex.json')

    return vector_index


def answer_me(vector_index):
    storage_context = StorageContext.from_defaults(persist_dir='vectorIndex.json')
    v_index = load_index_from_storage(storage_context, index_id="vector_index")

    while True:
        prompt = input('Please ask: ')
        query_engine = v_index.as_query_engine()
        response = query_engine.query(prompt)
        print(f"Query: {prompt} \n")
        print(f"Response: {response} \n")


if __name__ == "__main__":
    os.environ["OPENAI_API_KEY"] = "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"

    vector_index = create_vector_index()
    answer_me(vector_index)
