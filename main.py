
import json

import forward_index_main
import reverse_index
import barrel
import searching


while True:

    print(f"What do you want to do?")
    print(f"1. Search")
    print(f"2. Add Articles")
    print(f"3. Exit")
    choice = input("Enter you choice: ")



    if choice == "1":
        print(f"Hello!")
        # Define the file path
        # forward_index = 'alt_forward_index.json'
        words_from_user = input("Enter the word you want to search: ").lower()
        searching.query_search(words_from_user)
        
    elif choice == "2":
        print(f"1. Will be providing multiple files")
        print(f"2. Will be providing single file")
        print(f"3. Go back!")
        
        sub_choice = input("Enter your choice: ")
        if sub_choice == "1":
            folder_path = input("Provide folder path: ")
            new_forward_index =  forward_index_main.add_forward_index_through_folder(folder_path)
        elif sub_choice == "2":
            file_path = input("Enter file path: ")
            new_forward_index = forward_index_main.add_forward_index_through_single_json_file(file_path)
        elif sub_choice == "3":
            continue
        else:
            print(f"Error!")
            exit()
        
    
        if new_forward_index is not None:
            with open('new_forward_index.json', 'w') as nf:
                json.dump(new_forward_index, nf, indent=0)
        else:
            continue
        # forward_index_alt.alt_fi()
        
        input_file = "new_forward_index.json"
        output_file = "reverse_index.json"
        
       
            
        reverse_index.create_word_index(input_file,output_file)
        barrel.complete_barrels(output_file)
        
    elif choice == "3" :
        exit()
    