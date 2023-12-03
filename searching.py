import json
import json
import string
import nltk
import timeit
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count


def search_word(forward_index, reverse_index,word_from_user):
       #this will just read the file open
       with open(reverse_index,'r') as f:
           word_ids=json.load(f)
       if word_from_user not in word_ids:
            print(f"Opps sorry the '{word_from_user}' not found in the file")
       else:
            word_data = word_ids[word_from_user]
            
            # Opening the forward index file
            with open(forward_index,'r') as f_forward:
                forward_index = json.load(f_forward)
                
            # Printing the titles in the forward index of relevant words
            for data in word_data:
                doc_id = data['doc_id']
                if str(doc_id) in forward_index:
                    # Create a clickable link in HTML format
                    title = forward_index[str(doc_id)]['title']
                    url = forward_index[str(doc_id)]['url']
                    
                    clickable_title = f"\033]8;;{url}\033\\{title}\033]8;;\033\\"
                    print(f"Title associated with '{word_from_user}' in Doc ID {doc_id}: {clickable_title}")
# these are the files for forward_index and reverse index        
forward_index = 'forward_index.json'
reverse_index = 'output.json'

word_from_user= input("Enter the word you want to search: ").lower()

#finding out the time taken for the word to be searched in seconds
timer = timeit.Timer(stmt='search_word(forward_index,reverse_index,word_from_user)', globals=globals())
time_taken_seconds = timer.timeit(number=1)
print(f"Time taken: {time_taken_seconds} seconds")


