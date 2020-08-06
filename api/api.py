from flask import Flask, jsonify, request, redirect, url_for
from elasticsearch import Elasticsearch

import time
time.sleep(12)

app = Flask(__name__)
app.config["DEBUG"] = True

ES_HOST = 'elasticsearch'
ES_PORT = 9200

es = Elasticsearch(host=ES_HOST, port=ES_PORT)
# es = Elasticsearch(hosts=[{"host":'elasticsearch'}])

if not es.indices.exists(index="book-index"):
    es.indices.create(index="book-index")

def create(book_info):
    res = es.index(index="book-index", body=book_info)
    if "result" in res and res["result"] == "created":
        return res["_id"]
    return False

def read(book_id):
    res = es.get(index="book-index", id=book_id)
    if "found" in res and "_source" in res and res["_source"]:
        return res["_source"]
    return None

def update(book_info, book_id):
    res = es.index(index="book-index", id=book_id, body=book_info)
    if "result" in res and res["result"] == "updated":
        return True
    return False

def delete(book_id):
    res = es.delete(index="book-index", id=book_id)
    if "found" in res and "result" in res and res["result" == "deleted"]:
        return True
    return False

def search():
    res = es.search(index="book-index", body={"query": {"match_all": {}}})
    books = []
    for hit in res['hits']['hits']:
        hit["_source"]["id"] = hit["_id"]
        books.append(hit["_source"])
    return books

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404

@app.errorhandler(400)
def bad_request(e):
    return "<h1>400</h1><p>Bad JSON data.</p>", 400

@app.route('/', methods=['GET'])
def home():
    return '''  <h1>Book API</h1>
                <p>A prototype API for distant reading of science fiction novels.</p>'''

@app.route('/api/books', methods=['GET', 'POST'])
def book_list():

    if request.method == 'GET':
        result = search()
        return jsonify(result)
    else:
        data = request.get_json() or {}
        if 'title' not in data or 'author' not in data:
            return bad_request(400)
        create(data)
        return redirect(url_for('book_list'))


@app.route('/api/books/<id>', methods=['GET', 'POST'])
def book_page(id):

    if request.method == 'GET':
        if not id:
            return page_not_found(404)
        result = read(id)
        return jsonify(result)
    else:
        data = request.get_json() or {}
        if 'title' not in data or 'author' not in data:
            return bad_request(400)
        update(data, id)
        return redirect(url_for('book_list'))
    

@app.route('/api/books/<id>', methods=['DELETE'])
def delete_book(id):
    
    result = read(id)
    if not result == None:
        delete(id)
    return redirect(url_for('book_list'))


if __name__ == "__main__":
    app.run()