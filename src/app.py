from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import uuid

app = Flask(__name__, static_url_path='', static_folder='static')
CORS(app)
saved_texts = {}

@app.route('/save', methods=['POST'])
def save_text():
    text = request.json.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    identifier = str(uuid.uuid4())
    saved_texts[identifier] = text

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
