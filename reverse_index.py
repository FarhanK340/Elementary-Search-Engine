import json
     
def create_word_index(input_file,output_file):
    # opening and reading the file
    with open(input_file, 'r') as f:
        json_data = json.load(f)
    try:
        with open(output_file,'r') as r:
            reverse_index = json.load(r)
    except FileNotFoundError:
        reverse_index = {}        
    
    for doc_id, data in json_data.items():
        for word, frequency in data['word_frequencies'].items():
            if word in reverse_index:
                reverse_index[word].append({
                        "doc_id": int(doc_id),
                        "frequency": frequency,
                 })
            else:
                 reverse_index[word] = [{
                        "doc_id": int(doc_id),
                        "frequency": frequency,
                 }]
                 
    # Sort the data based on the "frequency" attribute within each dictionary
    sorted_data = {word: quicksort(docs) for word, docs in reverse_index.items()}
    # Save the sorted data to a new file
    with open(output_file, 'w') as f:
        json.dump(sorted_data, f, indent=0)

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]['frequency']
    left = [x for x in arr if x['frequency'] > pivot]
    middle = [x for x in arr if x['frequency'] == pivot]
    right = [x for x in arr if x['frequency'] < pivot]
    return quicksort(left) + middle + quicksort(right)
