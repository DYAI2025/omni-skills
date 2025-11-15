# Slice‑Vorschläge

**Produkt:** Onboarding 1.0
**Goal:** Schnell registrieren und ersten Nutzen erleben

## Slice 1 – MVP (Walking Skeleton)

**Ziel:** End-to-End nutzbare Complete Product Experience

**Outcome/Metrik:** Aktivierungsrate D1 ≥ 30 % (TTFV ≤ 10 min)

**Hypothese:** Wir glauben, dass ein einfacher, schneller Onboarding-Flow mit minimaler Guided Tour zu höherer Aktivierung führt als ein Feature-überladenes Onboarding.

**Scope (Stories):**

- **ST1**: Formular E‑Mail/Passwort (activity=A1, step=S11)
- **ST2**: Double‑Opt‑In (activity=A1, step=S12)
- **ST3**: Guided Tour Overlay (activity=A2, step=S21)
- **ST4**: Erste Aufgabe abschließen (activity=A2, step=S22)

**Metriken:**

- `user.registered` Event-Count
- `user.email_confirmed` Event-Count
- `user.tour_completed` Event-Count
- `user.first_action_completed` Event-Count
- Time to First Value (TTFV) < 10 Minuten

**Dependencies:**

- E-Mail-Service (SendGrid/AWS SES)
- User-Database (PostgreSQL)
- Analytics-Service (Amplitude/Mixpanel)

**Risiken:**

- E-Mail-Zustellung kann verzögert sein (Spamfilter)
- Performance bei Peak-Load unklar
- Tour könnte als störend empfunden werden (A/B-Test geplant)

**Timebox:** 3 Sprints (6 Wochen)

**Definition of Done:**

- [ ] Alle ACs erfüllt und getestet
- [ ] Telemetrie aktiv für alle Events
- [ ] Unit- und Integrationstests grün (>80% Coverage)
- [ ] Code Review abgeschlossen
- [ ] Deployed in Production
- [ ] Manuelle QA durchgeführt
- [ ] Performance-Tests bestanden (>1000 concurrent users)
- [ ] A/B-Test Setup vorbereitet

---

## Slice 2 – Komfort & Alternativen

**Ziel:** Alternativen und Komfortfunktionen für bessere UX

**Scope (potenzielle Stories):**

- OAuth-Login (Google, Microsoft)
- Passwort-Vergessen-Flow
- Erweiterte Guided Tour mit mehr Schritten
- Profilbild hochladen
- Passwort-Stärke-Anzeige mit Echtzeit-Feedback
- Auto-Save im Formular

**Hypothese:** Wir glauben, dass OAuth-Login die Registrierungsrate um 15% erhöht.

**Metriken:**

- Registrierungsrate via OAuth vs. E-Mail
- Passwort-Vergessen-Nutzung

**Timebox:** 2 Sprints (4 Wochen)

---

## Slice 3 – Optimierungen & Advanced Features

**Ziel:** Feinschliff und erweiterte Features

**Scope (potenzielle Stories):**

- Multi-Faktor-Authentifizierung (MFA)
- Social Sharing nach erster Aufgabe
- Gamification (Badges, Progress Bar)
- A/B-Test Varianten für Tour
- Performance-Optimierungen
- Analytics-Dashboard für Onboarding-Metriken

**Hypothese:** Wir glauben, dass Gamification die Completion-Rate um 20% erhöht.

**Timebox:** 2-3 Sprints (4-6 Wochen)

---

**Hinweise:**

- Slice 1 (MVP) enthält mind. 1 Story pro kritischem Backbone-Schritt
- Folge-Slices fügen 'Fleisch' hinzu: Alternativen, Komfort, Optimierungen
- Jede Slice sollte mit Outcomes/Metriken versehen werden
- Dependencies zwischen Stories beachten!
- Nach jedem Slice: Metriken prüfen und lernen, bevor nächste Slice gestartet wird
