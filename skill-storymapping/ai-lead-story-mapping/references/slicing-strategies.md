# Slicing‑Strategien (Releases planen)

## Grundprinzip: Vertikales Slicing

Story Mapping ermöglicht **horizontale Cut-Lines**, die verschiedene Release-Inkremente definieren. Jede Slice sollte:

- Vertikal durch die gesamte Applikation gehen (UI → Logic → Data)
- Einen nutzbaren Wert liefern
- Testbar sein
- Mit Metriken/Outcomes verbunden sein

## MVP zuerst (Walking Skeleton)

### Definition

Der erste Slice ist das **Walking Skeleton** oder **MVP**:

- Pro kritischem Backbone‑Schritt mind. eine Story
- Liefert eine durchgängige Complete Product Experience (CPE)
- Dünn, aber funktional vollständig
- End-to-End nutzbar, auch wenn minimal

### Kriterien für MVP

- ✅ Nutzer kann das primäre Ziel erreichen
- ✅ Alle kritischen Activities sind abgedeckt
- ✅ System funktioniert von Frontend bis Backend
- ✅ Testbar und deploybar
- ❌ Keine "schönen" Features
- ❌ Keine Alternativen oder Komfort
- ❌ Keine Optimierungen

### Beispiel MVP (Onboarding)

```
Activity: Registrieren
  ✓ Story: Basic E-Mail/Passwort-Formular
  ✓ Story: Double-Opt-In

Activity: Erste Schritte
  ✓ Story: Einfache Guided Tour (3 Tipps)
  ✓ Story: Erste Mini-Aufgabe
```

## Folge‑Slices „Fleisch hinzufügen"

Nach dem MVP bauen weitere Slices auf:

### Slice 2: Komfort & Alternativen

- OAuth-Login (Alternative zu E-Mail)
- Passwort-Vergessen-Flow
- Erweiterte Guided Tour mit mehr Schritten
- Profilbild hochladen

### Slice 3: Optimierungen & Nice-to-haves

- Passwort-Stärke-Anzeige
- Auto-Save im Formular
- Animations und Transitions
- Analytics-Events verfeinern

### Slice 4+: Weitere Features

- Multi-Faktor-Authentifizierung
- Social Sharing
- Gamification
- A/B-Tests

## Opening/Mid/End‑Game pro Release‑Slice

Jede Slice sollte strukturiert geplant werden:

### Opening (Strategie & Ziele)

- **Ziel/Outcome:** Was wollen wir erreichen?
- **Hypothese:** Wir glauben, dass...
- **Metriken:** Wie messen wir Erfolg?
- **Scope:** Welche Stories sind enthalten?

### Mid-Game (Umsetzung)

- **Dependencies:** Was muss zuerst gebaut werden?
- **Risiken:** Was könnte schiefgehen?
- **Assumptions:** Was nehmen wir an?
- **Team-Kapazität:** Passt der Scope in den Timebox?

### End-Game (Validierung)

- **Definition of Done:** Alle ACs erfüllt?
- **Testing:** Manuelle & automatisierte Tests grün?
- **Metrics Check:** Metriken implementiert und aktiv?
- **Review:** Stakeholder-Feedback eingeholt?
- **Retrospektive:** Was haben wir gelernt?

## Slice-Priorisierung

### Faktoren für Priorisierung

1. **Value:** Nutzen für User/Business
2. **Risk:** Technisches oder fachliches Risiko
3. **Dependencies:** Abhängigkeiten zu anderen Stories
4. **Learning:** Validierung von Annahmen
5. **Effort:** Aufwand (aber nicht der wichtigste Faktor!)

### Priorisierungs-Frameworks (optional)

Nach dem Slicing können Stories mit bewährten Frameworks priorisiert werden:

- **WSJF** (Weighted Shortest Job First): (Business Value + Time Criticality + Risk Reduction) / Job Size
- **RICE**: (Reach × Impact × Confidence) / Effort
- **Kano-Modell**: Must-haves, Performance, Delighters

## Best Practices

### ✅ Do's

- Slice so dünn wie möglich für schnelles Feedback
- Jede Slice muss deploybar und testbar sein
- Outcomes/Metriken pro Slice definieren
- Dependencies zwischen Slices dokumentieren
- Team bei Slicing-Entscheidungen einbeziehen

### ❌ Don'ts

- Nicht nach technischen Schichten slicen
- Keine zu großen Slices (max. 2-3 Sprints)
- MVP nicht überladen ("Minimum" ernst nehmen)
- Stories nicht isoliert betrachten (Gesamtbild!)
- Nicht zu früh in Details verfallen

## Slice-Template

```markdown
## Slice N – [Name]

**Ziel/Outcome:** [Messbares Ziel]
**Hypothese:** Wir glauben, dass [Annahme]
**Metriken:** [KPIs und Events]
**Scope (Stories):** ST-1, ST-3, ST-7
**Dependencies:** [Technische oder fachliche Abhängigkeiten]
**Risiken/Assumptions:** [Bekannte Unsicherheiten]
**Timebox:** [z.B. 2 Sprints, 4 Wochen]
**DoD:**

- [ ] Alle ACs erfüllt
- [ ] Tests grün
- [ ] Code Review done
- [ ] Deployed in Staging
- [ ] Metrics aktiv
```

## Visualisierung

Story Maps sollten die Slices visuell darstellen:

```
Activities:    [A1: Register] [A2: First Steps] [A3: Core Feature]
              ─────────────────────────────────────────────────
Slice 1 (MVP): ST-1, ST-2      ST-5                ST-8
              ─────────────────────────────────────────────────
Slice 2:       ST-3, ST-4      ST-6, ST-7          ST-9, ST-10
              ─────────────────────────────────────────────────
Slice 3:       ST-11           ST-12               ST-13, ST-14
```

## Maintenance

Story Maps sind **lebendige Artefakte**:

- Nach jedem Release: Map aktualisieren
- Neue Learnings einarbeiten
- Slices anpassen basierend auf Metriken
- Backlog kontinuierlich gegen Map abgleichen
