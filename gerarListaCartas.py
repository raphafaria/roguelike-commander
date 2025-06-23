import requests
import time

cartas = []
url = "https://api.scryfall.com/cards/search?order=edhrec&dir=asc&game=paper&q=format%3Aedh"

print("🔍 Buscando cartas do Scryfall (ordenadas por popularidade no Commander)...")

while url and len(cartas) < 2000:
    res = requests.get(url)
    data = res.json()

    for card in data["data"]:
        nome = card["name"]
        if nome not in cartas:
            cartas.append(nome)

    print(f"📦 Total atual: {len(cartas)} cartas")
    url = data.get("next_page", None)
    time.sleep(0.1)

with open("listaCartas.txt", "w", encoding="utf-8") as f:
    for nome in cartas[:2000]:
        f.write(nome + "\n")

print("✅ listaCartas.txt gerado com sucesso!")
