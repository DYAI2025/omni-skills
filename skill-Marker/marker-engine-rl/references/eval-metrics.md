# Evaluationsmetriken

Umfassende Metriken zur Bewertung der Marker-Engine-Policy während Training und Deployment.

## ATO/SEM/CLU F1-Scores

**Berechnung pro Ebene und Familie**

### Pro Ebene (Global)

```python
def calculate_f1_per_level(predictions, ground_truth, level):
    """
    level: "ATO", "SEM", "CLU", "MEMA"
    """
    pred_ids = set(m["id"] for m in predictions if m["id"].startswith(level))
    true_ids = set(m["id"] for m in ground_truth if m["id"].startswith(level))

    true_positives = len(pred_ids & true_ids)
    false_positives = len(pred_ids - true_ids)
    false_negatives = len(true_ids - pred_ids)

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0

    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": false_negatives
    }
```

### Pro Familie

```python
def calculate_f1_per_family(predictions, ground_truth):
    """
    Gruppiert nach Marker-Familien (z.B. UNCERTAINTY, CONFLICT, AVOIDANCE)
    """
    families = {}

    for marker in predictions + ground_truth:
        parts = marker["id"].split("_")
        if len(parts) >= 2:
            family = parts[1]  # z.B. "UNCERTAINTY" aus "SEM_UNCERTAINTY_TONING"
            if family not in families:
                families[family] = {"pred": set(), "true": set()}

    for marker in predictions:
        parts = marker["id"].split("_")
        if len(parts) >= 2:
            family = parts[1]
            families[family]["pred"].add(marker["id"])

    for marker in ground_truth:
        parts = marker["id"].split("_")
        if len(parts) >= 2:
            family = parts[1]
            families[family]["true"].add(marker["id"])

    results = {}
    for family, data in families.items():
        tp = len(data["pred"] & data["true"])
        fp = len(data["pred"] - data["true"])
        fn = len(data["true"] - data["pred"])

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        results[family] = {"precision": precision, "recall": recall, "f1": f1}

    return results
```

### Gesamt-F1 (Macro-Average)

```python
def calculate_macro_f1(predictions, ground_truth):
    """
    Durchschnitt über alle Ebenen
    """
    levels = ["ATO", "SEM", "CLU", "MEMA"]
    f1_scores = []

    for level in levels:
        metrics = calculate_f1_per_level(predictions, ground_truth, level)
        f1_scores.append(metrics["f1"])

    return sum(f1_scores) / len(f1_scores)
```

## Regelverletzungen/Episode

**Ziel**: Anzahl der Regelverstöße minimieren (↓)

### Tracked Violations

| Verstoß-Typ                  | Beschreibung                   | Schweregrad |
| ---------------------------- | ------------------------------ | ----------- |
| `SEM_COMPOSITION_VIOLATION`  | SEM mit <2 ATOs                | KRITISCH    |
| `MEMA_COMPOSITION_VIOLATION` | MEMA mit <2 CLUs               | KRITISCH    |
| `BOTTOM_UP_VIOLATION`        | Höhere Ebene vor niedrigerer   | HOCH        |
| `ARS_OUT_OF_RANGE`           | ARS <0 oder >5                 | MITTEL      |
| `DECAY_INVALID`              | Decay ≤0 oder ≥1               | MITTEL      |
| `MARKER_SPAM`                | Gleicher Marker >3× im Fenster | NIEDRIG     |

### Berechnung

```python
def count_violations(episode_data):
    violations = {
        "SEM_COMPOSITION_VIOLATION": 0,
        "MEMA_COMPOSITION_VIOLATION": 0,
        "BOTTOM_UP_VIOLATION": 0,
        "ARS_OUT_OF_RANGE": 0,
        "DECAY_INVALID": 0,
        "MARKER_SPAM": 0
    }

    for step in episode_data:
        events = step["events"]

        # SEM-Kompositionsprüfung
        for sem in [e for e in events if e["id"].startswith("SEM_")]:
            atos = set(sem.get("composed_of", []))
            if len(atos) < 2:
                violations["SEM_COMPOSITION_VIOLATION"] += 1

        # MEMA-Kompositionsprüfung
        for mema in [e for e in events if e["id"].startswith("MEMA_")]:
            clus = [c for c in mema.get("composed_of", []) if c.startswith("CLU_")]
            if len(set(clus)) < 2:
                violations["MEMA_COMPOSITION_VIOLATION"] += 1

        # ARS-Prüfung
        for mema in [e for e in events if e["id"].startswith("MEMA_")]:
            ars = mema.get("ars", 0)
            if ars < 0 or ars > 5:
                violations["ARS_OUT_OF_RANGE"] += 1

            decay_str = mema.get("decay", "0.85/24h")
            try:
                decay = float(decay_str.split("/")[0])
                if decay <= 0 or decay >= 1:
                    violations["DECAY_INVALID"] += 1
            except:
                violations["DECAY_INVALID"] += 1

        # Spam-Prüfung
        marker_counts = {}
        for event in events:
            marker_id = event["id"]
            marker_counts[marker_id] = marker_counts.get(marker_id, 0) + 1

        for count in marker_counts.values():
            if count > 3:
                violations["MARKER_SPAM"] += 1

    return violations

def violation_score(violations):
    """
    Gewichteter Violation-Score (niedriger ist besser)
    """
    weights = {
        "SEM_COMPOSITION_VIOLATION": 10,
        "MEMA_COMPOSITION_VIOLATION": 8,
        "BOTTOM_UP_VIOLATION": 6,
        "ARS_OUT_OF_RANGE": 3,
        "DECAY_INVALID": 3,
        "MARKER_SPAM": 1
    }

    score = sum(violations[k] * weights[k] for k in violations)
    return score
```

## MEMA-ARS-Kohärenz

**Korrelation zwischen erwarteter und gemessener ARS-Logistik**

### Berechnung

```python
import numpy as np
from scipy.stats import pearsonr

def calculate_ars_coherence(memas_predicted, memas_ground_truth):
    """
    Berechnet Pearson-Korrelation zwischen predicted und expected ARS
    """
    if not memas_predicted or not memas_ground_truth:
        return 0.0

    # Match MEMAs by ID
    matched = []
    for pred in memas_predicted:
        for true in memas_ground_truth:
            if pred["id"] == true["id"]:
                matched.append((pred.get("ars", 0), true.get("ars", 0)))
                break

    if len(matched) < 2:
        return 0.0

    pred_ars = [m[0] for m in matched]
    true_ars = [m[1] for m in matched]

    correlation, p_value = pearsonr(pred_ars, true_ars)

    return correlation if not np.isnan(correlation) else 0.0

def calculate_ars_mae(memas_predicted, memas_ground_truth):
    """
    Mean Absolute Error für ARS-Werte
    """
    matched = []
    for pred in memas_predicted:
        for true in memas_ground_truth:
            if pred["id"] == true["id"]:
                matched.append((pred.get("ars", 0), true.get("ars", 0)))
                break

    if not matched:
        return 0.0

    errors = [abs(p - t) for p, t in matched]
    return sum(errors) / len(errors)
```

### Interpretation

- **Korrelation > 0.8**: Exzellente Kohärenz
- **Korrelation 0.6-0.8**: Gute Kohärenz
- **Korrelation 0.4-0.6**: Moderate Kohärenz
- **Korrelation < 0.4**: Schwache Kohärenz

## RF-Manifestationstreue

**Prüfung ob RF-Kontext korrekt zur Marker-Familie passt**

### Erwartete Manifestationen (Beispiele)

```python
RF_MANIFESTATIONS = {
    ("L1-STONE", "UNCERTAINTY"): ["Schonungsvolle Grenzsetzung", "Vorsichtige Positionierung"],
    ("L2-BRONZE", "CONFLICT"): ["Offene Meinungsverschiedenheit", "Direkte Konfrontation"],
    ("L3-IRON", "AVOIDANCE"): ["Strategischer Rückzug", "Thematische Ausweichung"],
    # ... weitere Mappings
}

def check_rf_manifestation(event, rf_context):
    """
    Prüft ob RF-Manifestation zum Marker passt
    """
    marker_id = event["id"]
    rf_level = rf_context.get("level", "")

    # Extrahiere Familie
    parts = marker_id.split("_")
    if len(parts) < 2:
        return False

    family = parts[1]

    expected_manifestations = RF_MANIFESTATIONS.get((rf_level, family), [])
    actual_manifestation = event.get("rf_manifestation", "")

    # Fuzzy Match
    for expected in expected_manifestations:
        if expected.lower() in actual_manifestation.lower():
            return True

    return False

def calculate_rf_accuracy(predictions, ground_truth):
    """
    Prozentsatz korrekter RF-Manifestationen
    """
    total = 0
    correct = 0

    for pred_event in predictions:
        if "rf_manifestation" in pred_event:
            total += 1

            # Finde entsprechendes Ground-Truth-Event
            for true_event in ground_truth:
                if pred_event["id"] == true_event["id"]:
                    if pred_event.get("rf_manifestation") == true_event.get("rf_manifestation"):
                        correct += 1
                    break

    return correct / total if total > 0 else 0.0
```

## Lehr-Loop-Fortschritt

**Tracking der Explain → Demonstrate → Practice → Feedback → Certify Phasen**

### Metriken pro Phase

```python
class LehrLoopMetrics:
    def __init__(self):
        self.phases = {
            "explain": {"completed": False, "duration_min": 0},
            "demonstrate": {"completed": False, "examples_shown": 0},
            "practice": {"completed": False, "episodes": 0, "avg_reward": 0},
            "feedback": {"completed": False, "corrections": 0},
            "certify": {"completed": False, "passed": False}
        }

    def mark_phase_complete(self, phase, **kwargs):
        self.phases[phase]["completed"] = True
        self.phases[phase].update(kwargs)

    def is_ready_for_next_phase(self, current_phase):
        phase_order = ["explain", "demonstrate", "practice", "feedback", "certify"]
        current_idx = phase_order.index(current_phase)

        if current_idx == 0:
            return True

        previous_phase = phase_order[current_idx - 1]
        return self.phases[previous_phase]["completed"]

    def certification_criteria(self):
        """
        Prüft ob alle Kriterien für Zertifizierung erfüllt sind
        """
        criteria = {
            "f1_threshold": 0.75,
            "violation_threshold": 5,
            "ars_coherence_threshold": 0.7,
            "min_practice_episodes": 100
        }
        return criteria
```

### Kurzvalidierungen

Nach jeder Epoche 1-2 Sätze Output:

```python
def generate_short_validation(epoch_metrics):
    """
    Generiert 1-2 Sätze Validierungs-Feedback
    """
    f1_change = epoch_metrics["f1_current"] - epoch_metrics["f1_previous"]
    violations = epoch_metrics["violations_total"]
    ars_coherence = epoch_metrics["ars_coherence"]

    messages = []

    # F1-Change
    if f1_change > 0.05:
        messages.append(f"F1 +{f1_change:.02f} (signifikante Verbesserung)")
    elif f1_change < -0.05:
        messages.append(f"F1 {f1_change:.02f} (Verschlechterung)")

    # Violations
    if violations < 10:
        messages.append(f"Regelverletzungen ↓{violations} (gut)")
    else:
        messages.append(f"Regelverletzungen {violations} (zu hoch)")

    # ARS
    if ars_coherence > 0.7:
        messages.append(f"ARS-Kohärenz {ars_coherence:.02f} (stark)")

    # Entscheidung
    if f1_change > 0 and violations < 10 and ars_coherence > 0.6:
        decision = "Weiter mit aktuellem Setup"
    elif violations > 20:
        decision = "Zurück: Reward-Shaping anpassen"
    else:
        decision = "LR halbieren und weiter"

    summary = ". ".join(messages) + f". Entscheidung: {decision}."
    return summary
```

## Dashboard-Metriken (Zusammenfassung)

```python
def generate_eval_report(all_predictions, all_ground_truth, violations, training_history):
    """
    Erzeugt umfassenden Evaluations-Report
    """
    report = {
        "f1_scores": {
            "ATO": calculate_f1_per_level(all_predictions, all_ground_truth, "ATO")["f1"],
            "SEM": calculate_f1_per_level(all_predictions, all_ground_truth, "SEM")["f1"],
            "CLU": calculate_f1_per_level(all_predictions, all_ground_truth, "CLU")["f1"],
            "MEMA": calculate_f1_per_level(all_predictions, all_ground_truth, "MEMA")["f1"],
            "macro_avg": calculate_macro_f1(all_predictions, all_ground_truth)
        },
        "violations": {
            "total": sum(violations.values()),
            "by_type": violations,
            "weighted_score": violation_score(violations)
        },
        "ars_coherence": {
            "correlation": calculate_ars_coherence(
                [m for m in all_predictions if m["id"].startswith("MEMA_")],
                [m for m in all_ground_truth if m["id"].startswith("MEMA_")]
            ),
            "mae": calculate_ars_mae(
                [m for m in all_predictions if m["id"].startswith("MEMA_")],
                [m for m in all_ground_truth if m["id"].startswith("MEMA_")]
            )
        },
        "rf_manifestation": {
            "accuracy": calculate_rf_accuracy(all_predictions, all_ground_truth)
        },
        "training_summary": {
            "total_epochs": len(training_history),
            "best_f1": max(h["f1"] for h in training_history),
            "final_f1": training_history[-1]["f1"] if training_history else 0
        }
    }

    return report
```
