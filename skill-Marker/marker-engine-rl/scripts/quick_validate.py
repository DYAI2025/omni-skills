#!/usr/bin/env python3
"""
Quick validation script for Marker-Engine-RL skill structure.
Validates SKILL.md format, frontmatter, and required sections.
"""

import re
import sys
import os

RE_NAME = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
REQUIRED_HEADINGS = [
    "## Wann verwenden",
    "## Workflow/Anweisungen",
    "## Eingaben",
    "## Ausgabeformat",
    "## Beispiele",
    "## Qualitätssicherung"
]

def parse_frontmatter(txt: str):
    """Parse YAML frontmatter from markdown content."""
    if not txt.startswith("---"):
        return {}
    
    lines = txt.splitlines()
    fm_lines = []
    end = 0
    
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
        fm_lines.append(lines[i])
    
    fm = {}
    for ln in fm_lines:
        if ":" in ln:
            k, v = ln.split(":", 1)
            fm[k.strip()] = v.strip().strip('"')
    
    return fm

def validate_skill_md(path: str):
    """Validate SKILL.md structure and content."""
    if not os.path.isfile(path):
        print("❌ FAIL: SKILL.md fehlt")
        return False
    
    with open(path, "r", encoding="utf-8") as f:
        txt = f.read()
    
    ok = True
    
    # Parse frontmatter
    fm = parse_frontmatter(txt)
    
    # Validate name
    name = fm.get("name", "")
    if not RE_NAME.fullmatch(name):
        print(f"❌ FAIL: Ungültiger name: {name!r} (muss lowercase mit Bindestrichen sein)")
        ok = False
    else:
        print(f"✓ Name: {name}")
    
    # Validate description
    desc = fm.get("description", "")
    if not desc or len(desc) < 10:
        print("❌ FAIL: description fehlt oder zu kurz")
        ok = False
    elif "<" in desc or ">" in desc:
        print("❌ FAIL: description enthält spitze Klammern")
        ok = False
    else:
        print(f"✓ Description: {desc[:50]}...")
    
    # Validate required headings
    missing_headings = []
    for h in REQUIRED_HEADINGS:
        if h not in txt:
            missing_headings.append(h)
            ok = False
    
    if missing_headings:
        print(f"❌ FAIL: Fehlende Abschnitte: {', '.join(missing_headings)}")
    else:
        print(f"✓ Alle {len(REQUIRED_HEADINGS)} erforderlichen Abschnitte vorhanden")
    
    return ok

def validate_references(base_path: str):
    """Validate that all reference files exist."""
    ref_dir = os.path.join(base_path, "references")
    required_files = [
        "rl-design.md",
        "sft-format.md",
        "reward-schemes.md",
        "eval-metrics.md",
        "coaching-orchestration.md"
    ]
    
    if not os.path.isdir(ref_dir):
        print("❌ FAIL: references/ Verzeichnis fehlt")
        return False
    
    ok = True
    for fname in required_files:
        fpath = os.path.join(ref_dir, fname)
        if not os.path.isfile(fpath):
            print(f"❌ FAIL: {fname} fehlt in references/")
            ok = False
        else:
            print(f"✓ Referenz: {fname}")
    
    return ok

def validate_scripts(base_path: str):
    """Validate that core scripts exist."""
    required_scripts = [
        "scripts/quick_validate.py",
        "scripts/package_skill.py",
        "scripts/data/prepare_sft.py",
        "scripts/rl/offline_env.py",
        "scripts/rl/train_ppo.py",
        "scripts/rl/validate_checkpoint.py",
        "scripts/python/engine.py",
        "scripts/python/apply.py"
    ]
    
    ok = True
    for script in required_scripts:
        spath = os.path.join(base_path, script)
        if not os.path.isfile(spath):
            print(f"❌ FAIL: {script} fehlt")
            ok = False
    
    if ok:
        print(f"✓ Alle {len(required_scripts)} Scripts vorhanden")
    
    return ok

def main():
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <skill-folder>")
        print("Example: python quick_validate.py ./marker-engine-rl")
        sys.exit(2)
    
    skill_folder = sys.argv[1]
    
    if not os.path.isdir(skill_folder):
        print(f"❌ FAIL: Verzeichnis nicht gefunden: {skill_folder}")
        sys.exit(1)
    
    print(f"\n🔍 Validiere Skill: {skill_folder}\n")
    print("=" * 60)
    
    # Validate SKILL.md
    print("\n📄 SKILL.md Validierung:")
    print("-" * 60)
    skill_md_path = os.path.join(skill_folder, "SKILL.md")
    skill_ok = validate_skill_md(skill_md_path)
    
    # Validate references
    print("\n📚 References Validierung:")
    print("-" * 60)
    refs_ok = validate_references(skill_folder)
    
    # Validate scripts
    print("\n🔧 Scripts Validierung:")
    print("-" * 60)
    scripts_ok = validate_scripts(skill_folder)
    
    # Final result
    print("\n" + "=" * 60)
    all_ok = skill_ok and refs_ok and scripts_ok
    
    if all_ok:
        print("✅ VALIDATION PASSED - Skill-Struktur ist vollständig und valide")
        sys.exit(0)
    else:
        print("❌ VALIDATION FAILED - Siehe Fehler oben")
        sys.exit(1)

if __name__ == "__main__":
    main()
