from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Caminho para as cartas do Raphael
DECK_PATH = os.path.join("Jogadores", "Raphael", "Asset", "Decklist")

@app.route('/')
def index():
    return send_from_directory('Jogadores/Raphael', 'decklist.html')

@app.route('/cartas')
def cartas():
    arquivos = sorted([
        f for f in os.listdir(DECK_PATH)
        if f.lower().endswith(('.jpg', '.png'))
    ])
    return jsonify(arquivos)

@app.route('/Asset/Decklist/<path:filename>')
def serve_card(filename):
    return send_from_directory(DECK_PATH, filename)

@app.route('/Asset/Commander/<path:filename>')
def serve_commander(filename):
    commander_path = os.path.join("Jogadores", "Raphael", "Asset", "Commander")
    return send_from_directory(commander_path, filename)

@app.route('/<path:path>')
def catch_all(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
