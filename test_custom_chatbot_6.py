# pip install unstructured for directectoryloader

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain

import os
os.environ["OPENAI_API_KEY"] = "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"

from langchain.chat_models import ChatOpenAI
llm = ChatOpenAI(temperature=0.2, model_name = "gpt-4")

from langchain.document_loaders import DirectoryLoader
from langchain.document_loaders import JSONLoader
import json
from pathlib import Path
from pprint import pprint

file_path='D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data\R&M.json'
data = json.loads(Path(file_path).read_text())

file_path='D:\ESIEE\VOYAGE SINGAP 2023\project_custom_chatbot_nyp\my_data\EWB.json'
data_EWB = json.loads(Path(file_path).read_text())


# json_loader = DirectoryLoader('./my_data/', glob="**/*.json")
txt_loader = DirectoryLoader('./my_data/', glob="**/*.txt")
xlsx_loader = DirectoryLoader('./my_data/', glob="**/*.xlsx")

loaders = [txt_loader, xlsx_loader]
documents = []
print(loaders)
for loader in loaders: 
    documents.extend(loader.load())
documents.append(data)
documents.append(data_EWB)

print(F"total number of documents: ,{documents} {len(documents)}")