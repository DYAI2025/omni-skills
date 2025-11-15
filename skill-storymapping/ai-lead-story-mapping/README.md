# AI Lead Story Mapping Sub-Skill

> **Zweck:** Erstellt und pflegt User‑Story‑Maps als Sub‑Skill des AI‑Lead‑Orchestrators; führt Teams von Ziel & Persona über Backbone/Activities und vertikale Priorisierung zum Slicing (MVP/Walking Skeleton) und exportiert testbare Backlog‑Artefakte.

## 📁 Struktur

```
ai-lead-story-mapping/
├── SKILL.md                          # Haupt-Skill-Beschreibung
├── README.md                         # Diese Datei
├── references/                       # Referenzdokumente & Best Practices
│   ├── glossary.md                  # Begriffserklärungen
│   ├── mapping-patterns.md          # Mapping & Cutting Patterns
│   ├── slicing-strategies.md        # Release-Planung & Slicing
│   ├── workshop-facilitation.md     # Workshop-Anleitung
│   └── acceptance-criteria-examples.md
├── scripts/                          # Python-Werkzeuge
│   ├── story_map_validator.py       # Validiert JSON-Format
│   ├── slice_suggester.py           # Generiert Slice-Vorschläge
│   ├── export_backlog_csv.py        # CSV-Export für Priorisierung
│   └── map_to_mermaid.py            # Mermaid-Diagramm-Generator
├── assets/
│   ├── templates/                   # Wiederverwendbare Templates
│   │   ├── story-map-canvas.md
│   │   ├── story-map.json
│   │   ├── story-slice.md
│   │   ├── user-journey.md
│   │   └── ac-template.md
│   └── examples/                    # Vollständige Beispiele
│       ├── example-story-map.json
│       ├── example-backlog.csv
│       └── example-slices.md
```

## 🚀 Quick Start

### 1. Story Map validieren

```bash
python3 scripts/story_map_validator.py assets/examples/example-story-map.json
```

**Output:**

```
[story-map-validator] ✓ Valid: assets/examples/example-story-map.json
  - 2 Activities
  - 4 Steps
  - 4 Stories
```

### 2. Slices vorschlagen

```bash
python3 scripts/slice_suggester.py assets/examples/example-story-map.json --out slices.md
```

Generiert MVP (Walking Skeleton) + Folge-Slices basierend auf Heuristik.

### 3. Backlog exportieren

```bash
python3 scripts/export_backlog_csv.py assets/examples/example-story-map.json --out backlog.csv
```

Exportiert Stories mit allen Feldern für Priorisierung (WSJF, RICE, etc.).

### 4. Visualisierung erstellen

```bash
python3 scripts/map_to_mermaid.py assets/examples/example-story-map.json > storymap.mmd
```

Erzeugt Mermaid-Flowchart für visuelle Darstellung der Journey.

## 📋 Workflow

1. **Framing** → Ziel, Persona, KPIs klären
2. **Backbone** → Aktivitäten horizontal anordnen
3. **Stories sammeln** → Vertikal priorisieren (Must-haves oben)
4. **Map walken** → Lücken & Dependencies aufdecken
5. **Slicing** → MVP + Releases planen
6. **Artefakte erzeugen** → JSON, CSV, Mermaid exportieren

## 🎯 Kernkonzepte

### Horizontal: Backbone (chronologisch)

- Activities = große Schritte der User Journey (3-7)
- Steps = Teilschritte innerhalb einer Activity (3-7)
- Von links nach rechts: Start → Ziel

### Vertikal: Priorität

- Oben: Must-haves (MVP)
- Unten: Nice-to-haves, Alternativen
- "Und" vs. "Oder" Lesen

### Slicing: Release-Planung

- **Slice 1 = MVP/Walking Skeleton**: Minimaler End-to-End-Weg
- **Slice 2+**: Komfort, Alternativen, Optimierungen
- Jede Slice mit Outcomes/Metriken

## 📚 Referenzen

- **glossary.md**: Begriffe wie Activity, Story, MVP, Walking Skeleton
- **mapping-patterns.md**: Von Goal zu Stories, Cutting-Strategien
- **slicing-strategies.md**: MVP-Definition, Release-Planung, Opening/Mid/End-Game
- **workshop-facilitation.md**: Vorbereitung, Ablauf (4h Workshop), Moderations-Tipps
- **acceptance-criteria-examples.md**: Gherkin-Format, 50+ Beispiele nach Pattern

## 🔧 Script-Details

### story_map_validator.py

Validiert JSON gegen Schema:

- Top-Level: product, actor, goal, kpis, activities, stories, version
- Activities mit Steps
- Stories mit ACs, activity_id, step_id
- Prüft Referenzen und Duplikate

### slice_suggester.py

Heuristik:

- MVP = 1 Story pro Step (erste verfügbare)
- Rest aufgeteilt in 2-3 Slices
- Outcomes/Metriken hinzufügen

### export_backlog_csv.py

CSV-Felder:

- id, title, description, depends_on
- actor, goal, activity, step, pattern
- effort, reach, impact, confidence (RICE)
- bv, tc, rr, js (WSJF)

### map_to_mermaid.py

- Subgraph pro Activity
- Nodes = Steps
- Kanten = Reihenfolge
- Styling möglich

## ✅ Validierung & Tests

Alle Scripts wurden getestet:

- ✅ Validator erkennt fehlerhafte JSON
- ✅ Slice Suggester erzeugt korrektes MVP
- ✅ CSV Export enthält alle Felder
- ✅ Mermaid Diagramm ist syntaktisch korrekt

## 🎓 Anwendungsbeispiel

**Produkt:** Onboarding 1.0  
**Ziel:** Schnell registrieren und ersten Nutzen erleben  
**KPIs:** Activation Rate (D1), TTFV

**Activities:**

1. Registrieren (E-Mail/PW, Double-Opt-In)
2. Erste Schritte (Tour, erste Aufgabe)

**MVP Slice:**

- ST1: Registrierungsformular
- ST2: E-Mail-Bestätigung
- ST3: Guided Tour (3 Tipps)
- ST4: Erste Aufgabe abschließen

**Outcome:** Aktivierungsrate ≥ 30%, TTFV ≤ 10 min

## 🔗 AI-Lead Integration

Dieser Skill ist als Sub-Skill konzipiert:

```
AI-Lead Orchestrator
  ├─> story_map.create(context) -> story_map.json
  ├─> story_map.validate(json) -> validation_report
  ├─> story_map.slice(json) -> slices.md
  ├─> story_map.export_backlog(json) -> backlog.csv
  └─> story_map.visualize(json) -> storymap.mmd
```

## 📖 Weiterführende Literatur

- Jeff Patton: "User Story Mapping" (O'Reilly)
- INVEST-Kriterien für Stories
- Gherkin/BDD für Acceptance Criteria
- WSJF/RICE für Priorisierung

## 📝 Lizenz & Quellen

Basierend auf etablierten Story-Mapping-Praktiken nach Jeff Patton und agilen Prinzipien.

---

**Version:** 1.0  
**Erstellt:** November 2025  
**Status:** Production Ready ✅
