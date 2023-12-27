import json
from itertools import count

def create_alt_forward_indexing(json_data):

    forward_index = {}

    counter_file_path = "counter_id_2.txt"

    try:
        with open(counter_file_path, 'r') as counter_file:
            current_counter_value = int(counter_file.read().strip())
    except FileNotFoundError:
        current_counter_value = 1
        with open(counter_file_path, 'w') as counter_file:
            counter_file.write(str(current_counter_value))

    id_counter = count(start=current_counter_value)

    existing_data = {}
    json_file_path = "alt_forward_index.json"

    try:
        with open(json_file_path, 'r') as json_file:
            existing_data = json.load(json_file)
    except FileNotFoundError:
        existing_data = {}
        
        
    # for article in json_data:
    #     doc_id = next(id_counter)
    #     forward_index[doc_id] = {
    #         "title": article["title"],
    #         "url": article.get("url", "")  # Use get to handle the case where "url" is not present in an article
    #     }

    # counter_file_path = "counter_id_2.txt"
    # with open(counter_file_path, 'w') as text_file:
    #     text_file.write(str(next(id_counter)))
        
    # # Check if the title and URL already exist in the alternate forward index
    # existing_entries = {(info["title"], info["url"]) for info in existing_data.values()}
    # new_entries = {(info["title"], info["url"]) for info in forward_index.values()} - existing_entries

    # # Skip adding existing entries to the alternate forward index
    # new_entries_info = [info for info in forward_index.values() if (info["title"], info["url"]) in new_entries]

    # # Add new entries to the existing alternate forward index
    # for doc_id, info in enumerate(new_entries_info, start=current_counter_value):
    #     existing_data[doc_id] = info


    # for doc_id, info in forward_index.items():
    #     if doc_id in existing_data:
    #         existing_data[doc_id].update(info)
    #     else:
    #         existing_data[doc_id] = info


        
    for article in json_data:
        # Check if the title and URL already exist in the alternate forward index
        if (article["title"], article.get("url", "")) in {(info["title"], info["url"]) for info in existing_data.values()}:
            # print(f"Skipping alternate forward indexing for existing article: {article['title']}")
            continue

        doc_id = next(id_counter)
        forward_index[doc_id] = {
            "title": article["title"],
            "url": article.get("url", "")
        }

    counter_file_path = "counter_id_2.txt"
    with open(counter_file_path, 'w') as text_file:
        text_file.write(str(next(id_counter)))

    # Add new entries to the existing alternate forward index
    for doc_id, info in forward_index.items():
        existing_data[doc_id] = info
        
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

    return json_data

def alt_fi():
    
    file_path = "concatenated_json_data.json"
    json_data = load_and_format_json(file_path)
    create_alt_forward_indexing(json_data)