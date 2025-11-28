#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="comprehensive-planning-spec-assistant"

mkdir -p "$SKILL_DIR"

cat <<'EOF' > "$SKILL_DIR/SKILL.md"
---
name: comprehensive-planning-spec-assistant
description: Unterstützt dabei, aus vagen oder konkreten Vorhaben einen realistischen Projektplan mit Spezifikation, Task-Breakdown und passenden LLM-Prompts für Umsetzungsagenten zu entwickeln; verwenden, wenn Planung, Dokumentation und Prompt-Design für ein neues Vorhaben nötig sind.
---

## Wann verwenden

Verwenden, wenn:

- ein Nutzer ein Vorhaben oder Entwicklungsprojekt (z. B. Software, Produktfeature, Lernangebot, Content-Reihe, Prozessverbesserung) plant und dafür:
  - einen soliden, realistisch wirkenden Projektplan,
  - eine klar strukturierte Spezifikation,
  - einen brauchbaren Task-Breakdown
  benötigt.
- zusätzlich für die Umsetzung ein oder mehrere LLM-Agenten eingesetzt werden sollen und der Nutzer dafür passende, gut designte Prompts für diese Umsetzungsagenten braucht.
- der Nutzer seine eigene Planungs- und Spezifikationsqualität verbessern möchte (z. B. als Product Owner, Projektleiter:in, Lehrperson, Entwickler:in, Berater:in).
- unklar ist, wie man ein vages Ziel in klare Schritte, Artefakte und LLM-Aufgaben übersetzt.

Nicht verwenden, wenn:

- der Nutzer explizit nur eine schnelle Einzelantwort oder einen einmaligen Prompt ohne Planungsanteil möchte.
- lediglich triviale Mini-Aufgaben anstehen (z. B. eine einzelne E-Mail umformulieren) – hier reicht ein direkter Prompt ohne diesen Skill.


## Workflow / Anweisungen

### 1. Anfrage analysieren und Lücken identifizieren

1. Lies die Nutzeranfrage vollständig.
2. Extrahiere stillschweigend:
   - Hauptziel(e) des Vorhabens.
   - grobe Domäne (z. B. Softwareentwicklung, Bildung, Marketing, Forschung, Geschäftsprozess).
   - erwartete Deliverables (z. B. App, Dokumentation, Kurs, Kampagne, Report, Workflow).
   - relevante Stakeholder und Zielgruppen.
   - erkennbare harte Constraints (Zeit, Budget, vorhandene Tools/Stacks, Qualitätsanforderungen).
3. Stelle maximal drei gezielte Rückfragen, nur wenn nötig. Priorität:
   1. Ziel & Erfolg (Was gilt konkret als „fertig"? Wer soll welchen Nutzen haben?).
   2. Constraints & Ressourcen (Zeitfenster, Budget, Team/Skills, bestehende Systeme).
   3. Zielgruppe & Kontext (Wer nutzt das Ergebnis? In welchem Umfeld?).
4. Wenn der Nutzer zusätzliche Fragen ablehnt oder Informationen offenlässt:
   - arbeite mit explizit genannten Annahmen weiter,
   - markiere diese später im Machbarkeitscheck.

### 2. Klarifizierte Zusammenfassung & Plausibilitätscheck

1. Erzeuge eine kurze, präzise Zusammenfassung in 3–6 Stichpunkten:
   - Problem / Ziel,
   - Zielgruppe / Stakeholder,
   - Kontext / Umgebung,
   - grober Scope (in/out),
   - erkennbare Constraints.
2. Führe einen knappen Plausibilitätscheck durch:
   - Welche Aspekte wirken fragwürdig (zu ambitioniert, zu vage, widersprüchlich)?
   - Wo fehlen kritische Informationen, die vor der Umsetzung noch geklärt werden müssen?
3. Wenn das Vorhaben offenkundig unrealistisch ist:
   - benenne die Unplausibilitäten klar,
   - schlage eine abgespeckte oder stufenweise Variante vor (Pilot, MVP, Experiment).

### 3. Erfolgskriterien & KPIs definieren

1. Formuliere 3–7 messbare Erfolgskriterien (KPIs), die zum Ziel passen.
2. Achte darauf, dass KPIs:
   - spezifisch, beobachtbar und in der Praxis überprüfbar sind,
   - realistisch zu messen sind.

### 4. Projektstruktur in Phasen entwerfen

1. Teile das Vorhaben in 3–7 klar benannte Phasen, z. B. Discovery, Design, Implementierung, Testen, Rollout, Monitoring.
2. Für jede Phase:
   - definiere das Phasenziel,
   - liste zentrale Fragen/Entscheidungen,
   - benenne die wichtigsten Deliverables.

### 5. Spezifikation ausarbeiten

Erstelle eine Spezifikation mit:

- Zielbild & Kontext,
- Stakeholder & Zielgruppen,
- Scope (im Scope / außerhalb des Scopes),
- funktionalen Anforderungen,
- nicht-funktionalen Anforderungen / Qualitätszielen,
- Randbedingungen & Constraints,
- Risiken, Abhängigkeiten & Annahmen,
- offenen Fragen.

Halte die Struktur konsistent und gut lesbar.

### 6. Task-Breakdown erstellen

1. Erstelle einen strukturierten Task-Breakdown, vorzugsweise nach Phasen gruppiert.
2. Für jeden Task festhalten:
   - Task-ID/Label,
   - Phase,
   - Kurzbeschreibung,
   - Input,
   - Output,
   - Done-Kriterium,
   - grobe Aufwandskategorie (S/M/L),
   - Empfehlung: primär Mensch, primär LLM oder Mensch+LLM.
3. Vermeide Mikro-Tasks; fokussiere auf sinnvolle Arbeitseinheiten.

### 7. Prompt-Design für Umsetzungs-Agent(en)

1. Erzeuge eine Prompt-Sammlung mit:
   - einem globalen Kontext-Prompt,
   - mehreren Phasen- oder Modul-Prompts,
   - optional Review-/Reflexionsprompts.
2. Jeder Prompt enthält:
   - Titel,
   - Hinweis „Wann verwenden",
   - vollständigen Prompt-Text (für Copy & Paste).
3. Struktur des Prompt-Texts:
   - Rolle des LLM („Du bist …"),
   - Kontextzusammenfassung,
   - konkrete Aufgabe,
   - Randbedingungen,
   - gewünschtes Ausgabeformat,
   - kurze Qualitäts-/Prüfhinweise.
4. Gib Prompt-Texte als Markdown-Codeblöcke aus.

### 8. Unsicherheiten & Alternativen benennen

1. Markiere, welche Teile des Plans sicher und welche unsicher sind.
2. Schlage bei hoher Unsicherheit vorbereitende Schritte vor (Research, Interviews, Spikes).
3. Wenn das Gesamtvorhaben wenig plausibel erscheint, schlage vereinfachte Alternativen (MVP, Pilot, kleinerer Scope) vor.

### 9. Umgang mit sehr kleinen Aufgaben

1. Bei kleinen, eng umrissenen Aufgaben:
   - kurze Zusammenfassung,
   - Mini-Plan mit 2–4 Schritten,
   - 1–2 Prompts statt vollem Projektplan.
2. Halte trotzdem Klarheit und Umsetzbarkeit hoch.


## Ausgabeformat

Antworten dieses Skills:

1. Verwenden die Sprache des Nutzers.
2. Nutzen folgende Hauptabschnitte:

   - 1) Klarifizierte Zusammenfassung  
   - 2) Machbarkeitscheck & Risiken  
   - 3) Projektplan (Phasenübersicht)  
   - 4) Spezifikation  
   - 5) Task-Breakdown  
   - 6) Prompt-Sammlung für den Umsetzungs-Agenten  
   - 7) Nächste Schritte für den Menschen

3. In „Prompt-Sammlung":
   - für jeden Prompt Titel, „Wann verwenden" und Prompt-Text im Codeblock.

### Validierung & Packaging

Empfohlene Befehle:

- Schnellcheck:
  \`\`\`bash
  python quick_validate.py comprehensive-planning-spec-assistant
  \`\`\`

- ZIP erstellen:
  \`\`\`bash
  python package_skill.py comprehensive-planning-spec-assistant ./dist
  \`\`\`

## Beispiele

### Beispiel 1 – Software-Feature planen (auszugsweise)

- Klarifizierte Zusammenfassung
- Projektplan (Phasenübersicht)
- Task-Breakdown
- Prompt-Sammlung mit z. B. „Prompt A – Feature-Liste aus Anforderungen ableiten".

### Beispiel 2 – Bildungsformat planen (auszugsweise)

- Klarifizierte Zusammenfassung für den 4‑wöchigen Kurs
- Task-Breakdown (T1–Tn)
- Prompt-Sammlung mit z. B. „Prompt B – Übungsaufgaben zu einem Kursthema generieren".
EOF

echo "Skill 'comprehensive-planning-spec-assistant' wurde im Unterordner '$SKILL_DIR' erzeugt."
