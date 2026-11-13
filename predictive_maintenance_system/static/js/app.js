/* =========================================================
   Predictive Maintenance System — Frontend JavaScript
========================================================= */

// ── Tab Navigation ──────────────────────────────────────
document.querySelectorAll('.tab-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + btn.dataset.tab).classList.add('active');

    // Auto-load history tab
    if (btn.dataset.tab === 'history') loadHistory();
    if (btn.dataset.tab === 'dashboard') loadStats();
  });
});

// ── Load dashboard stats on page load ────────────────────
window.addEventListener('DOMContentLoaded', loadStats);

async function loadStats() {
  try {
    const res  = await fetch('/api/stats');
    const data = await res.json();
    if (data.success) {
      const s = data.stats;
      document.getElementById('kpiHealthy').textContent = s.healthy;
      document.getElementById('kpiWarning').textContent = s.warning;
      document.getElementById('kpiFailure').textContent = s.failure;
      document.getElementById('kpiAlerts').textContent  = s.total_alerts;
    }
  } catch (e) { console.error('Stats error:', e); }
}

// ── Quick preset loader ──────────────────────────────────
const PRESETS = {
  healthy: { temp: 52,  vib: 0.28, pres: 102, rpm: 1510 },
  warning: { temp: 74,  vib: 0.72, pres: 84,  rpm: 1260 },
  failure: { temp: 102, vib: 1.85, pres: 55,  rpm: 880  }
};

function loadPreset(type) {
  const p = PRESETS[type];
  document.getElementById('inp_temp').value  = p.temp;
  document.getElementById('inp_vib').value   = p.vib;
  document.getElementById('inp_pres').value  = p.pres;
  document.getElementById('inp_rpm').value   = p.rpm;
}

// ── Run Prediction ───────────────────────────────────────
async function runPrediction() {
  const btn = document.getElementById('analyseBtn');

  const temp = parseFloat(document.getElementById('inp_temp').value);
  const vib  = parseFloat(document.getElementById('inp_vib').value);
  const pres = parseFloat(document.getElementById('inp_pres').value);
  const rpm  = parseFloat(document.getElementById('inp_rpm').value);

  if (isNaN(temp) || isNaN(vib) || isNaN(pres) || isNaN(rpm)) {
    alert('Please fill in all sensor values before analysing.');
    return;
  }

  btn.innerHTML = '<span class="loading"></span> Analysing…';
  btn.disabled  = true;

  try {
    const res  = await fetch('/api/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temperature: temp, vibration: vib, pressure: pres, rpm })
    });
    const data = await res.json();

    if (data.success) {
      renderResult(data.result);
      document.getElementById('resultPanel').style.display = 'block';
      loadStats(); // refresh KPIs
    } else {
      alert('Prediction error: ' + data.error);
    }
  } catch (e) {
    alert('Connection error. Is the Flask server running?');
  } finally {
    btn.innerHTML = '🔬 Analyse Machine';
    btn.disabled  = false;
  }
}

// ── Render Prediction Result ─────────────────────────────
function renderResult(r) {
  const condEl = document.getElementById('resultCondition');
  const icons  = { Healthy: '✅ HEALTHY', Warning: '⚠️ WARNING', Failure: '🔴 FAILURE' };
  const cls    = { Healthy: 'cond-healthy', Warning: 'cond-warning', Failure: 'cond-failure' };

  condEl.textContent = icons[r.condition] || r.condition;
  condEl.className   = 'result-condition ' + (cls[r.condition] || '');

  document.getElementById('confText').textContent = r.confidence + '%';
  document.getElementById('confBar').style.width  = r.confidence + '%';

  const probs = r.probabilities;
  document.getElementById('probHealthy').querySelector('span').textContent = probs.Healthy + '%';
  document.getElementById('probWarning').querySelector('span').textContent = probs.Warning + '%';
  document.getElementById('probFailure').querySelector('span').textContent = probs.Failure + '%';

  // Root Cause Analysis
  const rcaCont = document.getElementById('rcaContainer');
  rcaCont.innerHTML = (r.root_causes || []).map(c => `
    <div class="rca-card">
      <div class="rca-cause">🔍 ${c.cause}</div>
      <div class="rca-sensor">Sensor: ${c.sensor} — Value: ${c.value}</div>
      <div class="rca-explanation">${c.explanation}</div>
      <div class="rca-action">✔ Action: ${c.action}</div>
    </div>
  `).join('');

  // Threshold Alerts
  const alertCont = document.getElementById('alertsContainer');
  const alerts    = r.threshold_alerts || [];
  if (alerts.length > 0) {
    alertCont.innerHTML = '<div class="card-header" style="margin-top:1rem">⚡ Threshold Alerts</div>' +
      alerts.map(a => `<div class="alert-box alert-${a.level}">
        <strong>${a.level}</strong>: ${a.msg}
      </div>`).join('');
  } else {
    alertCont.innerHTML = '<div style="color:var(--green);font-size:0.82rem;margin-top:0.5rem">✅ No threshold violations detected</div>';
  }
}

// ── Digital Twin ─────────────────────────────────────────
let twinChart = null;

async function runDigitalTwin() {
  const temp = parseFloat(document.getElementById('twin_temp').value);
  const vib  = parseFloat(document.getElementById('twin_vib').value);
  const pres = parseFloat(document.getElementById('twin_pres').value);
  const rpm  = parseFloat(document.getElementById('twin_rpm').value);

  if (isNaN(temp) || isNaN(vib) || isNaN(pres) || isNaN(rpm)) {
    alert('Please fill in all starting values.'); return;
  }

  try {
    const res  = await fetch('/api/digital-twin', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ temperature: temp, vibration: vib, pressure: pres, rpm })
    });
    const data = await res.json();

    if (data.success) {
      renderTwin(data.timeline);
      document.getElementById('twinResultCard').style.display = 'block';
    }
  } catch (e) { alert('Error running simulation.'); }
}

function renderTwin(timeline) {
  const hours  = timeline.map(t => 'H' + t.hour);
  const health = timeline.map(t => t.health);
  const temps  = timeline.map(t => t.temperature);

  const colors = timeline.map(t => ({
    'Healthy': 'rgba(34,197,94,0.7)',
    'Warning': 'rgba(245,158,11,0.7)',
    'Failure': 'rgba(239,68,68,0.7)'
  })[t.condition] || 'rgba(56,189,248,0.7)');

  const ctx = document.getElementById('twinChart').getContext('2d');
  if (twinChart) twinChart.destroy();

  twinChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: hours,
      datasets: [
        {
          label: 'Health Score (%)',
          data: health,
          borderColor: '#38bdf8',
          backgroundColor: 'rgba(56,189,248,0.08)',
          borderWidth: 2,
          pointBackgroundColor: colors,
          pointRadius: 4,
          tension: 0.3,
          yAxisID: 'y'
        },
        {
          label: 'Temperature (°C)',
          data: temps,
          borderColor: '#f59e0b',
          backgroundColor: 'rgba(245,158,11,0.05)',
          borderWidth: 1.5,
          borderDash: [4, 3],
          pointRadius: 2,
          tension: 0.3,
          yAxisID: 'y2'
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { labels: { color: '#94a3b8', font: { family: 'JetBrains Mono', size: 11 } } }
      },
      scales: {
        x:  { ticks: { color: '#64748b' }, grid: { color: '#1e293b' } },
        y:  { min: 0, max: 100, ticks: { color: '#64748b' }, grid: { color: '#1e293b' }, position: 'left',
              title: { display: true, text: 'Health %', color: '#38bdf8' } },
        y2: { ticks: { color: '#64748b' }, grid: { display: false }, position: 'right',
              title: { display: true, text: 'Temp °C', color: '#f59e0b' } }
      }
    }
  });

  // Timeline badges
  const tlEl = document.getElementById('twinTimeline');
  tlEl.innerHTML = timeline.map(t => {
    const cls = { Healthy: 'healthy-tick', Warning: 'warning-tick', Failure: 'failure-tick' }[t.condition] || '';
    const col = { Healthy: 'var(--green)', Warning: 'var(--amber)', Failure: 'var(--red)' }[t.condition] || '#fff';
    return `<div class="twin-tick ${cls}">
      <div class="t-hour">Hour ${t.hour}</div>
      <div class="t-cond" style="color:${col}">${t.condition}</div>
      <div>${t.health}%</div>
    </div>`;
  }).join('');
}

// ── Chat ─────────────────────────────────────────────────
async function sendChat() {
  const input = document.getElementById('chatInput');
  const msg   = input.value.trim();
  if (!msg) return;

  appendChat('user', msg);
  input.value = '';

  try {
    const res  = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg })
    });
    const data = await res.json();
    if (data.success) appendChat('bot', data.reply);
    else appendChat('bot', 'Sorry, an error occurred. Please try again.');
  } catch (e) {
    appendChat('bot', 'Connection error. Is the Flask server running?');
  }
}

function appendChat(role, msg) {
  const win    = document.getElementById('chatWindow');
  const isBot  = role === 'bot';
  const div    = document.createElement('div');
  div.className = 'chat-msg ' + (isBot ? 'bot' : 'user');
  div.innerHTML = `
    <div class="chat-avatar">${isBot ? '🤖' : '👤'}</div>
    <div class="chat-bubble">${msg}</div>
  `;
  win.appendChild(div);
  win.scrollTop = win.scrollHeight;
}

function quickChat(msg) {
  document.getElementById('chatInput').value = msg;
  sendChat();
}

// ── History ──────────────────────────────────────────────
async function loadHistory() {
  try {
    const res  = await fetch('/api/history');
    const data = await res.json();
    if (!data.success) return;

    const tbody = document.getElementById('historyBody');
    const recs  = data.records;

    if (recs.length === 0) {
      tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:#64748b">No records yet.</td></tr>';
      return;
    }

    tbody.innerHTML = recs.map(r => {
      const badge = `badge-${r.condition.toLowerCase()}`;
      const ts    = r.timestamp ? r.timestamp.substring(0, 19).replace('T', ' ') : '–';
      return `<tr>
        <td>${r.id}</td>
        <td>${ts}</td>
        <td>${parseFloat(r.temperature).toFixed(1)}°C</td>
        <td>${parseFloat(r.vibration).toFixed(3)}g</td>
        <td>${parseFloat(r.pressure).toFixed(1)} PSI</td>
        <td>${parseFloat(r.rpm).toFixed(0)}</td>
        <td><span class="badge ${badge}">${r.condition}</span></td>
        <td>${parseFloat(r.confidence).toFixed(1)}%</td>
      </tr>`;
    }).join('');

  } catch (e) { console.error('History error:', e); }
}
