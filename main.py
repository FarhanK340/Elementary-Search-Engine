import os
import json
import string
import nltk
import regex
import unicodedata
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count
from collections import Counter

def create_forward_indexing(json_data):

    def remove_special_characters(text):
        text = text.encode('ascii','ignore').decode('utf-8')
        text = text.replace('\\', '').encode('utf-8', errors='ignore').decode('unicode_escape')
        text = regex.sub(r'[^a-zA-Z0-9\s\p{P}]+', '', text)
        text = regex.sub(r'[^\w\s]', '', text)
        # Normalize Unicode characters
        text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')  
         
        return text; 

    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        stop_words.add('@')
        tokens = nltk.word_tokenize(text)
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        return ' '.join(filtered_tokens)

    json_data = json_data.replace('@', '')
    json_data = json_data.replace('\n', '')

    # # Load JSON data into a Python list
    try:
        python_data = json.loads(json_data)
    except json.decoder.JSONDecodeError as e:
        # Print the problematic part of the JSON data
        print("Problematic JSON data:", repr(json_data[e.pos - 15:e.pos + 15]))
        raise e

    # Function to remove punctuation marks
    def removePunc(mystr):
        mystr = mystr.translate(str.maketrans('', '', string.punctuation))
        return mystr

    # Function for stemming of words. It receives a list of words
    def stemming(words):
        ps = PorterStemmer()
        stemmed_words = [ps.stem(w) for w in words]
        return stemmed_words

    # Function for tokenization of an article etc.
    def tokenize(article):
        
        article_id = article["id"]
        content = article["content"]
        author = article["author"]       

        # Tokenize content
        content = remove_special_characters(content)
        content = remove_stopwords(content)  # Removes stopwords
        content = removePunc(content)
        content_tokens = stemming(nltk.word_tokenize(content)) 

        # Tokenize author
        author_tokens = set(nltk.word_tokenize(author))  # Remove duplicate tokens

        # Tokenize article id
        article_id = article_id.replace("--", " ")
        article_id_mod = remove_stopwords(article_id)  # Removes stopwords
        article_id_mod = removePunc(article_id_mod)
        article_id_mod_tokens = set(nltk.word_tokenize(article_id_mod))  # Remove duplicate tokens

        return {
            "doc_id": article["id"],
            "content_tokens": content_tokens,
            "author_tokens": author_tokens,
            "article_id_tokens": article_id_mod_tokens,
            "title": article["title"],
            "url": article["url"]
            
        }

    # Create a forward index
    forward_index = {}

    counter_file_path = "counter_id.txt"

    # Check if the counter file exists
    try:
        with open(counter_file_path, 'r') as counter_file:
            current_counter_value = int(counter_file.read().strip())
    except FileNotFoundError:
        # If the file doesn't exist, create it with the initial value of 1
        current_counter_value = 1
        with open(counter_file_path, 'w') as counter_file:
            counter_file.write(str(current_counter_value))

    # Assign the new value to id_counter
    id_counter = count(start=current_counter_value)

    # Iterate over articles and tokenize
    for article in python_data:
        entry = tokenize(article)

        # Add title and URL to the entry
        entry["title"] = article["title"]
        entry["url"] = article["url"]

        # Count the frequency of each word
        word_frequencies = Counter(entry["content_tokens"] + list(entry["article_id_tokens"]))


        # Assign the next incremental ID to the document
        doc_id = next(id_counter)

        # Map the title, URL and word frequencies to the document ID in the forward index
        forward_index[doc_id] = {
            "title": article["title"],
            "url": article["url"],
            "word_frequencies": dict(word_frequencies)
        }

    counter_file_path = "counter_id.txt"
    with open(counter_file_path, 'w') as text_file:
        text_file.write(str(next(id_counter)))
    
    # For Updating some existing file
    existing_data = {}
    json_file_path = "forward_index.json"

    # Check if the forward index file exists
    try:
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        # If the file doesn't exist, create it with an empty dictionary
        existing_data = {}

    # Update the existing forward index with the new data
    for doc_id, word_freq in forward_index.items():
        if doc_id in existing_data:
            existing_data[doc_id].update(word_freq)
        else:
            existing_data[doc_id] = word_freq

    # Write back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
        
def load_and_format_json(file_path):

    if not file_path.endswith('.json'):
        print("Error: The file is not a JSON file.")
        return None

    try:
        with open(file_path, 'r') as json_file:
            json_data = json.load(json_file)
    except json.decoder.JSONDecodeError as e:
        print(f"Error: Failed to decode JSON in the file '{file_path}'.")
        print("Error message:", e)
        return None

    formatted_data = json.dumps(json_data, indent=4, ensure_ascii=False)
    
    return formatted_data

folder_path = "D:\\CODE RLTed\\DSA Project\\New CLone\\DSA-project\\JSON"

# Iterate over all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        json_data = load_and_format_json(file_path)
        create_forward_indexing(json_data)
