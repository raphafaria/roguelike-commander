from flask import Flask, jsonify, send_from_directory, abort
import os

app = Flask(__name__, static_folder='.', static_url_path='')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Caminho para as cartas do Raphael
DECKLIST_PATH = os.path.join(BASE_DIR, 'Jogadores', 'Raphael', 'Asset', 'Decklist')
COMMANDER_PATH = os.path.join(BASE_DIR, 'Jogadores', 'Raphael', 'Asset', 'Commander')
RAPHAEL_PATH = os.path.join(BASE_DIR, 'Jogadores', 'Raphael')

@app.route('/')
def index():
    # Página index na raiz roguelike-tools
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/jogadores.html')
def jogadores():
    return send_from_directory(BASE_DIR, 'jogadores.html')

@app.route('/Jogadores/<jogador>/<filename>')
def serve_jogador_html(jogador, filename):
    # Serve arquivos HTML (ou outros) dentro da pasta Jogadores/<jogador>/
    jogador_path = os.path.join(BASE_DIR, 'Jogadores', jogador)
    file_path = os.path.join(jogador_path, filename)
    if os.path.isfile(file_path):
        return send_from_directory(jogador_path, filename)
    else:
        abort(404)

@app.route('/Asset/<path:filename>')
def serve_asset(filename):
    # Serve arquivos na pasta Asset (logo.png e afins) na raiz roguelike-tools
    asset_path = os.path.join(BASE_DIR, 'Asset')
    return send_from_directory(asset_path, filename)

@app.route('/Jogadores/Raphael/Asset/Decklist/<path:filename>')
def serve_decklist_card(filename):
    # Serve as cartas do deck do Raphael
    return send_from_directory(DECKLIST_PATH, filename)

@app.route('/Jogadores/Raphael/Asset/Commander/<path:filename>')
def serve_commander_card(filename):
    # Serve imagens dos comandantes do Raphael
    return send_from_directory(COMMANDER_PATH, filename)

@app.route('/cartas')
def listar_cartas():
    # Lista as cartas jpg/png na pasta do deck do Raphael
    try:
        arquivos = sorted([
            f for f in os.listdir(DECKLIST_PATH)
            if f.lower().endswith(('.jpg', '.png'))
        ])
        return jsonify(arquivos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/<path:path>')
def catch_all(path):
    # Tenta servir qualquer arquivo estático na raiz ou subpastas
    abs_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(abs_path):
        # Serve arquivo estático se existir
        dir_path = os.path.dirname(abs_path)
        filename = os.path.basename(abs_path)
        return send_from_directory(dir_path, filename)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
