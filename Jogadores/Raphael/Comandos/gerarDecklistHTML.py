import os

decklist_path = os.path.join("..", "Asset", "Decklist")
output_path = os.path.join("..", "decklist.html")

# Cabeçalho do HTML
html_top = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Decklist - Raphael</title>
  <style>
    body { background-color: #121212; color: #f0e6d2; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 0; padding: 2rem; text-align: center; }
    h1 { font-size: 2rem; color: #ffd700; margin-bottom: 1rem; }
    .top-nav { margin-bottom: 2rem; }
    .top-nav a { background-color: #222; border: 1px solid #555; border-radius: 8px; padding: 0.5rem 1.5rem; color: #f0e6d2; text-decoration: none; font-size: 1rem; transition: background 0.3s; }
    .top-nav a:hover { background-color: #f0e6d2; color: #121212; }
    .deck-section { margin-bottom: 3rem; }
    .deck-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 1.5rem; }
    .card { width: 223px; border-radius: 8px; overflow: hidden; box-shadow: 0 0 10px #000; }
    .card img { width: 100%; display: block; }
    .section-title { font-size: 1.5rem; color: #ffcc00; margin-bottom: 1.5rem; }
  </style>
</head>
<body>
  <h1>Decklist - Raphael</h1>
  <div class="top-nav">
    <a href="raphael.html">⬅ Voltar para Perfil</a>
  </div>
  <div class="deck-section">
    <div class="section-title">Comandante(s)</div>
    <div class="deck-container">
      <div class="card"><img src="Asset/Commander/Atla Palani, Nest Tender.jpg" alt="Atla Palani, Nest Tender" loading="lazy" /></div>
      <div class="card"><img src="Asset/Commander/Piper Wright, Publick Reporter.png" alt="Piper Wright, Publick Reporter" loading="lazy" /></div>
    </div>
  </div>
  <div class="deck-section">
    <div class="section-title">Cartas do Deck</div>
    <div class="deck-container">
"""

# Rodapé do HTML
html_bottom = """
    </div>
  </div>
</body>
</html>"""

# Gera blocos de imagem
blocos = []
for filename in sorted(os.listdir(decklist_path)):
    if filename.lower().endswith(('.jpg', '.png')):
        path = f'Asset/Decklist/{filename}'
        alt = os.path.splitext(filename)[0]
        blocos.append(f'      <div class="card"><img src="{path}" alt="{alt}" loading="lazy" /></div>')

# Escreve o HTML final
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html_top)
    f.write("\n".join(blocos))
    f.write(html_bottom)

print("✅ decklist.html atualizado com sucesso!")
