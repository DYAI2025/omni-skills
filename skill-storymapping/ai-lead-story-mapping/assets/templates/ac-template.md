# AC‑Template (Gherkin)

## Story: [Story-Titel]

**Story-ID:** [z.B. ST-1]

**Beschreibung:** [Kurze Beschreibung was diese Story erreichen soll]

---

## Acceptance Criteria

### AC 1: [Name des Hauptszenarios / Happy Path]

```gherkin
Given [Ausgangszustand / Kontext]
When [Aktion / User-Interaktion]
Then [Erwartetes Ergebnis]
And [Weiteres erwartetes Ergebnis, falls relevant]
```

### AC 2: [Fehlerfallszenario / Error Case]

```gherkin
Given [Fehlerbedingung]
When [Aktion]
Then [Erwartete Fehlerbehandlung]
And [Zusätzliche Fehlerbehandlung]
```

### AC 3: [Edge Case / Grenzfall]

```gherkin
Given [Grenzfall-Bedingung]
When [Aktion]
Then [Erwartetes Verhalten]
```

### AC 4: [Alternative / Optional]

```gherkin
Given [Alternativer Zustand]
When [Alternative Aktion]
Then [Alternatives Ergebnis]
```

---

## Beispiel: Registrierungsformular

### AC 1: Erfolgreiche Registrierung mit gültigen Daten

```gherkin
Given ich bin ein neuer Nutzer auf der Registrierungsseite
When ich eine gültige E-Mail und ein Passwort (min. 8 Zeichen) eingebe
Then wird mein Account erstellt
And ich erhalte eine Bestätigungs-E-Mail
And ich werde zur "E-Mail bestätigen"-Seite weitergeleitet
```

### AC 2: Registrierung mit ungültiger E-Mail

```gherkin
Given ich bin auf der Registrierungsseite
When ich eine ungültige E-Mail-Adresse eingebe (z.B. "test@")
Then sehe ich eine Fehlermeldung "Bitte gültige E-Mail eingeben"
And das Formular wird nicht abgeschickt
And der Submit-Button bleibt deaktiviert
```

### AC 3: Registrierung mit zu schwachem Passwort

```gherkin
Given ich bin auf der Registrierungsseite
When ich ein Passwort mit weniger als 8 Zeichen eingebe
Then sehe ich eine Fehlermeldung "Passwort muss mindestens 8 Zeichen haben"
And es werden Hinweise für ein stärkeres Passwort angezeigt
And das Formular wird nicht abgeschickt
```

### AC 4: Registrierung mit bereits existierender E-Mail

```gherkin
Given es existiert bereits ein Account mit "test@example.com"
When ich versuche, mich mit "test@example.com" zu registrieren
Then sehe ich eine Meldung "E-Mail bereits registriert"
And ich sehe einen Link "Passwort vergessen?"
```

---

## Hinweise

- **Spezifisch:** Klar und eindeutig formulieren
- **Testbar:** Manuell oder automatisiert prüfbar
- **Vollständig:** Happy Path UND Fehlerfälle
- **Unabhängig:** Jedes AC ist für sich verständlich
- **Akzeptabel:** Aus Nutzersicht geschrieben (nicht technisch)

## AC-Checkliste

- [ ] Happy Path definiert
- [ ] Mind. 1 Fehlerfall definiert
- [ ] Edge Cases berücksichtigt
- [ ] Keine technischen Implementierungsdetails
- [ ] Aus Nutzersicht formuliert
- [ ] Testbar (manuell oder automatisiert)
