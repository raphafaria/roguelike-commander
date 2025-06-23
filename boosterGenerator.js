const fs = require('fs');
const fetch = (...args) => import('node-fetch').then(({default: fetch}) => fetch(...args));

// === Carrega o cards.json (com 2000 cartas populares) ===
const todasAsCartas = JSON.parse(fs.readFileSync('cards.json', 'utf-8'));

// === Separa cartas por raridade ===
const cartasPorRaridade = {
  Diamante: [],
  Ouro: [],
  Prata: [],
  Bronze: [],
};

for (const carta of todasAsCartas) {
  if (cartasPorRaridade[carta.raridade]) {
    cartasPorRaridade[carta.raridade].push(carta);
  }
}

// === Função para sortear cartas únicas ===
function sortearCartas(array, qtd) {
  const sorteadas = [];
  const indicesSorteados = new Set();

  while (sorteadas.length < qtd && indicesSorteados.size < array.length) {
    const i = Math.floor(Math.random() * array.length);
    if (!indicesSorteados.has(i)) {
      sorteadas.push(array[i]);
      indicesSorteados.add(i);
    }
  }

  return sorteadas;
}

// === Booster de Vitorioso (5 cartas) ===
function gerarBoosterVitorioso() {
  return [
    ...sortearCartas(cartasPorRaridade.Diamante, 1),
    ...sortearCartas(cartasPorRaridade.Ouro, 1),
    ...sortearCartas(cartasPorRaridade.Prata, 1),
    ...sortearCartas(cartasPorRaridade.Bronze, 2),
  ];
}

// === Booster de Consolação (3 cartas) ===
function gerarBoosterConsolacao() {
  const diamanteOuOuro = Math.random() < 0.2
    ? sortearCartas(cartasPorRaridade.Diamante, 1)
    : sortearCartas(cartasPorRaridade.Ouro, 1);

  return [
    ...sortearCartas(cartasPorRaridade.Prata, 1),
    ...sortearCartas(cartasPorRaridade.Bronze, 1),
    ...diamanteOuOuro,
  ];
}

// === Omnibooster (7 cartas aleatórias do Scryfall) ===
async function gerarOmnibooster() {
  const booster = [];

  for (let i = 0; i < 7; i++) {
    const res = await fetch('https://api.scryfall.com/cards/random?q=format:commander');
    const data = await res.json();

    booster.push({
      nome: data.name,
      raridade: data.rarity.charAt(0).toUpperCase() + data.rarity.slice(1), // ex: 'rare' → 'Rare'
    });
  }

  return booster;
}

// === Exibir booster no terminal ===
function mostrarBooster(nome, cartas) {
  console.log(`\n📦 ${nome}:\n`);
  cartas.forEach((carta, i) => {
    console.log(`${i + 1}. ${carta.nome} [${carta.raridade}]`);
  });
  console.log('\n----------------------------------');
}

// === Menu de seleção ===
console.log('\nEscolha o tipo de booster:');
console.log('1 - Vitorioso (5 cartas)');
console.log('2 - Consolação (3 cartas)');
console.log('3 - Omnibooster (7 cartas aleatórias da Scryfall)');

const readline = require('readline').createInterface({
  input: process.stdin,
  output: process.stdout,
});

readline.question('\nDigite o número do booster desejado: ', async (opcao) => {
  let booster;

  if (opcao === '1') {
    booster = gerarBoosterVitorioso();
    mostrarBooster('Booster de Vitorioso', booster);
  } else if (opcao === '2') {
    booster = gerarBoosterConsolacao();
    mostrarBooster('Booster de Consolação', booster);
  } else if (opcao === '3') {
    booster = await gerarOmnibooster();
    mostrarBooster('Omnibooster (via Scryfall)', booster);
  } else {
    console.log('❌ Opção inválida.');
  }

  readline.close();
});
