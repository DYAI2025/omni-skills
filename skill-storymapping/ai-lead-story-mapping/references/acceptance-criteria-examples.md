# Akzeptanzkriterien – Beispiele (Gherkin)

## Gherkin-Format

Acceptance Criteria (ACs) werden im **Given/When/Then**-Format geschrieben:

- **Given** = Ausgangszustand / Kontext
- **When** = Aktion / Trigger
- **Then** = Erwartetes Ergebnis

## Beispiele nach Pattern

### Workflow/Process Stories

#### Registrierung

```gherkin
Given ich bin ein Neukunde ohne Account
When ich registriere mich mit E‑Mail und Passwort
Then erhalte ich eine Bestätigungs‑E‑Mail
And mein Account ist im Status "pending"
```

#### Passwort-Validierung

```gherkin
Given ich gebe ein schwaches Passwort ein (< 8 Zeichen)
When ich sende das Registrierungsformular
Then sehe ich eine Fehlermeldung zur Passwortstärke
And kann nicht fortfahren
And erhalte Hinweise für ein stärkeres Passwort
```

#### Login

```gherkin
Given ich habe einen bestätigten Account
When ich melde mich mit korrekten Credentials an
Then werde ich zur Dashboard-Seite weitergeleitet
And sehe eine Willkommensnachricht mit meinem Namen
```

### Interface/UI Stories

#### Guided Tour

```gherkin
Given ich bin ein Erstnutzer und logge mich zum ersten Mal ein
When die Anwendung lädt
Then sehe ich ein Overlay mit einer Guided Tour
And es werden 3 Hinweise nacheinander angezeigt
And ich kann die Tour jederzeit beenden
```

#### Formular-Validierung

```gherkin
Given ich bin auf dem Kontaktformular
When ich verlasse das E-Mail-Feld ohne gültige E-Mail einzugeben
Then sehe ich eine Inline-Fehlermeldung unter dem Feld
And das Feld wird rot umrandet
And der Submit-Button bleibt deaktiviert
```

#### Responsive Design

```gherkin
Given ich öffne die Anwendung auf einem mobilen Gerät (< 768px Breite)
When die Seite lädt
Then sehe ich eine mobile-optimierte Navigation (Hamburger-Menü)
And alle Inhalte sind ohne horizontales Scrollen lesbar
```

### Rule/Validation Stories

#### Preisberechnung

```gherkin
Given ich habe 3 Artikel im Warenkorb mit Gesamtwert 150€
When ich einen Gutschein-Code "SAVE20" mit 20% Rabatt eingebe
Then wird der Gesamtpreis auf 120€ reduziert
And der Rabatt wird als separate Zeile angezeigt
```

#### Zugangsberechtigung

```gherkin
Given ich bin als Standard-Nutzer eingeloggt (keine Admin-Rechte)
When ich versuche, auf den Admin-Bereich zuzugreifen
Then werde ich auf eine "Zugriff verweigert"-Seite weitergeleitet
And sehe eine Meldung "Sie haben keine Berechtigung für diese Seite"
```

#### Business Rule

```gherkin
Given ein Benutzer hat 3 fehlerhafte Login-Versuche innerhalb von 5 Minuten
When der 4. fehlerhafte Versuch erfolgt
Then wird das Konto für 15 Minuten gesperrt
And der Nutzer erhält eine E-Mail über die temporäre Sperrung
```

### Operation/Action Stories

#### Datei-Upload

```gherkin
Given ich bin auf der Profil-Seite
When ich ein Bild (< 5MB, Format: JPG/PNG) hochlade
Then wird das Bild als Vorschau angezeigt
And es erscheint eine Erfolgsmeldung "Profilbild aktualisiert"
And das Bild ist sofort in der Kopfzeile sichtbar
```

#### Daten löschen

```gherkin
Given ich habe einen Artikel in meinem Account erstellt
When ich auf "Löschen" klicke
Then erscheint eine Bestätigungsdialog "Möchten Sie wirklich löschen?"
And nach Bestätigung wird der Artikel entfernt
And ich sehe eine Bestätigung "Artikel erfolgreich gelöscht"
And der Artikel erscheint nicht mehr in der Liste
```

#### Export

```gherkin
Given ich habe 10 Einträge in meiner Liste
When ich auf "Als CSV exportieren" klicke
Then wird eine CSV-Datei mit allen 10 Einträgen heruntergeladen
And die Datei enthält Spalten für: ID, Titel, Datum, Status
And der Dateiname folgt dem Format: "export_YYYY-MM-DD.csv"
```

### Integration Stories

#### API-Call

```gherkin
Given die externe Wetter-API ist erreichbar
When ich meine Stadt eingebe und nach dem Wetter suche
Then sehe ich die aktuelle Temperatur und Wetterlage
And die Daten sind nicht älter als 10 Minuten
```

#### Fehlerbehandlung API

```gherkin
Given die externe Zahlungs-API ist nicht erreichbar
When ich versuche, eine Zahlung durchzuführen
Then sehe ich eine Fehlermeldung "Zahlungsdienst vorübergehend nicht verfügbar"
And die Transaktion wird nicht abgeschlossen
And ich werde aufgefordert, es später erneut zu versuchen
```

### Data/CRUD Stories

#### Datensatz erstellen

```gherkin
Given ich bin auf der "Neue Aufgabe erstellen"-Seite
When ich Titel, Beschreibung und Fälligkeitsdatum eingebe und speichere
Then wird die Aufgabe in der Datenbank gespeichert
And ich werde zur Aufgabenliste weitergeleitet
And die neue Aufgabe erscheint oben in der Liste
```

#### Datensatz bearbeiten

```gherkin
Given ich habe eine existierende Aufgabe mit Titel "Alte Aufgabe"
When ich den Titel zu "Neue Aufgabe" ändere und speichere
Then wird die Änderung in der Datenbank persistiert
And ich sehe sofort den neuen Titel "Neue Aufgabe"
And das "Zuletzt geändert"-Datum wird aktualisiert
```

## Negative Test Cases (wichtig!)

### Ungültige Eingaben

```gherkin
Given ich bin auf dem Registrierungsformular
When ich eine ungültige E-Mail-Adresse eingebe (z.B. "test@")
Then sehe ich eine Fehlermeldung "Bitte gültige E-Mail eingeben"
And das Formular wird nicht abgeschickt
```

### Fehlende Berechtigungen

```gherkin
Given ich bin nicht eingeloggt
When ich versuche, direkt auf eine geschützte Seite zuzugreifen
Then werde ich zur Login-Seite weitergeleitet
And sehe eine Meldung "Bitte melden Sie sich an"
```

### Timeout/Performance

```gherkin
Given die Datenbank-Abfrage dauert länger als 3 Sekunden
When ich eine Suche durchführe
Then sehe ich einen Lade-Indikator
And nach 3 Sekunden erscheint eine Meldung "Die Suche dauert länger als erwartet"
And nach 10 Sekunden wird die Anfrage abgebrochen mit "Timeout-Fehler"
```

## Edge Cases

### Leere Zustände

```gherkin
Given ich habe keine Aufgaben in meiner Liste
When ich die Aufgabenliste öffne
Then sehe ich eine "Keine Aufgaben vorhanden"-Nachricht
And einen Button "Erste Aufgabe erstellen"
```

### Grenzwerte

```gherkin
Given ich habe bereits 100 Artikel in meiner Bibliothek (Maximum)
When ich versuche, einen weiteren Artikel hinzuzufügen
Then sehe ich eine Fehlermeldung "Maximale Anzahl erreicht (100)"
And der Artikel wird nicht hinzugefügt
And ich sehe einen Hinweis zum Upgrade auf Premium
```

## Komplexe Szenarien (Scenario Outline)

### Mehrere Varianten testen

```gherkin
Scenario Outline: Passwort-Validierung für verschiedene Eingaben
  Given ich gebe ein Passwort "<password>" ein
  When ich das Formular absende
  Then sehe ich das Ergebnis "<result>"

  Examples:
    | password    | result                           |
    | 123         | Fehler: Zu kurz (min. 8 Zeichen) |
    | abcdefgh    | Fehler: Keine Zahl enthalten     |
    | Abcd1234    | Erfolg: Passwort akzeptiert      |
    | A1!@#$%^&*  | Erfolg: Passwort akzeptiert      |
```

## Best Practices für ACs

### ✅ Do's

- **Spezifisch:** Klar und eindeutig formulieren
- **Testbar:** Automatisiert oder manuell prüfbar
- **Vollständig:** Happy Path UND Fehlerfall
- **Unabhängig:** Jedes AC ist für sich verständlich
- **Akzeptabel:** Aus Nutzersicht geschrieben

### ❌ Don'ts

- Keine Implementierungsdetails ("mit SQL Query...")
- Nicht zu vage ("sollte gut funktionieren")
- Nicht zu viele ACs pro Story (max. 5-7)
- Keine technischen Details für Business-Stories

## AC-Template

```gherkin
Story: [Titel der Story]

AC 1: [Name des Szenarios]
  Given [Ausgangszustand]
  When [Aktion]
  Then [Erwartetes Ergebnis]
  And [Weiteres erwartetes Ergebnis, optional]

AC 2: [Fehlerfall-Szenario]
  Given [Fehlerbedingung]
  When [Aktion]
  Then [Erwartete Fehlerbehandlung]

AC 3: [Edge Case]
  Given [Grenzfall]
  When [Aktion]
  Then [Erwartetes Verhalten]
```

## Integration in Story Map

ACs werden direkt in der Story Map bzw. im story_map.json hinterlegt:

```json
{
  "id": "ST1",
  "title": "Formular E-Mail/Passwort",
  "ac": [
    "Given Felder leer, When gültig ausfüllen, Then Konto angelegt",
    "Given ungültige E-Mail, When absenden, Then Fehlermeldung sichtbar"
  ]
}
```
