from flask import Flask, request
from resources import EntryManager, Entry

app = Flask(__name__)
FOLDER = './tmp/'


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/entries/")
def get_entries():
    print(FOLDER)
    entry_manager = EntryManager(FOLDER).load()
    res = list()
    for em in entry_manager.entries:
        res.append(em.json())
    return res


@app.route('/api/save_entries/', methods=['POST'])
def save_entries():
    entry_manager = EntryManager(FOLDER)
    content = request.get_json()
    for entry in content:
        entry_manager.entries.append(Entry.from_json(entry))
    entry_manager.save()
    return {'status': 'success'}


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)