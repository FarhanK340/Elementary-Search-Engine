from flask import Flask, render_template, request
import searching
import forward_index_main
import reverse_index
import barrel
import os, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    results = []
    query = request.form['query']
    results = searching.query_search(query.lower())
    return render_template('results.html', query=query, results=results)


@app.route('/add')
def add():

    return render_template('addarticle.html')

def create_upload_folder():
    folder_path = os.path.join(app.root_path, 'uploads')
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

@app.route('/added', methods=['POST'])
def added():
    create_upload_folder()

    file_path = request.form.get('file_path')
    uploaded_file = request.files.get('file_upload')

    if not file_path and not uploaded_file:
        # Handle the case where neither file path nor file upload is provided
        return render_template('addarticle.html', error='No file provided')
    #testing
    if uploaded_file:
        # Save the uploaded file to a specified path
        file_path = os.path.join('uploads', uploaded_file.filename)
        uploaded_file.save(file_path)

    print("File Path:", file_path)

    # Rest of your code
    new_forward_index = forward_index_main.add_forward_index_through_single_json_file(file_path)

    if new_forward_index is not None:
        with open('new_forward_index.json', 'w') as nf:
            json.dump(new_forward_index, nf, indent=0)

    input_file = "new_forward_index.json"
    output_file = "reverse_index.json"

    # if os.path.exists(output_file):
    #     input_file = "new_forward_index.json"

    reverse_index.create_word_index(input_file, output_file)
    barrel.complete_barrels(output_file)

    return render_template('addarticle.html', success='File uploaded successfully')

if __name__ == '__main__':
    app.run(debug=True)