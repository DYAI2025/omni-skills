#!/usr/bin/env python3
"""
package_skill.py – Package Marker Annotator Skill

Erstellt ein ZIP-Archiv mit allen Skill-Dateien (SKILL.md, references/, 
scripts/, chrome-extension/) mit Zeitstempel für Versionierung.
"""

import sys
import zipfile
from pathlib import Path
from datetime import datetime

def package_skill(skill_dir: Path, output_dir: Path | None = None) -> Path:
    """
    Erstellt ZIP-Archiv mit allen Skill-Dateien.
    
    Args:
        skill_dir: Verzeichnis des Skills (enthält SKILL.md)
        output_dir: Zielverzeichnis (optional, default: skill_dir)
    
    Returns:
        Path zum erstellten ZIP-Archiv
    """
    if output_dir is None:
        output_dir = skill_dir
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_name = f"marker-annotator_{timestamp}.zip"
    zip_path = output_dir / zip_name
    
    # Liste aller zu packenden Dateien/Verzeichnisse
    includes = [
        "SKILL.md",
        "references/",
        "scripts/",
        "chrome-extension/"
    ]
    
    excluded_patterns = [
        "__pycache__",
        "*.pyc",
        ".DS_Store",
        ".git",
        "*.zip"
    ]
    
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for include in includes:
            include_path = skill_dir / include
            
            if not include_path.exists():
                print(f"⚠️  Warnung: {include} nicht gefunden, überspringe")
                continue
            
            if include_path.is_file():
                # Einzelne Datei
                arcname = include_path.relative_to(skill_dir)
                zf.write(include_path, arcname)
                print(f"   ✅ {arcname}")
            else:
                # Verzeichnis rekursiv
                for file_path in include_path.rglob("*"):
                    if file_path.is_file():
                        # Prüfe Ausschlussmuster
                        if any(
                            pattern in str(file_path) 
                            for pattern in excluded_patterns
                        ):
                            continue
                        
                        arcname = file_path.relative_to(skill_dir)
                        zf.write(file_path, arcname)
                        print(f"   ✅ {arcname}")
    
    return zip_path

def main():
    """Hauptfunktion: Packaged den Skill."""
    skill_dir = Path(__file__).parent.parent.resolve()
    
    print(f"📦 Package Skill: {skill_dir.name}\n")
    
    # Prüfe, ob SKILL.md existiert
    if not (skill_dir / "SKILL.md").exists():
        print("❌ SKILL.md nicht gefunden - ist dies ein Skill-Verzeichnis?")
        return 1
    
    # Package erstellen
    try:
        zip_path = package_skill(skill_dir)
        print(f"\n✅ Package erstellt: {zip_path.name}")
        print(f"   Größe: {zip_path.stat().st_size / 1024:.1f} KB")
        return 0
    except Exception as e:
        print(f"\n❌ Fehler beim Packaging: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
