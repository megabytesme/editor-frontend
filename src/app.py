from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid
import json
import os

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)
DATA_FILE = 'saved_texts.json'

def read_saved_texts():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def write_saved_texts(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

saved_texts = read_saved_texts()

@app.route('/save', methods=['POST'])
def save_text():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    identifier = str(uuid.uuid4())
    saved_texts[identifier] = text
    write_saved_texts(saved_texts)

    return jsonify({'identifier': identifier}), 201

@app.route('/recall/<identifier>', methods=['GET'])
def recall_text(identifier):
    text = saved_texts.get(identifier)
    if text:
        return jsonify({'text': text}), 200
    else:
        return jsonify({'error': 'Text not found'}), 404

@app.route('/config.json')
def serve_config():
    return send_from_directory(app.static_folder, 'config.json')

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
