from flask import Flask, jsonify, send_from_directory, abort
import os

app = Flask(__name__, static_folder='.', static_url_path='')

BASE_DIR = os.getcwd()
JOGADORES_PATH = os.path.join(BASE_DIR, 'Jogadores')

# Serve index.html da raiz
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# Serve jogadores.html da raiz
@app.route('/jogadores.html')
def jogadores():
    return send_from_directory('.', 'jogadores.html')

# Serve arquivos dentro de /Jogadores/{jogador}/
@app.route('/jogadores/<jogador>/<path:filename>')
def serve_jogador_file(jogador, filename):
    jogador_dir = os.path.join(JOGADORES_PATH, jogador)
    if os.path.isdir(jogador_dir):
        # Prevenir path traversal
        full_path = os.path.normpath(os.path.join(jogador_dir, filename))
        if full_path.startswith(jogador_dir) and os.path.isfile(full_path):
            return send_from_directory(jogador_dir, filename)
    abort(404)

# Serve as cartas do deck do Raphael
@app.route('/Jogadores/Raphael/Asset/Decklist/<path:filename>')
def serve_decklist_card(filename):
    deck_path = os.path.join(JOGADORES_PATH, 'Raphael', 'Asset', 'Decklist')
    return send_from_directory(deck_path, filename)

# Serve as cartas do comandante do Raphael
@app.route('/Jogadores/Raphael/Asset/Commander/<path:filename>')
def serve_commander_card(filename):
    commander_path = os.path.join(JOGADORES_PATH, 'Raphael', 'Asset', 'Commander')
    return send_from_directory(commander_path, filename)

# Catch-all para servir outros arquivos estáticos na raiz ou subpastas
@app.route('/<path:path>')
def serve_static(path):
    static_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(static_path):
        return send_from_directory(BASE_DIR, path)
    abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
