#!/usr/bin/env python3
"""
Prepare SFT (Supervised Fine-Tuning) dataset from raw examples.
Converts examples to JSONL format with validation checks.

Input: Text/CSV with examples
Output: JSONL with {"instruction": "...", "output": "...", "meta": {...}}

Validates:
- SEM composition (≥2 different ATOs)
- MEMA composition (≥2 CLUs)
- ARS range (0-5)
- Decay validity (0 < decay < 1)
"""

import json
import sys
import re
from typing import Dict, List, Any

def validate_sem_composition(sem_data: Dict[str, Any]) -> bool:
    """Validate that SEM has ≥2 different ATOs."""
    composed_of = sem_data.get("composed_of", [])
    unique_atos = set(composed_of)
    return len(unique_atos) >= 2

def validate_mema_composition(mema_data: Dict[str, Any]) -> bool:
    """Validate that MEMA has ≥2 CLUs."""
    composed_of = mema_data.get("composed_of", [])
    clus = [c for c in composed_of if c.startswith("CLU_")]
    return len(set(clus)) >= 2

def validate_ars(ars_value: float) -> bool:
    """Validate ARS is in range 0-5."""
    return 0 <= ars_value <= 5

def validate_decay(decay_str: str) -> bool:
    """Validate decay format and value."""
    try:
        parts = decay_str.split("/")
        decay_value = float(parts[0])
        return 0 < decay_value < 1
    except (ValueError, IndexError):
        return False

def create_sft_record(instruction: str, output: str, meta: Dict[str, Any] = None) -> Dict[str, Any]:
    """Create a single SFT record."""
    return {
        "instruction": instruction.strip(),
        "output": output.strip(),
        "meta": meta or {}
    }

def parse_simple_format(line: str) -> tuple:
    """
    Parse simple format: "instruction | output"
    Returns: (instruction, output, meta)
    """
    if "|" not in line:
        return None, None, None
    
    parts = line.split("|", 1)
    instruction = parts[0].strip()
    output = parts[1].strip()
    
    # Extract meta information from output
    meta = {
        "has_ato": "ATO_" in output,
        "has_sem": "SEM_" in output,
        "has_clu": "CLU_" in output,
        "has_mema": "MEMA_" in output,
        "has_rf": "RF-Manifestation" in output or "RF:" in output
    }
    
    # Check for rule validations in output
    if "≥2" in output or ">=2" in output:
        meta["mentions_composition_rule"] = True
    
    if "ARS" in output:
        # Try to extract ARS value
        ars_match = re.search(r'ARS:?\s*(\d+\.?\d*)', output)
        if ars_match:
            meta["ars_value"] = float(ars_match.group(1))
    
    return instruction, output, meta

def process_file(input_path: str, output_path: str, format_type: str = "simple"):
    """
    Process input file and create JSONL output.
    
    format_type: "simple" (instruction|output per line) or "json" (existing JSONL)
    """
    records = []
    
    with open(input_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            
            if format_type == "simple":
                instruction, output, meta = parse_simple_format(line)
                if instruction and output:
                    record = create_sft_record(instruction, output, meta)
                    records.append(record)
                else:
                    print(f"⚠️  Warning: Line {line_num} could not be parsed", file=sys.stderr)
            
            elif format_type == "json":
                try:
                    record = json.loads(line)
                    # Validate structure
                    if "instruction" in record and "output" in record:
                        records.append(record)
                    else:
                        print(f"⚠️  Warning: Line {line_num} missing required fields", file=sys.stderr)
                except json.JSONDecodeError as e:
                    print(f"⚠️  Warning: Line {line_num} invalid JSON: {e}", file=sys.stderr)
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    
    return records

def generate_statistics(records: List[Dict[str, Any]]):
    """Generate statistics about the dataset."""
    stats = {
        "total_records": len(records),
        "has_ato": 0,
        "has_sem": 0,
        "has_clu": 0,
        "has_mema": 0,
        "has_rf": 0,
        "mentions_rules": 0,
        "avg_instruction_length": 0,
        "avg_output_length": 0
    }
    
    total_instr_len = 0
    total_output_len = 0
    
    for record in records:
        meta = record.get("meta", {})
        stats["has_ato"] += 1 if meta.get("has_ato") else 0
        stats["has_sem"] += 1 if meta.get("has_sem") else 0
        stats["has_clu"] += 1 if meta.get("has_clu") else 0
        stats["has_mema"] += 1 if meta.get("has_mema") else 0
        stats["has_rf"] += 1 if meta.get("has_rf") else 0
        stats["mentions_rules"] += 1 if meta.get("mentions_composition_rule") else 0
        
        total_instr_len += len(record["instruction"])
        total_output_len += len(record["output"])
    
    if len(records) > 0:
        stats["avg_instruction_length"] = total_instr_len // len(records)
        stats["avg_output_length"] = total_output_len // len(records)
    
    return stats

def main():
    if len(sys.argv) < 3:
        print("Usage: python prepare_sft.py <input-file> <output-file> [format]")
        print()
        print("Arguments:")
        print("  input-file   : Path to input file")
        print("  output-file  : Path to output JSONL file")
        print("  format       : 'simple' (default) or 'json'")
        print()
        print("Format 'simple': Each line is 'instruction | output'")
        print("Format 'json': Each line is already a JSON object")
        sys.exit(2)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    format_type = sys.argv[3] if len(sys.argv) > 3 else "simple"
    
    if format_type not in ["simple", "json"]:
        print(f"❌ Error: Invalid format '{format_type}'. Use 'simple' or 'json'.")
        sys.exit(1)
    
    print(f"\n📝 Preparing SFT dataset")
    print(f"📂 Input: {input_path}")
    print(f"📄 Output: {output_path}")
    print(f"🔤 Format: {format_type}")
    print()
    
    try:
        records = process_file(input_path, output_path, format_type)
        stats = generate_statistics(records)
        
        print("✅ Dataset created successfully!")
        print("\n📊 Statistics:")
        print(f"  Total records: {stats['total_records']}")
        print(f"  With ATO: {stats['has_ato']}")
        print(f"  With SEM: {stats['has_sem']}")
        print(f"  With CLU: {stats['has_clu']}")
        print(f"  With MEMA: {stats['has_mema']}")
        print(f"  With RF-Manifestation: {stats['has_rf']}")
        print(f"  Mentions composition rules: {stats['mentions_rules']}")
        print(f"  Avg instruction length: {stats['avg_instruction_length']} chars")
        print(f"  Avg output length: {stats['avg_output_length']} chars")
        print(f"\n📍 Output written to: {output_path}")
        
    except FileNotFoundError:
        print(f"❌ Error: Input file not found: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
