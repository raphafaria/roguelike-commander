const fs = require('fs');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

const listaCartas = fs.readFileSync('listaCartas.txt', 'utf-8').split('\n').filter(Boolean);

async function obterInfoCarta(nome) {
  const res = await fetch(`https://api.scryfall.com/cards/named?exact=${encodeURIComponent(nome)}`);
  const json = await res.json();

  // Lida com cartas dupla face
  const tipo = json.type_line || json.card_faces?.[0]?.type_line || "Desconhecido";
  const cores = json.colors || json.card_faces?.[0]?.colors || [];

  return {
    nome: json.name,
    tipo: tipo,
    cores: cores,
  };
}

(async () => {
  const resultado = [];

  for (let i = 0; i < listaCartas.length; i++) {
    const nome = listaCartas[i];
    const info = await obterInfoCarta(nome);
    info.popularidade = i + 1;

    if (i < 100) info.raridade = "Diamante";
    else if (i < 300) info.raridade = "Ouro";
    else if (i < 1000) info.raridade = "Prata";
    else info.raridade = "Bronze";

    console.log(`🔄 ${i + 1}/${listaCartas.length} - ${nome} [${info.raridade}]`);
    resultado.push(info);
  }

  fs.writeFileSync('cards.json', JSON.stringify(resultado, null, 2));
  console.log("✅ cards.json gerado com sucesso!");
})();
