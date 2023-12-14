import json

with open('sorted_output.json', 'r') as f:
    json_data = json.load(f)

    for key in json_data.items():
        first_alphabet= key[0]
        # print(f"the first letters are :{first_alphabet}")
        ascii_value=ord(first_alphabet)
        hash_value=ascii_value%26

