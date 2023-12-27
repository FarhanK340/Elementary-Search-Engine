from flask import Flask, render_template, request
import searching

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = searching.query_search(query.lower())
    return render_template('results.html', query=query, results=results)

@app.route('/add')
def add_article():
    return render_template('addarticle.html')

if __name__ == '__main__':
    app.run(debug=True)