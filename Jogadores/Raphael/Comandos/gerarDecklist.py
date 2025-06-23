import os
import json

# Pasta das cartas (relativa ao script)
caminho = "../Asset/Decklist"

# Lista os arquivos .jpg e .png
arquivos = sorted([f for f in os.listdir(caminho) if f.lower().endswith(('.jpg', '.png'))])

# Gera o JSON
with open("decklist.json", "w", encoding="utf-8") as f:
    json.dump(arquivos, f, ensure_ascii=False, indent=2)

print(f"decklist.json gerado com {len(arquivos)} cartas.")
