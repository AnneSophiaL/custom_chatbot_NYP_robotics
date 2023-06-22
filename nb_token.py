import spacy

# Load the spaCy language model
nlp = spacy.load("en_core_web_sm")

# Read the file
file_path = "D:\\ESIEE\VOYAGE SINGAP 2023\\project\\test_jsonl.jsonl"
with open(file_path, "r", encoding="utf-8") as file:
    text = file.read()

# Process the text with spaCy
doc = nlp(text)

# Get the number of tokens
num_tokens = len(doc)

print("Number of tokens:", num_tokens)
# en date du 19/06/23 : 1405 tokens
# 21/06/23 : Number of tokens: 4570
# with jsonl : Number of tokens: 4514