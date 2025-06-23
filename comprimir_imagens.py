import os
from PIL import Image

# Caminho para a pasta de imagens do deck
PASTA = os.path.join("Jogadores", "Raphael", "Asset", "Decklist")

# Nível de qualidade (0 a 100) para JPEG
QUALIDADE = 75

def comprimir_imagens():
    for arquivo in os.listdir(PASTA):
        caminho = os.path.join(PASTA, arquivo)

        if not os.path.isfile(caminho):
            continue

        nome, extensao = os.path.splitext(arquivo)
        extensao = extensao.lower()

        if extensao in [".jpg", ".jpeg"]:
            try:
                img = Image.open(caminho)
                img.save(caminho, "JPEG", optimize=True, quality=QUALIDADE)
                print(f"Comprimido: {arquivo}")
            except Exception as e:
                print(f"Erro em {arquivo}: {e}")

        elif extensao == ".png":
            try:
                img = Image.open(caminho)
                img.save(caminho, "PNG", optimize=True)
                print(f"Comprimido: {arquivo}")
            except Exception as e:
                print(f"Erro em {arquivo}: {e}")

if __name__ == "__main__":
    comprimir_imagens()
