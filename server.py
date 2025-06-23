from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

# Caminhos principais
JOGADORES_PATH = 'Jogadores'
RAPHAEL_PATH = os.path.join(JOGADORES_PATH, 'Raphael')
DECKLIST_PATH = os.path.join(RAPHAEL_PATH, 'Asset', 'Decklist')
COMMANDER_PATH = os.path.join(RAPHAEL_PATH, 'Asset', 'Commander')

@app.route('/')
def index():
    # Serve a página principal do projeto (index.html na raiz roguelike-tools)
    return send_from_directory('.', 'index.html')

@app.route('/cartas')
def listar_cartas():
    try:
        arquivos = sorted([
            f for f in os.listdir(DECKLIST_PATH)
            if f.lower().endswith(('.jpg', '.png'))
        ])
        return jsonify(arquivos)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/Asset/Decklist/<path:filename>')
def serve_decklist(filename):
    return send_from_directory(DECKLIST_PATH, filename)

@app.route('/Asset/Commander/<path:filename>')
def serve_commander(filename):
    return send_from_directory(COMMANDER_PATH, filename)

@app.route('/decklist.html')
def serve_decklist_html():
    return send_from_directory(RAPHAEL_PATH, 'decklist.html')

@app.route('/raphael.html')
def serve_raphael_html():
    return send_from_directory(RAPHAEL_PATH, 'raphael.html')

# Serve outros arquivos estáticos (css, js, imagens da raiz, etc)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

if __name__ == '__main__':
    # Executa no host 0.0.0.0 e porta 5000, modo debug ligado para facilitar testes
    app.run(host='0.0.0.0', port=5000, debug=True)
