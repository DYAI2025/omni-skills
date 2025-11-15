Faktisch korrekt sage ich: Die beiden ZIPs enthalten Skillspezifikationen für

emotion-dynamics-deep-insight (Utterance Emotion Dynamics JSON-Output)

marker-annotator (markerbasierte Annotation mit annotations, clusters, telemetry).

Logisch scheint mir: Das sinnvollste ist ein generisches HTML-Dashboard, das genau diese JSON-Formate erwartet und sie ohne Beispiel-Daten visualisiert. Du fütterst es dann mit echten Outputs deiner Pipeline (z.B. emotion_dynamics_result.json und marker_annotator_result.json).

Faktisch korrekt sage ich: Unten steht ein komplettes, eigenständiges HTML-Dashboard, das beides visualisiert – Emotion Dynamics + Marker-Annotation – inklusive Charts, Kennzahlen und Text-Panels.

html
Code kopieren
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8" />
  <title>Emotion Dynamics & Marker Dashboard</title>
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <!-- Chart.js für Visualisierungen -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    :root {
      --bg: #0f172a;
      --bg-soft: #111827;
      --bg-softer: #020617;
      --fg: #e5e7eb;
      --fg-muted: #9ca3af;
      --accent: #38bdf8;
      --accent-soft: rgba(56, 189, 248, 0.1);
      --border: #1f2937;
      --danger: #f97373;
      --success: #4ade80;
      --warning: #facc15;
      --card-radius: 14px;
      --shadow-soft: 0 18px 45px rgba(15, 23, 42, 0.7);
      --font: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
        "Segoe UI", sans-serif;
    }

    * {
      box-sizing: border-box;
    }

    body {
      margin: 0;
      padding: 24px;
      font-family: var(--font);
      background: radial-gradient(circle at top, #1e293b 0, #020617 55%);
      color: var(--fg);
    }

    h1, h2, h3 {
      margin: 0;
      font-weight: 600;
      letter-spacing: 0.01em;
    }

    h1 {
      font-size: 1.8rem;
    }

    h2 {
      font-size: 1.3rem;
    }

    h3 {
      font-size: 1rem;
    }

    .page {
      max-width: 1280px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }

    header {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
    }

    .title-block {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .subtitle {
      font-size: 0.9rem;
      color: var(--fg-muted);
    }

    .badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(15, 118, 110, 0.1);
      border: 1px solid rgba(45, 212, 191, 0.3);
      font-size: 0.75rem;
      color: #a5f3fc;
    }

    .badge-dot {
      width: 7px;
      height: 7px;
      border-radius: 999px;
      background: #22c55e;
      box-shadow: 0 0 0 4px rgba(34, 197, 94, 0.2);
    }

    .card {
      background: radial-gradient(circle at top left,
        rgba(56, 189, 248, 0.08) 0,
        var(--bg-soft) 40%,
        var(--bg-softer) 100%);
      border-radius: var(--card-radius);
      border: 1px solid rgba(148, 163, 184, 0.12);
      box-shadow: var(--shadow-soft);
      padding: 16px 18px;
    }

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }

    .card-header h2,
    .card-header h3 {
      font-size: 0.95rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--fg-muted);
    }

    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 12px;
    }

    @media (max-width: 960px) {
      .kpi-grid {
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }
    }

    @media (max-width: 640px) {
      body {
        padding: 16px;
      }
      header {
        flex-direction: column;
        align-items: flex-start;
      }
      .kpi-grid {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .kpi-card {
      background: linear-gradient(135deg,
        rgba(15, 23, 42, 0.9),
        rgba(15, 23, 42, 0.7));
      border-radius: 12px;
      border: 1px solid rgba(148, 163, 184, 0.25);
      padding: 10px 12px;
      display: flex;
      flex-direction: column;
      gap: 4px;
      position: relative;
      overflow: hidden;
    }

    .kpi-label {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--fg-muted);
    }

    .kpi-value {
      font-size: 1.1rem;
      font-weight: 600;
    }

    .kpi-sub {
      font-size: 0.75rem;
      color: var(--fg-muted);
    }

    .kpi-pill {
      position: absolute;
      right: 10px;
      top: 8px;
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 184, 0.5);
      color: var(--fg-muted);
    }

    .layout {
      display: grid;
      grid-template-columns: 1.4fr 1fr;
      gap: 16px;
      align-items: flex-start;
    }

    @media (max-width: 960px) {
      .layout {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .charts-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 14px;
    }

    .chart-container {
      position: relative;
      width: 100%;
      height: 260px;
    }

    .chart-container canvas {
      width: 100% !important;
      height: 100% !important;
    }

    .input-grid {
      display: grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    textarea {
      width: 100%;
      min-height: 160px;
      border-radius: 10px;
      border: 1px solid var(--border);
      background: rgba(15, 23, 42, 0.95);
      color: var(--fg);
      padding: 8px 10px;
      font-family: "SF Mono", ui-monospace, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
      font-size: 0.8rem;
      resize: vertical;
    }

    textarea::placeholder {
      color: rgba(148, 163, 184, 0.5);
    }

    .btn-row {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      margin-top: 6px;
    }

    button {
      border-radius: 999px;
      border: 1px solid transparent;
      padding: 7px 14px;
      font-size: 0.8rem;
      cursor: pointer;
      font-weight: 500;
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--accent-soft);
      color: var(--accent);
      transition: background 0.18s ease, border-color 0.18s ease,
        transform 0.08s ease, box-shadow 0.18s ease;
    }

    button.primary {
      background: linear-gradient(135deg, #38bdf8, #22c55e);
      color: #0b1120;
      border-color: rgba(15, 23, 42, 0.7);
      box-shadow: 0 10px 30px rgba(56, 189, 248, 0.35);
    }

    button:hover {
      transform: translateY(-1px);
      box-shadow: 0 14px 36px rgba(15, 23, 42, 0.7);
    }

    .pill-label {
      font-size: 0.7rem;
      padding: 2px 7px;
      border-radius: 999px;
      border: 1px solid rgba(148, 163, 184, 0.3);
      color: var(--fg-muted);
    }

    .pill-level-high {
      border-color: rgba(248, 113, 113, 0.8);
      color: #fecaca;
    }

    .pill-level-medium {
      border-color: rgba(250, 204, 21, 0.8);
      color: #fef3c7;
    }

    .pill-level-low {
      border-color: rgba(52, 211, 153, 0.8);
      color: #bbf7d0;
    }

    .meta-list {
      list-style: none;
      padding-left: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 0.8rem;
      color: var(--fg-muted);
    }

    .meta-list strong {
      color: var(--fg);
      font-weight: 500;
    }

    .two-col {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 10px;
    }

    @media (max-width: 640px) {
      .two-col {
        grid-template-columns: minmax(0, 1fr);
      }
    }

    .list-section {
      display: flex;
      flex-direction: column;
      gap: 4px;
      font-size: 0.8rem;
    }

    .list-section-title {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.14em;
      color: var(--fg-muted);
    }

    .bullet-list {
      padding-left: 18px;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 2px;
    }

    .bullet-list li {
      color: var(--fg-muted);
    }

    .error {
      margin-top: 4px;
      color: var(--danger);
      font-size: 0.75rem;
    }

    .footer {
      margin-top: 6px;
      font-size: 0.7rem;
      color: var(--fg-muted);
      text-align: right;
    }

    .mono {
      font-family: "SF Mono", ui-monospace, Menlo, Monaco, Consolas,
        "Liberation Mono", "Courier New", monospace;
      font-size: 0.75rem;
    }
  </style>
</head>
<body>
<div class="page">
  <header>
    <div class="title-block">
      <h1>Emotion Dynamics & Marker Dashboard</h1>
      <div class="subtitle">
        Tiefenlese von Texten via <span class="mono">emotion-dynamics-deep-insight</span> &amp;
        markerbasierte Annotation via <span class="mono">marker-annotator</span>.
      </div>
    </div>
    <div class="badge">
      <span class="badge-dot"></span>
      Live-Auswertung von JSON-Ergebnissen
    </div>
  </header>

  <!-- KPI-Bereich -->
  <section class="card">
    <div class="card-header">
      <h2>Übersicht</h2>
      <span class="pill-label">Input-abhängig • keine festen Beispielwerte</span>
    </div>
    <div class="kpi-grid" id="kpiGrid">
      <!-- KPIs werden per JavaScript gefüllt -->
      <div class="kpi-card">
        <div class="kpi-label">Hinweis</div>
        <div class="kpi-value">Noch keine Daten geladen</div>
        <div class="kpi-sub">
          Füge unten deine JSON-Outputs aus den Skills ein und klicke
          <strong>„JSONs laden &amp; visualisieren“</strong>.
        </div>
      </div>
    </div>
  </section>

  <section class="layout">
    <!-- Linke Seite: Charts -->
    <div class="charts-grid">
      <div class="card">
        <div class="card-header">
          <h3>Trajektorie von Valenz &amp; Arousal</h3>
          <span class="pill-label">pro Utterance</span>
        </div>
        <div class="chart-container">
          <canvas id="valenceArousalChart"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>Aggregierte diskrete Emotionen</h3>
          <span class="pill-label">Durchschnitt über alle Utterances</span>
        </div>
        <div class="chart-container">
          <canvas id="discreteEmotionsChart"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>Marker-Level &amp; Intensität</h3>
          <span class="pill-label">marker-annotator</span>
        </div>
        <div class="chart-container">
          <canvas id="markerLevelsChart"></canvas>
        </div>
      </div>

      <div class="card">
        <div class="card-header">
          <h3>Marker-Dichte entlang des Verlaufs</h3>
          <span class="pill-label">msgIndex &amp; Fenster</span>
        </div>
        <div class="chart-container">
          <canvas id="markerTimelineChart"></canvas>
        </div>
      </div>
    </div>

    <!-- Rechte Seite: Input & psychologische Linsen -->
    <div class="card">
      <div class="card-header">
        <h3>Input &amp; qualitatives Profil</h3>
        <span class="pill-label">JSON aus deinen Skills</span>
      </div>

      <div class="input-grid">
        <div>
          <label class="kpi-label" for="emotionJson">
            Emotion Dynamics JSON
          </label>
          <textarea id="emotionJson" placeholder='Füge hier das JSON aus dem Skill "emotion-dynamics-deep-insight" ein (inkl. "input_meta", "utterance_states", "ued_metrics", "psychological_lenses", …).'></textarea>
          <div id="emotionError" class="error"></div>
        </div>

        <div>
          <label class="kpi-label" for="markerJson">
            Marker-Annotation JSON
          </label>
          <textarea id="markerJson" placeholder='Füge hier das JSON aus dem Skill "marker-annotator" ein (Felder: "sit", "annotations", "clusters", "telemetry").'></textarea>
          <div id="markerError" class="error"></div>
        </div>

        <div class="btn-row">
          <button id="clearBtn" type="button">
            Zurücksetzen
          </button>
          <button id="loadBtn" type="button" class="primary">
            JSONs laden &amp; visualisieren
          </button>
        </div>
      </div>

      <hr style="border-color: rgba(30,64,175,0.7); margin: 12px 0;" />

      <div class="two-col">
        <div>
          <div class="list-section">
            <div class="list-section-title">UED-Metriken</div>
            <ul id="uedMetricsList" class="bullet-list">
              <li>Noch keine UED-Metriken geladen.</li>
            </ul>
          </div>
        </div>
        <div>
          <div class="list-section">
            <div class="list-section-title">Psychologische Linsen</div>
            <ul id="lensesList" class="bullet-list">
              <li>Noch keine qualitativen Beschreibungen geladen.</li>
            </ul>
          </div>
        </div>
      </div>

      <div style="margin-top: 10px;">
        <div class="list-section-title">Marker-Telemetrie</div>
        <ul id="markerTelemetry" class="meta-list">
          <li>Noch keine Marker-Telemetrie geladen.</li>
        </ul>
      </div>

      <div class="footer">
        Erwartetes Format: wie in den jeweiligen <span class="mono">SKILL.md</span>-Definitionen.
      </div>
    </div>
  </section>
</div>

<script>
  // Chart-Instanzen für spätere Aktualisierung
  let valenceArousalChart = null;
  let discreteEmotionsChart = null;
  let markerLevelsChart = null;
  let markerTimelineChart = null;

  function safeDestroy(chart) {
    if (chart && typeof chart.destroy === "function") {
      chart.destroy();
    }
  }

  function clearErrors() {
    document.getElementById("emotionError").textContent = "";
    document.getElementById("markerError").textContent = "";
  }

  function classifyLevelPill(level) {
    const lvl = (level || "").toString().toLowerCase();
    if (lvl === "high") return "pill-level-high";
    if (lvl === "medium") return "pill-level-medium";
    if (lvl === "low") return "pill-level-low";
    return "";
  }

  function renderKPIs(emotionData, markerData) {
    const kpiGrid = document.getElementById("kpiGrid");
    kpiGrid.innerHTML = "";

    // Emotion Dynamics KPIs
    const utterances = (emotionData && Array.isArray(emotionData.utterance_states))
      ? emotionData.utterance_states
      : [];

    const inputMeta = emotionData && emotionData.input_meta ? emotionData.input_meta : {};
    const nUtterances = utterances.length;

    let homeBaseValence = null;
    let homeBaseArousal = null;
    let variabilityLevel = null;
    let emotionalIntensity = null;

    const ued = emotionData && emotionData.ued_metrics ? emotionData.ued_metrics : {};
    if (ued.home_base) {
      homeBaseValence = ued.home_base.valence;
      homeBaseArousal = ued.home_base.arousal;
    }
    if (ued.variability && ued.variability.level) {
      variabilityLevel = ued.variability.level;
    }
    // optional Felder wie "emotional_intensity", "emotional_saturation" etc.
    Object.keys(ued).forEach((key) => {
      if (!emotionalIntensity && ued[key] && ued[key].level) {
        // erster Metrik-Level, der wie Intensität/Sättigung interpretiert werden kann
        if (key.toLowerCase().includes("intensity") ||
            key.toLowerCase().includes("saturation")) {
          emotionalIntensity = ued[key].level;
        }
      }
    });

    // Marker KPIs
    const annotations = (markerData && Array.isArray(markerData.annotations))
      ? markerData.annotations
      : [];
    const telemetry = markerData && markerData.telemetry ? markerData.telemetry : {};
    const totalMarkers = typeof telemetry.total_markers === "number"
      ? telemetry.total_markers
      : annotations.length;
    const novelFiltered = typeof telemetry.novel_filtered === "number"
      ? telemetry.novel_filtered
      : null;
    const sit = typeof markerData?.sit === "number" ? markerData.sit : null;

    // Card helper
    function addKPI({ label, value, sub, pill }) {
      const card = document.createElement("div");
      card.className = "kpi-card";

      const labelEl = document.createElement("div");
      labelEl.className = "kpi-label";
      labelEl.textContent = label;

      const valueEl = document.createElement("div");
      valueEl.className = "kpi-value";
      valueEl.textContent = value;

      const subEl = document.createElement("div");
      subEl.className = "kpi-sub";
      subEl.textContent = sub || "";

      card.appendChild(labelEl);
      card.appendChild(valueEl);
      card.appendChild(subEl);

      if (pill) {
        const pillEl = document.createElement("div");
        pillEl.className = "kpi-pill";
        pillEl.textContent = pill;
        card.appendChild(pillEl);
      }

      kpiGrid.appendChild(card);
    }

    addKPI({
      label: "Utterances",
      value: nUtterances || "0",
      sub: inputMeta.text_type
        ? `Texttyp: ${inputMeta.text_type}`
        : "Keine Metadaten zu Texttyp gefunden.",
      pill: inputMeta.language ? `Sprache: ${inputMeta.language}` : "meta"
    });

    addKPI({
      label: "Home Base (Valenz / Arousal)",
      value:
        homeBaseValence != null && homeBaseArousal != null
          ? `${homeBaseValence.toFixed(2)} / ${homeBaseArousal.toFixed(2)}`
          : "n/a",
      sub:
        ued.home_base && ued.home_base.description
          ? ued.home_base.description
          : "Keine Home-Base-Beschreibung vorhanden.",
      pill: variabilityLevel ? `Variabilität: ${variabilityLevel}` : "Variabilität: n/a"
    });

    addKPI({
      label: "Marker gesamt",
      value: totalMarkers != null ? String(totalMarkers) : "0",
      sub:
        novelFiltered != null
          ? `Davon als novel gefiltert: ${novelFiltered}`
          : "Keine Novelty-Daten im Telemetry-Block.",
      pill: sit != null ? `SIT: ${sit.toFixed(2)}` : "SIT: n/a"
    });

    addKPI({
      label: "Emotionale Intensität",
      value: emotionalIntensity ? emotionalIntensity : "n/a",
      sub: "Level aus UED-Metriken (Interpretation je nach Skill-Output).",
      pill: emotionalIntensity ? "Skalenwert geladen" : "Skalenwert fehlt"
    });
  }

  function renderEmotionCharts(emotionData) {
    const utterances = (emotionData && Array.isArray(emotionData.utterance_states))
      ? emotionData.utterance_states
      : [];

    const labels = utterances.map((u, idx) =>
      u.order_index != null ? u.order_index : u.id != null ? u.id : idx + 1
    );
    const valence = utterances.map((u) =>
      typeof u.valence === "number" ? u.valence : null
    );
    const arousal = utterances.map((u) =>
      typeof u.arousal === "number" ? u.arousal : null
    );
    const dominance = utterances.map((u) =>
      typeof u.dominance === "number" ? u.dominance : null
    );

    // Aggregierte diskrete Emotionen
    const emotionSums = {};
    let countWithDiscrete = 0;
    utterances.forEach((u) => {
      if (!u.discrete_emotions) return;
      let hadAny = false;
      Object.entries(u.discrete_emotions).forEach(([name, value]) => {
        if (typeof value === "number") {
          emotionSums[name] = (emotionSums[name] || 0) + value;
          hadAny = true;
        }
      });
      if (hadAny) countWithDiscrete += 1;
    });

    const discreteLabels = Object.keys(emotionSums);
    const discreteValues = discreteLabels.map((name) =>
      countWithDiscrete > 0 ? emotionSums[name] / countWithDiscrete : 0
    );

    // Charts zerstören und neu zeichnen
    safeDestroy(valenceArousalChart);
    safeDestroy(discreteEmotionsChart);

    const ctx1 = document.getElementById("valenceArousalChart").getContext("2d");
    valenceArousalChart = new Chart(ctx1, {
      type: "line",
      data: {
        labels,
        datasets: [
          {
            label: "Valenz",
            data: valence,
            borderWidth: 2,
            tension: 0.25,
          },
          {
            label: "Arousal",
            data: arousal,
            borderWidth: 2,
            tension: 0.25,
          },
          {
            label: "Dominanz",
            data: dominance,
            borderWidth: 2,
            borderDash: [4, 4],
            tension: 0.25,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: "#e5e7eb",
            },
          },
        },
        scales: {
          x: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
          y: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
        },
      },
    });

    const ctx2 = document.getElementById("discreteEmotionsChart").getContext("2d");
    discreteEmotionsChart = new Chart(ctx2, {
      type: "bar",
      data: {
        labels: discreteLabels,
        datasets: [
          {
            label: "Durchschnittlicher Intensitätswert",
            data: discreteValues,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#e5e7eb" },
          },
        },
        scales: {
          x: {
            ticks: { color: "#9ca3af", maxRotation: 60, minRotation: 40 },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
          y: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
        },
      },
    });
  }

  function renderUEDandLenses(emotionData) {
    const uedList = document.getElementById("uedMetricsList");
    const lensesList = document.getElementById("lensesList");

    uedList.innerHTML = "";
    lensesList.innerHTML = "";

    const ued = emotionData && emotionData.ued_metrics ? emotionData.ued_metrics : {};
    const lenses =
      emotionData && emotionData.psychological_lenses
        ? emotionData.psychological_lenses
        : {};

    const uedKeys = Object.keys(ued);
    if (uedKeys.length === 0) {
      uedList.innerHTML = "<li>Keine UED-Metriken im JSON gefunden.</li>";
    } else {
      uedKeys.forEach((key) => {
        const metric = ued[key] || {};
        const li = document.createElement("li");
        const level = metric.level;
        const descr = metric.description || metric.comment || "";
        const pillClass = classifyLevelPill(level);

        li.innerHTML = `
          <span class="mono">${key}</span>
          ${
            level
              ? `<span class="pill-label ${pillClass}" style="margin-left:6px;">${level}</span>`
              : ""
          }
          ${descr ? `<div style="margin-left:4px;">${descr}</div>` : ""}
        `;
        uedList.appendChild(li);
      });
    }

    const lensKeys = Object.keys(lenses);
    if (lensKeys.length === 0) {
      lensesList.innerHTML =
        "<li>Keine psychologischen Linsen im JSON gefunden.</li>";
    } else {
      lensKeys.forEach((key) => {
        const val = lenses[key];
        const li = document.createElement("li");
        if (Array.isArray(val)) {
          li.innerHTML = `
            <strong>${key}:</strong>
            <ul class="bullet-list" style="margin-top:4px;">
              ${val.map((item) => `<li>${item}</li>`).join("")}
            </ul>
          `;
        } else {
          li.innerHTML = `<strong>${key}:</strong> ${val}`;
        }
        lensesList.appendChild(li);
      });
    }
  }

  function renderMarkerTelemetry(markerData) {
    const container = document.getElementById("markerTelemetry");
    container.innerHTML = "";

    const telemetry =
      markerData && markerData.telemetry ? markerData.telemetry : {};
    const sit =
      typeof markerData?.sit === "number" ? markerData.sit : null;
    const annotations = Array.isArray(markerData?.annotations)
      ? markerData.annotations
      : [];

    if (
      Object.keys(telemetry).length === 0 &&
      sit == null &&
      annotations.length === 0
    ) {
      container.innerHTML =
        "<li>Noch keine Marker-Telemetrie im JSON gefunden.</li>";
      return;
    }

    const totalMarkers =
      typeof telemetry.total_markers === "number"
        ? telemetry.total_markers
        : annotations.length;

    const novelFiltered =
      typeof telemetry.novel_filtered === "number"
        ? telemetry.novel_filtered
        : null;

    const li1 = document.createElement("li");
    li1.innerHTML = `<strong>Marker gesamt:</strong> ${totalMarkers}`;
    container.appendChild(li1);

    if (novelFiltered != null) {
      const li2 = document.createElement("li");
      li2.innerHTML = `<strong>Als novel gefiltert:</strong> ${novelFiltered}`;
      container.appendChild(li2);
    }

    if (sit != null) {
      const li3 = document.createElement("li");
      li3.innerHTML = `<strong>Style-Intensity-Threshold (SIT):</strong> ${sit.toFixed(
        2
      )}`;
      container.appendChild(li3);
    }

    if (telemetry.other_stats) {
      const li4 = document.createElement("li");
      li4.innerHTML =
        "<strong>Weitere Telemetrie:</strong> " +
        JSON.stringify(telemetry.other_stats);
      container.appendChild(li4);
    }
  }

  function renderMarkerCharts(markerData) {
    const annotations = Array.isArray(markerData?.annotations)
      ? markerData.annotations
      : [];
    const clusters = Array.isArray(markerData?.clusters)
      ? markerData.clusters
      : [];

    // Verteilung nach Level
    const levelCounts = {};
    // Marker pro msgIndex
    const msgCounts = {};

    annotations.forEach((a) => {
      const lvl = a.level || "UNKNOWN";
      levelCounts[lvl] = (levelCounts[lvl] || 0) + 1;

      const mi =
        typeof a.msgIndex === "number" ? a.msgIndex : null;
      if (mi != null) {
        msgCounts[mi] = (msgCounts[mi] || 0) + 1;
      }
    });

    // Clusters als Zusatz-Info über Fensterlänge
    clusters.forEach((c) => {
      if (!Array.isArray(c.window)) return;
      const size = c.window.length;
      const key = `CLUSTER_${size}`;
      levelCounts[key] = (levelCounts[key] || 0) + 1;
    });

    const levelLabels = Object.keys(levelCounts);
    const levelValues = levelLabels.map((l) => levelCounts[l]);

    const msgIndices = Object.keys(msgCounts)
      .map((k) => parseInt(k, 10))
      .sort((a, b) => a - b);
    const msgValues = msgIndices.map((k) => msgCounts[k]);

    // Charts zerstören & neu anlegen
    safeDestroy(markerLevelsChart);
    safeDestroy(markerTimelineChart);

    const ctx1 = document.getElementById("markerLevelsChart").getContext("2d");
    markerLevelsChart = new Chart(ctx1, {
      type: "bar",
      data: {
        labels: levelLabels,
        datasets: [
          {
            label: "Anzahl Marker / Cluster",
            data: levelValues,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#e5e7eb" },
          },
        },
        scales: {
          x: {
            ticks: { color: "#9ca3af", maxRotation: 40, minRotation: 20 },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
          y: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
        },
      },
    });

    const ctx2 = document.getElementById("markerTimelineChart").getContext("2d");
    markerTimelineChart = new Chart(ctx2, {
      type: "line",
      data: {
        labels: msgIndices,
        datasets: [
          {
            label: "Marker pro msgIndex",
            data: msgValues,
            borderWidth: 2,
            tension: 0.25,
          },
        ],
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: { color: "#e5e7eb" },
          },
        },
        scales: {
          x: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
          y: {
            ticks: { color: "#9ca3af" },
            grid: { color: "rgba(31,41,55,0.5)" },
          },
        },
      },
    });
  }

  document.getElementById("loadBtn").addEventListener("click", () => {
    clearErrors();

    const emotionRaw = document.getElementById("emotionJson").value.trim();
    const markerRaw = document.getElementById("markerJson").value.trim();

    let emotionData = null;
    let markerData = null;

    if (emotionRaw) {
      try {
        emotionData = JSON.parse(emotionRaw);
      } catch (err) {
        document.getElementById("emotionError").textContent =
          "Emotion Dynamics JSON konnte nicht geparst werden: " + err.message;
      }
    }

    if (markerRaw) {
      try {
        markerData = JSON.parse(markerRaw);
      } catch (err) {
        document.getElementById("markerError").textContent =
          "Marker-JSON konnte nicht geparst werden: " + err.message;
      }
    }

    // Wenn beides leer oder fehlerhaft, kurze Rückmeldung
    if (!emotionData && !markerData) {
      if (!emotionRaw && !markerRaw) {
        document.getElementById("emotionError").textContent =
          "Bitte mindestens ein JSON-Objekt einfügen.";
      }
      return;
    }

    renderKPIs(emotionData || {}, markerData || {});
    if (emotionData) {
      renderEmotionCharts(emotionData);
      renderUEDandLenses(emotionData);
    }
    if (markerData) {
      renderMarkerTelemetry(markerData);
      renderMarkerCharts(markerData);
    }
  });

  document.getElementById("clearBtn").addEventListener("click", () => {
    document.getElementById("emotionJson").value = "";
    document.getElementById("markerJson").value = "";
    clearErrors();

    // Reset KPIs & Listen
    const kpiGrid = document.getElementById("kpiGrid");
    kpiGrid.innerHTML = `
      <div class="kpi-card">
        <div class="kpi-label">Hinweis</div>
        <div class="kpi-value">Noch keine Daten geladen</div>
        <div class="kpi-sub">
          Füge unten deine JSON-Outputs aus den Skills ein und klicke
          <strong>„JSONs laden &amp; visualisieren“</strong>.
        </div>
      </div>
    `;

    document.getElementById("uedMetricsList").innerHTML =
      "<li>Noch keine UED-Metriken geladen.</li>";
    document.getElementById("lensesList").innerHTML =
      "<li>Noch keine psychologischen Linsen geladen.</li>";
    document.getElementById("markerTelemetry").innerHTML =
      "<li>Noch keine Marker-Telemetrie geladen.</li>";

    safeDestroy(valenceArousalChart);
    safeDestroy(discreteEmotionsChart);
    safeDestroy(markerLevelsChart);
    safeDestroy(markerTimelineChart);
  });
</script>
</body>
</html>
Logisch scheint mir: Du kannst dieses HTML als emotion-marker-dashboard.html speichern, im Browser öffnen und dann direkt die JSON-Ausgaben deiner beiden Skills reinkopieren. So bleibt alles streng an den definierten Output-Formaten orientiert – und du bekommst eine ziemlich klare, „shipbare“ Visualisierungsschicht obendrauf.