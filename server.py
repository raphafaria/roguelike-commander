from flask import Flask, jsonify, send_from_directory, abort, make_response, send_file
import os

app = Flask(__name__, static_folder='.', static_url_path='')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Função genérica com cache para qualquer imagem
def send_cached_image(directory, filename, max_age=86400):
    file_path = os.path.join(directory, filename)
    if not os.path.isfile(file_path):
        abort(404)
    response = make_response(send_file(file_path))
    response.headers['Cache-Control'] = f'public, max-age={max_age}'
    return response

@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/jogadores.html')
def jogadores():
    return send_from_directory(BASE_DIR, 'jogadores.html')

@app.route('/jogadores/<jogador>/<filename>')
@app.route('/Jogadores/<jogador>/<filename>')
def serve_jogador_html(jogador, filename):
    jogador_path = os.path.join(BASE_DIR, 'Jogadores', jogador)
    file_path = os.path.join(jogador_path, filename)
    if os.path.isfile(file_path):
        return send_from_directory(jogador_path, filename)
    else:
        abort(404)

@app.route('/cartas')
def cartas():
    try:
        deck_path = os.path.join(BASE_DIR, "Jogadores", "Raphael", "Asset", "Decklist")
        arquivos = sorted([
            f for f in os.listdir(deck_path)
            if f.lower().endswith(('.jpg', '.png'))
        ])
        return jsonify(arquivos)
    except Exception:
        abort(500)

# ===============================
# ROTAS DE IMAGENS COM CACHE
# ===============================

@app.route('/Asset/<path:filename>')
def serve_root_asset_image(filename):
    path = os.path.join(BASE_DIR, 'Asset')
    return send_cached_image(path, filename)

@app.route('/Jogadores/<jogador>/Asset/<folder>/<filename>')
def serve_jogador_asset_image(jogador, folder, filename):
    path = os.path.join(BASE_DIR, 'Jogadores', jogador, 'Asset', folder)
    return send_cached_image(path, filename)

# Ex: /Jogadores/Raphael/Asset/Decklist/nome.jpg

# ===============================
# CATCH-ALL PARA OUTROS ARQUIVOS
# ===============================
@app.route('/<path:path>')
def catch_all(path):
    full_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(full_path):
        return send_from_directory(BASE_DIR, path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
