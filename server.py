from flask import Flask, send_from_directory, abort, make_response
import os
from datetime import timedelta

app = Flask(__name__, static_folder='.', static_url_path='')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Função para servir arquivos com cache
def send_static_with_cache(directory, filename):
    response = make_response(send_from_directory(directory, filename))
    # Cache por 30 dias
    response.cache_control.max_age = 30 * 24 * 60 * 60
    response.cache_control.public = True
    return response

@app.route('/')
def index():
    return send_static_with_cache(BASE_DIR, 'index.html')

@app.route('/jogadores.html')
def jogadores():
    return send_static_with_cache(BASE_DIR, 'jogadores.html')

@app.route('/jogadores/<jogador>/<filename>')
@app.route('/Jogadores/<jogador>/<filename>')
def serve_jogador_html(jogador, filename):
    jogador_path = os.path.join(BASE_DIR, 'Jogadores', jogador)
    file_path = os.path.join(jogador_path, filename)
    if os.path.isfile(file_path):
        return send_static_with_cache(jogador_path, filename)
    else:
        abort(404)

@app.route('/<path:path>')
def catch_all(path):
    full_path = os.path.join(BASE_DIR, path)
    if os.path.isfile(full_path):
        return send_static_with_cache(BASE_DIR, path)
    else:
        abort(404)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
