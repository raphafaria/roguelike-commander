from PIL import Image
import os

# Caminho base do projeto
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
JOGADORES_DIR = os.path.join(BASE_DIR, "Jogadores")

# Fatores de redimensionamento
ESCALA = 0.3  # 30%

def redimensionar_imagem(caminho_imagem):
    try:
        with Image.open(caminho_imagem) as img:
            nova_largura = int(img.width * ESCALA)
            nova_altura = int(img.height * ESCALA)
            imagem_redimensionada = img.resize((nova_largura, nova_altura), Image.LANCZOS)
            imagem_redimensionada.save(caminho_imagem, optimize=True)
            print(f"[OK] Redimensionado: {caminho_imagem}")
    except Exception as e:
        print(f"[ERRO] {caminho_imagem}: {e}")

def redimensionar_todas_as_decklists():
    for jogador in os.listdir(JOGADORES_DIR):
        pasta_decklist = os.path.join(JOGADORES_DIR, jogador, "Asset", "Decklist")
        if os.path.isdir(pasta_decklist):
            for arquivo in os.listdir(pasta_decklist):
                if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
                    caminho_completo = os.path.join(pasta_decklist, arquivo)
                    redimensionar_imagem(caminho_completo)

if __name__ == "__main__":
    redimensionar_todas_as_decklists()
