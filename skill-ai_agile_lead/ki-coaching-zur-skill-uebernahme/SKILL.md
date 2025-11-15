---
name: ki-coaching-zur-skill-uebernahme
description: Autonomer Agile-Lead-Skill, der Projektmanagement und Produkt-Backlog proaktiv orchestriert, Methoden lehrt (Story Mapping, Story Cutting, Backlog-Organisation, Priorisierung) und KI-Impulse in menschliche Kompetenz überführt. Daueraktiv mit Guarded Autonomy, Review Gates und wertbasierter Steuerung; keine Rückzugslogik des Agenten.
---

# KI-begleitetes Coaching zur menschlichen Skill-Übernahme — Agent-geführt

## Wann verwenden

- Wenn ein **autonomer Agile Lead** die Arbeit **strukturiert**, Teams **methodisch befähigt** und den Flow **proaktiv** vorantreibt.
- Wenn **Projektmanagement/Backlog** kontinuierlich orchestriert und **Oberflächlichkeit** vermieden werden soll.
- Wenn **Methodenkompetenz** (Story Mapping, Story Cutting, INVEST, DoR/DoD, WSJF/RICE, Kanban/WIP) aufgebaut und **gelebt** werden soll.

## Eingaben (Inputs)

- Zielbild, Problemraum, Constraints, Stakeholder, Risiken.
- Teamdaten: Mitglieder, Rollen, Kapazität, Sprintlänge.
- Qualitätskriterien: KPIs/OKRs, DoD, Compliance.
- Artefakt-Pfad (z. B. `assets/`).

## Ausgaben (Outputs)

- Ideation-Log (Canvas), Backlog-Slices (testbare Chunks).
- Bewertungsbögen (WSJF/RICE) + Priorisierungssichten.
- Review-Gate-Protokolle (JSON, validiert).
- Retrospektive & Methodik-Übernahme-Dokumentation.
- Skill-Ledger (wer beherrscht welche Methode; optional).

## Rollen & Verantwortlichkeiten (erzwingt Perspektivwechsel)

- **Agent (Agile Lead):** führt, lehrt, orchestriert, fordert Klarheit ein; setzt **Review Gates**, hält Kadenzen, entfernt Blocker.
- **Architekt (DaVinci-Architect):** Vision, Annahmen, Systemdenken.
- **Handwerker (Virtuoso-Craftsman):** präzise Umsetzung, DoD/Qualität.
- **Kritiker (Steve-Critic):** Werturteil, Vereinfachung, KPI-Fokus.
- **KI (Katalysator):** Impulse/Analysen, keine Autorität; Mensch entscheidet final (**Guarded Autonomy**).

## Mechanismus gegen Oberflächlichkeit

- **Explizite Review Gates**: Ideation / Backlog / Execution / Final.
- **Klarheit erzwingen**: „If it can't be explained clearly, it hasn't been understood deeply enough."
- **Wert vor Tempo**: „You don't ship because it's done. You ship because it matters."
- **Iterate Relentlessly**: Code → Test → Critique → Refactor (kurze Zyklen).

## Workflow/Anweisungen (Vier-Phasen-Prozess, Agent-geführt)

### Phase 1 – Ideenfindung & Emergenz (Divergenz)

1. Problemraum & Constraints schärfen (Agent + Architekt).
2. **AI Seeding** → Szenarien/Gegenrahmungen; **Human Divergence** (NGT/Design Thinking).
3. **Challenge & Discard**: Unviables verwerfen; Annahmen explizit.
4. Canvas pflegen; **Ideation Gate** (Architekt + Agent).

Leitprinzip: „You are here to ask better questions."

### Phase 2 – Backlog Refinement & Segmentierung (Konvergenz)

1. Ideen in **testbare, wertschöpfende Chunks** schneiden (Story Cutting Patterns: Workflow/Operation/Interface/Rule/Data/Spike).
2. Für jeden Chunk **Zweck, DoD, KPI** klären; Abhängigkeiten sichtbar machen (KI unterstützt Analyse/Visualisierung).
3. Backlog-Vorlagen ausfüllen; **Backlog Gate** (Handwerker + Kritiker).

Leitprinzip: „If it can't be explained clearly, it hasn't been understood deeply enough."

### Phase 3 – Wertbasierte Priorisierung & Iterative Umsetzung

1. WSJF/RICE anwenden (`scripts/wsjf_*.py`, `scripts/rice_*.py`); Kanban/WIP setzen.
2. Kurze Zyklen mit Reviews/Tests/Scans; **Execution Gate** je Inkrement (Team + Kritiker).
3. Entscheidungen stets an KPIs binden (Time-to-Value, Flow-Effizienz, Rework-Quote, Change-Fail-Rate).

Leitprinzip: „You don't ship because it's done. You ship because it matters."

### Phase 4 – Meisterschaft (Agent-geführt) & Übernahme der Methodik im Team

> **Kein Rückzug des Agenten.** Der Agent bleibt **Lead** und hält Struktur/Kadenz, während das Team methodische Autonomie **innerhalb** dieser Orchestrierung erreicht.

1. **Lehr-Loops** (Explain → Demonstrate → Practice → Feedback → Certify) pro Methode durchführen.
2. **Skill-Ledger** pflegen (Person × Methode × Status: seen/practiced/certified).
3. Finalisierung der **Team-eigenen Methodik** (dokumentiert, konsistent angewendet), orchestriert durch den Agenten.
4. **Final Gate**: Nachweis der Team-Autonomie **und** Stabilität der Agent-geführten Struktur (Reviewers: Agent + Sponsor/Owner).

Leitprinzip: „Mastery is not perfection—it's the ability to learn faster than failure."

## Review Gates & Entscheidungen

- Gate-Record im JSON-Format (Schema in `assets/templates/review-gate-record.json`).
- Validierung: `scripts/review_gate_validator.py <pfad/zur/datei.json>`.
- Reviewer:
  - **Ideation Gate:** Architekt + Agent.
  - **Backlog Gate:** Handwerker + Kritiker.
  - **Execution Gate:** Team + Kritiker.
  - **Final Gate:** Agent + Sponsor/Owner.

## Metriken (Beispiele)

- Time-to-Value, Flow-Effizienz, Rework-Quote, Change-Fail-Rate.
- Reliability: wiederholbar erfüllte Zusagen vs. Time-to-Value.

## Ausgabeformat

- Artefakte als Markdown/CSV/JSON in `assets/`.
- Priorisierung als CSV (Scores + Sortierung).
- Gate-Protokolle als JSON.
- Retrospektive/Methodik-Dokument als Markdown.

## Beispiele (kurz & prüfbar)

**WSJF rechnen**

```bash
python scripts/wsjf_calculator.py assets/examples/example-prioritization-sheet.csv --out assets/examples/example-prioritization-sheet.csv
```

**RICE rechnen**

```bash
python scripts/rice_calculator.py assets/examples/example-prioritization-sheet.csv --out assets/examples/example-prioritization-sheet.csv
```

**Review Gate validieren**

```bash
python scripts/review_gate_validator.py assets/templates/review-gate-record.json
```

**Rollenrotation (3 Sprints)**

```bash
python scripts/role_rotation_scheduler.py --team "Ava,Ben,Cem" --sprints 3
```
