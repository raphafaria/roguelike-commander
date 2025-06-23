from flask import Flask, jsonify, send_from_directory, abort
import os

app = Flask(__name__, static_folder='.', static_url_path='')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminho para as cartas do Raphael
DECK_PATH = os.path.join(BASE_DIR, "Jogadores", "Raphael", "Asset", "Decklist")
COMMANDER_PATH = os.path.join(BASE_DIR, "Jogadores", "Raphael", "Asset", "Commander")

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/jogadores.html')
def jogadores():
    return send_from_directory(BASE_DIR, 'jogadores.html')

# Serve arquivos dentro da pasta Jogadores/<jogador>
@app.route('/jogadores/<jogador>/<filename>')
@app.route('/Jogadores/<jogador>/<filename>')
def serve_jogador_html(jogador, filename):
    jogador_path = os.path.join(BASE_DIR, 'Jogadores', jogador)
    file_path = os.path.join(jogador_path, filename)
    if os.path.isfile(file_path):
        return send_from_directory(jogador_path, filename)
    else:
        abort(404)

# Endpoint para lista JSON das cartas do deck do Raphael
@app.route('/cartas')
def cartas():
    try:
        arquivos = sorted([
            f for f in os.listdir(DECK_PATH)
            if f.lower().endswith(('.jpg', '.png'))
        ])
        return jsonify(arquivos)
    except Exception:
        abort(500)

# Serve imagens das cartas do decklist
@app.route('/Asset/Decklist/<path:filename>')
def serve_decklist_card(filename):
    return send_from_directory(DECK_PATH, filename)

# Serve imagens dos comandantes
@app.route('/Asset/Commander/<path:filename>')
def serve_commander(filename):
    return send_from_directory(COMMANDER_PATH, filename)

# Serve outros arquivos estáticos na raiz do projeto, incluindo a pasta Asset e node_modules
@app.route('/<path:path>')
def catch_all(path):
    full_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(full_path):
        return send_from_directory(BASE_DIR, path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
