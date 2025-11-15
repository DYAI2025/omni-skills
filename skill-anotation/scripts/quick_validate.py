#!/usr/bin/env python3
"""
quick_validate.py – Marker Annotator Skill Validation

Überprüft die Struktur des marker-annotator Skills auf Vollständigkeit:
- SKILL.md mit erforderlichen Abschnitten
- references/ mit Color-Palette und Dark-Mode Guidelines
- scripts/ mit Validation, Packaging und Server-Code
- chrome-extension/ mit Manifest, Content-Script und Styles
"""

import sys
import re
from pathlib import Path

REQUIRED_HEADINGS = [
    "Wann verwenden",
    "Workflow",
    "Eingaben",
    "Ausgabeformat",
    "Beispiele",
    "Qualitätssicherung"
]

REQUIRED_REFERENCES = [
    "annotation-schema.json",
    "color-palette.md",
    "dark-mode-guidelines.md"
]

REQUIRED_SCRIPTS = [
    "quick_validate.py",
    "package_skill.py",
    "python/server.py",
    "python/adapter.py",
    "python/colors.py"
]

REQUIRED_EXTENSION_FILES = [
    "manifest.json",
    "content.js",
    "styles.css",
    "assets/onboarding.txt"
]

def validate_skill_md(skill_path: Path) -> tuple[bool, list[str]]:
    """Überprüft SKILL.md auf Frontmatter und erforderliche Abschnitte."""
    errors = []
    
    if not skill_path.exists():
        errors.append(f"❌ SKILL.md nicht gefunden: {skill_path}")
        return False, errors
    
    content = skill_path.read_text(encoding="utf-8")
    
    # Frontmatter prüfen
    if not content.startswith("---"):
        errors.append("❌ Frontmatter fehlt (muss mit --- beginnen)")
    else:
        fm_match = re.search(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not fm_match:
            errors.append("❌ Frontmatter nicht korrekt geschlossen")
        else:
            fm = fm_match.group(1)
            if not re.search(r"^name:\s*marker-annotator\s*$", fm, re.MULTILINE):
                errors.append("❌ Frontmatter: 'name' muss 'marker-annotator' sein")
            if not re.search(r"^description:", fm, re.MULTILINE):
                errors.append("❌ Frontmatter: 'description' fehlt")
    
    # Erforderliche Überschriften prüfen
    for heading in REQUIRED_HEADINGS:
        pattern = rf"^#{1,2}\s+{re.escape(heading)}\s*$"
        if not re.search(pattern, content, re.MULTILINE):
            errors.append(f"❌ Überschrift fehlt: '{heading}'")
    
    return len(errors) == 0, errors

def validate_references(skill_dir: Path) -> tuple[bool, list[str]]:
    """Überprüft, ob alle erforderlichen Reference-Dateien vorhanden sind."""
    errors = []
    ref_dir = skill_dir / "references"
    
    if not ref_dir.exists():
        errors.append(f"❌ Verzeichnis fehlt: {ref_dir}")
        return False, errors
    
    for ref_file in REQUIRED_REFERENCES:
        ref_path = ref_dir / ref_file
        if not ref_path.exists():
            errors.append(f"❌ Reference-Datei fehlt: {ref_file}")
    
    return len(errors) == 0, errors

def validate_scripts(skill_dir: Path) -> tuple[bool, list[str]]:
    """Überprüft, ob alle erforderlichen Script-Dateien vorhanden sind."""
    errors = []
    scripts_dir = skill_dir / "scripts"
    
    if not scripts_dir.exists():
        errors.append(f"❌ Verzeichnis fehlt: {scripts_dir}")
        return False, errors
    
    for script_file in REQUIRED_SCRIPTS:
        script_path = scripts_dir / script_file
        if not script_path.exists():
            errors.append(f"❌ Script-Datei fehlt: {script_file}")
    
    return len(errors) == 0, errors

def validate_extension(skill_dir: Path) -> tuple[bool, list[str]]:
    """Überprüft, ob alle erforderlichen Chrome-Extension-Dateien vorhanden sind."""
    errors = []
    ext_dir = skill_dir / "chrome-extension"
    
    if not ext_dir.exists():
        errors.append(f"❌ Verzeichnis fehlt: {ext_dir}")
        return False, errors
    
    for ext_file in REQUIRED_EXTENSION_FILES:
        ext_path = ext_dir / ext_file
        if not ext_path.exists():
            errors.append(f"❌ Extension-Datei fehlt: {ext_file}")
    
    return len(errors) == 0, errors

def main():
    """Hauptfunktion: Führt alle Validierungen durch."""
    skill_dir = Path(__file__).parent.parent.resolve()
    skill_md = skill_dir / "SKILL.md"
    
    print(f"🔍 Validiere Skill: {skill_dir.name}\n")
    
    all_ok = True
    
    # 1. SKILL.md validieren
    print("1️⃣  SKILL.md:")
    ok, errors = validate_skill_md(skill_md)
    if ok:
        print("   ✅ Struktur korrekt")
    else:
        for err in errors:
            print(f"   {err}")
        all_ok = False
    
    # 2. references/ validieren
    print("\n2️⃣  references/:")
    ok, errors = validate_references(skill_dir)
    if ok:
        print(f"   ✅ Alle {len(REQUIRED_REFERENCES)} Reference-Dateien vorhanden")
    else:
        for err in errors:
            print(f"   {err}")
        all_ok = False
    
    # 3. scripts/ validieren
    print("\n3️⃣  scripts/:")
    ok, errors = validate_scripts(skill_dir)
    if ok:
        print(f"   ✅ Alle {len(REQUIRED_SCRIPTS)} Script-Dateien vorhanden")
    else:
        for err in errors:
            print(f"   {err}")
        all_ok = False
    
    # 4. chrome-extension/ validieren
    print("\n4️⃣  chrome-extension/:")
    ok, errors = validate_extension(skill_dir)
    if ok:
        print(f"   ✅ Alle {len(REQUIRED_EXTENSION_FILES)} Extension-Dateien vorhanden")
    else:
        for err in errors:
            print(f"   {err}")
        all_ok = False
    
    # Gesamtresultat
    print("\n" + "="*60)
    if all_ok:
        print("✅ VALIDATION PASSED - Skill-Struktur ist vollständig und valide")
        return 0
    else:
        print("❌ VALIDATION FAILED - Bitte fehlende Dateien ergänzen")
        return 1

if __name__ == "__main__":
    sys.exit(main())
