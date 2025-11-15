# Release‑Slice (Vorlage)

## Slice N – [Kurzbezeichnung]

**Ziel/Outcome:** [Messbares Ziel, z. B. Aktivierungsrate D1 auf 30 % erhöhen]

**Hypothese:** Wir glauben, dass [Annahme über Nutzerverhalten oder Business Impact]

**Metriken:**

- [Event/KPI 1, z.B. "user.registered" Event-Count]
- [KPI 2, z.B. "Time to First Value < 10 Minuten"]
- [Messfenster: z.B. "30 Tage nach Release"]

**Scope (Stories):**

- ST-[ID]: [Story-Titel]
- ST-[ID]: [Story-Titel]
- ST-[ID]: [Story-Titel]

**Risiken/Assumptions:**

- [Bekannte Unsicherheiten, z.B. "E-Mail-Zustellung hängt von externem Provider ab"]
- [Technische Risiken, z.B. "Performance bei >1000 gleichzeitigen Nutzern unklar"]
- [Annahmen, z.B. "Nutzer haben funktionierende E-Mail-Adresse"]

**Dependencies:**

- [Externe Dependencies, z.B. "E-Mail-Service API muss verfügbar sein"]
- [Interne Dependencies, z.B. "User-Service muss deployed sein"]

**Timebox:** [z.B. 2 Sprints, 4 Wochen]

**Definition of Done:**

- [ ] Alle Stories haben erfüllte ACs
- [ ] Telemetrie/Analytics aktiv für alle Metriken
- [ ] Unit- und Integrationstests grün (>80% Coverage)
- [ ] Code Review abgeschlossen
- [ ] Deployed in Staging
- [ ] Manual QA durchgeführt
- [ ] Regressionstests grün
- [ ] Dokumentation aktualisiert

---

## Beispiel: Slice 1 – MVP (Walking Skeleton)

**Ziel/Outcome:** Nutzer kann sich registrieren und erste Erfahrung mit Produkt machen (Activation Rate D1 ≥ 30 %)

**Hypothese:** Wir glauben, dass ein einfacher, schneller Onboarding-Flow mit minimaler Guided Tour zu höherer Aktivierung führt.

**Metriken:**

- `user.registered` Event-Count
- `user.first_action_completed` Event-Count
- Time to First Value (TTFV) < 10 Minuten
- Messfenster: 30 Tage nach Release

**Scope (Stories):**

- ST-1: Formular E-Mail/Passwort
- ST-2: Double-Opt-In
- ST-3: Guided Tour Overlay
- ST-4: Erste Aufgabe abschließen

**Risiken/Assumptions:**

- E-Mail-Zustellung kann verzögert sein (Spamfilter)
- Nutzer müssen E-Mail-Zugang haben
- Performance bei Peak-Load unklar

**Dependencies:**

- E-Mail-Service (SendGrid/AWS SES)
- User-Database (PostgreSQL)
- Analytics-Service (Amplitude/Mixpanel)

**Timebox:** 3 Sprints (6 Wochen)

**Definition of Done:**

- [x] Alle Stories haben erfüllte ACs
- [x] Telemetrie aktiv
- [x] Tests grün (Coverage 85%)
- [x] Code Review done
- [x] Deployed in Production
- [x] A/B-Test Setup vorbereitet
