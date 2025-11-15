1) FILETREE
text
Code kopieren
emotion-dynamics-deep-insight/
  SKILL.md
  references/
    emotion-dynamics-quick-notes.md
2) ALLE DATEIEN
markdown
Code kopieren
# path: emotion-dynamics-deep-insight/SKILL.md
---
name: emotion-dynamics-deep-insight
description: Analysiert Texte anhand von Utterance Emotion Dynamics (UED) und ergänzt sie um psychologische Tiefensicht, indem emotionale Zustände, Verläufe und Muster strukturiert rekonstruiert werden.
---

## Wann verwenden

- Wenn ein freier Text (z. B. Chat-Verlauf, Tagebucheintrag, Mail, Monolog, Kurzgeschichte) psychologisch „tief“ gelesen werden soll.
- Wenn explizit nach Emotion Dynamics / Utterance Emotion Dynamics (UED) gefragt wird.
- Wenn emotionale Zustände über den Verlauf eines Textes (Trajektorien) und nicht nur als Momentaufnahme verstanden werden sollen.
- Wenn qualitative Hinweise auf Emotionsregulation, typische emotionale „Home Bases“ und Muster (z. B. Vermeidung vs. Annäherung) rekonstruiert werden sollen – ohne klinische Diagnose zu stellen.

## Workflow/Anweisungen

### 1. Input erfassen und kontextualisieren

1. Nimm den gesamten vom Nutzer gegebenen Text als primären Input.
2. Falls vorhanden, nutze explizite Strukturhinweise:
   - Zeitstempel, Sprecherlabels, Zeilennummern, Kapitel, Absätze.
   - Sonst: segmentiere in Sätze oder sinnvolle Sinn-Einheiten (Utterances).
3. Dokumentiere kurz:
   - Sprache(n) des Textes.
   - Art des Textes (z. B. Chat zwischen zwei Personen, Tagebucheintrag einer Person, Dialog in einer Szene).

### 2. Segmentierung in Utterances und Sprecher

1. Erzeuge eine interne Liste von Utterances mit Feldern:
   - `id`: laufender Index ab 1.
   - `speaker`: falls ersichtlich (z. B. „ich“, „Partner“, „Chef“); sonst `"unknown"` bzw. `"self"` für Ich-Passagen.
   - `order_index`: Reihenfolge als Integer (1, 2, 3, …); falls echte Zeitstempel vorhanden sind, notiere sie zusätzlich.
   - `text`: der jeweilige Satz/Abschnitt.
2. Nutze eine robuste, sinnorientierte Segmentierung:
   - Längere Absätze ggf. in zwei bis drei thematisch zusammenhängende Utterances aufteilen.
   - Kurze Ein-Wort-Beiträge („ja“, „ok“) als eigene Utterance, wenn sie emotional bedeutsam wirken.

### 3. Emotionale Zustände pro Utterance ableiten

> Ziel: Für jede Utterance einen approximierten „Emotionszustand“ im Sinne von EmotionDynamics bestimmen.

Für jede Utterance bestimme:

1. **Kontinuierliche Dimensionen (VAD)**  
   - `valence`: subjektiv angenommene Positivität/Negativität im Bereich `[-1.0, 1.0]`
     - ca. `-1.0` stark negativ, `0.0` neutral, `1.0` stark positiv.
   - `arousal`: Aktivierungsgrad im Bereich `[0.0, 1.0]`
     - `0.0` sehr ruhig/unterdrückt, `1.0` hoch aktiviert/aufgewühlt.
   - `dominance`: Gefühl von Kontrolle/Macht im Bereich `[0.0, 1.0]`
     - `0.0` ausgeliefert/ohnmächtig, `1.0` sehr wirkmächtig/souverän.

   **Instruktion:**  
   - Schätze die Werte konsistent und relativ innerhalb des Textes.  
   - Nutze Wortwahl, Grammatik, Metaphern, Emoticons, Ausrufezeichen, Großschreibung etc. als Indizien.

2. **Diskrete Emotionsintensitäten (NRC-EmoLex-inspiriert)**  
   Erzeuge für jede Utterance ein Objekt `discrete_emotions` mit Werten im Bereich `[0.0, 1.0]`:

   - `anger`
   - `anticipation`
   - `disgust`
   - `fear`
   - `joy`
   - `sadness`
   - `surprise`
   - `trust`
   - `positive`
   - `negative`

   **Instruktion:**  
   - Setze Werte > 0.6 nur, wenn der Text starke Hinweise liefert.  
   - Halte `positive` und `negative` konsistent mit `valence`.  
   - Erlaube Ko-Existenz (z. B. gleichzeitig `joy` und `fear` bei ambivalenten Passagen).

3. **Confidence-Wert**  
   - Füge pro Utterance ein Feld `confidence` im Bereich `[0.0, 1.0]` hinzu.
   - Nutze v. a.:
     - Klarheit des Wortmaterials.
     - Kontextkonsistenz.
     - Ironie/Sarkasmus (senkt Confidence).

### 4. Emotion-Dynamics-Trajektorie konstruieren

1. Sortiere alle Utterances nach `order_index` (oder Zeitstempel).
2. Lege eine chronologische Sequenz der Zustände an:
   - Fokus mindestens auf `(valence, arousal)`.
3. Identifiziere auffällige Abschnitte:
   - größere Sprünge in Valenz (z. B. von > 0.3 nach < -0.3).
   - starke Arousal-Spitzen.
   - Sequenzen mit vielen Utterances, die emotional flach sind (geringe Varianz).

### 5. UED-inspirierte Metriken berechnen (qualitativ)

> Die folgenden Kennzahlen orientieren sich am UED-Framework (Home Base, Variabilität, Dichte, Rise/Recovery Rates etc.), werden hier aber qualitativ bzw. grob quantitativ geschätzt.

Für jede relevante Einheit (mindestens für die Hauptperson `"self"`, ggf. weitere Sprecher) bestimme:

1. **Home Base**
   - Schätze den typischen Emotionszustand als:
     - `home_base.valence` ≈ Mittel der Valenzwerte über alle Utterances des Sprechers.
     - `home_base.arousal` ≈ Mittel der Arousalwerte.
   - Ergänze eine qualitative Beschreibung:
     - z. B. „leicht negativ und moderat aktiviert“ oder „deutlich positiv bei mittlerer Aktivierung“.

2. **Variabilität**
   - Schätze, wie stark die Zustände um die Home Base schwanken:
     - Kategorie: `low`, `medium`, `high`.
   - Orientiere dich an der Varianz der Valenz- und Arousalwerte im Verlauf.

3. **Instabilität / Sprunghaftigkeit**
   - Beurteile, wie oft und wie abrupt Wechsel zwischen distanten Zuständen auftreten:
     - z. B. häufige Wechsel von deutlich positiv nach deutlich negativ.
   - Gib eine qualitative Einschätzung (`low`, `medium`, `high`) und ein bis zwei konkrete Textstellen als Beleg im Fließtext-Teil.

4. **Inertia (Trägheit / Rückkehr zur Home Base)**
   - Beobachte, wie schnell sich der Zustand nach einem Ausschlag wieder in Richtung Home Base bewegt.
   - Beschreibe:
     - „schnelle Rückkehr“, „moderate Rückkehr“ oder „langsame Rückkehr / langes Nachhallen“.

5. **Rise Rate / Recovery Rate (Reaktivität / Regulation)**
   - **Rise Rate**: Wie schnell steigt Arousal/Negativität nach einem Trigger (z. B. Kritik, Zurückweisung)?
   - **Recovery Rate**: Wie schnell beruhigt sich der Zustand danach?
   - Nutze konkrete Verlaufsausschnitte, um beides textnah zu illustrieren.

6. **Density (emotionale Dichte)**
   - Schätze, wie stark der Text insgesamt emotional „gesättigt“ ist:
     - Anteil der Utterances mit klaren Emotionen (Valenz |Arousal| > 0.3 oder Emotionsintensität > 0.5).
   - Kategorie: `low`, `medium`, `high`.

### 6. Psychologische Tiefensicht (heuristisch, nicht-diagnostisch)

> Dieser Teil geht über das UED-Framework hinaus und liefert interpretative Hypothesen. Er ist explizit nicht diagnostisch.

Analysiere auf Basis der Dynamiken:

1. **Emotionsregulation-Muster (deskriptiv)**
   - Beschreibe typische Muster, z. B.:
     - „starke innere Aufschaukelung ohne klare Beruhigungsphase“,
     - „rasches Abkühlen nach Konflikten“,
     - „Vermeidungstendenzen (Abbruch von emotionalen Themen)“.
   - Verweise auf konkrete Ausschnitte aus der Trajektorie (z. B. Utterance-IDs).

2. **Annäherungs- vs. Vermeidungstendenzen**
   - Beurteile, ob die Person eher in Richtung:
     - Annäherung/Problembearbeitung (Fragen stellen, Lösungen suchen) oder
     - Vermeidung/Rückzug (Themenwechsel, emotionales Abschalten)
   geht – bezogen auf die emotionale Dynamik.

3. **Wiederkehrende emotionale Themen**
   - Identifiziere häufig wiederkehrende Kombinationen:
     - z. B. „Kombination aus Angst (fear) und Traurigkeit (sadness) bei Bezug auf Nähe/Distanz“,
     - „Ärger (anger) plus Ohnmachtsgefühl (niedrige Dominanz) bei Autoritätspersonen“.
   - Beschreibe diese Muster klar und knapp.

4. **Spannungen und Konflikte im Inneren**
   - Hebe Ambivalenzen hervor, z. B.:
     - gleichzeitig hohe `joy` und `fear`,
     - Valenz schwankt stark bei einem bestimmten Thema.
   - Formuliere die Spannungen als Hypothesen, z. B.:
     - „Es wirkt, als ob … auf der einen Seite …, auf der anderen Seite …“.

5. **Meta-Hinweise und Selbstfürsorge-Perspektive**
   - Abschließend formuliere 2–3 mögliche „Lernsätze“ oder Meta-Perspektiven, die sich aus dem Verlauf ergeben könnten, ohne Ratschläge aufzuzwingen.
   - Beispiel:
     - „Wenn der innere Stress schnell steigt, aber schlecht abklingt, könnte es hilfreich sein, Mikro-Pausen oder Distanzierungsschritte im Alltag zu beobachten oder zu erproben – im Sinne eines Experiments, nicht als Therapie-Empfehlung.“

### 7. Grenzen und Sicherheitshinweise

- Stelle klar, dass:
  - keine psychische Diagnose gestellt wird,
  - keine Therapie ersetzt wird,
  - die Interpretation ein Text-Spiegel ist, kein Urteil über die Person.
- Formuliere explizit:
  - Bei Anzeichen starker Belastung, Suizidgedanken oder massiver Beeinträchtigung verweise respektvoll auf professionelle Hilfe (Hausarzt, Psychotherapeut:innen, Krisendienste).

## Ausgabeformat

Die Ausgabe besteht aus zwei Schichten:

1. **Strukturierte JSON-ähnliche Übersicht** (maschinell verwertbar):

   ```json
   {
     "input_meta": {
       "language": "de",
       "text_type": "tagebucheintrag",
       "notes": "ein Sprecher (ich-Form)"
     },
     "utterance_states": [
       {
         "id": 1,
         "speaker": "self",
         "order_index": 1,
         "text": "…",
         "valence": -0.4,
         "arousal": 0.7,
         "dominance": 0.3,
         "discrete_emotions": {
           "anger": 0.6,
           "anticipation": 0.1,
           "disgust": 0.3,
           "fear": 0.4,
           "joy": 0.0,
           "sadness": 0.7,
           "surprise": 0.2,
           "trust": 0.1,
           "positive": 0.1,
           "negative": 0.8
         },
         "confidence": 0.78
       }
       // weitere Utterances …
     ],
     "ued_metrics": {
       "home_base": {
         "valence": -0.2,
         "arousal": 0.6,
         "description": "leicht negativ, moderat aktiviert"
       },
       "variability": {
         "level": "medium",
         "comment": "spürbare Ausschläge, aber nicht extrem"
       },
       "instability": {
         "level": "high",
         "comment": "häufige Sprünge zwischen positiv und negativ"
       },
       "inertia": {
         "level": "low",
         "comment": "Zustand kippt schnell, kehrt aber nicht stabil zurück"
       },
       "rise_rate": {
         "level": "high",
         "comment": "Arousal steigt nach Triggern schnell an"
       },
       "recovery_rate": {
         "level": "low",
         "comment": "beruhigt sich nur langsam"
       },
       "density": {
         "level": "high",
         "comment": "hohe emotionale Sättigung im Text"
       }
     },
     "psychological_lenses": {
       "emotion_regulation_pattern": "…",
       "approach_avoidance_tendencies": "…",
       "recurrent_themes": [
         "…"
       ],
       "inner_tensions": [
         "…"
       ],
       "meta_reflections": [
         "…"
       ]
     },
     "disclaimers": {
       "diagnostic_limitations": "Keine klinische Diagnose, nur textbasierte Rekonstruktion.",
       "support_hint": "Bei starker Belastung professionelle Hilfe erwägen."
     }
   }
Fließtextzusammenfassung (für Menschen lesbar), in der Sprache des Inputs, mit:

kurzer Einordnung,

Beschreibung der Trajektorie,

Beschreibung der wichtigsten UED-artigen Kennzahlen,

psychologischer Tiefensicht (klar als Interpretation gekennzeichnet),

freundlichem, respektvollem Ton.

Beispiele
Beispiel 1 – Kurzer Tagebucheintrag
Input (deutsch)

Ich wache auf und fühle mich schon wieder völlig erschöpft.
Der Gedanke an die Arbeit macht mir Angst, aber ich lächle nach außen, damit niemand etwas merkt.
Später, als ich mit meiner Freundin rede, wird es kurz leichter, aber kaum bin ich wieder allein, ist der Druck wieder da.

Erwartete strukturierte Kern-Ausgabe (gekürzt)

json
Code kopieren
{
  "utterance_states": [
    {
      "id": 1,
      "valence": -0.6,
      "arousal": 0.5,
      "dominance": 0.2,
      "discrete_emotions": {
        "sadness": 0.7,
        "fear": 0.3,
        "negative": 0.9
      }
    },
    {
      "id": 2,
      "valence": -0.7,
      "arousal": 0.8,
      "dominance": 0.2,
      "discrete_emotions": {
        "fear": 0.7,
        "sadness": 0.5,
        "negative": 0.9
      }
    },
    {
      "id": 3,
      "valence": 0.2,
      "arousal": 0.4,
      "dominance": 0.4,
      "discrete_emotions": {
        "joy": 0.4,
        "trust": 0.5,
        "positive": 0.6
      }
    },
    {
      "id": 4,
      "valence": -0.5,
      "arousal": 0.7,
      "dominance": 0.2,
      "discrete_emotions": {
        "sadness": 0.6,
        "fear": 0.5,
        "negative": 0.8
      }
    }
  ],
  "ued_metrics": {
    "home_base": {
      "valence": -0.4,
      "arousal": 0.6,
      "description": "klar in den negativen Bereich verschoben, eher angespannt"
    },
    "variability": {
      "level": "medium"
    },
    "instability": {
      "level": "medium"
    },
    "rise_rate": {
      "level": "high"
    },
    "recovery_rate": {
      "level": "low"
    }
  }
}
Fließtext-Zusammenfassung (Stichworte)

Grundstimmung über den Tag klar negativ, mit anhaltender Anspannung.

Kurze Entlastung im Kontakt mit der Freundin, danach Rückfall in ähnlichen Druck wie zuvor.

Emotion Dynamics deuten auf hohe Reaktivität auf Belastung (Arbeit) bei geringer nachhaltiger Beruhigung hin.

Psychologische Tiefensicht: mögliches Muster von „Funktionieren nach außen, innerer Druck nach innen“, gekoppelt an soziale Situationen als kurzfristige Ressource.

Beispiel 2 – Kurzer Dialogauszug
Input (gekürzt, deutsch)

A: „Warum hast du gestern nicht geschrieben?“
B: „Ich war müde und hatte keine Lust zu reden.“
A: „Es fühlt sich an, als wärst du gar nicht mehr bei mir.“
B: „Das stimmt nicht, ich brauche nur manchmal Ruhe.“

Kernelemente der erwarteten Analyse

Getrennte Trajektorien für Sprecher A und B.

Für A: negativere Valenz, höheres Arousal, stärkerer fear/sadness-Fokus (Verlustangst).

Für B: eher moderate Valenz, mittleres Arousal, leichte irritation/anger plus Bedürfnis nach Ruhe (niedrigere Dominanz in Bezug auf die Beziehungssituation, aber Versuch, Raum zu behaupten).

UED-Metriken pro Sprecher mit je eigener Home Base und Variabilität.

markdown
Code kopieren
# path: emotion-dynamics-deep-insight/references/emotion-dynamics-quick-notes.md
# Emotion Dynamics & UED – Kurzreferenz

## Kernideen

- Emotion Dynamics (Hollenstein 2015; Kuppens & Verduyn 2017) beschreibt, wie sich emotionale Zustände über die Zeit verändern, statt sie nur als statische Momentaufnahmen zu betrachten.
- Hipson & Mohammad (2021) führen **Utterance Emotion Dynamics (UED)** ein:  
  Emotionsdynamik wird aus einer Sequenz von Äußerungen (Utterances) abgeleitet – z. B. aus Dialogen, Tagebucheinträgen, Tweets. :contentReference[oaicite:2]{index=2}
- Das verlinkte EmotionDynamics-Repository nutzt Wort-Emotion-Lexika (NRC VAD / NRC EmoLex), um aus Text kontinuierliche Emotionswerte (Valenz, Arousal, Dominanz) und daraus abgeleitete Metriken zu berechnen. :contentReference[oaicite:3]{index=3}

## Typische UED-Metriken (vereinfacht)

- **Home Base**  
  - Typischer Emotionszustand einer Person (z. B. leicht positiv, gering aktiviert).
- **Variabilität**  
  - Wie stark schwanken die Emotionen um die Home Base?
- **Instabilität / Sprunghaftigkeit**  
  - Wie häufig und wie abrupt wechseln Emotionen zwischen weit entfernten Zuständen?
- **Inertia (Trägheit)**  
  - Wie schnell kehren Emotionen nach einem Ausschlag zur Home Base zurück?
- **Rise Rate**  
  - Wie schnell steigen Emotionen nach einem auslösenden Ereignis an?
- **Recovery Rate**  
  - Wie schnell beruhigen sie sich wieder?
- **Density**  
  - Wie stark ist der Text insgesamt emotional gesättigt?

## Adaption in diesem Skill

- Statt numerischer Berechnung aus Lexika arbeitet der Skill mit qualitativen, konsistent skalierten Schätzungen für:
  - Valenz, Arousal, Dominanz (`[-1,1]` bzw. `[0,1]`).
  - Diskrete Emotionen (anger, fear, joy, sadness, usw.) im Bereich `[0,1]`.
- Die oben genannten UED-Metriken werden:
  - grob aggregiert (Mittelwerte, Muster über den Verlauf),
  - qualitativ beschrieben,
  - mit psychologischen Interpretations-Hypothesen verknüpft – ohne diagnostischen Anspruch.
3) OPTIONAL: Bash-Installer
bash
Code kopieren
# path: install_emotion_dynamics_deep_insight.sh
#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="emotion-dynamics-deep-insight"

mkdir -p "$BASE_DIR"
mkdir -p "$BASE_DIR/references"

cat <<'EOF' > "$BASE_DIR/SKILL.md"
---
name: emotion-dynamics-deep-insight
description: Analysiert Texte anhand von Utterance Emotion Dynamics (UED) und ergänzt sie um psychologische Tiefensicht, indem emotionale Zustände, Verläufe und Muster strukturiert rekonstruiert werden.
---

## Wann verwenden

- Wenn ein freier Text (z. B. Chat-Verlauf, Tagebucheintrag, Mail, Monolog, Kurzgeschichte) psychologisch „tief“ gelesen werden soll.
- Wenn explizit nach Emotion Dynamics / Utterance Emotion Dynamics (UED) gefragt wird.
- Wenn emotionale Zustände über den Verlauf eines Textes (Trajektorien) und nicht nur als Momentaufnahme verstanden werden sollen.
- Wenn qualitative Hinweise auf Emotionsregulation, typische emotionale „Home Bases“ und Muster (z. B. Vermeidung vs. Annäherung) rekonstruiert werden sollen – ohne klinische Diagnose zu stellen.

## Workflow/Anweisungen

[... gleicher Inhalt wie oben in SKILL.md, hier der Kürze halber im Installer ersetzt du ihn lokal idealerweise durch die vollständige Version ...]
EOF

cat <<'EOF' > "$BASE_DIR/references/emotion-dynamics-quick-notes.md"
# Emotion Dynamics & UED – Kurzreferenz

## Kernideen

- Emotion Dynamics (Hollenstein 2015; Kuppens & Verduyn 2017) beschreibt, wie sich emotionale Zustände über die Zeit verändern, statt sie nur als statische Momentaufnahmen zu betrachten.
- Hipson & Mohammad (2021) führen Utterance Emotion Dynamics (UED) ein: Emotionsdynamik wird aus einer Sequenz von Äußerungen (Utterances) abgeleitet – z. B. aus Dialogen, Tagebucheinträgen, Tweets.
- Das verlinkte EmotionDynamics-Repository nutzt Wort-Emotion-Lexika (NRC VAD / NRC EmoLex), um aus Text kontinuierliche Emotionswerte (Valenz, Arousal, Dominanz) und daraus abgeleitete Metriken zu berechnen.

## Typische UED-Metriken (vereinfacht)

- Home Base
- Variabilität
- Instabilität / Sprunghaftigkeit
- Inertia (Trägheit)
- Rise Rate
- Recovery Rate
- Density

## Adaption in diesem Skill

- Qualitative, konsistent skalierte Schätzungen für VAD und diskrete Emotionen.
- UED-Metriken als qualitative Zusammenfassung plus psychologische Interpretations-Hypothesen (nicht-diagnostisch).
EOF

echo "Skill-Ordner '$BASE_DIR' wurde erzeugt."
Hinweis: Im Installer habe ich im SKILL.md-Block einen Platzhalter-Kommentar [... gleicher Inhalt wie oben ...] eingefügt, damit das Skript lesbar bleibt; für eine echte Nutzung solltest du dort den vollständigen SKILL.md-Inhalt einfügen.

4) Packaging-Hinweis
bash
Code kopieren
# Quick-Validation (lokal, falls du ein entsprechendes Script nutzt)
python quick_validate.py emotion-dynamics-deep-insight

# ZIP-Paket erzeugen
python package_skill.py emotion-dynamics-deep-insight ./dist