# RL-Design für MarkerEnv

**Ziel**: Eine Policy lernen, die Marker an den relevanten Textstellen **richtig, sparsam und kontextsensibel** anwendet, ohne die deterministischen Regeln zu brechen.

## Umgebung (Gym)

- **State**: Nachrichtenfenster (Tokens), erkannte ATOs/SEMs, RF-Level-Schätzung, Gate-Status, letzte Aktion.
- **Action Space**: Diskret { APPLY(marker_id), PROMOTE(family), SKIP, ADJUST_WINDOW(k) }.
- **Reward**:
  - +ΔF1 (ATO/SEM/CLU) ggü. Baseline, +Gate-Pass, +SEM-Regeltreue, +MEMA/ARS-Kohärenz.
  - −False-Positives, −SEM-Regelbruch, −Überdetektion/Spam.
- **Algorithmen**: Actor-Critic (PPO/SAC) für sample-effizientes Lernen in sequentiellen Entscheidungen.

## Intuition-Integration

- Zustände (provisional→confirmed→decayed) werden als Teil des States geführt; **confirmed** triggert temporäre **Multiplier** (Score-Boost), die als Reward-Bonus und als Policy-Output gespiegelt werden.

## MEMA & ARS

- MEMA nur nach CLU-Aktivierung (Bottom-up). ARS (0–5, mit Decay) wird als Zielgröße für Kohärenz-Boni genutzt.

## Technische Details

### State-Repräsentation

Der State wird als Dictionary strukturiert:

```python
state = {
    "window": ["msg_1", "msg_2", ...],  # Nachrichtenfenster
    "atos": [{"id": "ATO_X", "score": 0.8, ...}],
    "sems": [{"id": "SEM_Y", "evidence": [...], ...}],
    "clus": [{"id": "CLU_Z", "confidence": 0.6, ...}],
    "rf_level": "L1-STONE",
    "rf_intensity": 0.52,
    "gates": {"passed": True, "min_markers": 3},
    "intuition_state": "provisional",  # oder confirmed, decayed
    "last_action": "APPLY_MARKER",
    "step": 12
}
```

### Action Space

Diskrete Aktionen (0-N):

- `SKIP` (0): Keine Aktion, nächster Schritt
- `APPLY_MARKER(id)` (1-M): Wende spezifischen Marker an
- `PROMOTE_FAMILY(family)` (M+1-K): Verstärke Marker-Familie (z.B. UNCERTAINTY)
- `ADJUST_WINDOW(delta)` (K+1-N): Fenster vergrößern/verkleinern (+1, -1)

### Reward-Komponenten

1. **Precision/Recall Reward**: ΔF1 für ATO/SEM/CLU
2. **Rule Compliance**: +10 für SEM mit ≥2 ATOs, -50 für Verstoß
3. **ARS Coherence**: +5 wenn MEMA-ARS im erwarteten Bereich
4. **False Positive Penalty**: -2 pro falsch-positivem Marker
5. **Spam Prevention**: -1 wenn >3 gleiche Marker in Fenster
6. **Gate Bonus**: +15 wenn alle Gates bestanden

### Training-Strategie

1. **Warm-Start**: Initiale Policy aus deterministischer Pipeline
2. **Curriculum Learning**: Start mit einfachen (nur ATO/SEM), dann komplexere (CLU/MEMA)
3. **Exploration**: ε-greedy mit decay (Start 0.3 → 0.05)
4. **Sample Efficiency**: Experience Replay Buffer (10K Transitionen)
5. **Stabilität**: Target Network Updates alle 100 Steps

## Validierungs-Metriken

- **Regelverletzungen pro Episode** (Ziel: <5)
- **F1-Score** für jede Ebene (ATO/SEM/CLU/MEMA)
- **ARS-Kohärenz** (Korrelation erwartete vs. tatsächliche ARS)
- **Effizienz** (Anzahl Aktionen pro korrekt erkanntem Pattern)

## Hyperparameter-Empfehlungen

- **Learning Rate**: 3e-4 (Adam)
- **Batch Size**: 64
- **γ (Discount)**: 0.95
- **λ (GAE)**: 0.95
- **Clip ε (PPO)**: 0.2
- **Entropy Coefficient**: 0.01 (Exploration)
- **Epochs pro Update**: 4
