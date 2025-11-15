#!/usr/bin/env python3
"""
Gym-like environment for training Marker-Policy with Reinforcement Learning.

State: Window of messages, detected ATOs/SEMs/CLUs, RF-level, gates
Action: SKIP, APPLY_MARKER, PROMOTE_FAMILY, ADJUST_WINDOW
Reward: F1-delta, rule compliance, ARS coherence, efficiency

This is a simplified offline environment for demonstration.
In production, replace with real marker detection pipeline.
"""

import json
import random
from typing import Dict, Any, List, Tuple
from collections import Counter, deque


class MarkerEnv:
    """
    Offline RL environment for Marker-Policy training.
    
    Simulates marker detection and provides rewards based on:
    - F1 improvement over baseline
    - Rule compliance (SEM ≥2 ATOs, MEMA ≥2 CLUs)
    - ARS coherence
    - Efficiency (no spam)
    """
    
    # Action space
    ACTION_SKIP = 0
    ACTION_APPLY_MARKER = 1
    ACTION_PROMOTE_FAMILY = 2
    ACTION_ADJUST_WINDOW = 3
    
    ACTION_NAMES = ["SKIP", "APPLY_MARKER", "PROMOTE_FAMILY", "ADJUST_WINDOW"]
    
    def __init__(self, dataset_path: str, baseline: Dict[str, float] = None, window_size: int = 5):
        """
        Initialize environment.
        
        Args:
            dataset_path: Path to JSONL file with training examples
            baseline: Baseline F1 scores (default: {"ato": 0.6, "sem": 0.5, "clu": 0.4, "mema": 0.3})
            window_size: Size of message window for context
        """
        self.dataset_path = dataset_path
        self.window_size = window_size
        
        # Load dataset
        try:
            with open(dataset_path, 'r', encoding='utf-8') as f:
                self.data = [json.loads(line) for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Warning: Dataset not found at {dataset_path}, using dummy data")
            self.data = self._generate_dummy_data()
        
        # Baseline F1 scores
        self.baseline = baseline or {
            "ato": 0.60,
            "sem": 0.50,
            "clu": 0.40,
            "mema": 0.30
        }
        
        # State
        self.current_index = 0
        self.window = deque(maxlen=window_size)
        self.step_count = 0
        self.episode_markers = []
        self.episode_violations = []
        
        # Stats
        self.total_reward = 0.0
    
    def _generate_dummy_data(self) -> List[Dict[str, Any]]:
        """Generate dummy data for testing."""
        return [
            {"text": "I'm not sure... maybe we should wait.", "markers": ["ATO_UNCERTAINTY", "SEM_UNCERTAINTY_TONING"]},
            {"text": "Let's postpone this discussion.", "markers": ["ATO_DELAY", "SEM_AVOIDANT_BEHAVIOR"]},
            {"text": "I completely agree with you!", "markers": ["ATO_AGREEMENT"]},
        ] * 10
    
    def reset(self) -> Dict[str, Any]:
        """Reset environment to initial state."""
        self.current_index = 0
        self.window.clear()
        self.step_count = 0
        self.episode_markers = []
        self.episode_violations = []
        self.total_reward = 0.0
        
        # Initial state
        state = self._get_state()
        return state
    
    def _get_state(self) -> Dict[str, Any]:
        """Get current state representation."""
        return {
            "window": list(self.window),
            "atos": self._count_markers("ATO_"),
            "sems": self._count_markers("SEM_"),
            "clus": self._count_markers("CLU_"),
            "memas": self._count_markers("MEMA_"),
            "rf_level": "L1-STONE",  # Simplified
            "rf_intensity": 0.5 + random.uniform(-0.1, 0.1),
            "gates": {"passed": len(self.episode_markers) >= 3},
            "step": self.step_count,
            "episode_progress": self.current_index / max(1, len(self.data))
        }
    
    def _count_markers(self, prefix: str) -> int:
        """Count markers in episode with given prefix."""
        return sum(1 for m in self.episode_markers if m.startswith(prefix))
    
    def step(self, action: int) -> Tuple[Dict[str, Any], float, bool, Dict[str, Any]]:
        """
        Execute one step in the environment.
        
        Args:
            action: Action index (0-3)
        
        Returns:
            (next_state, reward, done, info)
        """
        self.step_count += 1
        
        # Process action
        reward = 0.0
        info = {"action": self.ACTION_NAMES[action], "violations": []}
        
        if action == self.ACTION_SKIP:
            reward += 0.0  # Neutral
        
        elif action == self.ACTION_APPLY_MARKER:
            # Simulate marker application
            marker_id = self._sample_marker()
            self.episode_markers.append(marker_id)
            reward += 1.0  # Base reward for applying marker
            
            # Check for spam
            marker_counts = Counter(self.episode_markers)
            if marker_counts[marker_id] > 3:
                reward -= 5.0  # Spam penalty
                info["violations"].append("MARKER_SPAM")
        
        elif action == self.ACTION_PROMOTE_FAMILY:
            # Promote a family (e.g., boost UNCERTAINTY markers)
            reward += 0.5
        
        elif action == self.ACTION_ADJUST_WINDOW:
            # Adjust window size
            self.window_size = max(2, min(10, self.window_size + random.choice([-1, 1])))
            reward += 0.2
        
        # Add message to window
        if self.current_index < len(self.data):
            self.window.append(f"msg_{self.current_index}")
            self.current_index += 1
        
        # Calculate rule compliance reward
        rule_reward, violations = self._calculate_rule_reward()
        reward += rule_reward
        info["violations"].extend(violations)
        self.episode_violations.extend(violations)
        
        # Calculate F1 delta reward
        f1_reward = self._calculate_f1_reward()
        reward += f1_reward
        
        # Check if episode is done
        done = self.current_index >= min(50, len(self.data)) or self.step_count >= 100
        
        # Get next state
        next_state = self._get_state()
        
        self.total_reward += reward
        info["total_reward"] = self.total_reward
        info["episode_markers"] = len(self.episode_markers)
        
        return next_state, reward, done, info
    
    def _sample_marker(self) -> str:
        """Sample a marker ID (simplified)."""
        markers = [
            "ATO_UNCERTAINTY", "ATO_HESITATION", "ATO_DELAY",
            "SEM_UNCERTAINTY_TONING", "SEM_AVOIDANT_BEHAVIOR",
            "CLU_INTUITION_UNCERTAINTY", "CLU_CONFLICT_CYCLE",
            "MEMA_RELATIONSHIP_STRAIN"
        ]
        return random.choice(markers)
    
    def _calculate_rule_reward(self) -> Tuple[float, List[str]]:
        """
        Calculate reward based on rule compliance.
        
        Returns:
            (reward, violations)
        """
        reward = 0.0
        violations = []
        
        # Check SEM composition (simplified: assume every 2 ATOs can form 1 SEM)
        ato_count = self._count_markers("ATO_")
        sem_count = self._count_markers("SEM_")
        
        if sem_count > 0:
            # Each SEM should have ≥2 ATOs
            expected_atos = sem_count * 2
            if ato_count >= expected_atos:
                reward += 10.0 * sem_count
            else:
                reward -= 50.0  # Hard penalty
                violations.append("SEM_COMPOSITION_VIOLATION")
        
        # Check MEMA composition (simplified: assume every 2 CLUs can form 1 MEMA)
        clu_count = self._count_markers("CLU_")
        mema_count = self._count_markers("MEMA_")
        
        if mema_count > 0:
            expected_clus = mema_count * 2
            if clu_count >= expected_clus:
                reward += 15.0 * mema_count
            else:
                reward -= 40.0
                violations.append("MEMA_COMPOSITION_VIOLATION")
        
        return reward, violations
    
    def _calculate_f1_reward(self) -> float:
        """
        Calculate reward based on F1 improvement (simplified simulation).
        
        In production, compare predicted markers with ground truth.
        """
        # Simplified: reward proportional to marker diversity
        unique_families = set()
        for marker in self.episode_markers:
            parts = marker.split("_")
            if len(parts) >= 2:
                unique_families.add(parts[1])
        
        # More families = better coverage = higher F1
        estimated_f1 = min(0.9, 0.5 + len(unique_families) * 0.1)
        baseline_f1 = sum(self.baseline.values()) / len(self.baseline)
        
        f1_delta = estimated_f1 - baseline_f1
        return f1_delta * 100  # Scale up for significance
    
    def render(self):
        """Render current state (for debugging)."""
        state = self._get_state()
        print(f"\n=== Step {self.step_count} ===")
        print(f"Window: {state['window']}")
        print(f"Markers: ATO={state['atos']}, SEM={state['sems']}, CLU={state['clus']}, MEMA={state['memas']}")
        print(f"RF: {state['rf_level']} @ {state['rf_intensity']:.2f}")
        print(f"Gates: {state['gates']}")
        print(f"Total Reward: {self.total_reward:.2f}")
        print(f"Violations: {len(self.episode_violations)}")


def test_env():
    """Test the environment."""
    print("🧪 Testing MarkerEnv...")
    
    # Create dummy dataset
    import os
    import tempfile
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.jsonl') as f:
        f.write('{"text": "Test", "markers": []}\n')
        temp_path = f.name
    
    try:
        env = MarkerEnv(temp_path)
        state = env.reset()
        
        print(f"\n✓ Environment created")
        print(f"  Dataset: {len(env.data)} examples")
        print(f"  Action space: {len(env.ACTION_NAMES)}")
        print(f"  Baseline F1: {env.baseline}")
        
        # Run a few steps
        for i in range(5):
            action = random.randint(0, 3)
            next_state, reward, done, info = env.step(action)
            print(f"\n  Step {i+1}: {info['action']} → reward={reward:.2f}")
            
            if done:
                break
        
        print("\n✅ Environment test passed!")
        
    finally:
        os.unlink(temp_path)


if __name__ == "__main__":
    test_env()
