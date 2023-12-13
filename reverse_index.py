import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count


     
def create_word_index(input_file,output_file):
    # opening and reading the file
    with open(input_file, 'r') as f:
        json_data = json.load(f)

    word_id = {}
    for doc_id, data in json_data.items():
        for word, frequency in data['word_frequencies'].items():
            if word in word_id:
                word_id[word].append({
                        "doc_id": int(doc_id),
                        "frequency": frequency,
                        "title": data.get("title", ""),  # Include title
                        "url": data.get("url", "")      # Include url
                 })
            else:
                 word_id[word] = [{
                        "doc_id": int(doc_id),
                        "frequency": frequency,
                        "title": data.get("title", ""),  # Include title
                        "url": data.get("url", "")      # Include url
                 }]

# # Writing the modified reverse index to the output file
    with open(output_file, 'w') as f:
        json.dump(word_id, f, indent=2)
      #here we are providing the input_file and also the output_file which can vary with the device that 
      # you are using.  
input_file='forward_index.json'
output_file='output.json'
create_word_index(input_file, output_file)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]['frequency']
    left = [x for x in arr if x['frequency'] > pivot]
    middle = [x for x in arr if x['frequency'] == pivot]
    right = [x for x in arr if x['frequency'] < pivot]
    return quicksort(left) + middle + quicksort(right)

with open('output.json', 'r') as f:
    data = json.load(f)

# Sort the data based on the "frequency" attribute within each dictionary
sorted_data = {word: quicksort(docs) for word, docs in data.items()}

# Save the sorted data to a new file
with open('sorted_output.json', 'w') as f:
    json.dump(sorted_data, f, indent=2)

      