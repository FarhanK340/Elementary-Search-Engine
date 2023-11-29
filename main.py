import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count

json_data = r''''''

def create_forward_indexing(json_data):

    def remove_stopwords(text):
        stop_words = set(stopwords.words('english'))
        stop_words.add('@')
        tokens = nltk.word_tokenize(text)
        filtered_tokens = [word for word in tokens if word.lower() not in stop_words]
        return ' '.join(filtered_tokens)


    json_data = json_data.replace('@', '')
    json_data = json_data.replace('\n', '')
    # Remove backslashes and handle special characters
    json_data = json_data.replace('\\', '').encode('utf-8', errors='ignore').decode('unicode_escape')

    # Assuming your JSON data is stored in a variable called json_data
    try:
        python_data = json.loads(json_data)
    except json.decoder.JSONDecodeError as e:
        # Print the problematic part of the JSON data
        print("Problematic JSON data:", repr(json_data[e.pos - 15:e.pos + 15]))
        raise e

    # Load JSON data into a Python list
    python_data = json.loads(json_data)

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
        content = remove_stopwords(content)  # Removes stopwords
        content = removePunc(content)
        content_tokens = stemming(nltk.word_tokenize(content))   # Remove duplicate tokens

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
            "article_id_tokens": article_id_mod_tokens
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

        # Combine content tokens and article ID tokens into a single list
        combined_tokens = list(entry["content_tokens"]) + list(entry["article_id_tokens"])

        # Assign the next incremental ID to the document
        doc_id = next(id_counter)

        # Map the combined tokens to the document ID
        forward_index[doc_id] = combined_tokens

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

    existing_data.update(forward_index)

    # Write back to the JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)
        

create_forward_indexing(json_data)