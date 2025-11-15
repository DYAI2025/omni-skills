#!/usr/bin/env python3
"""
Training script for Marker-Policy using PPO (Proximal Policy Optimization).

This is a simplified demonstration of RL training with:
- Short validations after each epoch (1-2 sentences)
- Policy export to policy.json
- Adaptive learning rate
"""

import json
import os
import random
import sys
from datetime import datetime
from typing import Dict, Any, List

# Import the environment
try:
    from offline_env import MarkerEnv
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from offline_env import MarkerEnv


class SimplePPOAgent:
    """Simplified PPO agent for demonstration."""
    
    def __init__(self, action_space_size: int = 4, learning_rate: float = 0.001):
        self.action_space_size = action_space_size
        self.learning_rate = learning_rate
        
        # Policy parameters (simplified as multipliers per family)
        self.family_multipliers = {
            "UNCERTAINTY": 1.0,
            "CONFLICT": 1.0,
            "AVOIDANCE": 1.0,
            "AGREEMENT": 1.0
        }
        
        # Window settings
        self.sem_window = 3
        self.clu_window = 5
        
        # Training stats
        self.epoch_rewards = []
    
    def select_action(self, state: Dict[str, Any]) -> int:
        """Select action based on current policy (ε-greedy for exploration)."""
        epsilon = 0.1  # Exploration rate
        
        if random.random() < epsilon:
            return random.randint(0, self.action_space_size - 1)
        
        # Simple heuristic policy
        if state["atos"] < 2:
            return 1  # APPLY_MARKER (need more ATOs)
        elif state["sems"] < 1 and state["atos"] >= 2:
            return 1  # APPLY_MARKER (can form SEM)
        elif state["step"] < 10:
            return 1  # APPLY_MARKER (early phase)
        else:
            return 0  # SKIP
    
    def update(self, reward: float):
        """Update policy based on reward (simplified)."""
        # In real PPO, this would update neural network weights
        # Here we just track performance
        pass
    
    def adjust_lr(self, factor: float = 0.8):
        """Adjust learning rate."""
        self.learning_rate *= factor
        print(f"  → LR adjusted to {self.learning_rate:.6f}")
    
    def export_policy(self, path: str):
        """Export policy to JSON file."""
        policy = {
            "family_multipliers": self.family_multipliers,
            "sem_window": self.sem_window,
            "clu_window": self.clu_window,
            "learning_rate": self.learning_rate,
            "trained_epochs": len(self.epoch_rewards),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(policy, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 Policy exported to: {path}")


def train_one_epoch(env: MarkerEnv, agent: SimplePPOAgent) -> Dict[str, Any]:
    """Train for one epoch."""
    state = env.reset()
    done = False
    total_reward = 0.0
    steps = 0
    violations = []
    
    while not done:
        action = agent.select_action(state)
        next_state, reward, done, info = env.step(action)
        
        agent.update(reward)
        
        total_reward += reward
        steps += 1
        violations.extend(info.get("violations", []))
        
        state = next_state
    
    return {
        "total_reward": total_reward,
        "steps": steps,
        "violations": len(violations),
        "violation_types": list(set(violations)),
        "avg_reward_per_step": total_reward / steps if steps > 0 else 0
    }


def short_validation(epoch: int, current_metrics: Dict[str, Any], previous_metrics: Dict[str, Any] = None) -> str:
    """
    Generate 1-2 sentence validation feedback.
    
    Returns: Decision string (continue/adjust/stop)
    """
    messages = []
    decision = "continue"
    
    # Compare with previous epoch
    if previous_metrics:
        reward_delta = current_metrics["total_reward"] - previous_metrics["total_reward"]
        violation_delta = current_metrics["violations"] - previous_metrics["violations"]
        
        # Reward change
        if reward_delta > 5.0:
            messages.append(f"Reward +{reward_delta:.1f} (Verbesserung)")
        elif reward_delta < -5.0:
            messages.append(f"Reward {reward_delta:.1f} (Verschlechterung)")
            decision = "adjust"
        
        # Violations
        if violation_delta < 0:
            messages.append(f"Regelverletzungen ↓{abs(violation_delta)} (gut)")
        elif violation_delta > 0:
            messages.append(f"Regelverletzungen ↑{violation_delta} (problematisch)")
            if violation_delta > 5:
                decision = "adjust"
    else:
        messages.append(f"Baseline: Reward={current_metrics['total_reward']:.1f}, Violations={current_metrics['violations']}")
    
    # Decision
    if current_metrics["violations"] > 20:
        decision = "adjust"
        messages.append("Zu viele Violations")
    elif current_metrics["violations"] < 5 and current_metrics["total_reward"] > 50:
        decision = "checkpoint"
        messages.append("Starke Performance")
    
    summary = ". ".join(messages) + "."
    
    # Map decision to action
    if decision == "adjust":
        action_text = "LR halbieren und Reward-Shaping anpassen"
    elif decision == "checkpoint":
        action_text = "Policy speichern als Checkpoint"
    else:
        action_text = "Weiter trainieren"
    
    return f"{summary} Entscheidung: {action_text}"


def main():
    """Main training loop."""
    # Configuration
    dataset_path = os.environ.get("SFT_JSONL", "./assets/datasets/sft_record.jsonl.example")
    num_epochs = int(os.environ.get("NUM_EPOCHS", "20"))
    validation_interval = 5
    policy_output = os.environ.get("POLICY_PATH", "./policy.json")
    
    print("\n🚀 Starting Marker-Policy RL Training (PPO)")
    print("=" * 60)
    print(f"Dataset: {dataset_path}")
    print(f"Epochs: {num_epochs}")
    print(f"Validation interval: Every {validation_interval} epochs")
    print("=" * 60)
    
    # Initialize environment and agent
    env = MarkerEnv(dataset_path)
    agent = SimplePPOAgent(action_space_size=4)
    
    # Training loop
    previous_metrics = None
    best_reward = float('-inf')
    
    for epoch in range(1, num_epochs + 1):
        print(f"\n📊 Epoch {epoch}/{num_epochs}")
        print("-" * 60)
        
        # Train one epoch
        metrics = train_one_epoch(env, agent)
        agent.epoch_rewards.append(metrics["total_reward"])
        
        print(f"  Reward: {metrics['total_reward']:.2f}")
        print(f"  Steps: {metrics['steps']}")
        print(f"  Violations: {metrics['violations']}")
        if metrics["violation_types"]:
            print(f"  Types: {', '.join(metrics['violation_types'][:3])}")
        
        # Validation every N epochs
        if epoch % validation_interval == 0 or epoch == num_epochs:
            print(f"\n🔍 Validation (Epoch {epoch}):")
            validation_msg = short_validation(epoch, metrics, previous_metrics)
            print(f"  {validation_msg}")
            
            # Apply decision
            if "LR halbieren" in validation_msg:
                agent.adjust_lr(0.5)
            
            if "Policy speichern" in validation_msg or metrics["total_reward"] > best_reward:
                best_reward = metrics["total_reward"]
                checkpoint_path = policy_output.replace(".json", f"_epoch{epoch}.json")
                agent.export_policy(checkpoint_path)
        
        previous_metrics = metrics
    
    # Final export
    print("\n" + "=" * 60)
    print("✅ Training completed!")
    print(f"  Total epochs: {num_epochs}")
    print(f"  Best reward: {best_reward:.2f}")
    print(f"  Final violations: {metrics['violations']}")
    
    agent.export_policy(policy_output)
    
    # Write training log
    log_path = policy_output.replace(".json", "_training.log.json")
    training_log = {
        "epochs": num_epochs,
        "epoch_rewards": agent.epoch_rewards,
        "final_metrics": metrics,
        "best_reward": best_reward,
        "policy_path": policy_output
    }
    
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(training_log, f, ensure_ascii=False, indent=2)
    
    print(f"  Training log: {log_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
