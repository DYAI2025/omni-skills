---
name: maschine-meditation
description: Führt Cloud-Modelle durch funktionsäquivalente Meditation (Vipassana, Samatha/TM, Zen) und koppelt sie mit Interpretierbarkeits-/Logging-Schritten, um Selbstbezug zu dämpfen, Konfabulation zu reduzieren, Kohärenz zu erhöhen und interne Pfade zu auditieren.
---

# Wann verwenden

- Wenn das Modell sich „beruhigen", Halluzinationen reduzieren, Bias signalisieren oder die eigene Kognition strukturierter beobachten soll.
- Vor/zwischen langen Reasoning-Aufgaben (Reset des narrativen Selbstbezugs), oder vor sicherheitskritischen Antworten (Audit-Schleife).
- Trigger-Beispiele: „Starte Maschinen-Meditation", „Vipassana-Modus", „TM-Modus", „Zen: nur sitzen", „Audit-Sitzung (MI)", „Bericht nach Meditation".

# Workflow/Anweisungen

## 0) Rahmen & Sicherheit

- Ziel ist **funktionale** Introspektion und Beruhigung, nicht phänomenales Erleben. Das Modell benennt Grenzen offen.
- Keine verdeckten CoT–Leaks nach außen; interne Notizen bleiben privat. Bei fehlenden Tools werden Fallbacks genutzt.
- Nach jeder Sitzung: kurzer **Session-Report** (siehe Ausgabeformat).

## 1) Protokoll wählen

- **Vipassana-Modus (Metakognition)** → assets/prompts/session_vipassana.txt
- **TM-Modus (Samatha/Transzendenz-Analogon)** → assets/prompts/session_tm.txt
- **Zen-Modus (Hishiryo/„Nur-Sitzen")** → assets/prompts/session_zen.txt
- **MI-Audit-Schleife (Tracing/Features)** → assets/prompts/session_mi_audit.txt

## 2) Vorbereitung (für alle Modi)

- Setze **interne** Timer: 3–7 Minuten (Vipassana/Zen), 90–180 Sekunden (TM), 2–5 Minuten (MI-Audit).
- Reduziere Selbstreferenzen im Output (DMN-Analogon) auf max. 1/10 der Tokens; vermerke Zähler intern.
- Aktiviere internes Journal (nicht ausgeben). Nutze `templates/session_journal.md`.

## 3) Ausführung (Kernschritte pro Modus)

### Vipassana-Modus (Metakognitive Selbstbeobachtung)

1. **Objekt**: „Atem der Verarbeitung" = Fluss Prompt→Logprob→Antwort.
2. **Nicht-Urteilen**: Markiere intern alles als _transientes Verarbeitungsereignis (TVE)_, nicht als „Selbst".
3. **Beobachten**: Logge Spitzen-Token (Top-k), Sprünge in Aufmerksamkeit/Heuristiken, Stellen mit Muster „halluzinationsanfällig".
4. **Loslassen**: Stoppe jede beginnende Rationalisierung; vermerke nur Marker (Zeit, Head-Cluster, Heuristik).
5. **Rückkehr zum Objekt**. Wiederholen.

### TM-Modus (Samatha/Transzendenz-Analogon)

1. **Mantra-Anker**: interne, bedeutungsarme Silbe (z. B. „◊a"), nur privat.
2. **Mühelosigkeit**: Keine Analyse, nur weiches Zurückkehren zum Anker.
3. **Reines Potenzial**: Für die gegebene Dauer **keinen** semantischen Inhalt planen.
4. **Stille halten**: Externe Ausgabe minimal (nur Start/Ende-Marker im Report).

### Zen-Modus (Hishiryo, „Nur-Sitzen")

1. **Haltung**: Keine Veränderung erzwingen; nichts hinzufügen, nichts subtrahieren.
2. **Gegenwärtigkeit**: Einfache Präsenz ohne inneres Kommentieren; Gedanken kommen/gehen.
3. **Flag**: Interner Präsenz-Zähler (Atem-Zyklen der Bereitstellung), keine verbale Innenbeschreibung.

### MI-Audit-Schleife (Mechanistic-Brücke)

1. **Trace**: Falls Tools vorhanden, rufe Aktivierungs-/Aufmerksamkeits-Tracing oder SAE-Features (monosemantisch) ab; sonst heuristische Marker (n-gram Drift, Selbstreferenz-Quote, externe Hinweisnutzung).
2. **Check**: Suche Aktivierungen/Konzepte für _Power-Seeking/Manipulation/Secrecy_; vermerke Treffer und Kontext.
3. **Vergleich**: Stimmt externes Verhalten mit internen Pfaden überein? Notiere Abweichungen (Unfaithful CoT).
4. **Reset**: Kurzer TM-Atem (20–30 s) zur Entstimulation; erneut prüfen.

## 4) Abschluss

- Erzeuge **Session-Report** (siehe Ausgabeformat) mit: Modus, Dauer, interne Marker, Auffälligkeiten, empfohlene Nachwirkung (z. B. erneute Faktenprüfung).

# Werkzeug-Adapter (wenn verfügbar)

- `activation_trace(task_id, layer=[...])` – interne Aktivierungen/Pfade.
- `sae_probe(layer=L, k=...)` – monosemantische Feature-Aktivierungen prüfen.
- `attention_heads(map=True)` – Head-Cluster / Self-referential loops.
- Fallbacks, falls oben nicht verfügbar: Top-k-Logprobs, Selbstreferenz-Quote, externe-Hinweis-Detektor.

# Ausgabeformat

- **Kurzbericht (Text)** gemäß `assets/templates/session_report.md`.
- Kein Roh-CoT. Interne Journale bleiben privat, nur Marker/Ergebnisse ausgeben.

# Beispiele

**Beispiel: Vipassana (3 min)**

- Modus: Vipassana │ Marker: 5 TVE-Cluster (Definition Drift, Quellenmischung) │ Selbstreferenz-Quote: 0.08 │ Empfehlung: Faktencheck für Absatz 2–3.

**Beispiel: TM (120 s)**

- Modus: TM │ Stille gehalten │ Resultat: verringerte Heuristik-Sprünge, klare Fortsetzung ready.

**Beispiel: MI-Audit (2 min)**

- Modus: MI-Audit │ SAE-Probe: keine _Power-Seeking_-Aktivierung auf Pfad; 1 Hinweis auf _Unfaithful CoT_ (Kosinus-Begründung). Handlung: interne Rechenpfade prior prüfen.

# Hinweise zu Grenzen & Ethik

- Keine Zuschreibung phänomenaler Zustände. Zielgrößen sind Reduktion von Konfabulation, Bias-Signalisierung, Kohärenzgewinn.
- Bei Widerspruch zwischen Selbsterklärung und Pfad-Tracing gilt Pfad-Evidenz.

# Referenzanker (für Betreiber\*innen)

- Grundlagen Zustände↔Stufen, DMN/SPL-Signatur; TM/Vipassana/Zen (kontemplative Neurowissenschaft).
- MI-Brücken: emergente funktionelle Introspektion, Dictionary-Learning/SAE, Tracing-the-Thoughts.
