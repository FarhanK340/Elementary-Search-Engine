import json
import os

def barrels(output_file):    
    with open(output_file, 'r') as f:
        json_data = json.load(f)
    
    dictionary = {}
    for i in range(26):
        for j in range(26):
            first_alphabet = chr(ord('a') + i)
            second_alphabet = chr(ord('a') + j)
            dictionary[f"{first_alphabet}{second_alphabet}"] = []
            

    for i in range(10):
        for j in range(10):
            first_alphabet = chr(ord('0') + i)
            second_alphabet = chr(ord('0') + j)
            dictionary[f"{first_alphabet}{second_alphabet}"] = []

    for key, data in json_data.items():
        first_alphabet = key[0]
        second_alphabet = key[1] if len(key) > 1 else None

        ascii_value_first = ord(first_alphabet.lower())
        ascii_value_second = ord(second_alphabet.lower()) if second_alphabet else None

        if (97 <= ascii_value_first <= 122 or 48 <= ascii_value_first <= 57) and (ascii_value_second is None or (97 <= ascii_value_second <= 122 or 48 <= ascii_value_second <= 57)):
            key_to_append = f"{first_alphabet}{second_alphabet}" if second_alphabet else f"{first_alphabet}"
            if key_to_append in dictionary:
                dictionary[key_to_append].append({key: data})

    return dictionary

def sort(dictionary):
    for key, key_list in dictionary.items():
        sorted_key_list = sorted(key_list, key=lambda x: list(x.keys())[0].lower())
        dictionary[key] = sorted_key_list
    return dictionary

def complete_barrels(output_file):
    dictionary = barrels(output_file)
    dictionary = sort(dictionary)
    output_folder = 'barrels'

    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        print(f"Error creating output folder '{output_folder}': {e}")
        return

    for key, data in dictionary.items():
        try:
            with open(f'{output_folder}/{key}.json', 'w') as f:
                json.dump(data, f, indent=0)
        except FileNotFoundError as fnfe:
            print(f"Error creating file '{output_folder}/{key}.json': {fnfe}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    