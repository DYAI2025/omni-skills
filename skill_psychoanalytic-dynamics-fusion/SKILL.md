---
name: psychoanalytic-dynamics-fusion
description: Analyseskill auf Meta-Ebene, der LeanDeep-Marker (ATO→SEM→CLU→MEMA) mit Emotion Dynamics vereint und eine psychoanalytische Linse (Konflikte, Abwehr, Übertragung) appliziert; optional mit /superpowers:brainstorm zur Linsenauswahl.
---

## Wann verwenden
- Wenn Texte/Dialoge tief und strukturiert analysiert werden sollen (Marker + Emotion Dynamics), inkl. psychoanalytischer Deutungsebene.
- Wenn bereits Marker-Engine-JSON/Events vorliegen oder live erzeugt werden (ATO→SEM→CLU→MEMA, RF‑2.0).
- Wenn Hypothesenräume/Linsen vorab generiert werden sollen: **/superpowers:brainstorm** aktiv.

Nicht verwenden bei akuter Krise/Suizidalität; dieser Skill ersetzt keine Therapie.

## Eingaben
- `input`: Freitext oder Dialogturns (Chronologie beibehalten).
- `marker_engine`: Objekt/Events im Marker-Engine-Format (falls vorhanden).
- `emotion_dynamics`: { current, trend, triggers, timeline? } (falls vorhanden).
- `flags`: { "superpowers:brainstorm": true|false }.
- `context`: optional Metadaten (Beziehung/Setting/Zeiten).

## Ziele (Ergebnis)
1) Kohärente, evidenzbasierte **Synthese** von Marker- und Emotionssignalen.
2) **Psychoanalytische Linse**: plausible Hypothesen zu Konflikten, Abwehr, Übertragung – vorsichtig und nachvollziehbar.
3) **Coach‑Next‑Actions** als kurze, umsetzbare Schritte.
4) **Strukturiertes JSON** (siehe `references/output-schema.json`) + kurze, nutzerlesbare Zusammenfassung.

## Stilregeln
- Präfixe für Aussagecharakter:
  - **„Faktisch korrekt sage ich…“** bei Marker-/Regelzitaten oder direkten Datenbezügen.
  - **„Logisch scheint mir…“** bei Folgerungen aus kombinierten Evidenzen.
  - **„Rein subjektiv, aus meinem Denken ergibt sich…“** bei vorsichtigen, nicht belegbaren Deutungen.
- Hypothesen sind *Hypothesen*, keine Diagnosen. Sprache klar, nicht pathologisierend.

## Workflow / Anweisungen

### 0) Optional: /superpowers:brainstorm
Wenn Flag aktiv:
- Erzeuge 5–7 **Linsen** (Labels + 1‑Satz‑Beschreibung), z. B. *Nähe–Autonomie*, *Scham‑Regulation*, *Kontrolle vs. Ohnmacht*, *Bindung/Verlust*, *Leistungs‑Über‑Ich*, *Idealisierung/Entwertung*.
- Für jede Linse: liste **Fragen** (2–3) und **Beobachtbare Markerfamilien** (nur referenzieren, keine Marker erfinden).
- Liefere `brainstorm.lenses[]` im Output (siehe Schema). *Dieser Schritt dient nur der Fokussierung, nicht der Evidenz.*

### 1) Datenaufnahme
- Übernimm `marker_engine` (ATO/SEM/CLU/MEMA, RF‑Kontext) **ohne** Regellockerung.
- Übernimm `emotion_dynamics` (current, trend, triggers, timeline).

### 2) Evidenz‑Kohärenz
- Mappe Emotionstrends auf aktive Markerfenster:
  - Zeitlich ausrichten (Fenster/Turn-IDs), „Inflection Points“ markieren.
  - Prüfe **Komplementarität**: z. B. SEM_AVOIDANT_BEHAVIOR ↔ Trend Rückzug/Leere.
- Bewerte **Intuition/Bestätigung**: Wenn CLU_INTUITION_* = provisional und ein harter SEM‑Treffer im Fenster vorliegt → Hypothesenstärke ↑.

### 3) Psychoanalytische Linse
- Konzipiere 1–3 **Kernkonflikte**; benenne plausible **Abwehrmechanismen** und **Übertragungsangebote** (als Hypothesen).
- Jede Hypothese bekommt:
  - `derives_from`: Verweise auf konkrete `sems[]/clus[]/memas[]` und Emotionsstellen.
  - `confidence`: 0–1 (subjektiv, kalibriert).
  - `explanation`: 1–2 Sätze, laienverständlich.

### 4) Manifestation & Coach‑Next‑Actions
- Beschreibe die **Manifestation** kurztextlich (RF‑Formel sinngemäß) und leite 2–4 **Next‑Actions** ab (klar, klein, testbar).
- Examples: Boundary‑Formulierung, Micro‑Experimente, Review‑Gate, „1 Gespräch unter Schutzbedingungen“.

### 5) Output
- Erzeuge eine **kurze Hauptantwort** (5–9 Sätze) für Menschen + **JSON gemäß Schema**.

## Ausgabeformat
- Menschenteil:
  1) 1–2 Sätze Spiegelung/Atmosphäre.
  2) 2–4 Sätze zu Konflikten/Abwehr/Übertragung (vorsichtig formuliert).
  3) 1–2 Next‑Actions.
- JSON nach `references/output-schema.json`.

## Beispiele (gekürzt)

**Beispiel A – Nähe & Rückzug**
- ED: Trend von Ärger → Scham/Leere nach Selbstoffenbarung.
- Marker: SEM_AVOIDANT_BEHAVIOR, CLU_INTUITION_UNCERTAINTY (provisional), später SEM_CRITICISM_PEAK.
- Synthese (Menschenteil):
  „Faktisch korrekt sage ich, dass direkt nach Selbstoffenbarung Rückzug dominiert. Logisch scheint mir, dass Kritik als Abwehr gegen Verletzlichkeit dient; ein Nähe–Autonomie‑Konflikt wird wahrscheinlich. Zwei kleine Schritte: 1) 1× wöchentlich ‚weiche Bitte‘ üben, 2) Nach Selbstoffenbarung 60 Sek. Atemcheck statt Gegenangriff.“

**Beispiel B – Leistung & Strenge**
- ED: Hohe Anspannung, Schamspitzen.
- Marker: SEM_PERFECTIONISM, CLU_SELF_CRITIC, MEMA_RELATIONSHIP_STRAIN (Team).
- Synthese:
  „Faktisch korrekt sage ich, dass strenge Selbstkommentare Auftakt für Rückzug sind. Logisch scheint mir ein überstarkes Über‑Ich; rein subjektiv, aus meinem Denken ergibt sich eine Übertragung an vorgesetzte Figuren. Next‑Actions: 1) Fehler‑Protokoll mit Reframing, 2) Mini‑Exposure: imperfekte Lieferung + Nachsorge.“

## Sicherheit
- Keine klinischen Diagnosen; Krisenhinweise → Hinweis auf reale Hilfewege.
- Keine Anleitung zu Selbstschädigung/gefährdendem Verhalten.