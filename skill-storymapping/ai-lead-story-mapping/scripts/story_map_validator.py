#!/usr/bin/env python3
"""
Story Map Validator

Prüft das JSON-Format gemäß Template (product, actor, goal, kpis, activities, stories, version).
Exit 0 bei Erfolg, sonst != 0 mit Fehlermeldung.
"""
import sys
import json

REQ_TOP = ["product", "actor", "goal", "activities", "stories", "version"]
REQ_ACTIVITY = ["id", "title", "steps"]
REQ_STEP = ["id", "title"]
REQ_STORY = ["id", "title", "activity_id", "step_id", "ac"]


def die(msg, code=1):
    """Fehler ausgeben und beenden"""
    print(f"[story-map-validator] ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def validate_top_level(data):
    """Validiere Top-Level-Felder"""
    for k in REQ_TOP:
        if k not in data:
            die(f"Pflichtfeld fehlt: {k}")
    
    if not isinstance(data["activities"], list) or not data["activities"]:
        die("activities muss nicht-leere Liste sein.")
    
    if not isinstance(data["stories"], list) or not data["stories"]:
        die("stories muss nicht-leere Liste sein.")


def validate_activities(data):
    """Validiere Activities und Steps, erstelle Index"""
    act_index = {}
    step_index = {}
    
    for a in data["activities"]:
        # Prüfe Required-Felder
        for k in REQ_ACTIVITY:
            if k not in a:
                die(f"Aktivität unvollständig (fehlt: {k}): {a}")
        
        # Prüfe Steps
        if not isinstance(a["steps"], list) or not a["steps"]:
            die(f"steps fehlen in Aktivität: {a.get('id')}")
        
        # Prüfe doppelte Activity-ID
        if a["id"] in act_index:
            die(f"Doppelte activity_id: {a['id']}")
        
        act_index[a["id"]] = a
        
        # Validiere Steps
        for s in a["steps"]:
            for k in REQ_STEP:
                if k not in s:
                    die(f"Schritt unvollständig (fehlt: {k}): {s}")
            
            if s["id"] in step_index:
                die(f"Doppelte step_id: {s['id']}")
            
            step_index[s["id"]] = {"step": s, "activity_id": a["id"]}
    
    return act_index, step_index


def validate_stories(data, act_index, step_index):
    """Validiere Stories"""
    seen_ids = set()
    
    for st in data["stories"]:
        # Prüfe Required-Felder
        for k in REQ_STORY:
            if k not in st:
                die(f"Story unvollständig (fehlt: {k}): {st}")
        
        # Prüfe doppelte Story-ID
        if st["id"] in seen_ids:
            die(f"Doppelte Story-ID: {st['id']}")
        seen_ids.add(st["id"])
        
        # Prüfe Referenzen
        if st["activity_id"] not in act_index:
            die(f"Unbekannte activity_id: {st['activity_id']} in Story: {st['id']}")
        
        if st["step_id"] not in step_index:
            die(f"Unbekannte step_id: {st['step_id']} in Story: {st['id']}")
        
        # Prüfe AC
        if not isinstance(st["ac"], list) or not st["ac"]:
            die(f"AC fehlen in Story: {st['id']}")
        
        # Optional: Prüfe Dependencies
        if "depends_on" in st and st["depends_on"]:
            dep_id = st["depends_on"]
            if dep_id not in seen_ids and dep_id != st["id"]:
                # Warnung, kein Fehler (Story könnte später im Array kommen)
                print(f"[story-map-validator] WARNING: Story {st['id']} referenziert depends_on={dep_id}, die noch nicht gesehen wurde.", file=sys.stderr)


def main():
    if len(sys.argv) < 2:
        die("Bitte Pfad zur Story-Map-JSON angeben (z. B. assets/examples/example-story-map.json).")
    
    path = sys.argv[1]
    
    # JSON laden
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        die(f"Datei nicht gefunden: {path}")
    except json.JSONDecodeError as e:
        die(f"Ungültiges JSON: {e}")
    except Exception as e:
        die(f"Kann JSON nicht lesen: {e}")
    
    # Validierungen
    validate_top_level(data)
    act_index, step_index = validate_activities(data)
    validate_stories(data, act_index, step_index)
    
    # Success
    print(f"[story-map-validator] ✓ Valid: {path}")
    print(f"  - {len(data['activities'])} Activities")
    print(f"  - {sum(len(a['steps']) for a in data['activities'])} Steps")
    print(f"  - {len(data['stories'])} Stories")


if __name__ == "__main__":
    main()
