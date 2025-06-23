from flask import Flask, jsonify, send_from_directory, abort, make_response, send_file
import os

app = Flask(__name__, static_folder='.', static_url_path='')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Função genérica para servir imagens com cache
def send_cached_image(path, filename, max_age=86400):
    full_path = os.path.join(path, filename)
    if not os.path.isfile(full_path):
        abort(404)
    response = make_response(send_file(full_path))
    response.headers['Cache-Control'] = f'public, max-age={max_age}'
    return response

# Página inicial
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

@app.route('/jogadores.html')
def jogadores():
    return send_from_directory(BASE_DIR, 'jogadores.html')

# Serve páginas dos jogadores
@app.route('/Jogadores/<jogador>/<filename>')
def serve_jogador_page(jogador, filename):
    jogador_path = os.path.join(BASE_DIR, 'Jogadores', jogador)
    full_path = os.path.join(jogador_path, filename)
    if os.path.isfile(full_path):
        return send_from_directory(jogador_path, filename)
    else:
        abort(404)

# Serve imagens: Commander, Decklist, Reliquias de qualquer jogador
@app.route('/Jogadores/<jogador>/Asset/<folder>/<filename>')
def serve_player_image(jogador, folder, filename):
    path = os.path.join(BASE_DIR, 'Jogadores', jogador, 'Asset', folder)
    return send_cached_image(path, filename)

# Serve imagem da pasta Asset raiz
@app.route('/Asset/<filename>')
def serve_global_asset(filename):
    path = os.path.join(BASE_DIR, 'Asset')
    return send_cached_image(path, filename)

# Endpoint dinâmico de decklist (usado por decklist.html para Raphael)
@app.route('/cartas')
def cartas():
    deck_path = os.path.join(BASE_DIR, 'Jogadores', 'Raphael', 'Asset', 'Decklist')
    try:
        arquivos = sorted([
            f for f in os.listdir(deck_path)
            if f.lower().endswith(('.jpg', '.png'))
        ])
        return jsonify(arquivos)
    except Exception:
        abort(500)

# Rota genérica para arquivos estáticos que não caem nas outras rotas
@app.route('/<path:path>')
def catch_all(path):
    full_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(full_path):
        return send_from_directory(BASE_DIR, path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
