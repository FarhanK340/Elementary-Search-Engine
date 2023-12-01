import json
import string
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from itertools import count



def create_word_index(input_file,output_file):
    with open(input_file,'r') as f:
        json_data=json.load(f)

    word_ids={}
    for doc_id,stem_words in json_data.items():
        for stem_word in stem_words:
            word_id=stem_word
        
            if word_id in word_ids:
              word_ids[word_id].append(int(doc_id))
            else:
              word_ids[word_id]=[int(doc_id)]
        
    with open(output_file,'w') as f:
     json.dump(word_ids,f,indent=2)
        
        
input_file='forward_index_2.json'
output_file='output2.json'
create_word_index(input_file, output_file)



      