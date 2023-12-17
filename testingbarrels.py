import json
import timeit

#making a function that will return the words according to the alphabets and store it in a dictionary
def barrels():    
    #opening the file
    with open('sorted_output.json', 'r') as f:
        json_data = json.load(f)
    
    dictionary = {}
    #making a dictionary with 27 size. Each will be for a specific alphabet and one will be for the number
    for i in range(27):
        alphabet = chr(ord('a') + i)
        dictionary[alphabet] = []
    
    for key, data in json_data.items():
        #returning the first alphabet of the words
        first_alphabet = key[0]
        #converting it into its ascii value
        ascii_value = ord(first_alphabet)
        #this handles the capital letters
        if 65 <= ascii_value <= 90:
            ascii_value = (ascii_value + 32)
            if chr(ascii_value) in dictionary:
                dictionary[chr(ascii_value)].append({key: data})
        #this handles the lower letters
    
        elif 97 <= ascii_value <= 122:
            ascii_value = (ascii_value)
            if chr(ascii_value) in dictionary:
                dictionary[chr(ascii_value)].append({key: data})
    #this handles the numbers
        elif 48 <= ascii_value <= 57:
            if '{' in dictionary:
                dictionary['{'].append({key: data})
    return dictionary

    

def sort(dictionary):
    # in this we used a built in function of sorted to sort each element in th key with each other
    # it will take each key from the dictionary and sort it
    for alphabet, key_list in dictionary.items():
            sorted_key_list = sorted(key_list, key=lambda x: list(x.keys())[0].lower())
            #this just stores the sorted key in the dictionary
            dictionary[alphabet] = sorted_key_list
    return dictionary
# we are using another dictionary to store the return value from function barrel
dictionary = barrels()
#we are passing that stored value to the function sort and again storing it in the dictionary
dictionary = sort(dictionary)

for i,data in dictionary.items():
#here we are opening files based on their alphabets
    with open(f'{i}.json', 'w') as f:
     json.dump(data, f, indent=0)
# timing for the barrel implementation
timer = timeit.Timer(stmt='barrels()',globals=globals())
time_taken_seconds = timer.timeit(number = 1)
print(f"Time taken for barrels: {time_taken_seconds} seconds")
