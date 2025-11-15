---
name: marker-annotator
description: Subskill zur Marker Engine für strikt markerbasierte JSON-Annotationen mit Farbhervorhebung; enthält Overlapping-Span-Merging, Dark-Mode-Farben und eine In-Page-SIT-UI (ohne Popup). Erzwingt ZIP-Entpacken, Supabase-Nutzung und Anti-Halluzination (Only-Original-Marker + 3×-Schwelle).
---

## Wann verwenden

- Wenn Markertreffer präzise als Spannen annotiert und robust visualisiert werden sollen (inkl. Überlappungen).
- Wenn Nutzer SIT (0.0–1.0) direkt auf der Seite einstellen möchten, ohne Browser-Popup.
- Wenn Dark-Mode-Unterstützung und AA-Kontrast benötigt werden.

## Workflow/Anweisungen (Kurz)

1. **Engine-Ergebnisse abrufen**: Via `/annotate` (server.py) mit `{ texts[], sit }`.
2. **IDs gegen Katalog validieren**: Only-Original-Marker. Novelty nur als `post_analysis.novel_candidates` wenn ≥3× Threshold erreicht.
3. **Overlapping-Span-Merging**: Pro Nachricht Segmentierung über alle Start/End-Grenzen; zusammenhängende/überlappende Spannen werden zu Segmenten verschmolzen. Mehrfachabdeckung wird als Streifenverlauf visualisiert.
4. **Dark-Mode**: Palette wechselt automatisch per `prefers-color-scheme: dark` und kann manuell über In-Page-UI überschrieben werden.
5. **In-Page-SIT-UI**: Schwebendes Panel (Slider + Buttons) steuert SIT, Dark/Light/Auto und (De)Aktivierung der Highlights.

## Eingaben

- **texts**: Array von Strings (max. 50 Nachrichten)
- **sit**: Float 0.0–1.0 (Style-Intensity-Threshold)
- **marker_source**: `supabase` (empfohlen) | `local`

## Ausgabeformat

Siehe `references/annotation-schema.json`. Die Extension reinterpretiert die Level-Farben clientseitig abhängig vom Theme.

Beispiel:

```json
{
  "sit": 0.7,
  "annotations": [
    {
      "msgIndex": 0,
      "start": 4,
      "end": 12,
      "level": "ATO",
      "id": "ATO_UNCERTAINTY_PHRASE",
      "label": "not sure",
      "color": "#7c3aed"
    }
  ],
  "clusters": [
    {
      "id": "CLU_INTUITION_UNCERTAINTY",
      "level": "CLU",
      "window": ["m1", "m2"]
    }
  ],
  "telemetry": {
    "total_markers": 12,
    "novel_filtered": 0
  }
}
```

## Beispiele

**Beispiel 1: Einfache Annotation**

Input: `["I'm not sure... maybe we should postpone this."]`, SIT: 0.7

Output: ATOs für "not sure", "maybe", "postpone" → SEM_UNCERTAINTY_TONING

**Beispiel 2: Überlappende Spannen**

Input: `["I'm really not sure at all"]`, SIT: 0.8

Falls "not sure" (ATO_UNCERTAINTY) und "really not sure" (SEM_UNCERTAINTY_TONING) beide matchen:

- Segmentierung: [0-4: "I'm "], [4-21: overlap], [21-28: " at all"]
- Segment [4-21] wird als Streifen-Gradient (Violett + Hellblau) dargestellt

**Beispiel 3: Dark-Mode Toggle**

User klickt "Dark" in In-Page-UI → Theme wechselt zu `--ld-dark` Variablen, Farben ändern sich zu helleren Varianten (z.B. ATO: #a78bfa statt #7c3aed)

## Qualitätssicherung

**Annotationen**:

- [ ] Overlaps korrekt gemerged (Segmentierung an allen Grenzpunkten)
- [ ] Spans decken exakt den erkannten Text ab (keine Halluzination)
- [ ] Nur Marker aus offiziellem Katalog (Supabase/ZIP)

**Visualisierung**:

- [ ] Farbkontrast ≥ AA-Standard (WCAG 2.1)
- [ ] Dark-Mode korrekt implementiert (prefers-color-scheme + manuell)
- [ ] Overlaps als Streifen erkennbar

**UI**:

- [ ] SIT-Slider funktioniert (0.0–1.0)
- [ ] Theme-Buttons (Auto/Light/Dark) aktualisieren CSS-Variablen
- [ ] Enable/Disable entfernt Highlights vollständig

**Server**:

- [ ] FastAPI läuft auf Port 8642
- [ ] CORS für Chrome-Extension aktiviert
- [ ] Supabase-Verbindung getestet

## Integration mit Marker Engine

Der Annotator ist ein **Client-Layer** über der Marker Engine:

1. **Marker Engine** (marker-engine-rl): Erkennt ATOs/SEMs/CLUs/MEMAs, exportiert Events
2. **Adapter** (adapter.py): Konvertiert Engine-Events in Annotations mit Spans
3. **Server** (server.py): FastAPI-Endpoint `/annotate` kombiniert Engine + Adapter
4. **Chrome Extension**: Ruft Server auf, visualisiert Annotations mit Overlapping-Support

## Deployment

### Server starten

```bash
export SUPABASE_URL="https://your-project.supabase.co"
export SUPABASE_ANON_KEY="your-anon-key"
python -m pip install fastapi uvicorn pydantic requests
python skill-anotation/scripts/python/server.py
```

Server läuft auf `http://127.0.0.1:8642`

### Extension installieren

1. Chrome: `chrome://extensions`
2. "Entwicklermodus" aktivieren
3. "Entpackte Erweiterung laden"
4. Ordner wählen: `skill-anotation/chrome-extension/`

### Nutzung

1. Beliebige Webseite öffnen
2. In-Page-Panel erscheint rechts unten
3. SIT einstellen (z.B. 0.7)
4. "Analyse" klicken
5. Texte werden highlighted mit Farben/Badges

## Technische Details

### Overlapping-Span-Algorithmus

```javascript
function segmentize(spans) {
  // 1. Sammle alle unique Start/End-Punkte
  const points = new Set();
  spans.forEach((s) => {
    points.add(s.start);
    points.add(s.end);
  });

  // 2. Sortiere Punkte
  const sorted = Array.from(points).sort((a, b) => a - b);

  // 3. Bilde Segmente zwischen benachbarten Punkten
  const segments = [];
  for (let i = 0; i < sorted.length - 1; i++) {
    const start = sorted[i],
      end = sorted[i + 1];
    // Finde alle Spans, die dieses Segment abdecken
    const covers = spans.filter((s) => s.start < end && s.end > start);
    if (covers.length) {
      segments.push({ start, end, covers, colors: covers.map((c) => c.color) });
    }
  }
  return segments;
}
```

### Dark-Mode CSS-Variablen

```css
:root {
  --ld-ato: #7c3aed; /* Light */
}
.ld-dark:root {
  --ld-ato: #a78bfa; /* Dark */
}
```

### Streifen-Gradient für Overlaps

```javascript
function gradientFor(colors, dark) {
  if (colors.length === 1) return solid(colors[0], dark);
  // Repeating stripes: 6px breite Streifen
  const stripes = colors.map((c, i) => {
    const pos = i * 6;
    return `${hexAlpha(c, 0.36)} ${pos}px, ${hexAlpha(c, 0.36)} ${pos + 6}px`;
  });
  return `repeating-linear-gradient(135deg, ${stripes.join(", ")})`;
}
```

## Erweiterungen / Roadmap

- [ ] WebSocket-Support für Live-Updates
- [ ] Export-Funktion (JSON/CSV Download)
- [ ] Filter nach Level (nur ATOs, nur SEMs, etc.)
- [ ] Timeline-View für Cluster über Nachrichtensequenzen
- [ ] Performance-Optimierung für >100 Nachrichten
