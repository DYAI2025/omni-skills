# Workshop‑Facilitation (Story Mapping)

## Vorbereitung

### Framing

Vor dem Workshop klären:

- **Problem Statement:** Welches Nutzerproblem lösen wir?
- **Elevator Pitch:** In 30 Sekunden erklärbar?
- **Personas:** Wer sind die primären Nutzer? (1-3 Personas)
- **Nutzen/Value:** Was ist der erwartete Business Value?
- **Scope:** Was ist explizit NICHT Teil dieser Map?
- **Timebox:** Wie viel Zeit haben wir? (idealer Workshop: 2-4h)

### Team zusammenstellen

Cross‑funktional ist Pflicht:

- **Product Owner / Stakeholder** (1-2): Fachliche Vision & Priorisierung
- **Entwicklung** (3-5): Technische Machbarkeit & Dependencies
- **UX/Design** (1): Nutzerperspektive & Interface
- **QA/Testing** (1, optional): Testbarkeit & ACs
- **Gesamt:** 5–10 Personen ideal (max. 12)

⚠️ **Wichtig:** Entwickler\*innen müssen dabei sein! Ohne Tech-Perspektive entstehen unrealistische Maps.

### Format wählen

- **Physisch (empfohlen):**
  - Großes Whiteboard oder Wand
  - Haftnotizen (verschiedene Farben für Activities/Steps/Stories)
  - Marker
  - Kamera für Dokumentation
  - Vorteile: Haptisch, bessere Gruppendynamik
- **Digital:**
  - Tools: Miro, Mural, FigJam, Azure Boards
  - Templates vorbereiten
  - Video-Call mit Screenshare
  - Vorteile: Remote-Teams, leichte Nachbearbeitung

## Workshop‑Ablauf (vereinfacht)

### Phase 1: Framing & Warm-Up (15-30 min)

1. **Ziel klären:** Elevator Pitch präsentieren
2. **Personas vorstellen:** Primäre Nutzer identifizieren
3. **Erwartungen setzen:** Was ist das Ergebnis? (Story Map + MVP-Slice)
4. **Regeln:**
   - Alle Meinungen zählen
   - Keine Diskussionen über Implementierung (später)
   - "Yes, and..." statt "Yes, but..."
   - Timeboxing respektieren

### Phase 2: Backbone erstellen (30-60 min)

**Horizontale Achse: Die gesamte Reise**

1. **Big Picture:**
   - Frage: "Was muss der Nutzer tun, um sein Ziel zu erreichen?"
   - Sammle 5-10 große Aktivitäten (brainstorming)
2. **Chronologisch ordnen:**
   - Von links nach rechts: Start → Ziel
   - Duplikate entfernen, ähnliche gruppieren
   - Auf 3-7 Activities konsolidieren
3. **Validieren:**
   - Frage: "Haben wir die gesamte Reise abgedeckt?"
   - Frage: "Fehlt etwas Kritisches?"
   - Lücken mit neuen Activities füllen

**Output:** Backbone mit 3-7 Activities horizontal angeordnet

### Phase 3: Stories sammeln & priorisieren (60-90 min)

**Vertikale Achse: Wichtigkeit & Alternativen**

1. **Steps hinzufügen:**

   - Für jede Activity: 3-7 konkrete Steps
   - Unter die jeweilige Activity kleben
   - Steps bleiben in chronologischer Reihenfolge

2. **Stories generieren:**

   - Für jeden Step: Was muss implementiert werden?
   - Jede Story auf separate Haftnotiz
   - Format: "Als [Persona] möchte ich [Aktion], damit [Nutzen]"
   - Mind. 1 Story pro Step

3. **Vertikal priorisieren:**
   - Must-haves nach oben (Was brauchen wir unbedingt?)
   - Nice-to-haves darunter (Was wäre schön zu haben?)
   - Alternativen darunter ("oder" statt "und")
   - Frage: "Was ist je Schritt am wichtigsten?"

**Output:** Stories unter jedem Step, vertikal priorisiert

### Phase 4: Map abwandern & verfeinern (30-45 min)

**Lücken, Dependencies & Risiken aufdecken**

1. **Walk Through:**
   - Moderator "geht" die Map narrativ durch
   - "Unser Nutzer startet bei Activity 1, Step 1..."
   - Team unterbricht bei Unklarheiten
2. **Lücken identifizieren:**

   - Fehlen Schritte? → Ergänzen
   - Fehlen Stories? → Hinzufügen
   - Gibt es Sprünge in der Journey? → Füllen

3. **Technische Stories aufdecken:**

   - Entwickler: "Was brauchen wir technisch?"
   - Beispiele: API-Setup, DB-Schema, Auth-Service
   - Als separate Stories hinzufügen

4. **Dependencies markieren:**
   - Welche Stories hängen voneinander ab?
   - Mit Pfeilen oder Nummern kennzeichnen
   - Risiken notieren (z.B. externe API, Performance)

**Output:** Vollständige, validierte Map mit Dependencies

### Phase 5: Slicing & Releases planen (30-60 min)

**Horizontale Cut-Lines ziehen**

1. **MVP/Walking Skeleton (Slice 1):**

   - Frage: "Was ist der dünnste End-to-End-Weg?"
   - Oberste horizontale Linie ziehen
   - Mind. 1 Story aus jedem kritischen Backbone-Schritt
   - Validieren: Liefert das eine Complete Product Experience?

2. **Folge-Slices:**

   - Weitere horizontale Linien für Slice 2, 3, ...
   - Jede Slice fügt "Fleisch" hinzu
   - Frage: "Was kommt als Nächstes für maximalen Nutzen?"

3. **Outcomes & Metriken definieren:**
   - Pro Slice: Was wollen wir erreichen?
   - Wie messen wir Erfolg?
   - Hypothesen formulieren

**Output:** 2-4 Slices mit klaren Zielen und Metriken

### Phase 6: Wrap-Up & Artefakte (15-30 min)

1. **Foto/Screenshot:** Map dokumentieren
2. **Digitalisieren:** In Tool/JSON übertragen (kann nach Workshop passieren)
3. **Nächste Schritte klären:**
   - Wer erstellt Backlog-Items?
   - Wann ist Sprint Planning?
   - Wer pflegt die Map?
4. **Retrospektive (kurz):**
   - Was lief gut?
   - Was würden wir anders machen?

## Moderations-Tipps

### Do's ✅

- **Timeboxing strikt einhalten:** Nutze Timer
- **Visualisiere kontinuierlich:** Alle sehen dasselbe
- **Stille Phasen einplanen:** Individuelle Reflexion vor Diskussion
- **Parkplatz für Tangenten:** Wichtige, aber off-topic Punkte festhalten
- **Energie managen:** Pausen alle 60-90 Minuten
- **Alle einbeziehen:** Ruhigere Teilnehmer gezielt ansprechen
- **Divergieren dann Konvergieren:** Erst sammeln, dann filtern

### Don'ts ❌

- **Nicht zu früh in Details:** Erst Big Picture, dann Verfeinerung
- **Keine Implementierungs-Diskussionen:** "Wie bauen wir das?" kommt später
- **Keine Dominanz einzelner:** Alle Stimmen zählen gleich
- **Nicht überladen:** Lieber 70% fertig und nutzbar als 100% chaotisch
- **Keine perfekte Map erwarten:** Iterativ verbessern

## Facilitation-Techniken

### Dot Voting

Bei Uneinigkeit über Prioritäten:

- Jede Person bekommt 3-5 Punkte (Dots)
- Punkte auf wichtigste Stories verteilen
- Stories mit meisten Punkten = höchste Priorität

### Silent Brainstorming

Für bessere Ideen-Generierung:

- 5-10 min stille Phase
- Jede Person schreibt eigene Stories auf Haftnotizen
- Dann gleichzeitig aufhängen und clustern

### Crazy 8's

Für alternative Flows:

- 8 Minuten, 8 schnelle Skizzen pro Person
- Fördert kreatives Denken
- Beste Ideen in Map übernehmen

### Impact/Effort Matrix

Für Priorisierung nach MVP:

- 2×2 Matrix: High/Low Impact × High/Low Effort
- Stories positionieren
- High Impact + Low Effort = Quick Wins (Slice 2)

## Nach dem Workshop

### Lebendiges Artefakt pflegen

Story Maps sind **nicht einmalig**:

- Nach jedem Sprint/Release aktualisieren
- Neue Learnings einarbeiten
- Abgeschlossene Stories markieren
- Neue Stories basierend auf Feedback hinzufügen
- Map als Single Source of Truth im Team nutzen

### Regelmäßige Reviews

- **Monatlich:** Kurzer Check-In (15-30 min)
- **Quarterly:** Größere Refinement-Session (2h)
- **Nach Major Release:** Vollständige Map-Review (halber Tag)

### Integration in Team-Prozesse

- Sprint Planning: Gegen Map abgleichen
- Backlog Refinement: Stories aus Map ableiten
- Retrospektiven: Map als Diskussionsgrundlage
- Roadmap-Planung: Slices als Release-Inkremente

## Beispiel-Agenda (4h Workshop)

```
09:00-09:30  Framing & Warm-Up
09:30-10:30  Backbone erstellen
10:30-10:45  Pause ☕
10:45-12:00  Stories sammeln & priorisieren
12:00-13:00  Mittagspause 🍴
13:00-13:45  Map abwandern & verfeinern
13:45-14:45  Slicing & Releases
14:45-15:00  Wrap-Up & Next Steps
```

## Remote Workshop Besonderheiten

### Zusätzliche Vorbereitung

- Miro/Mural-Board vorher aufsetzen
- Test-Call 30 min vorher
- Breakout-Rooms konfigurieren
- Digitale Timer-Tools bereithalten

### Engagement erhöhen

- Mehr Pausen (alle 60 min)
- Breakout-Sessions für kleinere Diskussionen
- Chat für Fragen nutzen
- Reaktionen/Emojis für schnelles Feedback
- Noch strikter timen (Remote ermüdet schneller)

### Dokumentation

- Screen Recording für Nachvollziehbarkeit
- Live-Transkription für spätere Referenz
- Regelmäßige Screenshots als Zwischenstände
