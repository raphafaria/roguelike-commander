import os
from PIL import Image

# Caminho raiz do seu projeto (ajuste se necessário)
PROJECT_ROOT = "./roguelike-tools"

# Qualidade da imagem compactada (1-95), 85 é um bom equilíbrio
QUALITY = 85

# Formatos aceitos
EXTENSIONS = (".jpg", ".jpeg", ".png")

def compress_image(file_path):
    try:
        img = Image.open(file_path)
        # Converter para RGB se PNG for com transparência, pois JPEG não suporta alfa
        if img.mode in ("RGBA", "LA"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])  # 3 é canal alpha
            img = background
        else:
            img = img.convert("RGB")

        # Salvar compactado, sobrescrevendo original
        img.save(file_path, optimize=True, quality=QUALITY)
        print(f"Compactado: {file_path}")
    except Exception as e:
        print(f"Erro ao compactar {file_path}: {e}")

def walk_and_compress(root_dir):
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower().endswith(EXTENSIONS):
                full_path = os.path.join(dirpath, filename)
                compress_image(full_path)

if __name__ == "__main__":
    print(f"Iniciando compressão das imagens na pasta {PROJECT_ROOT}")
    walk_and_compress(PROJECT_ROOT)
    print("Compressão finalizada.")
