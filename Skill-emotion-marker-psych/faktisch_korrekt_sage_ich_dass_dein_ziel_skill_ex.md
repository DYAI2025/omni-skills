Faktisch korrekt sage ich, dass dein Ziel‑Skill explizit auf der LeanDeep‑Marker‑Architektur (ATO→SEM→CLU→MEMA mit RF‑2.0‑Manifestation) aufsetzt und deren deterministische Regeln (z. B. SEM‑Komposition ≥ 2 unterschiedliche ATOs, CLU‑Fenster, MEMA‑ARS 0–5 mit Decay) respektiert; das ist in euren Marker‑Skill‑Leitfäden festgelegt.
Logisch scheint mir, dass wir diese Pipeline mit Emotion Dynamics verschalten, darüber eine psychoanalytische Linse legen (Konflikte, Abwehr, Übertragung) und optional /superpowers:brainstorm zum Start nutzen, um geeignete „Linsen“ und Hypothesenräume systematisch zu generieren; die RL‑Erweiterung kann als Policy‑Gewichtung dienen, ohne Grundregeln zu lockern.
Faktisch korrekt sage ich außerdem, dass ein separater Brainstorm‑Skill vorhanden ist; wir binden ihn als vorbereitende Heuristik ein. brainstorm
1) FILETREE
text
Code kopieren
psychoanalytic-dynamics-fusion/
  SKILL.md
  references/
    output-schema.json
  assets/
    prompt_superpowers_brainstorm.md
    prompt_runtime_guidelines.md
2) ALLE DATEIEN
markdown
Code kopieren
# path: psychoanalytic-dynamics-fusion/SKILL.md
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

json
Code kopieren
# path: psychoanalytic-dynamics-fusion/references/output-schema.json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "PsychoanalyticDynamicsFusionOutput",
  "type": "object",
  "properties": {
    "summary_text": { "type": "string" },
    "brainstorm": {
      "type": "object",
      "properties": {
        "lenses": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "rationale": { "type": "string" },
              "questions": { "type": "array", "items": { "type": "string" } },
              "related_marker_families": { "type": "array", "items": { "type": "string" } }
            },
            "required": ["label", "rationale"]
          }
        }
      }
    },
    "marker_engine": {
      "description": "Passthrough/Subset aus Marker-Engine (rf_stage, atos, sems, clus, tends, memas, manifestation)",
      "type": "object"
    },
    "emotion_dynamics": {
      "type": "object",
      "properties": {
        "current": { "type": "array", "items": { "type": "string" } },
        "trend": { "type": "string" },
        "triggers": { "type": "array", "items": { "type": "string" } },
        "timeline": { "type": "array", "items": { "type": "object" } }
      }
    },
    "psychoanalytic_inference": {
      "type": "object",
      "properties": {
        "core_conflicts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "label": { "type": "string" },
              "derives_from": { "type": "array", "items": { "type": "string" } },
              "confidence": { "type": "number", "minimum": 0, "maximum": 1 },
              "explanation": { "type": "string" }
            },
            "required": ["label", "derives_from", "confidence"]
          }
        },
        "defenses": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": { "type": "string" },
              "derives_from": { "type": "array", "items": { "type": "string" } },
              "confidence": { "type": "number" }
            },
            "required": ["type", "derives_from"]
          }
        },
        "transference": {
          "type": "object",
          "properties": {
            "pattern": { "type": "string" },
            "possible_origin": { "type": "string" },
            "derives_from": { "type": "array", "items": { "type": "string" } },
            "confidence": { "type": "number" }
          }
        }
      }
    },
    "coach_next_actions": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "gate": { "type": "string", "enum": ["Ideation", "Backlog", "Execution", "Final"] },
          "action": { "type": "string" },
          "rationale": { "type": "string" }
        },
        "required": ["gate", "action"]
      }
    },
    "evidence_prefixed_declarations": {
      "description": "Liste von Sätzen mit Präfix zur Klarheit über Gewissheitsgrad",
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "prefix": { "type": "string", "enum": ["Faktisch korrekt sage ich", "Logisch scheint mir", "Rein subjektiv, aus meinem Denken ergibt sich"] },
          "text": { "type": "string" }
        },
        "required": ["prefix", "text"]
      }
    },
    "self_check": {
      "type": "object",
      "properties": {
        "validation_summary": { "type": "string" },
        "next_step_or_correction": { "type": "string" }
      }
    }
  },
  "required": ["summary_text", "psychoanalytic_inference", "coach_next_actions", "evidence_prefixed_declarations"]
}
markdown
Code kopieren
# path: psychoanalytic-dynamics-fusion/assets/prompt_superpowers_brainstorm.md
/superpowers:brainstorm — Vorbereitungsmodus für Linsen

ZIEL
- Vor Analyse 5–7 Linsen generieren, die sinnvoll auf Markerfamilien & Emotionsmuster mappen.
- Keine Marker erfinden; nur Familien/Beispiele benennen.

ANWEISUNGEN
1) Erzeuge `lenses[]` mit:
   - label (kurz), rationale (1 Satz),
   - 2–3 Fragen,
   - related_marker_families (Strings, z. B. „avoidance“, „criticism“, „shame_regulation“ — keine IDs).
2) Richte Linsen an vorliegenden Emotions-Trends aus (z. B. Ärger→Scham, Rückzug nach Nähe).
3) Gib Ergebnis unter `brainstorm.lenses` aus.
4) Danach normale Analyse (Marker + Emotion Dynamics + psychoanalytische Linse).

HINWEIS
- Linsen sind Hypothesen-Rahmen, keine Evidenz. Im Hauptlauf zählen Marker-/Trend-Evidenzen.
markdown
Code kopieren
# path: psychoanalytic-dynamics-fusion/assets/prompt_runtime_guidelines.md
RUNTIME-GUIDELINES (Kurz)

1) Menschenteil zuerst (5–9 Sätze), freundlich, vorsichtig, ohne Diagnosen.
2) Präfix-Regel: 
   - „Faktisch korrekt sage ich…“ bei Daten/Regeln/Markerhits.
   - „Logisch scheint mir…“ bei Folgerungen aus Kombinationen.
   - „Rein subjektiv, aus meinem Denken ergibt sich…“ bei freien Deutungen.
3) Danach JSON gemäß Schema.
4) Bei Widersprüchen: im `self_check` transparent benennen & Korrektur vorschlagen.
5) Krisenindikationen → Hinweis auf reale Hilfewege, keine riskanten Handlungsanleitungen.
3) OPTIONAL: Bash‑Installer
bash
Code kopieren
# path: install_psychoanalytic_dynamics_fusion.sh
#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="psychoanalytic-dynamics-fusion"
mkdir -p "$SKILL_DIR/references" "$SKILL_DIR/assets"

cat > "$SKILL_DIR/SKILL.md" <<'EOF'
--- 
name: psychoanalytic-dynamics-fusion
description: Analyseskill auf Meta-Ebene, der LeanDeep-Marker (ATO→SEM→CLU→MEMA) mit Emotion Dynamics vereint und eine psychoanalytische Linse (Konflikte, Abwehr, Übertragung) appliziert; optional mit /superpowers:brainstorm zur Linsenauswahl.
---
[... identisch zum oben stehenden Inhalt ...]
EOF

cat > "$SKILL_DIR/references/output-schema.json" <<'EOF'
[... identisch zum oben stehenden Inhalt ...]
EOF

cat > "$SKILL_DIR/assets/prompt_superpowers_brainstorm.md" <<'EOF'
[... identisch zum oben stehenden Inhalt ...]
EOF

cat > "$SKILL_DIR/assets/prompt_runtime_guidelines.md" <<'EOF'
[... identisch zum oben stehenden Inhalt ...]
EOF

echo "Installed $SKILL_DIR"
4) Validierung & Packaging
Schneller Check (lokal):
bash
Code kopieren
python quick_validate.py psychoanalytic-dynamics-fusion
ZIP-Paket erstellen:
bash
Code kopieren
python package_skill.py psychoanalytic-dynamics-fusion ./dist
Faktisch korrekt sage ich, dass dieser Skill kompatibel zur Marker‑Engine‑Spezifikation (inkl. RF‑2.0‑Manifestation und Coach‑Next‑Actions) entworfen ist und die RL‑Variante als Policy‑Gewichtung ohne Regelbruch gedacht ist.
Logisch scheint mir, dass /superpowers:brainstorm euren Linsen‑Backlog liefert, danach die deterministische Marker‑Kaskade + Emotion‑Trends die Evidenz stützen und die psychoanalytische Ebene diese Evidenz in sinnvolle, psychologisch nachvollziehbare Hypothesen übersetzt. brainstorm