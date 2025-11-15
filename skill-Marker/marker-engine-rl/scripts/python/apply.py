#!/usr/bin/env python3
"""
CLI application for applying marker detection to text input.

Reads text from stdin or file, applies marker engine, outputs NDJSON events.
"""

import os
import sys
import json

# Import engine
try:
    from engine import MarkerEngine
except ImportError:
    sys.path.append(os.path.dirname(__file__))
    from engine import MarkerEngine


def main():
    """Main application entry point."""
    # Configuration
    markers_source = "supabase" if (os.environ.get("SUPABASE_URL") and 
                                     os.environ.get("SUPABASE_ANON_KEY")) else "local"
    policy_path = os.environ.get("POLICY_PATH")
    
    # Check for input
    if len(sys.argv) > 1:
        # Read from file
        input_file = sys.argv[1]
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print(f"Error: File not found: {input_file}", file=sys.stderr)
            sys.exit(1)
    else:
        # Read from stdin
        texts = [line.strip() for line in sys.stdin if line.strip()]
    
    if not texts:
        print("Usage: python apply.py [input-file]", file=sys.stderr)
        print("       OR: echo 'text' | python apply.py", file=sys.stderr)
        print("", file=sys.stderr)
        print("Environment variables:", file=sys.stderr)
        print("  SUPABASE_URL       - Supabase project URL", file=sys.stderr)
        print("  SUPABASE_ANON_KEY  - Supabase anon key", file=sys.stderr)
        print("  POLICY_PATH        - Path to policy.json (optional)", file=sys.stderr)
        sys.exit(2)
    
    # Initialize engine (suppress stdout during init)
    import io
    from contextlib import redirect_stdout
    
    with redirect_stdout(io.StringIO()):
        engine = MarkerEngine(markers_source=markers_source, policy_path=policy_path)
    
    # Apply marker detection
    result = engine.apply(texts)
    
    # Output NDJSON (one event per line)
    for event in result["events"]:
        print(json.dumps(event, ensure_ascii=False))
    
    # Optionally output telemetry to stderr
    if os.environ.get("VERBOSE", "").lower() in ["1", "true", "yes"]:
        print(json.dumps(result["telemetry"], ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
