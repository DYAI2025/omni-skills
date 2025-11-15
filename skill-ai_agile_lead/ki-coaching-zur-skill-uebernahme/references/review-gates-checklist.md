# Review Gates – Checkliste (Agent-geführt)

## Pflichtfelder je Gate (im JSON-Record)

- gate_name: "Ideation|Backlog|Execution|Final"
- date: ISO-Datum (YYYY-MM-DD)
- reviewers: Liste von Namen/Rollen
- decision: "approve" | "changes" | "reject"
- rationale: prägnante Begründung
- risks: Top-Risiken + Gegenmaßnahmen
- next_actions: Schritte, Verantwortliche, Termin

## Zusatzkriterien

- Ideation: Annahmen explizit? Unviables verworfen? Canvas gepflegt? (Reviewer: Architekt + **Agent**)
- Backlog: Zweck je Chunk klar? DoD testbar? Abhängigkeiten sichtbar? (Reviewer: Handwerker + Kritiker)
- Execution: KPI-Bezug? Qualität (Tests/Security) erfüllt? (Reviewer: Team + Kritiker)
- Final: Team-Autonomie nachgewiesen **im Agent-Rahmen**? Struktur stabil? (Reviewer: **Agent** + Sponsor/Owner)
