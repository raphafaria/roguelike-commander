from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Caminhos principais
BASE_DIR = os.path.abspath('.')  # raiz do projeto (roguelike-tools)
RAPHAEL_DIR = os.path.join(BASE_DIR, 'Jogadores', 'Raphael')

# Serve o index.html do site principal
@app.route('/')
def index():
    return send_from_directory(BASE_DIR, 'index.html')

# Serve qualquer arquivo estático da raiz (css, js, img, etc)
@app.route('/<path:path>')
def static_files(path):
    # Primeiro tenta servir da raiz
    arquivo = os.path.join(BASE_DIR, path)
    if os.path.isfile(arquivo):
        return send_from_directory(BASE_DIR, path)
    # Depois tenta servir da pasta do Raphael (ex: Jogadores/Raphael/...)
    arquivo_raphael = os.path.join(RAPHAEL_DIR, path)
    if os.path.isfile(arquivo_raphael):
        return send_from_directory(RAPHAEL_DIR, path)
    # Se não achar, retorna 404 simples
    return "Arquivo não encontrado", 404

# Endpoint para listar cartas (json) - opcional se quiser API dedicada
@app.route('/cartas')
def cartas():
    deck_path = os.path.join(RAPHAEL_DIR, 'Asset', 'Decklist')
    arquivos = sorted([
        f for f in os.listdir(deck_path)
        if f.lower().endswith(('.jpg', '.png'))
    ])
    return {"cartas": arquivos}

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
