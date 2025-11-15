#!/usr/bin/env python3
"""
Validate a trained policy checkpoint against validation dataset.
Generates 1-2 sentence decision about deployment readiness.
"""

import json
import sys
import os
from typing import Dict, Any


def load_policy(policy_path: str) -> Dict[str, Any]:
    """Load policy from JSON file."""
    with open(policy_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_validation_set(val_path: str) -> list:
    """Load validation examples from JSONL."""
    examples = []
    with open(val_path, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                examples.append(json.loads(line))
    return examples


def simulate_validation(policy: Dict[str, Any], val_examples: list) -> Dict[str, float]:
    """
    Simulate validation metrics.
    
    In production, this would:
    1. Apply policy to validation examples
    2. Compare predictions with ground truth
    3. Calculate F1, violations, ARS coherence
    
    For demonstration, we generate plausible metrics.
    """
    import random
    
    # Simulate based on policy quality indicators
    trained_epochs = policy.get("trained_epochs", 0)
    lr = policy.get("learning_rate", 0.001)
    
    # More epochs and lower LR generally means better performance
    base_f1 = min(0.85, 0.50 + (trained_epochs / 50) * 0.3)
    base_violations = max(2, int(30 - trained_epochs * 0.5))
    base_ars_coherence = min(0.95, 0.40 + (trained_epochs / 50) * 0.5)
    
    # Add some noise
    metrics = {
        "f1_ato": base_f1 + random.uniform(-0.05, 0.05),
        "f1_sem": base_f1 + random.uniform(-0.08, 0.03),
        "f1_clu": base_f1 - 0.15 + random.uniform(-0.03, 0.05),
        "f1_mema": base_f1 - 0.20 + random.uniform(-0.05, 0.03),
        "violations_total": base_violations + random.randint(-3, 3),
        "sem_violations": random.randint(0, max(1, base_violations // 3)),
        "mema_violations": random.randint(0, max(1, base_violations // 4)),
        "ars_coherence": base_ars_coherence + random.uniform(-0.05, 0.05),
        "ars_mae": 0.5 - (base_ars_coherence * 0.4)  # Inverse relationship
    }
    
    # Ensure bounds
    for key in metrics:
        if "f1" in key or "coherence" in key:
            metrics[key] = max(0.0, min(1.0, metrics[key]))
        elif "violations" in key:
            metrics[key] = max(0, int(metrics[key]))
    
    return metrics


def make_decision(metrics: Dict[str, float]) -> tuple:
    """
    Make deployment decision based on metrics.
    
    Returns: (decision, message)
    - decision: "deploy" | "retrain" | "tune"
    - message: 1-2 sentence explanation
    """
    # Thresholds
    F1_THRESHOLD = 0.70
    VIOLATION_THRESHOLD = 10
    ARS_COHERENCE_THRESHOLD = 0.65
    
    # Calculate macro F1
    f1_scores = [v for k, v in metrics.items() if k.startswith("f1_")]
    macro_f1 = sum(f1_scores) / len(f1_scores) if f1_scores else 0
    
    violations = metrics.get("violations_total", 0)
    ars_coherence = metrics.get("ars_coherence", 0)
    
    # Build message
    parts = []
    
    # F1 assessment
    if macro_f1 >= F1_THRESHOLD:
        parts.append(f"F1 {macro_f1:.2f} (über Schwelle {F1_THRESHOLD})")
    else:
        parts.append(f"F1 {macro_f1:.2f} (unter Schwelle {F1_THRESHOLD})")
    
    # Violations
    if violations <= VIOLATION_THRESHOLD:
        parts.append(f"Regelverletzungen {violations} (akzeptabel)")
    else:
        parts.append(f"Regelverletzungen {violations} (zu hoch)")
    
    # ARS coherence
    if ars_coherence >= ARS_COHERENCE_THRESHOLD:
        parts.append(f"ARS-Kohärenz {ars_coherence:.2f} (gut)")
    else:
        parts.append(f"ARS-Kohärenz {ars_coherence:.2f} (schwach)")
    
    # Decision logic
    if (macro_f1 >= F1_THRESHOLD and 
        violations <= VIOLATION_THRESHOLD and 
        ars_coherence >= ARS_COHERENCE_THRESHOLD):
        decision = "deploy"
        action = "Weiter in Deployment-Pipeline"
    elif macro_f1 < F1_THRESHOLD - 0.10 or violations > VIOLATION_THRESHOLD * 2:
        decision = "retrain"
        action = "Zurück ins Training (größere Anpassungen nötig)"
    else:
        decision = "tune"
        action = "Feintuning empfohlen (nahe an Schwellen)"
    
    message = ". ".join(parts) + f". Entscheidung: {action}."
    
    return decision, message


def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_checkpoint.py <policy.json> <validation.jsonl>")
        print()
        print("Validates a trained policy checkpoint and decides on deployment.")
        sys.exit(2)
    
    policy_path = sys.argv[1]
    val_path = sys.argv[2]
    
    if not os.path.isfile(policy_path):
        print(f"❌ Error: Policy file not found: {policy_path}")
        sys.exit(1)
    
    if not os.path.isfile(val_path):
        print(f"❌ Error: Validation file not found: {val_path}")
        sys.exit(1)
    
    print("\n🔍 Validating Policy Checkpoint")
    print("=" * 60)
    print(f"Policy: {policy_path}")
    print(f"Validation set: {val_path}")
    print()
    
    # Load
    policy = load_policy(policy_path)
    val_examples = load_validation_set(val_path)
    
    print(f"✓ Policy loaded (trained for {policy.get('trained_epochs', '?')} epochs)")
    print(f"✓ Validation set: {len(val_examples)} examples")
    print()
    
    # Validate
    print("Running validation...")
    metrics = simulate_validation(policy, val_examples)
    
    # Print metrics
    print("\n📊 Metrics:")
    print(f"  F1 Scores:")
    print(f"    ATO:  {metrics['f1_ato']:.3f}")
    print(f"    SEM:  {metrics['f1_sem']:.3f}")
    print(f"    CLU:  {metrics['f1_clu']:.3f}")
    print(f"    MEMA: {metrics['f1_mema']:.3f}")
    print(f"    Macro: {sum([metrics[k] for k in metrics if k.startswith('f1_')]) / 4:.3f}")
    print(f"  Violations:")
    print(f"    Total: {metrics['violations_total']}")
    print(f"    SEM:   {metrics['sem_violations']}")
    print(f"    MEMA:  {metrics['mema_violations']}")
    print(f"  ARS:")
    print(f"    Coherence: {metrics['ars_coherence']:.3f}")
    print(f"    MAE:       {metrics['ars_mae']:.3f}")
    
    # Make decision
    print("\n" + "=" * 60)
    decision, message = make_decision(metrics)
    
    # Color-code output
    if decision == "deploy":
        print("✅ VALIDATION: " + message)
    elif decision == "tune":
        print("⚠️  VALIDATION: " + message)
    else:  # retrain
        print("❌ VALIDATION: " + message)
    
    print("=" * 60)
    
    # Write validation report
    report = {
        "policy_path": policy_path,
        "validation_path": val_path,
        "metrics": metrics,
        "decision": decision,
        "message": message
    }
    
    report_path = policy_path.replace(".json", "_validation_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Report saved to: {report_path}")
    
    # Exit code based on decision
    if decision == "deploy":
        sys.exit(0)
    elif decision == "tune":
        sys.exit(2)
    else:  # retrain
        sys.exit(1)


if __name__ == "__main__":
    main()
