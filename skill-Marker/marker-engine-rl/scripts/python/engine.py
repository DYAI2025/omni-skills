#!/usr/bin/env python3
"""
Runtime Engine for Marker Detection with LeanDeep 4.0 Methodology.

Implements deterministic bottom-up pipeline:
- ATO (Atomic) detection via regex patterns
- SEM (Semantic) composition from ≥2 different ATOs
- CLU (Cluster) pattern recognition from SEMs
- MEMA (Meta-Analysis) from ≥2 CLUs with ARS (0-5) and decay

Features:
- Loads markers from Supabase (or local fallback)
- Optional policy.json for tuning (multipliers, windows)
- Enforces composition rules strictly
- Outputs NDJSON events with RF-context
"""

import os
import re
import json
import requests
from typing import Dict, Any, List, Set
from collections import defaultdict, deque, Counter


# Configuration from environment
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY", "")
POLICY_PATH = os.environ.get("POLICY_PATH", "./policy.json")


class MarkerEngine:
    """Main engine for marker detection."""
    
    def __init__(self, markers_source: str = "local", policy_path: str = None):
        """
        Initialize engine.
        
        Args:
            markers_source: "supabase" | "local" | "zip"
            policy_path: Path to policy.json (optional)
        """
        self.markers_source = markers_source
        self.policy_path = policy_path or POLICY_PATH
        
        # Load markers
        self.atoms, self.sems, self.clus, self.memas = self._load_markers()
        
        # Load policy (if exists)
        self.policy = self._load_policy()
        
        # Runtime settings
        self.sem_window = self.policy.get("sem_window", 3) if self.policy else 3
        self.clu_window = self.policy.get("clu_window", 5) if self.policy else 5
        self.family_multipliers = self.policy.get("family_multipliers", {}) if self.policy else {}
        
        print(f"✓ Engine initialized: {len(self.atoms)} ATOs, {len(self.sems)} SEMs, {len(self.clus)} CLUs, {len(self.memas)} MEMAs")
        if self.policy:
            print(f"✓ Policy loaded: SEM window={self.sem_window}, CLU window={self.clu_window}")
    
    def _load_markers(self) -> tuple:
        """Load markers from configured source."""
        if self.markers_source == "supabase" and SUPABASE_URL and SUPABASE_KEY:
            return self._load_from_supabase()
        else:
            return self._load_dummy_markers()
    
    def _load_from_supabase(self) -> tuple:
        """Load markers from Supabase REST API."""
        try:
            url = f"{SUPABASE_URL}/rest/v1/markers?select=*"
            headers = {
                "apikey": SUPABASE_KEY,
                "Authorization": f"Bearer {SUPABASE_KEY}"
            }
            
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            
            rows = response.json()
            atoms, sems, clus, memas = [], [], [], []
            
            for row in rows:
                if not row.get("active", True):
                    continue
                
                marker_id = row["id"]
                if marker_id.startswith("ATO_"):
                    atoms.append(row)
                elif marker_id.startswith("SEM_"):
                    sems.append(row)
                elif marker_id.startswith("CLU_"):
                    clus.append(row)
                elif marker_id.startswith("MEMA_"):
                    memas.append(row)
            
            return atoms, sems, clus, memas
        
        except Exception as e:
            print(f"⚠️  Warning: Failed to load from Supabase: {e}")
            print("   Falling back to dummy markers")
            return self._load_dummy_markers()
    
    def _load_dummy_markers(self) -> tuple:
        """Load dummy markers for testing."""
        atoms = [
            {"id": "ATO_UNCERTAINTY_PHRASE", "pattern": [r"\bnot\s+sure\b", r"\bunsicher\b", r"\bvielleicht\b"]},
            {"id": "ATO_HESITATION", "pattern": [r"\bhmm\b", r"\buh\b", r"\bwell\b"]},
            {"id": "ATO_DELAY_PHRASE", "pattern": [r"\blater\b", r"\bmorgen\b", r"\bverschieben\b"]},
            {"id": "ATO_CONFLICT_WORD", "pattern": [r"\bdisagree\b", r"\bproblem\b", r"\bkonflikt\b"]},
        ]
        
        sems = [
            {"id": "SEM_UNCERTAINTY_TONING", "composed_of": ["ATO_UNCERTAINTY_PHRASE", "ATO_HESITATION"]},
            {"id": "SEM_AVOIDANT_BEHAVIOR", "composed_of": ["ATO_DELAY_PHRASE", "ATO_UNCERTAINTY_PHRASE"]},
            {"id": "SEM_CONFLICT_MARKER", "composed_of": ["ATO_CONFLICT_WORD", "ATO_HESITATION"]},
        ]
        
        clus = [
            {"id": "CLU_INTUITION_UNCERTAINTY", "composed_of": ["SEM_UNCERTAINTY_TONING", "SEM_AVOIDANT_BEHAVIOR"], "x_of_y": [2, 2]},
            {"id": "CLU_CONFLICT_CYCLE", "composed_of": ["SEM_CONFLICT_MARKER"], "x_of_y": [1, 1]},
        ]
        
        memas = [
            {"id": "MEMA_RELATIONSHIP_STRAIN", "composed_of": ["CLU_CONFLICT_CYCLE", "CLU_INTUITION_UNCERTAINTY"]},
        ]
        
        return atoms, sems, clus, memas
    
    def _load_policy(self) -> Dict[str, Any]:
        """Load policy from JSON file."""
        if os.path.isfile(self.policy_path):
            try:
                with open(self.policy_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Warning: Failed to load policy: {e}")
        return {}
    
    def detect_atos(self, text: str) -> List[Dict[str, Any]]:
        """Detect atomic markers in text."""
        hits = []
        
        for atom in self.atoms:
            patterns = atom.get("pattern", [])
            
            for pattern_str in patterns:
                try:
                    regex = re.compile(pattern_str, re.IGNORECASE | re.UNICODE)
                    for match in regex.finditer(text):
                        hits.append({
                            "type": "ATO_HIT",
                            "id": atom["id"],
                            "match": match.group(0),
                            "span": [match.start(), match.end()]
                        })
                except re.error as e:
                    print(f"⚠️  Invalid regex in {atom['id']}: {e}")
        
        return hits
    
    def compose_sems(self, ato_hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Compose SEMs from ATOs.
        
        Rule: SEM requires ≥2 different ATOs from composed_of list.
        """
        present_atos = set(h["id"] for h in ato_hits)
        sem_hits = []
        
        for sem in self.sems:
            required = set(sem.get("composed_of", []))
            
            # Check rule: ≥2 different ATOs
            if len(required) < 2:
                continue  # Invalid SEM definition
            
            # Check if all required ATOs are present
            if required.issubset(present_atos):
                sem_hits.append({
                    "type": "SEM_HIT",
                    "id": sem["id"],
                    "evidence": list(required),
                    "rule_check": "✓ ≥2 ATOs"
                })
        
        return sem_hits
    
    def detect_clus(self, sem_hits: List[Dict[str, Any]], window_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Detect CLU patterns from SEMs within window.
        
        Uses X-of-Y logic (e.g., need 2 out of 3 SEMs).
        """
        present_sems = set(h["id"] for h in sem_hits)
        clu_hits = []
        
        for clu in self.clus:
            required = set(clu.get("composed_of", []))
            x_of_y = clu.get("x_of_y", [len(required), len(required)])  # Default: all required
            x, y = x_of_y[0], x_of_y[1]
            
            matched = required.intersection(present_sems)
            
            if len(matched) >= x:
                clu_hits.append({
                    "type": "CLU_HIT",
                    "id": clu["id"],
                    "window": window_ids,
                    "evidence": list(matched),
                    "x_of_y": f"{len(matched)}/{y}"
                })
        
        return clu_hits
    
    def synthesize_memas(self, clu_hits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Synthesize MEMAs from CLUs.
        
        Rule: MEMA requires ≥2 different CLUs.
        Calculates ARS (0-5) and decay.
        """
        present_clus = set(h["id"] for h in clu_hits)
        mema_hits = []
        
        for mema in self.memas:
            required = set(mema.get("composed_of", []))
            required_clus = [c for c in required if c.startswith("CLU_")]
            
            # Check rule: ≥2 CLUs
            if len(set(required_clus)) < 2:
                continue
            
            matched = set(required_clus).intersection(present_clus)
            
            if len(matched) >= 2:
                # Calculate ARS (simplified: based on number of CLUs)
                ars = min(5.0, 1.5 + len(matched) * 0.8)
                decay = 0.85  # Default decay rate
                
                mema_hits.append({
                    "type": "MEMA_HIT",
                    "id": mema["id"],
                    "evidence": list(matched),
                    "ars": round(ars, 2),
                    "decay": f"{decay}/24h",
                    "rule_check": "✓ ≥2 CLUs"
                })
        
        return mema_hits
    
    def apply(self, texts: List[str]) -> Dict[str, Any]:
        """
        Apply marker detection to texts.
        
        Args:
            texts: List of text messages
        
        Returns:
            Result with events and telemetry
        """
        all_events = []
        window = deque(maxlen=self.clu_window)
        
        for i, text in enumerate(texts):
            msg_id = f"m{i+1}"
            window.append(msg_id)
            
            # ATO detection
            ato_hits = self.detect_atos(text)
            for hit in ato_hits:
                hit["messageId"] = msg_id
            
            # SEM composition (within SEM window)
            recent_atos = [e for e in all_events if e["type"] == "ATO_HIT" and e.get("messageId") in list(window)[-self.sem_window:]]
            sem_hits = self.compose_sems(recent_atos + ato_hits)
            
            # CLU detection (within CLU window)
            recent_sems = [e for e in all_events if e["type"] == "SEM_HIT"][-self.clu_window:]
            clu_hits = self.detect_clus(recent_sems + sem_hits, list(window))
            
            # MEMA synthesis
            recent_clus = [e for e in all_events if e["type"] == "CLU_HIT"]
            mema_hits = self.synthesize_memas(recent_clus + clu_hits)
            
            all_events.extend(ato_hits + sem_hits + clu_hits + mema_hits)
        
        # RF context (simplified)
        rf_context = {
            "level": "L1-STONE",
            "intensity": 0.52
        }
        
        # Telemetry
        telemetry = {
            "segments": len(texts),
            "sem_violations": self._count_violations(all_events, "SEM"),
            "mema_violations": self._count_violations(all_events, "MEMA"),
            "policy": self.policy_path if self.policy else None
        }
        
        return {
            "events": all_events,
            "rf_context": rf_context,
            "telemetry": telemetry
        }
    
    def _count_violations(self, events: List[Dict[str, Any]], level: str) -> int:
        """Count rule violations (simplified check)."""
        # In production, this would validate composition rules
        return 0


def main():
    """CLI entry point."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python engine.py <text-file>")
        print("Environment variables:")
        print("  SUPABASE_URL - Supabase project URL")
        print("  SUPABASE_ANON_KEY - Supabase anon key")
        print("  POLICY_PATH - Path to policy.json (optional)")
        sys.exit(2)
    
    text_file = sys.argv[1]
    
    # Load texts
    with open(text_file, 'r', encoding='utf-8') as f:
        texts = [line.strip() for line in f if line.strip()]
    
    print(f"\n🔍 Marker Engine - Processing {len(texts)} text(s)")
    print("=" * 60)
    
    # Initialize engine
    markers_source = "supabase" if SUPABASE_URL and SUPABASE_KEY else "local"
    engine = MarkerEngine(markers_source=markers_source)
    
    # Apply
    result = engine.apply(texts)
    
    # Output as JSON
    print("\n📊 Results:")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    print("\n" + "=" * 60)
    print(f"✓ Processed {result['telemetry']['segments']} segments")
    print(f"✓ Detected {len(result['events'])} events")
    print(f"  - ATO: {sum(1 for e in result['events'] if e['type'] == 'ATO_HIT')}")
    print(f"  - SEM: {sum(1 for e in result['events'] if e['type'] == 'SEM_HIT')}")
    print(f"  - CLU: {sum(1 for e in result['events'] if e['type'] == 'CLU_HIT')}")
    print(f"  - MEMA: {sum(1 for e in result['events'] if e['type'] == 'MEMA_HIT')}")


if __name__ == "__main__":
    main()
