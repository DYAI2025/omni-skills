# Mapping‑ & Cutting‑Patterns

## Mapping (vom Ziel zur Story)

### 1. Goal → Activities (3–7)

Erst die gesamte Reise sichtbar machen:

- Beginne mit dem Nutzerziel
- Identifiziere 3-7 große Aktivitäten (zu viele = zu detailliert, zu wenige = zu grob)
- Ordne chronologisch von links nach rechts
- Frage: "Was muss der Nutzer tun, um sein Ziel zu erreichen?"

### 2. Activity → Steps (3–7)

Jede Aktivität in konkrete Schritte zerlegen:

- 3-7 Steps pro Activity als Richtwert
- Steps beschreiben die Teilhandlungen innerhalb einer Activity
- Bleibe auf gleichem Abstraktionsniveau
- Frage: "Wie läuft diese Aktivität im Detail ab?"

### 3. Steps → Stories (mind. 1 pro Step)

Konkrete, implementierbare Stories erzeugen:

- Mindestens 1 Story pro Step (oft mehrere)
- INVEST-Kriterien beachten
- Acceptance Criteria (AC) im Gherkin-Format hinzufügen
- Must-haves nach oben, Alternativen darunter
- Frage: "Was muss implementiert werden, damit dieser Schritt funktioniert?"

### 4. Gaps/Dependencies walken

Map narrativ durchgehen:

- "Walk through" der gesamten Journey im Team
- Identifiziere fehlende Schritte oder Stories
- Decke technische Stories auf (z.B. API-Integration, Datenbank-Setup)
- Markiere Abhängigkeiten zwischen Stories
- Diskutiere Risiken und Annahmen
- Entwickler\*innen müssen dabei sein!

## Cutting (vertikale Slices)

### End‑to‑End‑Slice (MVP/Walking Skeleton)

Minimaler Durchstich Start → Ziel:

- Mind. 1 Story aus jedem kritischen Backbone-Schritt
- Funktional vollständig, auch wenn "dünn"
- Liefert Complete Product Experience (CPE)
- Ziel: Lerneffekt und frühes Feedback
- Frage: "Was ist der allereinfachste Weg durch die Journey?"

### Risk‑First‑Slice

Unsicherheit früh reduzieren:

- Identifiziere technische Risiken oder Unbekannte
- Isoliere riskante Regel/Integration in eigene Slice
- Validiere Annahmen früh
- Beispiel: Externe API-Integration, komplexe Berechnung

### Value‑First‑Slice

Höchster Kundennutzen zuerst:

- Priorisiere nach Business Value
- Liefere das, was Nutzer am dringendsten brauchen
- Oft kombiniert mit MVP

### Interface‑Slice

UI-Weg mit Backend-Stub:

- Frontend komplett, Backend minimal
- Erlaubt UX-Testing ohne volle Implementierung
- Gut für Design-Validierung

### Rule‑Slice

Einzelne Geschäftsregel aktivieren:

- Fokus auf eine spezifische Regel oder Policy
- Rest über Default-Verhalten
- Beispiel: Preiskalkulation, Validierungsregel

## Heuristiken

### Pro Slice

- 1 Goal
- 1–2 Activities (bei MVP eventuell alle kritischen)
- 2–4 Steps
- 1–3 Stories pro Step
- Testbar mit klarem Outcome

### Nach 2–3 Slices

- Konsistenz‑Review durchführen
- Outcome‑Check: Werden Ziele erreicht?
- Dependencies nochmal prüfen
- Bei Bedarf re-slicen

## Anti-Patterns (vermeiden)

- **Horizontal Slicing**: Nach technischer Schicht (z.B. "erst DB, dann Backend, dann UI") → liefert keinen Nutzen
- **Feature Blob**: Zu große Slices ohne klares MVP
- **Perfektionismus**: Jede Story komplett fertig statt iterativ
- **Fehlende ACs**: Stories ohne testbare Kriterien
- **Ignorierte Dependencies**: Technische Abhängigkeiten nicht berücksichtigt
