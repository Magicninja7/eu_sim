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

function setMapStatus(message, isError = false) {
  const el = document.getElementById('mapStatus');
  if (!el) return;
  if (!message) {
    el.hidden = true;
    el.textContent = '';
    return;
  }
  el.hidden = false;
  el.textContent = message;
  el.style.color = isError ? '#ffb0b0' : '';
}

async function loadEvent() {
  const data = await fetchJson('/api/event');
  const eventWindow = document.getElementById('eventWindow');
  if (data.done) {
    if (eventWindow) eventWindow.hidden = true;
    setText('eventDescription', '');
    setMapStatus('');
    const container = document.getElementById('decisions');
    if (container) container.innerHTML = '';
    return;
  }

  if (eventWindow) eventWindow.hidden = false;
  setMapStatus('');

  setText('eventDescription', data.description);

  const container = document.getElementById('decisions');
  container.innerHTML = '';

  for (const d of data.decisions) {
    const btn = document.createElement('button');
    btn.className = 'decision';

    btn.textContent = d.label;
    btn.addEventListener('click', async () => {
      btn.disabled = true;
      try {
        await fetch('/api/choose', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ decisionId: d.id }),
        });
        await loadEvent();
      } finally {
        btn.disabled = false;
      }
    });
    container.appendChild(btn);
  }

  if (!data.decisions.length) {
    const btn = document.createElement('button');
    btn.className = 'decision';
    btn.textContent = 'No choices available.';
    btn.disabled = true;
    container.appendChild(btn);
  }
}

function getCountryNameFromFeature(feature) {
  if (!feature || !feature.properties) return null;

  return (
    feature.properties.name ||
    feature.properties.ADMIN ||
    feature.properties.admin ||
    feature.properties.NAME ||
    null
  );
}

async function loadCountriesLayer(map) {
  setMapStatus('Loading country borders…');
  const sources = [
    '/static/countries.geojson',
    'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json',
  ];

  let geo = null;
  for (const url of sources) {
    try {
      geo = await fetchJson(url);
      setMapStatus('');
      break;
    } catch (e) {
      //try next source
    }
  }

  if (!geo) {
    setMapStatus(
      'Could not load country borders. If you are offline, download a GeoJSON as static/countries.geojson.',
      true
    );
    return;
  }

  const normalStyle = {
    color: 'rgba(255,255,255,0.35)',
    weight: 1,
    fillColor: 'rgba(122,162,255,0.18)',
    fillOpacity: 0.6,
  };

  const hoverStyle = {
    color: 'rgba(255,255,255,0.85)',
    weight: 2,
    fillColor: 'rgba(122,162,255,0.30)',
    fillOpacity: 0.8,
  };

  let selectedLayer = null;

  const layer = L.geoJSON(geo, {
    style: normalStyle,
    onEachFeature: (feature, lyr) => {
      lyr.on('mouseover', () => {
        lyr.setStyle(hoverStyle);
      });
      lyr.on('mouseout', () => {
        if (selectedLayer && selectedLayer === lyr) {
          lyr.setStyle({ ...hoverStyle, fillColor: 'rgba(122,162,255,0.40)' });
        } else {
          lyr.setStyle(normalStyle);
        }
      });
      lyr.on('click', () => {
        if (selectedLayer && selectedLayer !== lyr) {
          selectedLayer.setStyle(normalStyle);
        }
        selectedLayer = lyr;
        lyr.setStyle({ ...hoverStyle, fillColor: 'rgba(122,162,255,0.40)' });

        const name = getCountryNameFromFeature(feature) || '(unknown)';
        setText('countryName', name);
      });
    },
  }).addTo(map);

  try {
    map.fitBounds(layer.getBounds(), { padding: [20, 20] });
  } catch {
    // ignore
  }
}

function initMap() {
  const map = L.map('map', {
    worldCopyJump: true,
    zoomControl: true,
  }).setView([20, 0], 2);

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 6,
    attribution: '&copy; OpenStreetMap contributors',
  }).addTo(map);

  loadCountriesLayer(map);
}

let lastKnownDay = null;

async function pollDay() {
  const data = await fetchJson('/api/day');
  if (typeof data.day === 'number') {
    setText('dateCounter', data.date);
    const dayChanged = lastKnownDay !== null && data.day !== lastKnownDay;
    lastKnownDay = data.day;
    if (dayChanged) {
      await loadEvent();
    }
  }
}

async function loadStatCounter() {
  const data = await fetchJson('/api/stats');
  if (typeof data.gdp === 'number') {
    setText('gdpCounter', data.gdp);
  }
  if (typeof data.tax_l === 'number') {
    setText('taxCounterL', data.tax_l);
  }
  if (typeof data.tax_m === 'number') {
    setText('taxCounterM', data.tax_m);
  }
  if (typeof data.tax_h === 'number') {
    setText('taxCounterH', data.tax_h);
    setText('taxCounterHFull', data.tax_h);
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

(async function main() {
  await pollDay();
  await loadStatCounter();
  await loadEvent();
  initMap();
  setInterval(pollDay, 2000);
  setInterval(loadStatCounter, 4000);
})();
 