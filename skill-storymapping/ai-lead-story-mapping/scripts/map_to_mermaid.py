#!/usr/bin/env python3
"""
Map to Mermaid

Erzeugt ein Mermaid-Flowchart (flowchart LR) aus story_map.json.
- Subgraph je Aktivität
- Kanten in Steps-Reihenfolge
"""
import sys
import json


def node_id(activity_id, step_id):
    """Generiere validen Mermaid Node-ID"""
    return f"{activity_id}_{step_id}".replace("-", "_").replace(" ", "_")


def sanitize_label(text):
    """Bereinige Text für Mermaid-Labels (entferne []Zeichen)"""
    return text.replace('[', '(').replace(']', ')').replace('"', "'")


def main():
    if len(sys.argv) < 2:
        print("Usage: map_to_mermaid.py <story_map.json>", file=sys.stderr)
        sys.exit(1)
    
    path = sys.argv[1]
    
    # JSON laden
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[map-to-mermaid] ERROR: Kann JSON nicht lesen: {e}", file=sys.stderr)
        sys.exit(1)
    
    acts = data.get("activities", [])
    
    lines = []
    lines.append("flowchart LR")
    lines.append("")
    
    # Subgraphs pro Aktivität
    for a in acts:
        activity_id = a["id"]
        activity_title = sanitize_label(a["title"])
        
        lines.append(f"  subgraph {activity_id}[\"{activity_title}\"]")
        lines.append(f"    direction TB")
        
        # Nodes
        for s in a.get("steps", []):
            nid = node_id(activity_id, s["id"])
            label = sanitize_label(s["title"])
            lines.append(f"    {nid}[\"{label}\"]")
        
        # Edges in Reihenfolge
        steps = a.get("steps", [])
        for i in range(len(steps) - 1):
            s1, s2 = steps[i], steps[i + 1]
            n1 = node_id(activity_id, s1["id"])
            n2 = node_id(activity_id, s2["id"])
            lines.append(f"    {n1} --> {n2}")
        
        lines.append("  end")
        lines.append("")
    
    # Verbindungen zwischen Activities (optional: erste Step → erste Step)
    if len(acts) > 1:
        for i in range(len(acts) - 1):
            a1, a2 = acts[i], acts[i + 1]
            if a1.get("steps") and a2.get("steps"):
                last_step_a1 = a1["steps"][-1]
                first_step_a2 = a2["steps"][0]
                n1 = node_id(a1["id"], last_step_a1["id"])
                n2 = node_id(a2["id"], first_step_a2["id"])
                lines.append(f"  {n1} -.-> {n2}")
    
    # Styling (optional)
    lines.append("")
    lines.append("  classDef activityStyle fill:#e1f5ff,stroke:#0078d4,stroke-width:2px")
    for a in acts:
        lines.append(f"  class {a['id']} activityStyle")
    
    print("\n".join(lines))


if __name__ == "__main__":
    main()
