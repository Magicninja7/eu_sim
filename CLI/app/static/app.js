async function fetchJson(url) {
  const res = await fetch(url, { cache: 'no-store' });
  if (!res.ok) {
    const err = new Error(`HTTP ${res.status} for ${url}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

function setText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}

function setNotificationText(id, value) {
  const el = document.getElementById(id);
  if (el) el.textContent = value;
}


const DECISION_ZONE_IDS = ['zone-tl', 'zone-tr', 'zone-bl', 'zone-br'];
const NOTIFICATION_DISPLAY_MS = 4200;
let dragOffsetX = 0;
let dragOffsetY = 0;
let draggingPointerId = null;
let dragStartPointerX = 0;
let dragStartPointerY = 0;
let dragStartOffsetX = 0;
let dragStartOffsetY = 0;
let activeDropZone = null;
let chooseInFlight = false;
const notificationQueue = [];
let notificationDisplayTimer = null;
let notificationInView = null;
let notificationsPollInFlight = false;

function getDecisionZones() {
  return DECISION_ZONE_IDS
    .map((id) => document.getElementById(id))
    .filter(Boolean);
}



function setCardTransform(withAnimation = false) {
  const card = document.getElementById('eventCard');
  if (!card) return;

  card.style.transition = withAnimation ? 'transform 180ms ease-out' : 'none';
  card.style.transform = `translate(calc(-50% + ${dragOffsetX}px), calc(-50% + ${dragOffsetY}px))`;
}

function resetCardPosition(withAnimation = false) {
  dragOffsetX = 0;
  dragOffsetY = 0;
  setCardTransform(withAnimation);
}

function setActiveDropZone(zone) {
  if (activeDropZone && activeDropZone !== zone) {
    activeDropZone.classList.remove('is-active-drop');
  }
  activeDropZone = zone;
  if (activeDropZone) {
    activeDropZone.classList.add('is-active-drop');
  }
}

function clearActiveDropZone() {
  setActiveDropZone(null);
}

// Returns the decision zone if the point (x, y) is within the zone's full
// horizontal extent and within the label's vertical bounds.
function getZoneAtPoint(x, y) {
  const zones = getDecisionZones();
  for (const zone of zones) {
    if (!zone.dataset.decisionId) continue;
    const label = zone.querySelector('.decision-label');
    if (!label) continue;
    const zoneRect = zone.getBoundingClientRect();
    const labelRect = label.getBoundingClientRect();
    if (x >= zoneRect.left && x <= zoneRect.right &&
        y >= labelRect.top && y <= labelRect.bottom) {
      return zone;
    }
  }
  return null;
}



// Render event data already in memory — no extra fetch needed.
function applyEventData(data) {
  const eventWindow = document.getElementById('eventWindow');

  if (data.game_over) {
    triggerGameOver(data.collapsed || []);
    if (eventWindow) eventWindow.hidden = true;
    return;
  }

  if (data.done) {
    if (eventWindow) eventWindow.hidden = true;
    setText('eventDescription', '');
    renderDecisionZones([]);
    resetCardPosition(true);
    return;
  }

  if (eventWindow) eventWindow.hidden = false;
  setText('eventDescription', data.description);
  renderDecisionZones(Array.isArray(data.decisions) ? data.decisions.slice(0, 4) : []);
  resetCardPosition(true);
}

async function chooseDecision(decisionId) {
  if (!decisionId || chooseInFlight) return;

  const card = document.getElementById('eventCard');
  chooseInFlight = true;
  if (card) card.classList.add('busy');

  try {
    const res = await fetch('/api/choose', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ decisionId }),
    });
    const data = await res.json();
    // Server returns next event inline — no second GET needed.
    applyEventData(data);
  } finally {
    chooseInFlight = false;
    if (card) card.classList.remove('busy');
  }
}

function renderDecisionZones(decisions) {
  const zones = getDecisionZones();

  zones.forEach((zone, index) => {
    const decision = decisions[index] || null;
    zone.classList.remove('is-active-drop', 'is-empty');

    const label = zone.querySelector('.decision-label');
    if (label) {
      label.textContent = decision ? decision.label : 'No choice available here';
    }

    if (decision) {
      zone.disabled = false;
      zone.dataset.decisionId = decision.id;
    } else {
      zone.disabled = true;
      zone.dataset.decisionId = '';
      zone.classList.add('is-empty');
    }
  });
}

function initDecisionDragAndDrop() {
  const card = document.getElementById('eventCard');
  if (!card || card.dataset.dragInit === 'true') return;

  card.dataset.dragInit = 'true';

  card.addEventListener('pointerdown', (ev) => {
    if (chooseInFlight || ev.button !== 0) return;

    draggingPointerId = ev.pointerId;
    dragStartPointerX = ev.clientX;
    dragStartPointerY = ev.clientY;
    dragStartOffsetX = dragOffsetX;
    dragStartOffsetY = dragOffsetY;

    card.setPointerCapture(ev.pointerId);
    card.classList.add('dragging');
    card.style.transition = 'none';
  });

  card.addEventListener('pointermove', (ev) => {
    if (draggingPointerId !== ev.pointerId) return;

    dragOffsetX = dragStartOffsetX + (ev.clientX - dragStartPointerX);
    dragOffsetY = dragStartOffsetY + (ev.clientY - dragStartPointerY);
    setCardTransform(false);

    const zone = getZoneAtPoint(ev.clientX, ev.clientY);
    if (zone) {
      setActiveDropZone(zone);
    } else {
      clearActiveDropZone();
    }
  });

  async function finishDrag(ev) {
    if (draggingPointerId !== ev.pointerId) return;

    card.classList.remove('dragging');
    card.releasePointerCapture(ev.pointerId);
    draggingPointerId = null;

    const zoneFromPointer = getZoneAtPoint(ev.clientX, ev.clientY);
    const zone = zoneFromPointer || activeDropZone;
    clearActiveDropZone();

    if (zone && zone.dataset.decisionId) {
      resetCardPosition(true);
      await chooseDecision(zone.dataset.decisionId);
      return;
    }

    resetCardPosition(true);
  }

  card.addEventListener('pointerup', finishDrag);
  card.addEventListener('pointercancel', finishDrag);

  resetCardPosition(false);
}

async function loadEvent() {
  const data = await fetchJson('/api/event');
  applyEventData(data);
}


let lastKnownDay = null;
let gameIsOver = false;
const prevStats = {};

const STAT_LABELS = {
  economics: 'Economics',
  inner_workings: 'Inner Workings',
  diplomacy: 'Diplomacy',
  security: 'Security',
  demographics: 'Demographics',
  people: 'People',
  human_rights: 'Human Rights',
};

function flashStat(key, gained) {
  const el = document.getElementById(`stat-${key}`);
  if (!el) return;
  el.classList.remove('stat-gain', 'stat-loss');
  void el.offsetWidth; // force reflow to restart animation
  el.classList.add(gained ? 'stat-gain' : 'stat-loss');
  el.addEventListener('animationend', () => {
    el.classList.remove('stat-gain', 'stat-loss');
    const valEl = el.querySelector('.stat-value');
    if (valEl) valEl.style.color = '';
  }, { once: true });
}

function updateStats(stats) {
  for (const [key, val] of Object.entries(stats)) {
    const valEl = document.getElementById(`val-${key}`);
    if (valEl) valEl.textContent = Math.round(val);

    if (key in prevStats) {
      const diff = val - prevStats[key];
      if (Math.abs(diff) >= 0.05) {
        flashStat(key, diff > 0);
      }
    }
    prevStats[key] = val;
  }
}

function triggerGameOver(collapsed) {
  if (gameIsOver) return;
  gameIsOver = true;
  const overlay = document.getElementById('gameOverlay');
  const reason = document.getElementById('gameOverReason');
  if (!overlay) return;
  if (reason) {
    const labels = collapsed.map(k => STAT_LABELS[k] || k).join(', ');
    reason.textContent = `${labels} collapsed to zero.`;
  }
  overlay.hidden = false;
}

// Single poll replaces the two separate pollDay + loadStatCounter intervals.
async function pollStatus() {
  const data = await fetchJson('/api/status');
  setText('dateCounter', data.date);
  if (typeof data.gdp === 'number') setText('gdpCounter', data.gdp);
  if (typeof data.tax_l === 'number') setText('taxCounterL', data.tax_l);
  if (typeof data.tax_m === 'number') setText('taxCounterM', data.tax_m);
  if (typeof data.tax_h === 'number') {
    setText('taxCounterH', data.tax_h);
    setText('taxCounterHFull', data.tax_h);
  }
  if (data.stats) updateStats(data.stats);
  if (data.game_over) {
    triggerGameOver(data.collapsed || []);
    return;
  }
  const dayChanged = lastKnownDay === null || data.day !== lastKnownDay;
  lastKnownDay = data.day;
  if (dayChanged) {
    await loadEvent();
  }
}

// ── Tax dropdown toggle ──
(function initTaxDropdown() {
  const dropdown = document.querySelector('.tax-dropdown');
  const toggle = document.getElementById('taxToggle');
  if (!toggle || !dropdown) return;

  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    dropdown.classList.toggle('open');
  });

  document.addEventListener('click', () => {
    dropdown.classList.remove('open');
  });
})();

(function initNotificationCentre() {
  const toggle = document.getElementById('notificationToggle');
  if (!toggle) return;

  setNotificationCentreOpen(true);
  renderNotification(null);

  toggle.addEventListener('click', (event) => {
    event.stopPropagation();
    const centre = document.getElementById('notificationCentre');
    const isOpen = !(centre && centre.classList.contains('is-open'));
    setNotificationCentreOpen(isOpen);
  });
})();

(async function main() {
  initDecisionDragAndDrop();
  await pollStatus();

  setInterval(pollStatus, 2000);
})();
