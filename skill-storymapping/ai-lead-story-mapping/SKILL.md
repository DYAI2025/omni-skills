---
name: ai-lead-story-mapping
description: Erstellt und pflegt User‑Story‑Maps als Sub‑Skill des AI‑Lead‑Orchestrators; führt Teams von Ziel & Persona über Backbone/Activities und vertikale Priorisierung zum Slicing (MVP/Walking Skeleton) und exportiert testbare Backlog‑Artefakte (JSON/CSV/Mermaid).
---

# Story Mapping Sub‑Skill (für AI Lead)

> **Kernidee:** Story Mapping verwandelt ein flaches Backlog in eine zweidimensionale, kontextreiche Landkarte mit einer horizontalen Reise (Backbone) und vertikaler Wichtigkeit—und macht so MVP & Releases über **Slicing** sichtbar.

## Wann verwenden

- Wenn Nutzerziele, Backbone‑Aktivitäten und Schritte **sichtbar** gemacht und in **testbare Stories & Slices** überführt werden sollen.
- Wenn MVP/Releases als **horizontale Cut‑Lines** (Slicing) geplant werden, sodass der erste Slice ein **Walking Skeleton** (dünnster, aber end‑to‑end nutzbarer Weg) ist.
- Wenn der AI‑Lead Orchestrator methodische Sub‑Skills steuert (z. B. Story Mapping → Priorisierung → Delivery), und strukturierte Artefakte benötigt (JSON/CSV/Mermaid).

## Inputs (vom Orchestrator)

- **context.product** (Name, Domäne), **context.actor/persona**, **context.goal/outcome**, **context.kpis[]**
- **constraints** (Timebox, Non‑Goals, Policies)
- **seed_items** (vorhandene Stories/Backlog‑Tickets, optional)
- **work_mode**: `workshop|async` (für Moderationstipps siehe _Workshop‑Facilitation_).

## Outputs (an Orchestrator)

- **story_map.json** (Activities/Steps/Stories inkl. AC)
- **slices.md** (MVP + Folge‑Releases, inkl. Outcome/Metriken)
- **backlog.csv** (Export zur Priorisierung z. B. WSJF/RICE im AI‑Lead‑Flow)
- **storymap.mmd** (Mermaid zur Visualisierung)
- **validation_report** (Format/Referenz‑Checks)

## Aktionen (Sub‑Skill‑Contract)

- `story_map.create(context, seed_items?) -> story_map.json`
- `story_map.enrich(story_map.json, hints?) -> story_map.json`
- `story_map.validate(story_map.json) -> validation_report`
- `story_map.slice(story_map.json, strategy?) -> slices.md`
- `story_map.visualize(story_map.json) -> storymap.mmd`
- `story_map.export_backlog(story_map.json) -> backlog.csv`

## Workflow/Anweisungen

1. **Vorbereitung (Framing)**  
   Ziel/Outcome und Persona klären (Elevator Pitch), Teilnehmer cross‑funktional festlegen (7–10 ideal), physisch/digital planen.

2. **Backbone aufbauen (horizontale Achse)**  
   Große Benutzeraktivitäten von links nach rechts in chronologischer Reihenfolge. **Horizontale Frage:** Haben wir die gesamte Reise?

3. **Stories sammeln (vertikale Achse)**  
   Unter jede Aktivität konkrete Stories/Tasks hängen; nach oben die Must‑haves (INVEST); Alternativen darunter (**„oder"‑Lesen**). **Vertikale Frage:** Was ist je Schritt am wichtigsten?

4. **Strukturieren, Lücken/Abhängigkeiten aufdecken**  
   Gemeinsames „Durchwandern" der Map deckt Gaps, technische Stories und Abhängigkeiten auf; Entwickler\*innen müssen anwesend sein.

5. **Slicing & Releases planen**  
   Nach vertikaler Priorisierung horizontale **Cut‑Lines** ziehen: oberster Slice = **MVP/Walking Skeleton** (mind. eine Story aus jedem kritischen Backbone‑Schritt), weitere Slices fügen „Fleisch" hinzu. Jede Slice mit Ziel/Metriken testbar halten.

6. **Artefakte erzeugen**  
   Validator, CSV‑Export, Mermaid‑Diagramm ausführen und an AI‑Lead übergeben.

## Leitprinzipien

- **Value‑Delivery statt Feature‑Fabrik:** Fokus auf Nutzerproblem & vollständige End‑to‑End‑Erfahrung (CPE) statt „Top‑5‑Features‑Liste".
- **MVP = Walking Skeleton:** Dünnster, funktional vollständiger Durchstich durch die Journey.
- **Lebendes Artefakt:** Map fortlaufend pflegen, nicht „wegwerfen".

## CLI‑Nutzung (lokal)

```bash
# Validieren
python scripts/story_map_validator.py assets/examples/example-story-map.json

# Slices vorschlagen (Happy‑Path‑Heuristik)
python scripts/slice_suggester.py assets/examples/example-story-map.json --out assets/examples/example-slices.md

# Backlog exportieren
python scripts/export_backlog_csv.py assets/examples/example-story-map.json --out assets/examples/example-backlog.csv

# Mermaid erzeugen
python scripts/map_to_mermaid.py assets/examples/example-story-map.json > storymap.mmd
```

## Ausgabeformat

- **story_map.json** gemäß Template (Activities/Steps/Stories, AC im Gherkin‑Stil)
- **slices.md** (MVP/Follow‑Up mit Outcome & Metriken)
- **backlog.csv** (id,title,description,depends_on,actor,goal,activity,step,pattern,effort,reach,impact,confidence,bv,tc,rr,js)
- **storymap.mmd** Mermaid Flowchart

## Beispiele

Siehe `assets/examples/` für eine Onboarding‑Map mit MVP‑Slice und CSV‑Export (inkl. Abhängigkeiten & ACs).

## Hinweise & Quellen

Definition, Anatomie und Nutzen des Story Mappings (Backbone horizontal, Priorität vertikal; Unterschied zu flachem Backlog; MVP/Slicing/Walking Skeleton; Workshop‑Vorgehen & Facilitation) basieren auf etablierten Praktiken nach Jeff Patton und agilen Prinzipien.
