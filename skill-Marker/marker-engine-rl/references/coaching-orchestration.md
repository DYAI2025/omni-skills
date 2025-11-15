# Orchestrierung & Lehr-Loop (Agent Lead)

Strukturierter Prozess zur systematischen Entwicklung und Validierung der Marker-Engine mit RL-Vertiefung.

## Grundprinzipien

- **Agent bleibt dauerhaft Lead**: Der Agent führt durch alle Phasen, stellt Fragen, validiert Fortschritt
- **Verhindert Oberflächlichkeit**: Jede Phase erfordert expliziten Nachweis/Output
- **Vier Phasen mit Review-Gates**: Keine Phase wird übersprungen oder voreilig abgeschlossen
- **Lehr-Loop integriert**: Explain → Demonstrate → Practice → Feedback → Certify

## Vier-Phasen-Prozess

### Phase 1: Foundation (Grundlagen etablieren)

**Ziel**: Datenbasis, deterministische Pipeline und Validierungs-Infrastruktur aufbauen

**Tasks**:

1. Marker-Daten aus Supabase/ZIP laden und validieren
2. Deterministische Pipeline implementieren (ATO→SEM→CLU→MEMA)
3. Regeln erzwingen (SEM ≥2 ATOs, MEMA ≥2 CLUs, Bottom-up)
4. Basis-Evaluierung implementieren (F1, Violations)

**Review-Gate**:

- [ ] Alle Marker geladen (min. 50 ATOs, 30 SEMs, 15 CLUs, 5 MEMAs)
- [ ] Pipeline erzeugt valide Outputs (keine Regelverstöße)
- [ ] Test-Suite läuft durch (≥10 Testfälle, alle bestanden)

**Output**: `foundation_report.json` mit Marker-Counts, Pipeline-Tests, Beispiel-Outputs

---

### Phase 2: SFT Preparation (Supervised Fine-Tuning vorbereiten)

**Ziel**: SFT-Datensätze erstellen und SFT durchführen

**Tasks**:

1. SFT-Beispiele im Format `[Instruktion|Output]` generieren
2. Kategorien abdecken: ATO-Erkennung, SEM-Komposition, CLU-Pattern, MEMA-Synthese
3. Negativ-Beispiele für Regelbrüche einbauen
4. SFT-Training durchführen (oder Mock-Training für Proof-of-Concept)

**Review-Gate**:

- [ ] ≥100 SFT-Beispiele erstellt (balanciert über Ebenen)
- [ ] Alle Beispiele validiert (SEM-Regel, MEMA-Regel geprüft)
- [ ] SFT-Modell zeigt Verbesserung vs. Baseline (ΔF1 ≥ +0.05)

**Output**: `sft_dataset.jsonl`, `sft_metrics.json` (F1 vorher/nachher)

**Lehr-Loop**:

- **Explain**: "SFT lernt Kompositionsregeln aus gelabelten Beispielen"
- **Demonstrate**: 3-5 Beispiele zeigen mit Erklärung
- **Practice**: SFT-Training laufen lassen
- **Feedback**: Metriken analysieren, Schwächen identifizieren
- **Certify**: F1-Schwelle erreicht → weiter zu Phase 3

---

### Phase 3: RL Training (Reinforcement Learning Policy)

**Ziel**: Policy lernen die Marker kontextsensibel, sparsam und regelkonform anwendet

**Tasks**:

1. MarkerEnv (Gym) implementieren mit State/Action/Reward
2. Reward-Shaping konfigurieren (F1-Delta, Regel-Compliance, ARS-Kohärenz)
3. PPO/SAC-Training durchführen (offline, mit Replay-Buffer)
4. Checkpoints validieren nach jeder Epoche (1-2 Sätze Feedback)

**Review-Gate**:

- [ ] MarkerEnv funktioniert (min. 10 Test-Episodes fehlerfrei)
- [ ] Reward steigt über Training (Trend-Check)
- [ ] Policy erfüllt Qualitätskriterien (F1 ≥0.75, Violations <10/Episode, ARS-Kohärenz ≥0.7)

**Output**: `policy.json`, `rl_training_log.json`, `validation_report.json`

**Lehr-Loop**:

- **Explain**: "RL optimiert Marker-Auswahl durch trial-and-error mit Reward-Signal"
- **Demonstrate**: 1 Episode manuell durchgehen (State→Action→Reward)
- **Practice**: Training (z.B. 50 Epochen mit Kurzvalidierung)
- **Feedback**: Nach jeder 5. Epoche: "F1 +X, Violations ↓Y, Entscheidung: Z"
- **Certify**: Policy exportiert, Validierung bestanden → weiter zu Phase 4

**Kurzvalidierungs-Beispiele**:

```
[Epoche 5] F1 +0.08, SEM-Regelverletzungen ↓12. Entscheidung: Weiter mit LR*0.8.
[Epoche 10] ARS-Kohärenz +0.12, False-Positives ↓18%. Entscheidung: Policy speichern.
[Epoche 15] Violations ↑6 (Rückschritt). Entscheidung: Reward-Shaping anpassen, zurück zu Epoche 10.
```

---

### Phase 4: Deployment & Integration

**Ziel**: Runtime-Engine mit Policy und Supabase-Integration deployen

**Tasks**:

1. Runtime-Engine (`engine.py`, `apply.py`) implementieren
2. Supabase-Anbindung testen (live Marker laden)
3. Policy laden und anwenden (optional, als Multiplikator/Fenster-Tuning)
4. End-to-End-Tests (Text → Events mit ARS/Decay)

**Review-Gate**:

- [ ] Engine lädt Marker aus Supabase (oder ZIP Fallback)
- [ ] Policy wird korrekt angewendet (wenn vorhanden)
- [ ] Output entspricht Schema (NDJSON mit ATO/SEM/CLU/MEMA)
- [ ] Regeln werden eingehalten (keine Verstöße in 20 Test-Inputs)

**Output**: Funktionsfähige Runtime, `deployment_report.json`, Beispiel-Outputs

**Lehr-Loop**:

- **Explain**: "Runtime kombiniert deterministische Pipeline mit gelernter Policy"
- **Demonstrate**: Live-Demo mit 3 Beispieltexten
- **Practice**: Integration in Target-System (API, CLI, etc.)
- **Feedback**: Fehlerrate, Latenz, Edge-Cases
- **Certify**: Production-Ready → Skill vollständig

---

## Lehr-Loop Details

### Explain (Erklären)

**Ziel**: Konzept/Mechanik verständlich machen

**Format**:

- Was wird getan?
- Warum ist das wichtig?
- Welche Regeln/Constraints gelten?

**Beispiel**:

> "SFT-Training zeigt dem Modell gelabelte Beispiele der Marker-Anwendung.
> Dabei lernt es die Kompositionsregeln (SEM ≥2 ATOs) und RF-Manifestationen.
> Das ist wichtig, weil es die deterministische Basis 'weicher' und kontextsensibel macht."

### Demonstrate (Vorführen)

**Ziel**: Konkrete Beispiele zeigen

**Format**:

- 2-5 repräsentative Beispiele
- Mit Input, erwarteter Output, Erklärung

**Beispiel (SEM-Komposition)**:

```
Input: "Ich bin mir nicht sicher... vielleicht überschätze ich."
ATOs erkannt: ATO_UNCERTAINTY_PHRASE, ATO_HEDGING_VOCAB
→ SEM_UNCERTAINTY_TONING = {ATO_UNCERTAINTY_PHRASE, ATO_HEDGING_VOCAB} ✓
Regel erfüllt: ≥2 unterschiedliche ATOs
```

### Practice (Üben)

**Ziel**: Training/Implementierung durchführen

**Format**:

- Systematische Ausführung (z.B. Training-Loop)
- Mit Monitoring (Metriken, Logs)
- Inkrementelle Verbesserung

**Beispiel (RL-Training)**:

```python
for epoch in range(50):
    total_reward = train_one_epoch(env, agent)

    if epoch % 5 == 0:
        metrics = validate_policy(agent, val_set)
        feedback = generate_short_validation(metrics)
        print(f"[Epoche {epoch}] {feedback}")

        if should_adjust(metrics):
            adjust_hyperparameters(agent, metrics)
```

### Feedback (Rückmeldung)

**Ziel**: Fortschritt bewerten, Korrekturen vornehmen

**Format**:

- Kriterienbasiert (F1, Violations, etc.)
- 1-2 Sätze Zusammenfassung
- Klare Entscheidung (weiter/korrigieren/zurück)

**Beispiel**:

> "SEM-Regelverletzungen ↓22%, ARS-Kohärenz +0.08.
> Nächster Schritt: LR halbieren und 10 weitere Epochen."

### Certify (Zertifizieren)

**Ziel**: Phase abschließen, Freigabe für nächste Phase

**Kriterien**:

- Alle Review-Gate-Checkboxen erfüllt
- Metriken über Schwellwerten
- Output dokumentiert und validiert

**Format**:

```json
{
  "phase": "SFT_PREPARATION",
  "status": "CERTIFIED",
  "timestamp": "2025-11-08T12:34:56Z",
  "metrics": {
    "sft_examples": 127,
    "f1_improvement": 0.12,
    "violations": 0
  },
  "next_phase": "RL_TRAINING"
}
```

---

## Korrektur-Schleifen

Wenn Review-Gate nicht bestanden:

1. **Diagnose**: Welche Kriterien fehlen?
2. **Root-Cause**: Warum ist das Kriterium nicht erfüllt?
3. **Maßnahme**: Konkrete Anpassung (z.B. mehr Daten, Hyperparameter-Tuning)
4. **Re-Test**: Erneute Validierung

**Beispiel**:

```
Gate-Check: F1 SEM = 0.62 (Ziel: ≥0.70) → FAILED
Diagnose: Zu viele False-Positives bei SEM_UNCERTAINTY_TONING
Root-Cause: Model übersieht SEM-Kompositionsregel, markiert SEMs mit nur 1 ATO
Maßnahme: 20 Negativ-Beispiele (SEM mit 1 ATO = FALSCH) zu SFT-Datensatz hinzufügen
Re-Train: SFT nochmal, dann F1 = 0.74 → PASSED
```

---

## Workflow-Diagramm (Text)

```
START
  ↓
┌─────────────────────────┐
│ Phase 1: Foundation     │
│ - Marker laden          │
│ - Pipeline bauen        │
│ - Tests validieren      │
└────────┬────────────────┘
         ↓ [Review-Gate]
┌─────────────────────────┐
│ Phase 2: SFT Prep       │
│ - Datensatz erstellen   │
│ - SFT Training          │
│ - Lehr-Loop (E→D→P→F→C) │
└────────┬────────────────┘
         ↓ [Review-Gate]
┌─────────────────────────┐
│ Phase 3: RL Training    │
│ - MarkerEnv setup       │
│ - PPO Training          │
│ - Kurzvalidierungen     │
│ - Policy Export         │
└────────┬────────────────┘
         ↓ [Review-Gate]
┌─────────────────────────┐
│ Phase 4: Deployment     │
│ - Runtime Engine        │
│ - Supabase Integration  │
│ - End-to-End Tests      │
└────────┬────────────────┘
         ↓ [Certify]
       DONE
```

---

## Checkliste für Agent

Als Agent:

- [ ] Erkläre jede Phase bevor du startest (Explain)
- [ ] Zeige Beispiele bevor du implementierst (Demonstrate)
- [ ] Implementiere systematisch mit Monitoring (Practice)
- [ ] Validiere nach jedem Schritt (Feedback)
- [ ] Warte auf explizite Freigabe vor nächster Phase (Certify)
- [ ] Bei Gate-Failure: Diagnose → Maßnahme → Re-Test
- [ ] Dokumentiere alle Outputs (JSON-Reports)
- [ ] Halte User über Fortschritt informiert (1-2 Sätze Updates)

---

## Anti-Patterns (Vermeiden)

❌ **Phasen überspringen**: "Wir können SFT überspringen und direkt zu RL"
✅ **Systematisch durchgehen**: "SFT liefert Basis für RL, muss zuerst validiert werden"

❌ **Oberflächliche Validierung**: "Sieht gut aus, weiter"
✅ **Kriterienbasiert**: "F1=0.78 ✓, Violations=3 ✓, ARS-Kohärenz=0.72 ✓ → Gate bestanden"

❌ **Keine Dokumentation**: "Policy trainiert, läuft"
✅ **Output dokumentiert**: "policy.json exportiert, rl_training_log.json mit 50 Epochen, validation_report.json mit Metriken"

❌ **Bei Fehler weitermachen**: "Violations hoch, aber trainieren wir weiter"
✅ **Korrekturschleife**: "Violations=25 (Ziel <10) → Reward-Shaping anpassen, Epoche 20 neu starten"
