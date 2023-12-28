from flask import Flask, render_template, request
import searching
import forward_index_alt
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

@app.route('/added', methods=['POST'])
def added():
    file_path = request.form['file_path']
    print(file_path)
    if file_path:
        # Execute your Python script with the provided folder path
        new_forward_index = forward_index_main.add_forward_index_through_single_json_file(file_path)

        if new_forward_index is not None:
            with open('new_forward_index.json', 'w') as nf:
                json.dump(new_forward_index, nf, indent=0)

        forward_index_alt.alt_fi()

        input_file = "forward_index.json"
        output_file = "reverse_index.json"

        if os.path.exists(output_file):
            input_file = "new_forward_index.json"

        reverse_index.create_word_index(input_file, output_file)
        barrel.complete_barrels(output_file)
    return render_template('addarticle.html')
if __name__ == '__main__':
    app.run(debug=True)