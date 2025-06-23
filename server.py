from flask import Flask, send_from_directory, abort, make_response, request, jsonify
import os
from datetime import datetime, timedelta
import json

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

# Novo endpoint para receber escolha de carta ou crédito
@app.route('/api/registrar-booster', methods=['POST'])
def registrar_booster():
    data = request.get_json()
    jogador = data.get("jogador")
    booster = data.get("booster")
    cartas = data.get("cartas")
    escolhida = data.get("escolhida")  # nome da carta ou "LIGA_COIN"
    quantidade = data.get("quantidade")  # só se for LIGA_COIN
    agora = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if not jogador or not booster or not cartas:
        return jsonify({"status": "erro", "mensagem": "Dados incompletos."}), 400

    # Pasta do jogador
    pasta = os.path.join(BASE_DIR, 'Jogadores', jogador, 'Comandos')
    os.makedirs(pasta, exist_ok=True)
    historico_path = os.path.join(pasta, 'historico_boosters.json')

    try:
        if os.path.exists(historico_path):
            with open(historico_path, 'r', encoding='utf-8') as f:
                historico = json.load(f)
        else:
            historico = []

        registro = {
            "data": agora,
            "tipo": booster,
            "cartas": cartas,
            "escolhida": escolhida,
        }

        if escolhida == "LIGA_COIN":
            registro["quantidade"] = quantidade

        historico.append(registro)

        with open(historico_path, 'w', encoding='utf-8') as f:
            json.dump(historico, f, indent=2, ensure_ascii=False)

        return jsonify({"status": "ok"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
