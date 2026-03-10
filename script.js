const STARTER_DECK = [
  { name: 'Mate con Vecinos', cost: 0, text: '+1 popularidad', popularity: 1 },
  { name: 'Volanteada Barrial', cost: 0, text: '+1 influencia', influence: 1 },
  { name: 'Mate con Vecinos', cost: 0, text: '+1 popularidad', popularity: 1 },
  { name: 'Volanteada Barrial', cost: 0, text: '+1 influencia', influence: 1 },
  { name: 'Microfonazo Local', cost: 0, text: '+1 caja política', treasury: 1 },
  { name: 'Microfonazo Local', cost: 0, text: '+1 caja política', treasury: 1 },
  { name: 'Asamblea de Base', cost: 0, text: '+2 influencia, +1 tensión', influence: 2, unrest: 1 },
  { name: 'Asamblea de Base', cost: 0, text: '+2 influencia, +1 tensión', influence: 2, unrest: 1 }
];

const MARKET = [
  { name: 'Rosca Parlamentaria', cost: 3, text: '+3 influencia', influence: 3 },
  { name: 'Cadena Nacional', cost: 4, text: '+2 popularidad, +1 tensión', popularity: 2, unrest: 1 },
  { name: 'Acuerdo Federal', cost: 5, text: '+2 popularidad, +2 influencia', popularity: 2, influence: 2 },
  { name: 'Operativo Clamor', cost: 6, text: '+4 popularidad', popularity: 4 },
  { name: 'Consultora Amiga', cost: 4, text: '+2 caja política, +1 influencia', treasury: 2, influence: 1 },
  { name: 'Pase de Bloque', cost: 5, text: '+3 influencia, +1 tensión', influence: 3, unrest: 1 },
  { name: 'Pacto de Gobernabilidad', cost: 7, text: '+3 popularidad, -1 tensión', popularity: 3, unrest: -1 }
];

const state = {
  turn: 1,
  popularity: 5,
  unrest: 0,
  treasury: 0,
  influence: 0,
  deck: [],
  discard: [],
  hand: [],
  gameOver: false
};

const ui = {
  turn: document.getElementById('turn'),
  popularity: document.getElementById('popularity'),
  unrest: document.getElementById('unrest'),
  treasury: document.getElementById('treasury'),
  influence: document.getElementById('influence'),
  hand: document.getElementById('hand'),
  market: document.getElementById('market'),
  log: document.getElementById('log'),
  endTurnButton: document.getElementById('endTurnButton'),
  restartButton: document.getElementById('restartButton'),
  cardTemplate: document.getElementById('cardTemplate')
};

function cloneCard(card) {
  return { ...card };
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
}

function addLog(message, className = '') {
  const item = document.createElement('li');
  item.textContent = message;
  if (className) item.classList.add(className);
  ui.log.prepend(item);
}

function drawCards(amount) {
  for (let i = 0; i < amount; i += 1) {
    if (state.deck.length === 0) {
      state.deck = state.discard;
      state.discard = [];
      shuffle(state.deck);
      if (state.deck.length === 0) return;
    }
    state.hand.push(state.deck.pop());
  }
}

function applyCard(card) {
  state.popularity += card.popularity ?? 0;
  state.unrest += card.unrest ?? 0;
  state.treasury += card.treasury ?? 0;
  state.influence += card.influence ?? 0;
  state.popularity = Math.max(0, state.popularity);
  state.unrest = Math.max(0, state.unrest);
  addLog(`Jugaste ${card.name}: ${card.text}`);
}

function playCard(index) {
  if (state.gameOver) return;
  const [card] = state.hand.splice(index, 1);
  applyCard(card);
  state.discard.push(card);
  evaluateEndConditions();
  render();
}

function buyCard(card) {
  if (state.gameOver) return;
  if (state.influence < card.cost) {
    addLog(`No alcanza la influencia para ${card.name}.`, 'bad');
    return;
  }
  state.influence -= card.cost;
  state.discard.push(cloneCard(card));
  addLog(`Compraste ${card.name}.`, 'good');
  render();
}

function endTurn() {
  if (state.gameOver) return;
  state.discard.push(...state.hand);
  state.hand = [];
  state.turn += 1;
  state.influence = 0;
  drawCards(5);
  addLog(`Comienza el turno ${state.turn}.`);
  evaluateEndConditions();
  render();
}

function evaluateEndConditions() {
  if (state.unrest >= 15) {
    state.gameOver = true;
    addLog('La tensión social se desbordó. Perdiste la gobernabilidad.', 'bad');
  } else if (state.turn > 12) {
    state.gameOver = true;
    if (state.popularity >= 20) {
      addLog('¡Ganaste la elección con una campaña aceitada!', 'good');
    } else {
      addLog('Llegó la elección y no alcanzó la popularidad. Derrota.', 'bad');
    }
  }
}

function renderHand() {
  ui.hand.innerHTML = '';
  state.hand.forEach((card, index) => {
    const node = ui.cardTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector('.card-title').textContent = card.name;
    node.querySelector('.card-cost').textContent = 'Costo: -';
    node.querySelector('.card-text').textContent = card.text;
    const button = node.querySelector('.card-action');
    button.textContent = 'Jugar carta';
    button.disabled = state.gameOver;
    button.addEventListener('click', () => playCard(index));
    ui.hand.appendChild(node);
  });
}

function renderMarket() {
  ui.market.innerHTML = '';
  MARKET.forEach((card) => {
    const node = ui.cardTemplate.content.firstElementChild.cloneNode(true);
    node.querySelector('.card-title').textContent = card.name;
    node.querySelector('.card-cost').textContent = `Costo: ${card.cost} influencia`;
    node.querySelector('.card-text').textContent = card.text;
    const button = node.querySelector('.card-action');
    button.textContent = 'Comprar';
    button.disabled = state.gameOver;
    button.addEventListener('click', () => buyCard(card));
    ui.market.appendChild(node);
  });
}

function render() {
  ui.turn.textContent = Math.min(state.turn, 12);
  ui.popularity.textContent = state.popularity;
  ui.unrest.textContent = state.unrest;
  ui.treasury.textContent = state.treasury;
  ui.influence.textContent = state.influence;
  ui.endTurnButton.disabled = state.gameOver;

  renderHand();
  renderMarket();
}

function resetGame() {
  state.turn = 1;
  state.popularity = 5;
  state.unrest = 0;
  state.treasury = 0;
  state.influence = 0;
  state.deck = STARTER_DECK.map(cloneCard);
  state.discard = [];
  state.hand = [];
  state.gameOver = false;
  shuffle(state.deck);
  drawCards(5);
  ui.log.innerHTML = '';
  addLog('Arranca la campaña. Construí tu aparato político.');
  render();
}

ui.endTurnButton.addEventListener('click', endTurn);
ui.restartButton.addEventListener('click', resetGame);

resetGame();
