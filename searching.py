import json
# import timeit
# import nltk
from nltk.corpus import stopwords

# import testmain2

def remove_stopwords(text):
    stop_words = set(stopwords.words('english'))
    stop_words.add('@')
    # tokens = nltk.word_tokenize(text)
    filtered_tokens = [word for word in text if word.lower() not in stop_words]
    return filtered_tokens

def search_word(word_from_user):
        
    # Check which barrel contains the searched word
    first_alphabet = word_from_user[0]
    second_alphabet = word_from_user[1] if len(word_from_user) > 1 else None
    key_to_search = f"{first_alphabet}{second_alphabet}" if second_alphabet else f"{first_alphabet}"

    barrel_file_path = f"barrels/{key_to_search}.json"

    # Open the relevant barrel file
    with open(barrel_file_path, 'r') as f:
        barrel_data = json.load(f)
 
    # Search for the word in the barrel
    word_data = [entry for entry in barrel_data if word_from_user in entry.keys()]
    
    if not word_data:
        print(f"Oops! The '{word_from_user}' is not found in the '{key_to_search}' barrel.")
    else:
        forward_index = "alt_forward_index.json"
        # Opening the forward index file
        with open(forward_index,'r') as f_forward:
            forward_index = json.load(f_forward)
            
    # Prepare a list to store search results
    search_results = []

    # Iterate through word entries in the barrel
    for word_entry in word_data:
        word = list(word_entry.keys())[0]
        print(f"Occurrences of '{word}' in '{key_to_search}' barrel:")

        for doc_info in word_entry[word]:
            doc_id = str(doc_info['doc_id'])
            frequency = doc_info['frequency']

            if doc_id in forward_index:
                title = forward_index[doc_id]['title']
                url = forward_index[doc_id]['url']

                # Append result to the search_results list
                result_entry = {
                    'doc_id': doc_id,
                    'title': title,
                    'url': url,
                    'frequency': frequency
                }
                search_results.append(result_entry)

    # Return the search results
    return search_results
            
       
final_results = []

def query_search(words_from_user):
    final_results = []
    words = words_from_user.split()
    words = remove_stopwords(words)

     # Dictionary to store the relevance score for each document
    document_scores = {}

    # Iterate over the words and search for each one
    for word in words:
        print(f"Searching for word: {word}")
        # Call the search_word function and get the search results
        search_results = search_word(word)

        # Update the relevance scores based on search results
        for result in search_results:
            doc_id = result['doc_id']
            frequency = result['frequency']

            # Initialize the relevance score for the document if not present
            document_scores.setdefault(doc_id, 0)

            # Increment the relevance score based on frequency
            document_scores[doc_id] += frequency

    # Sort the documents based on the relevance scores in descending order
    sorted_documents = sorted(document_scores.items(), key=lambda x: x[1], reverse=True)

    # Retrieve information for the current document from the forward index
    forward_index_path = "alt_forward_index.json"  # Update the path accordingly
    with open(forward_index_path, 'r') as f_forward:
        forward_index = json.load(f_forward)
    
    for doc_id, relevance_score in sorted_documents:

        # Check if the doc_id is present in the forward_index
        if doc_id in forward_index:
            title = forward_index[doc_id]['title']
            url = forward_index[doc_id]['url']

            # Create the clickable title
            clickable_title = f"\033]8;;{url}\033\\{title}\033]8;;\033\\"

            # Print the result
            print(f"  Doc ID {doc_id}: {clickable_title}, Relevance Score: {relevance_score}")
            print(url)
            final_results.append({
                "Doc_ID": doc_id,
                "URL": url,
                "title": title
            })
    
    return final_results
        # else:
            # print(f"  Doc ID {doc_id}: [Title not available], Relevance Score: {relevance_score}, Frequency: {document_scores[doc_id]}")