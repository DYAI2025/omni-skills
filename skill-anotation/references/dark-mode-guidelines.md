# Dark-Mode Guidelines

Vollständige Implementierungsrichtlinien für automatisches und manuelles Theme-Switching.

## Übersicht

Das Annotation-System unterstützt drei Modi:

1. **Auto (Default)**: Folgt `prefers-color-scheme: dark`
2. **Light (Manuell)**: Erzwingt helles Design
3. **Dark (Manuell)**: Erzwingt dunkles Design

## Automatisches Theme-Switching

Basiert auf Browser-Einstellung via CSS Media Query:

```css
:root {
  /* Light-Mode als Default */
  --ld-bg: #ffffff;
  --ld-fg: #0b1020;
  --ld-ato: #7c3aed;
  --ld-sem: #0ea5e9;
  --ld-clu: #f59e0b;
  --ld-mema: #ef4444;
  --ld-outline: rgba(17, 24, 39, 0.16);
  --ld-shadow: rgba(0, 0, 0, 0.12);
}

@media (prefers-color-scheme: dark) {
  :root {
    /* Dark-Mode überschreibt */
    --ld-bg: #0b1020;
    --ld-fg: #e5e7eb;
    --ld-ato: #a78bfa;
    --ld-sem: #67e8f9;
    --ld-clu: #fbbf24;
    --ld-mema: #f87171;
    --ld-outline: rgba(229, 231, 235, 0.28);
    --ld-shadow: rgba(255, 255, 255, 0.12);
  }
}
```

## Manuelles Theme-Switching

Wird über Class-Toggling auf `<body>` oder `:root` gesteuert:

```javascript
// Light-Mode erzwingen
document.documentElement.classList.add("ld-light");
document.documentElement.classList.remove("ld-dark");

// Dark-Mode erzwingen
document.documentElement.classList.add("ld-dark");
document.documentElement.classList.remove("ld-light");

// Auto-Mode aktivieren (beide Classes entfernen)
document.documentElement.classList.remove("ld-light", "ld-dark");
```

**CSS-Regeln** (höhere Spezifität als Media Query):

```css
.ld-light {
  --ld-bg: #ffffff;
  --ld-fg: #0b1020;
  --ld-ato: #7c3aed;
  --ld-sem: #0ea5e9;
  --ld-clu: #f59e0b;
  --ld-mema: #ef4444;
  --ld-outline: rgba(17, 24, 39, 0.16);
  --ld-shadow: rgba(0, 0, 0, 0.12);
}

.ld-dark {
  --ld-bg: #0b1020;
  --ld-fg: #e5e7eb;
  --ld-ato: #a78bfa;
  --ld-sem: #67e8f9;
  --ld-clu: #fbbf24;
  --ld-mema: #f87171;
  --ld-outline: rgba(229, 231, 235, 0.28);
  --ld-shadow: rgba(255, 255, 255, 0.12);
}
```

## In-Page-Panel UI

Der SIT-Panel enthält Theme-Buttons:

```html
<div id="ld-sit-panel">
  <div class="ld-theme-buttons">
    <button class="ld-theme-btn" data-theme="auto">Auto</button>
    <button class="ld-theme-btn" data-theme="light">☀️ Light</button>
    <button class="ld-theme-btn" data-theme="dark">🌙 Dark</button>
  </div>
  <!-- ... -->
</div>
```

**Event-Handler**:

```javascript
document.querySelectorAll(".ld-theme-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const theme = btn.dataset.theme;

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

    updateActiveButton(theme);
  });
});

function updateActiveButton(activeTheme) {
  document.querySelectorAll(".ld-theme-btn").forEach((btn) => {
    btn.classList.toggle("ld-active", btn.dataset.theme === activeTheme);
  });
}
```

## Persistenz (localStorage)

Benutzerwahl speichern und beim Laden wiederherstellen:

```javascript
function initTheme() {
  const savedTheme = localStorage.getItem("ld-theme") || "auto";

  if (savedTheme === "light") {
    document.documentElement.classList.add("ld-light");
  } else if (savedTheme === "dark") {
    document.documentElement.classList.add("ld-dark");
  }
  // Bei 'auto' keine Classes setzen

  updateActiveButton(savedTheme);
}

// Beim Laden ausführen
initTheme();
```

## Highlight-Komponenten

Alle Marker-Highlights verwenden CSS-Variablen:

```css
.ld-mark {
  background-color: var(--ld-marker-bg); /* Dynamisch gesetzt */
  color: var(--ld-fg);
  border: 1px solid var(--ld-outline);
  box-shadow: 0 1px 2px var(--ld-shadow);
}

.ld-badge {
  background: var(--ld-marker-color); /* Volle Deckkraft */
  color: var(--ld-bg); /* Invertiert */
  border-radius: 9999px;
  padding: 2px 6px;
  font-size: 11px;
  font-weight: 600;
}
```

**JavaScript-seitige Farb-Logik**:

```javascript
function applyHighlight(span, level) {
  const isDark =
    document.documentElement.classList.contains("ld-dark") ||
    (window.matchMedia("(prefers-color-scheme: dark)").matches &&
      !document.documentElement.classList.contains("ld-light"));

  const color = isDark ? DARK_COLORS[level] : LIGHT_COLORS[level];
  const alpha = isDark ? 0.46 : 0.32;

  span.style.setProperty(
    "--ld-marker-bg",
    `${color}${Math.round(alpha * 255).toString(16)}`
  );
  span.style.setProperty("--ld-marker-color", color);
}
```

## Overlapping-Highlights (Striped Gradients)

Bei überlappenden Markern müssen Farben auch im Dark-Mode korrekt kombiniert werden:

```javascript
function gradientFor(levels, isDark) {
  const colors = isDark ? DARK_COLORS : LIGHT_COLORS;
  const alpha = isDark ? 0.46 : 0.32;

  const stops = [];
  levels.forEach((level, i) => {
    const color = colors[level];
    const start = i * 6;
    const end = (i + 1) * 6;
    stops.push(`${color}${Math.round(alpha * 255).toString(16)} ${start}px`);
    stops.push(`${color}${Math.round(alpha * 255).toString(16)} ${end}px`);
  });

  return `repeating-linear-gradient(135deg, ${stops.join(", ")})`;
}
```

## SIT-Panel Styling

Der Panel selbst passt sich dem Theme an:

```css
#ld-sit-panel {
  background: var(--ld-bg);
  color: var(--ld-fg);
  border: 1px solid var(--ld-outline);
  box-shadow: 0 4px 12px var(--ld-shadow);
  border-radius: 8px;
  padding: 12px 16px;
  z-index: 999999;
}

.ld-theme-btn {
  background: var(--ld-bg);
  color: var(--ld-fg);
  border: 1px solid var(--ld-outline);
  padding: 4px 10px;
  cursor: pointer;
  transition: background 0.2s, color 0.2s;
}

.ld-theme-btn:hover {
  background: var(--ld-outline);
}

.ld-theme-btn.ld-active {
  background: var(--ld-ato);
  color: var(--ld-bg);
  border-color: var(--ld-ato);
}
```

## Accessibility

1. **Forced-Colors Mode** (Windows High Contrast):

```css
@media (forced-colors: active) {
  .ld-mark {
    outline: 2px solid CanvasText;
    background: none;
  }
}
```

2. **Prefers-Contrast** (erhöhter Kontrast):

```css
@media (prefers-contrast: more) {
  :root {
    --ld-outline: rgba(17, 24, 39, 0.32); /* Dickere Outlines */
  }
  .ld-dark {
    --ld-outline: rgba(229, 231, 235, 0.44);
  }
}
```

3. **Reduced Motion**:

```css
@media (prefers-reduced-motion: reduce) {
  .ld-theme-btn,
  .ld-mark {
    transition: none;
  }
}
```

## Testing Checklist

**Browser-Dev-Tools**:

- [ ] Chrome DevTools → Rendering → Emulate: `prefers-color-scheme: dark`
- [ ] Firefox DevTools → Inspector → :dark Pseudo-Class
- [ ] Safari → Develop → Experimental Features → Dark Mode

**Manuelle Tests**:

- [ ] Auto-Mode: OS-Theme ändern (Light ↔ Dark)
- [ ] Light-Button: Erzwingt helles Design unabhängig von OS
- [ ] Dark-Button: Erzwingt dunkles Design unabhängig von OS
- [ ] localStorage-Persistenz: Seite neu laden, Theme bleibt erhalten

**Contrast Ratios** (alle Level müssen AA-Pass haben):

- [ ] Light-Mode: Alle Marker auf weißem Hintergrund ≥ 3:1
- [ ] Dark-Mode: Alle Marker auf #0b1020 ≥ 3:1
- [ ] Badge-Text: Auf Marker-Farbe ≥ 4.5:1

**Overlapping**:

- [ ] Streifen im Light-Mode korrekt differenzierbar
- [ ] Streifen im Dark-Mode korrekt differenzierbar
- [ ] Outline bleibt sichtbar bei Overlaps

## Debugging

**Console-Helper**:

```javascript
console.log(
  "Current Theme:",
  document.documentElement.classList.contains("ld-light")
    ? "Light"
    : document.documentElement.classList.contains("ld-dark")
    ? "Dark"
    : "Auto"
);

console.log(
  "OS prefers dark:",
  window.matchMedia("(prefers-color-scheme: dark)").matches
);

console.log("Computed variables:", {
  bg: getComputedStyle(document.documentElement).getPropertyValue("--ld-bg"),
  ato: getComputedStyle(document.documentElement).getPropertyValue("--ld-ato"),
});
```

## Best Practices

1. **Nie hardcoded Farben**: Immer CSS-Variablen verwenden
2. **Alpha-Werte separat**: Transparenz in JavaScript setzen, nicht im CSS
3. **Spezifität beachten**: `.ld-dark` > `@media (prefers-color-scheme: dark)` > `:root`
4. **Fallback**: Wenn CSS-Variablen nicht laden, Graustufen als Fallback
5. **Performance**: Theme-Switching sollte < 16ms dauern (1 Frame)
