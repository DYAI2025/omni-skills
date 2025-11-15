# Reward-Schemata (Shaping)

Reward-Funktionen für das RL-Training der Marker-Policy. Ziel ist es, präzise, regelkonforme und systemisch kohärente Marker-Anwendung zu incentivieren.

## Basisscore: ΔF1

**Komponente**: ΔF1 (ATO/SEM/CLU) vs. deterministische Baseline

**Berechnung**:

```python
reward_f1 = (f1_current - f1_baseline) * 100
```

- **f1_current**: F1-Score der Policy-Vorhersage
- **f1_baseline**: F1-Score der deterministischen Pipeline

**Gewichtung pro Ebene**:

- ATO: ×1.0 (Basis)
- SEM: ×2.0 (wichtiger, da kompositorisch)
- CLU: ×3.0 (Pattern-Erkennung)
- MEMA: ×5.0 (systemische Synthese, höchster Wert)

**Beispiel**:

```
F1_ATO: 0.82 → 0.85 (+0.03 → +3.0 Punkte)
F1_SEM: 0.71 → 0.76 (+0.05 → +10.0 Punkte)
Total: +13.0
```

## Regeltreue

**Regel**: +r bei SEM-Kompositions-Treue; −r bei Verstößen (harte Strafe)

### Positive Rewards

| Ereignis                          | Reward | Begründung                 |
| --------------------------------- | ------ | -------------------------- |
| SEM mit ≥2 unterschiedlichen ATOs | +10    | Korrekte Komposition       |
| MEMA mit ≥2 CLUs                  | +15    | Systemische Validität      |
| Bottom-up eingehalten             | +5     | Strukturelle Konsistenz    |
| Gate bestanden                    | +8     | Qualitätsschwelle erreicht |

### Negative Rewards (Strafen)

| Verstoß                                           | Penalty | Begründung                                |
| ------------------------------------------------- | ------- | ----------------------------------------- |
| SEM mit <2 ATOs                                   | -50     | **Harte Strafe**: Zentrale Regel verletzt |
| MEMA mit <2 CLUs                                  | -40     | Systemik-Regel gebrochen                  |
| Bottom-up verletzt (höhere vor niedrigerer Ebene) | -30     | Logik-Fehler                              |
| Gleicher Marker >3× im Fenster (Spam)             | -15     | Überdetektion                             |
| False Positive                                    | -5      | Precision-Verlust                         |

### Implementierung

```python
def rule_compliance_reward(state, action, next_state):
    reward = 0

    # SEM-Kompositionsprüfung
    for sem in next_state["sems"]:
        atos = set(sem.get("composed_of", []))
        if len(atos) >= 2:
            reward += 10
        else:
            reward -= 50  # Harte Strafe

    # MEMA-Kompositionsprüfung
    for mema in next_state["memas"]:
        clus = [c for c in mema.get("composed_of", []) if c.startswith("CLU_")]
        if len(set(clus)) >= 2:
            reward += 15
        else:
            reward -= 40

    # Spam-Prüfung
    marker_counts = Counter([e["id"] for e in next_state["events"]])
    for marker_id, count in marker_counts.items():
        if count > 3:
            reward -= 15 * (count - 3)

    return reward
```

## Systemik: ARS-Kohärenz

**Komponente**: +r für ARS-Kohärenz (MEMA korrekt aus CLUs abgeleitet), ARS auf 0–5 Logistikskala; Decay als zeitliches Regularisierungsziel

### ARS-Kohärenz-Reward

**Formel**:

```python
reward_ars = coherence_score * 20 - abs(ars_predicted - ars_expected) * 10
```

**coherence_score**: Wie gut passt die MEMA-ARS zu den enthaltenen CLUs?

**Berechnung**:

```python
def calculate_ars_coherence(mema, clus_scores):
    """
    clus_scores: Liste von CLU-Scores (0-1)
    Erwartete ARS: gewichteter Durchschnitt der CLU-Scores, auf 0-5 skaliert
    """
    if not clus_scores:
        return 0.0

    avg_clu_score = sum(clus_scores) / len(clus_scores)
    expected_ars = avg_clu_score * 5  # Skalierung auf 0-5

    actual_ars = mema.get("ars", 0)
    error = abs(actual_ars - expected_ars)

    # Kohärenz: 1.0 bei perfektem Match, 0.0 bei Abweichung >2.0
    coherence = max(0.0, 1.0 - error / 2.0)
    return coherence
```

**Beispiel**:

```
CLU_CONFLICT_CYCLE: 0.8
CLU_REPAIR_ATTEMPT: 0.4
→ Erwartete ARS: (0.8+0.4)/2 * 5 = 3.0

MEMA_RELATIONSHIP_STRAIN: ARS = 2.8
→ Abweichung: |2.8-3.0| = 0.2
→ Kohärenz: 1.0 - 0.2/2.0 = 0.9
→ Reward: 0.9 * 20 - 0.2 * 10 = 18 - 2 = +16
```

### Decay-Bonus

**Regel**: Decay muss zwischen 0.5 und 0.99 liegen

```python
def decay_reward(mema):
    decay = float(mema.get("decay", "0.85").split("/")[0])
    if 0.5 <= decay <= 0.99:
        return +5
    else:
        return -10  # Unrealistischer Decay
```

## Exploration-Schutz

**Ziel**: Penalty für „Marker-Spamming", Bonus für sparsamen, präzisen Einsatz

### Effizienz-Reward

```python
def efficiency_reward(state, action_history):
    total_actions = len(action_history)
    useful_actions = sum(1 for a in action_history if a["resulted_in_marker"])

    if total_actions == 0:
        return 0

    efficiency = useful_actions / total_actions

    if efficiency > 0.7:
        return +10  # Präzise
    elif efficiency < 0.3:
        return -10  # Zu viel Exploration/Spam
    else:
        return 0
```

### Diversität-Bonus

```python
def diversity_reward(next_state):
    unique_families = set()
    for event in next_state["events"]:
        family = event["id"].split("_")[0]  # z.B. "ATO", "SEM"
        if family in ["ATO", "SEM", "CLU", "MEMA"]:
            marker_family = "_".join(event["id"].split("_")[1:2])  # z.B. "UNCERTAINTY"
            unique_families.add(marker_family)

    # Bonus für Breite (mehrere Familien erkannt)
    if len(unique_families) >= 3:
        return +8
    elif len(unique_families) >= 2:
        return +4
    else:
        return 0
```

## Gesamte Reward-Funktion

```python
def total_reward(state, action, next_state, action_history, baseline):
    r = 0

    # 1. ΔF1 (Baseline-Vergleich)
    r += calculate_f1_delta(next_state, baseline) * 100

    # 2. Regeltreue
    r += rule_compliance_reward(state, action, next_state)

    # 3. ARS-Kohärenz
    for mema in next_state.get("memas", []):
        clus = [c for c in next_state["clus"] if c["id"] in mema["composed_of"]]
        clu_scores = [c.get("confidence", 0.5) for c in clus]
        coherence = calculate_ars_coherence(mema, clu_scores)
        r += coherence * 20
        r += decay_reward(mema)

    # 4. Effizienz
    r += efficiency_reward(state, action_history)
    r += diversity_reward(next_state)

    # 5. Gate-Bonus
    if next_state.get("gates", {}).get("passed", False):
        r += 15

    return r
```

## Reward-Normalisierung

Um Training zu stabilisieren:

```python
class RewardNormalizer:
    def __init__(self, clip_range=(-100, 100)):
        self.clip_range = clip_range
        self.mean = 0
        self.std = 1
        self.count = 0

    def update(self, reward):
        self.count += 1
        delta = reward - self.mean
        self.mean += delta / self.count
        self.std = np.sqrt((self.std**2 * (self.count-1) + delta**2) / self.count)

    def normalize(self, reward):
        normalized = (reward - self.mean) / (self.std + 1e-8)
        return np.clip(normalized, *self.clip_range)
```

## Hyperparameter

| Parameter       | Wert        | Beschreibung                 |
| --------------- | ----------- | ---------------------------- |
| `weight_f1`     | 1.0         | Gewicht für F1-Delta         |
| `weight_rule`   | 2.0         | Gewicht für Regel-Compliance |
| `weight_ars`    | 1.5         | Gewicht für ARS-Kohärenz     |
| `penalty_scale` | 1.0         | Multiplikator für Strafen    |
| `clip_range`    | (-100, 100) | Reward-Clipping              |

## Anpassung während Training

**Adaptive Reward-Gewichte** basierend auf Training-Fortschritt:

```python
def adaptive_weights(epoch, total_epochs):
    # Früh: Fokus auf Regeln
    # Spät: Fokus auf Feinheiten (ARS, Effizienz)

    progress = epoch / total_epochs

    return {
        "f1": 1.0,
        "rule": 3.0 * (1 - progress) + 1.0 * progress,  # 3.0 → 1.0
        "ars": 0.5 * (1 - progress) + 2.0 * progress,   # 0.5 → 2.0
        "efficiency": 0.2 * (1 - progress) + 1.5 * progress  # 0.2 → 1.5
    }
```
