// content.js – Chrome Extension Content Script für Marker Annotation

const API_URL = "http://127.0.0.1:8642/annotate";

const LIGHT_COLORS = {
  ATO: "#7c3aed",
  SEM: "#0ea5e9",
  CLU: "#f59e0b",
  MEMA: "#ef4444",
};

const DARK_COLORS = {
  ATO: "#a78bfa",
  SEM: "#67e8f9",
  CLU: "#fbbf24",
  MEMA: "#f87171",
};

// State
let currentSIT = 0.5;
let isEnabled = false;
let currentTheme = "auto";

/**
 * Initialisiert Theme aus localStorage
 */
function initTheme() {
  const savedTheme = localStorage.getItem("ld-theme") || "auto";
  currentTheme = savedTheme;

  if (savedTheme === "light") {
    document.documentElement.classList.add("ld-light");
    document.documentElement.classList.remove("ld-dark");
  } else if (savedTheme === "dark") {
    document.documentElement.classList.add("ld-dark");
    document.documentElement.classList.remove("ld-light");
  }
}

/**
 * Prüft, ob Dark-Mode aktiv ist
 */
function isDarkMode() {
  return (
    document.documentElement.classList.contains("ld-dark") ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches &&
      !document.documentElement.classList.contains("ld-light"))
  );
}

/**
 * Erstellt SIT-Panel falls nicht vorhanden
 */
function ensurePanel() {
  if (document.getElementById("ld-sit-panel")) return;

  const panel = document.createElement("div");
  panel.id = "ld-sit-panel";
  panel.innerHTML = `
    <div class="ld-panel-header">
      <span class="ld-panel-title">🎯 Marker Annotator</span>
      <button class="ld-close-btn" id="ld-close-btn">×</button>
    </div>
    
    <div class="ld-theme-buttons">
      <button class="ld-theme-btn" data-theme="auto">Auto</button>
      <button class="ld-theme-btn" data-theme="light">☀️ Light</button>
      <button class="ld-theme-btn" data-theme="dark">🌙 Dark</button>
    </div>
    
    <div class="ld-sit-control">
      <span class="ld-sit-label">SIT:</span>
      <input type="range" class="ld-sit-slider" id="ld-sit-slider" 
             min="0" max="1" step="0.01" value="0.5">
      <span class="ld-sit-value" id="ld-sit-value">0.50</span>
    </div>
    
    <button class="ld-enable-btn" id="ld-enable-btn">Enable Annotation</button>
  `;

  document.body.appendChild(panel);

  // Event-Listener
  document.getElementById("ld-close-btn").addEventListener("click", () => {
    panel.classList.add("ld-hidden");
  });

  document.getElementById("ld-sit-slider").addEventListener("input", (e) => {
    currentSIT = parseFloat(e.target.value);
    document.getElementById("ld-sit-value").textContent = currentSIT.toFixed(2);
  });

  document.getElementById("ld-enable-btn").addEventListener("click", () => {
    isEnabled = !isEnabled;
    const btn = document.getElementById("ld-enable-btn");
    btn.textContent = isEnabled ? "Disable Annotation" : "Enable Annotation";

    if (isEnabled) {
      annotateCurrentPage();
    } else {
      clearAnnotations();
    }
  });

  // Theme-Buttons
  document.querySelectorAll(".ld-theme-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      const theme = btn.dataset.theme;
      currentTheme = theme;

      if (theme === "auto") {
        document.documentElement.classList.remove("ld-light", "ld-dark");
        localStorage.setItem("ld-theme", "auto");
      } else if (theme === "light") {
        document.documentElement.classList.add("ld-light");
        document.documentElement.classList.remove("ld-dark");
        localStorage.setItem("ld-theme", "light");
      } else if (theme === "dark") {
        document.documentElement.classList.add("ld-dark");
        document.documentElement.classList.remove("ld-light");
        localStorage.setItem("ld-theme", "dark");
      }

      updateActiveThemeButton(theme);

      if (isEnabled) {
        annotateCurrentPage();
      }
    });
  });

  updateActiveThemeButton(currentTheme);
}

/**
 * Markiert aktiven Theme-Button
 */
function updateActiveThemeButton(activeTheme) {
  document.querySelectorAll(".ld-theme-btn").forEach((btn) => {
    btn.classList.toggle("ld-active", btn.dataset.theme === activeTheme);
  });
}

/**
 * Sammelt Texte aus der Seite (Paragraphen)
 */
function collectTexts() {
  const paragraphs = document.querySelectorAll("p, h1, h2, h3, h4, h5, h6");
  return Array.from(paragraphs)
    .map((p) => p.textContent.trim())
    .filter((t) => t.length > 0);
}

/**
 * Ruft Annotation-API auf
 */
async function fetchAnnotations(texts, sit) {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ texts, sit }),
    });

    if (!response.ok) {
      throw new Error(`API-Fehler: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Fehler beim Abrufen der Annotationen:", error);
    return null;
  }
}

/**
 * Segmentiert überlappende Spans
 */
function segmentize(spans) {
  const points = new Set();
  spans.forEach((s) => {
    points.add(s.start);
    points.add(s.end);
  });

  const sorted = Array.from(points).sort((a, b) => a - b);
  const segments = [];

  for (let i = 0; i < sorted.length - 1; i++) {
    const start = sorted[i];
    const end = sorted[i + 1];

    const active = spans.filter((s) => s.start <= start && s.end >= end);

    segments.push({
      start,
      end,
      levels: active.map((s) => s.level),
      ids: active.map((s) => s.id),
    });
  }

  return segments;
}

/**
 * Generiert Gradient für überlappende Marker
 */
function gradientFor(levels, dark) {
  const colors = dark ? DARK_COLORS : LIGHT_COLORS;
  const alpha = dark ? 0.46 : 0.32;

  const stops = [];
  levels.forEach((level, i) => {
    const color = colors[level] || (dark ? "#94a3b8" : "#64748b");
    const start = i * 6;
    const end = (i + 1) * 6;

    const alphaHex = Math.round(alpha * 255)
      .toString(16)
      .padStart(2, "0");
    stops.push(`${color}${alphaHex} ${start}px`);
    stops.push(`${color}${alphaHex} ${end}px`);
  });

  return `repeating-linear-gradient(135deg, ${stops.join(", ")})`;
}

/**
 * Highlightet einen Textblock mit Annotationen
 */
function highlightBlock(element, text, spans) {
  if (!spans || spans.length === 0) return;

  const dark = isDarkMode();
  const segments = segmentize(spans);

  let html = "";
  let lastEnd = 0;

  segments.forEach((seg) => {
    if (seg.start > lastEnd) {
      html += escapeHtml(text.substring(lastEnd, seg.start));
    }

    const content = escapeHtml(text.substring(seg.start, seg.end));

    if (seg.levels.length === 0) {
      html += content;
    } else if (seg.levels.length === 1) {
      const level = seg.levels[0];
      const color = (dark ? DARK_COLORS : LIGHT_COLORS)[level];
      const alpha = dark ? 0.46 : 0.32;
      const alphaHex = Math.round(alpha * 255)
        .toString(16)
        .padStart(2, "0");

      html += `<span class="ld-mark" style="background: ${color}${alphaHex}; --ld-marker-color: ${color};" title="${seg.ids.join(
        ", "
      )}">${content}<span class="ld-badge">${level}</span></span>`;
    } else {
      const gradient = gradientFor(seg.levels, dark);
      html += `<span class="ld-mark" style="background: ${gradient};" title="${seg.ids.join(
        ", "
      )}">${content}<span class="ld-badge">${seg.levels.join(
        "+"
      )}</span></span>`;
    }

    lastEnd = seg.end;
  });

  if (lastEnd < text.length) {
    html += escapeHtml(text.substring(lastEnd));
  }

  element.innerHTML = html;
}

/**
 * HTML-Escaping
 */
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

/**
 * Löscht alle Annotationen
 */
function clearAnnotations() {
  document.querySelectorAll(".ld-mark").forEach((mark) => {
    const parent = mark.parentNode;
    parent.replaceChild(document.createTextNode(mark.textContent), mark);
  });
}

/**
 * Annotiert die aktuelle Seite
 */
async function annotateCurrentPage() {
  const texts = collectTexts();
  if (texts.length === 0) {
    console.warn("Keine Texte gefunden");
    return;
  }

  const response = await fetchAnnotations(texts, currentSIT);
  if (!response) {
    console.error("Keine Annotation-Response erhalten");
    return;
  }

  const annotations = response.annotations || [];
  const paragraphs = document.querySelectorAll("p, h1, h2, h3, h4, h5, h6");

  annotations.forEach((ann) => {
    const msgIndex = ann.msgIndex;
    if (msgIndex < paragraphs.length) {
      const element = paragraphs[msgIndex];
      const text = texts[msgIndex];
      const spans = annotations.filter((a) => a.msgIndex === msgIndex);

      highlightBlock(element, text, spans);
    }
  });

  console.log(`✅ ${annotations.length} Annotationen angewandt`);
}

/**
 * Initialisierung
 */
function init() {
  initTheme();
  ensurePanel();
}

// Beim Laden starten
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", init);
} else {
  init();
}
