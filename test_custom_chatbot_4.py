
# Adding the OPEN_API_KEY to the operating system
import os
os.environ['OPENAI_API_KEY'] = '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'
# Import llama_index and indexing the documents stored in the data folder
from llama_index import GPTVectorStoreIndex, Document, SimpleDirectoryReader
documents = SimpleDirectoryReader('data').load_data()
index = GPTVectorStoreIndex.from_documents(documents)
index.save_to_disk('index.json')

# Bonus (Not required in the code, but for optimisation)
# Read the index.json later on for doing the indexation only once (#MoneySaving)
index = GPTVectorStoreIndex.load_from_disk('index.json')

print(index.query("What's next for AI Research?"))

