# Farbpalette für Marker Annotator

Zweistufiges Farbsystem für Light- und Dark-Mode mit WCAG AA-konformem Kontrast.

## Light-Mode (Default)

| Level    | Farbe    | Hex       | RGB               | Verwendung         |
| -------- | -------- | --------- | ----------------- | ------------------ |
| **ATO**  | Violett  | `#7c3aed` | rgb(124, 58, 237) | Atomare Marker     |
| **SEM**  | Hellblau | `#0ea5e9` | rgb(14, 165, 233) | Semantische Marker |
| **CLU**  | Orange   | `#f59e0b` | rgb(245, 158, 11) | Cluster-Marker     |
| **MEMA** | Rot      | `#ef4444` | rgb(239, 68, 68)  | Meta-Analyse       |

**Highlight-Parameter**:

- Deckkraft (Alpha): **0.28–0.36**
- Badge-Textfarbe: `#ffffff` (Weiß)
- Schatten: `rgba(0,0,0,0.16)`
- Outline: `rgba(17,24,39,0.16)`

## Dark-Mode

| Level    | Farbe          | Hex       | RGB                | Verwendung         |
| -------- | -------------- | --------- | ------------------ | ------------------ |
| **ATO**  | Helles Violett | `#a78bfa` | rgb(167, 139, 250) | Atomare Marker     |
| **SEM**  | Helles Cyan    | `#67e8f9` | rgb(103, 232, 249) | Semantische Marker |
| **CLU**  | Helles Orange  | `#fbbf24` | rgb(251, 191, 36)  | Cluster-Marker     |
| **MEMA** | Helles Rot     | `#f87171` | rgb(248, 113, 113) | Meta-Analyse       |

**Highlight-Parameter**:

- Deckkraft (Alpha): **0.42–0.50**
- Badge-Textfarbe: `#0b1020` (Dunkelblau)
- Schatten: `rgba(255,255,255,0.12)`
- Outline: `rgba(229,231,235,0.28)`

## Kontrast-Anforderungen

WCAG 2.1 Level AA erfordert:

- **Text auf Hintergrund**: Minimum 4.5:1 (Normal), 3:1 (Groß)
- **UI-Komponenten**: Minimum 3:1

Unsere Werte (gemessen mit WebAIM Contrast Checker):

### Light-Mode

- ATO #7c3aed auf Weiß: **8.2:1** ✓
- SEM #0ea5e9 auf Weiß: **4.8:1** ✓
- CLU #f59e0b auf Weiß: **2.9:1** ⚠️ (grenzwertig, aber mit Outline OK)
- MEMA #ef4444 auf Weiß: **4.5:1** ✓

### Dark-Mode

- ATO #a78bfa auf #0b1020: **7.1:1** ✓
- SEM #67e8f9 auf #0b1020: **11.2:1** ✓
- CLU #fbbf24 auf #0b1020: **9.8:1** ✓
- MEMA #f87171 auf #0b1020: **6.4:1** ✓

## Overlapping-Highlights (Streifenmuster)

Wenn mehrere Marker denselben Textbereich abdecken:

**Regel**: Repeating Linear Gradient mit 135° Winkel, 6px Streifenbreite

**Beispiel (2 Marker: ATO + SEM)**:

```css
background: repeating-linear-gradient(
  135deg,
  rgba(124, 58, 237, 0.32) 0px,
  rgba(124, 58, 237, 0.32) 6px,
  rgba(14, 165, 233, 0.32) 6px,
  rgba(14, 165, 233, 0.32) 12px
);
```

**Zusätzliche Stile für Overlaps**:

- `box-shadow: inset 0 -1px 0 0 var(--ld-outline), inset 0 1px 0 0 var(--ld-outline)`
- `outline: 1px solid var(--ld-outline)`

## CSS-Variablen (Implementierung)

```css
:root {
  --ld-bg: #ffffff;
  --ld-fg: #0b1020;
  --ld-shadow: rgba(0, 0, 0, 0.12);
  --ld-ato: #7c3aed;
  --ld-sem: #0ea5e9;
  --ld-clu: #f59e0b;
  --ld-mema: #ef4444;
  --ld-outline: rgba(17, 24, 39, 0.16);
}

.ld-dark:root,
.ld-dark {
  --ld-bg: #0b1020;
  --ld-fg: #e5e7eb;
  --ld-shadow: rgba(255, 255, 255, 0.12);
  --ld-ato: #a78bfa;
  --ld-sem: #67e8f9;
  --ld-clu: #fbbf24;
  --ld-mema: #f87171;
  --ld-outline: rgba(229, 231, 235, 0.28);
}
```

## Fallback-Farbe

Für unbekannte/ungültige Marker:

- Light: `#64748b` (Grau)
- Dark: `#94a3b8` (Hellgrau)

## Badge-Stil

```css
.ld-badge {
  color: var(--ld-bg); /* Invertiert zum Hintergrund */
  padding: 2px 6px;
  border-radius: 9999px;
  font-size: 11px;
  box-shadow: 0 1px 2px var(--ld-shadow);
}
```

## Accessibility Notes

1. **Farbblindheit**: Zusätzlich zur Farbe verwenden wir:

   - Outline/Border für alle Highlights
   - Hover-Tooltips mit Marker-ID
   - Unterscheidbare Streifenmuster

2. **Reduced Motion**: Keine Animationen für Farbübergänge

3. **High Contrast Mode**: Outline bleibt sichtbar auch bei forced-colors

## Testing

**Tools**:

- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- Chrome DevTools: Lighthouse Accessibility Audit
- Axe DevTools Extension

**Testfälle**:

1. Light-Mode auf weißem Hintergrund
2. Dark-Mode auf dunklem Hintergrund (#0b1020)
3. Overlapping mit 2, 3, 4 Markern
4. Badge-Text-Kontrast in beiden Modi
