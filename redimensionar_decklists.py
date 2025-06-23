from PIL import Image
import os

# Tamanho alvo
LARGURA = 450
ALTURA = 630

# Caminho base
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JOGADORES_DIR = os.path.join(BASE_DIR, "Jogadores")

def redimensionar_imagem(caminho_imagem):
    try:
        with Image.open(caminho_imagem) as img:
            imagem_redimensionada = img.resize((LARGURA, ALTURA), Image.LANCZOS)
            imagem_redimensionada.save(caminho_imagem, optimize=True)
            print(f"[OK] Redimensionado: {caminho_imagem}")
    except Exception as e:
        print(f"[ERRO] {caminho_imagem}: {e}")

def percorrer_e_redimensionar():
    for root, dirs, files in os.walk(JOGADORES_DIR):
        for nome_arquivo in files:
            if nome_arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                caminho_completo = os.path.join(root, nome_arquivo)
                redimensionar_imagem(caminho_completo)

if __name__ == "__main__":
    percorrer_e_redimensionar()
