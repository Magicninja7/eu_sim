const STATS = ['economy', 'security', 'people', 'technology'];
const ICONS = {
  economy: '€',
  security: '⚔',
  people: '☺',
  technology: '⌁'
};

const questions = [
  buildQuestion('Criminality is on the rise!', 'Fund surveillance AI systems', [-10, 30, -40, 20], 'Increase police presence', [-20, 10, -10, 0]),
  buildQuestion('The economy is struggling!', 'Invest in infrastructure', [10, -10, 10, 10], 'Cut taxes', [-20, -10, 20, -10]),
  buildQuestion('Technology development is stagnant!', 'Fund research grants', [-10, 10, 10, 20], 'Encourage private sector innovation', [0, -10, 5, 30]),
  buildQuestion('Public health is overloaded!', 'Build more hospitals', [-30, 10, 20, 10], 'Promote preventive care', [-10, 0, 10, 0]),
  buildQuestion('Energy prices spike!', 'Do nothing', [0, 0, -40, 0], 'Subsidize households', [-30, 10, 20, 0]),
  buildQuestion('Big companies create a bad influence on people', 'Regulate them!!!!', [-20, 10, 20, -20], 'Not our problem', [20, -10, -20, 10]),
  buildQuestion('Big bad country wants to attack us!', 'Increase military spending', [-20, 30, -20, 10], 'Appease them', [10, -20, -20, 10]),
  buildQuestion('Memeber state breaking human rights!', 'Impose sanctions', [-10, 0, 20, 0], 'Ignore it', [10, 0, -20, 0]),
  buildQuestion('Foreign-funded media outlets spreading misinformation!', 'Ban them', [0, 20, -10, 0], 'Informational campaign', [0, -20, 10, 0]),
  buildQuestion('Startups leave; too much regulations!', "Didn't need them anyway", [-20, 0, 10, 10], 'Ease regulation', [10, -10, -10, 10]),
  buildQuestion('Agining population!', 'Raise retirement age', [10, 0, -20, 0], 'Do nothing', [-20, 0, 10, 0]),
  buildQuestion('Too much dependency on foreign sources of electricity!', 'Diversify sources', [-10, 10, 10, 0], 'Do nothing', [0, 0, 0, 0]),
  buildQuestion('Foreign surveillance drone crashes', 'Put sanctions on the country!', [-10, 10, 10, 0], 'Invest in radar/AA systems', [-20, 20, 10, 0]),
  buildQuestion('Floods!', 'Limit environmental impact, invest in green energy', [-20, -10, 20, 10], 'Do nothing', [20, -10, -20, 0]),
  buildQuestion('New revolutionary technology!', 'Invest!!!!!!!', [10, 10, 10, 10], 'Leave to private sector', [20, -10, -10, 20]),
  buildQuestion('Humanitarian crisis in the Middle East!', 'Provide aid to the region', [-10, 0, -10, 0], 'Allow immigration', [10, -30, 10, 0]),
  buildQuestion('Civilian plane shot down over foreign country!', 'Ask for apology', [0, -10, 5, 0], 'Sanctions', [-20, 5, 10, 0]),
  buildQuestion('Foreign drone incursion!', 'Act of aggression! (militarise)', [-30, 20, 30, 0], 'Resolve issue diplomatically', [0, -10, 5, 0]),
  buildQuestion('Housing prices skyrocket!', 'Its the students, tourists & migrants!!!!', [-20, 5, 20, -20], 'Exponentially tax ownership of 3+ housing spaces', [10, 0, -10, 0]),
  buildQuestion('Push through chat control?', 'Yes', [0, 20, -20, 0], 'No', [0, -10, 10, 0]),
  buildQuestion('Cyberattack shuts down major bank!', 'Invest heavily in recovery', [-20, 20, 10, 0], 'Let it stabilise naturally', [0, 0, -20, 0]),
  buildQuestion('Heatwave causes crops to die!!', 'Subsidize farmers', [-20, 0, 20, 0], 'Do nothing', [10, 0, -20, 0]),
  buildQuestion('Internet cables severed by foreign ship!', 'Take over said ship & input sanctions', [-20, 20, 10, 0], 'Appease and resolve diplomatically', [20, -10, 0, 0]),
  buildQuestion('Strategic ally commits war crimes!', 'Denounce & sanctions', [-10, -10, 20, 0], 'Do nothing', [10, 10, -20, 0]),
  buildQuestion('Protests block cities!', 'Crackdown', [10, 0, -40, 0], 'Try to appease', [-20, 0, 10, 0]),
  buildQuestion('Mass disinformation during election campaign!', 'Crack down on the posts', [-10, 10, -10, 0], 'Do nothing', [0, -20, 10, 0]),
  buildQuestion('Foreign power imposes tarrifs!', 'Retaliate back with tarrifs!', [-30, 10, 10, 0], 'Accept tarrifs', [-10, 0, -10, 0]),
  buildQuestion('Lake becomes contaminated!', 'Clean the water', [-20, 0, 10, 0], 'Advise caution', [0, 0, -20, 0]),
  buildQuestion('New tech clashes with regulation', 'Ease regulation', [20, -10, 0, 0], 'Do nothing', [-10, 0, 0, 0]),
  buildQuestion('Spike in fraud targetting seniors', 'Awareness campaigns', [-10, 0, 10, 0], 'Do nothing', [0, 0, -10, 0]),
  buildQuestion('Critical machine used in hospitals malfunctions!', 'Quit using immediately', [-20, 10, 10, 15], 'Wait and monitor', [0, -10, -5, -10]),
  buildQuestion('Quantum research falls behind!', 'Invest heavily', [-25, 0, 0, 20], 'Let private sector lead', [0, 0, 0, -15]),
  buildQuestion('Critical satellite malfunctions!', 'Repair immediately', [-20, 10, 0, 15], 'Temporary, cheap, fixes', [0, -10, 0, -10]),
  buildQuestion('AI algorithms discriminate!', 'Force to redesign algorithm', [-15, 0, 10, 10], 'Ignore issue', [0, 0, -15, -5]),
  buildQuestion('Kim Kardashian launches eco-friendly perfume line!', "How did this shit get on my desk?!", [0, 0, 0, 0], 'Invest EU funds', [-5, 0, 0, 0]),
  buildQuestion('George Clooney gets French citizenship!', "Seriously… this is my problem now?", [0, 0, 0, 0], 'Celebrate with decree', [0, 0, 5, 0]),
  buildQuestion('Taylor Swift writes a song about inflation!', 'Commission follow-up study', [-5, 0, 5, 0], 'Its kindof good tho', [0, 0, 5, 0]),
  buildQuestion('Elon Musk tweets about EU bureaucracy!', "Subpoena him", [0, 0, 0, 0], 'Fine one of his companies', [-5, 10, 0, 5]),
  buildQuestion('Reality TV star becomes climate ambassador!', "Is this actually a thing?", [0, 0, 0, 0], 'Fund the campaign', [-5, 0, 5, 0]),
  buildQuestion('Celebrity chef opens a zero-carbon restaurant in Brussels!', "Why am I handling this?", [0, 0, 0, 0], 'How does that even work?', [0, 0, 0, 0]),
  buildQuestion('Famous pop star proposes new holiday in EU!', "I have a better idea, declare his birthday a national holiday", [0, 0, 5, 0], 'Declare national holiday', [0, 0, 10, 0])
];

const initialStats = STATS.reduce((acc, key) => ({ ...acc, [key]: 100 }), {});
let stats = { ...initialStats };
let deck = shuffle([...questions]);
let currentQuestion = null;
let gameOver = false;

const questionCard = document.getElementById('question-card');
const questionText = document.getElementById('question-text');
const answerElements = [
  document.getElementById('answer-left-text'),
  document.getElementById('answer-right-text')
];
const answerZones = [
  document.querySelector('.answer-left'),
  document.querySelector('.answer-right')
];
const statusMessage = document.getElementById('status-message');

const statElements = STATS.reduce((acc, key) => {
  return {
    ...acc,
    [key]: {
      container: document.querySelector(`.stat[data-key="${key}"]`),
      value: document.getElementById(`value-${key}`),
      fill: document.getElementById(`fill-${key}`)
    }
  };
}, {});

const statPulseTimers = {};
const IMPACT_COOLDOWN = 900;
let lastPreviewSide = null;
let lastImpactTime = 0;

let translate = { x: 0, y: 0 };
let dragOrigin = { x: 0, y: 0 };
let activePointer = null;
let isDragging = false;

setupDrag();
resetUI();

function resetUI() {
  stats = { ...initialStats };
  deck = shuffle([...questions]);
  gameOver = false;
  document.body.classList.remove('game-over');
  resetImpact();
  updateStatsUI();
  nextQuestion();
  showStatus('Drag the card to the side you support.');
}

function nextQuestion() {
  if (!deck.length) {
    deck = shuffle([...questions]);
  }
  currentQuestion = deck.pop();
  questionText.textContent = currentQuestion.prompt;
  answerElements[0].textContent = currentQuestion.options[0].text;
  answerElements[1].textContent = currentQuestion.options[1].text;
}

function applyChoice(index) {
  if (!currentQuestion || gameOver) {
    return;
  }
  const choice = currentQuestion.options[index];
  STATS.forEach((key) => {
    stats[key] = clamp(stats[key] + choice.effects[key], 0, 100);
  });
  updateStatsUI();

  if (isCollapse()) {
    triggerGameOver();
    return;
  }

  window.setTimeout(() => {
    if (!gameOver) {
      nextQuestion();
    }
  }, 400);
}

function updateStatsUI() {
  STATS.forEach((key) => {
    const value = Math.round(stats[key]);
    statElements[key].value.textContent = value;
    statElements[key].fill.style.width = `${value}%`;
  });
}

function describeEffects(effects) {
  const summary = STATS.map((key) => {
    const shift = effects[key];
    if (!shift) {
      return null;
    }
    const prefix = shift > 0 ? '+' : '';
    return `${ICONS[key]} ${prefix}${shift}`;
  }).filter(Boolean);

  return summary.length ? summary.join(' · ') : 'No immediate change.';
}

function isCollapse() {
  return STATS.some((key) => stats[key] <= 0);
}

function triggerGameOver() {
  gameOver = true;
  document.body.classList.add('game-over');
  const collapsed = STATS.filter((key) => stats[key] <= 0)
    .map((key) => `${ICONS[key]} depleted`)
    .join(' · ');
  showStatus(`Crisis! You lost! Refresh to try again.`);
}

function setupDrag() {
  questionCard.addEventListener('pointerdown', (event) => {
    if (gameOver) {
      return;
    }
    questionCard.setPointerCapture(event.pointerId);
    isDragging = true;
    activePointer = event.pointerId;
    questionCard.classList.add('dragging');
    dragOrigin = {
      x: event.clientX - translate.x,
      y: event.clientY - translate.y
    };
  });

  window.addEventListener('pointermove', (event) => {
    if (!isDragging || event.pointerId !== activePointer) {
      return;
    }
    translate = {
      x: event.clientX - dragOrigin.x,
      y: event.clientY - dragOrigin.y
    };
    setCardPosition(translate.x, translate.y);
    previewSide();
  });

  const finishDrag = (event) => {
    if (!isDragging || event.pointerId !== activePointer) {
      return;
    }
    questionCard.releasePointerCapture(activePointer);
    questionCard.classList.remove('dragging');
    isDragging = false;
    const pickIndex = determineSide();
    resetCardPosition();
    clearPreview();
    activePointer = null;
    if (!gameOver) {
      applyChoice(pickIndex);
    }
  };

  window.addEventListener('pointerup', finishDrag);
  window.addEventListener('pointercancel', finishDrag);
}

function previewSide() {
  const rect = questionCard.getBoundingClientRect();
  const sideIndex = rect.left + rect.width / 2 < window.innerWidth / 2 ? 0 : 1;
  highlightAnswer(sideIndex);
  previewImpact(sideIndex);
}

function clearPreview() {
  answerZones.forEach((zone) => zone.classList.remove('active'));
  resetImpact();
}

function highlightAnswer(index) {
  answerZones.forEach((zone, idx) => {
    zone.classList.toggle('active', idx === index);
  });
}

function determineSide() {
  const rect = questionCard.getBoundingClientRect();
  return rect.left + rect.width / 2 < window.innerWidth / 2 ? 0 : 1;
}

function setCardPosition(x, y) {
  questionCard.style.setProperty('--dx', `${x}px`);
  questionCard.style.setProperty('--dy', `${y}px`);
}

function resetCardPosition() {
  translate = { x: 0, y: 0 };
  window.requestAnimationFrame(() => {
    setCardPosition(0, 0);
  });
}

function showStatus(message) {
  statusMessage.textContent = message;
}

function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

function previewImpact(sideIndex) {
  if (!currentQuestion) {
    return;
  }
  const now = Date.now();
  if (sideIndex === lastPreviewSide && now - lastImpactTime < IMPACT_COOLDOWN) {
    return;
  }
  lastPreviewSide = sideIndex;
  lastImpactTime = now;
  showImpact(sideIndex);
}

function showImpact(index) {
  const option = currentQuestion?.options?.[index];
  if (!option) {
    return;
  }
  STATS.forEach((key) => {
    pulseStat(key, option.effects[key]);
  });
}

function pulseStat(statKey, delta) {
  const container = statElements[statKey]?.container;
  if (!container) {
    return;
  }
  container.classList.remove('pulse-positive', 'pulse-negative');
  window.clearTimeout(statPulseTimers[statKey]);
  if (!delta) {
    return;
  }
  const className = delta > 0 ? 'pulse-positive' : 'pulse-negative';
  // Force reflow so the animation can retrigger.
  void container.offsetWidth;
  container.classList.add(className);
  statPulseTimers[statKey] = window.setTimeout(() => {
    container.classList.remove(className);
  }, 1000);
}

function resetImpact() {
  STATS.forEach((key) => {
    const container = statElements[key]?.container;
    if (!container) {
      return;
    }
    container.classList.remove('pulse-positive', 'pulse-negative');
    window.clearTimeout(statPulseTimers[key]);
    statPulseTimers[key] = null;
  });
  lastPreviewSide = null;
}

function shuffle(items) {
  const list = [...items];
  for (let i = list.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [list[i], list[j]] = [list[j], list[i]];
  }
  return list;
}

function buildQuestion(prompt, leftText, leftEffects, rightText, rightEffects) {
  return {
    prompt,
    options: [
      { text: leftText, effects: toEffects(leftEffects) },
      { text: rightText, effects: toEffects(rightEffects) }
    ]
  };
}

function toEffects(values) {
  const [economy, security, people, technology] = values;
  return { economy, security, people, technology };
}
