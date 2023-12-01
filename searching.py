import json
import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count

def search_word(file_name,word_from_user):
       with open(file_name,'r') as f:
           word_ids=json.load(f)
        
       if word_from_user not in word_ids:
            print(f"Opps sorry the '{word_from_user}' not found in the file")
       else:
            print(f"Doc_ids associated with '{word_from_user}':{word_ids[word_from_user]}" )
        
file_name='output2.json'
word_from_user= input("Enter the word you want to search: ")
search_word(file_name, word_from_user)
     