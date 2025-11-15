#!/usr/bin/env python3
"""
Package skill into distributable ZIP file.
Creates a ZIP archive with the entire skill structure.
"""

import os
import sys
import zipfile
from datetime import datetime

def zipdir(root, ziph, base_path):
    """Recursively add directory contents to ZIP."""
    for dirpath, dirnames, filenames in os.walk(root):
        # Skip __pycache__ and .git
        dirnames[:] = [d for d in dirnames if d not in ['__pycache__', '.git', '.venv', 'venv']]
        
        for filename in filenames:
            # Skip .pyc files
            if filename.endswith('.pyc'):
                continue
            
            filepath = os.path.join(dirpath, filename)
            arcname = os.path.relpath(filepath, base_path)
            ziph.write(filepath, arcname)
            print(f"  + {arcname}")

def get_skill_name(skill_folder):
    """Extract skill name from SKILL.md frontmatter."""
    skill_md = os.path.join(skill_folder, "SKILL.md")
    if os.path.isfile(skill_md):
        with open(skill_md, 'r', encoding='utf-8') as f:
            in_frontmatter = False
            for line in f:
                if line.strip() == "---":
                    if not in_frontmatter:
                        in_frontmatter = True
                    else:
                        break
                elif in_frontmatter and line.startswith("name:"):
                    name = line.split(":", 1)[1].strip().strip('"')
                    return name
    
    # Fallback to folder name
    return os.path.basename(skill_folder.rstrip(os.sep))

def main():
    if len(sys.argv) < 2:
        print("Usage: python package_skill.py <skill-folder> [output-dir]")
        print("Example: python package_skill.py ./marker-engine-rl ./dist")
        sys.exit(2)
    
    skill_folder = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(os.path.dirname(skill_folder), "dist")
    
    if not os.path.isdir(skill_folder):
        print(f"❌ Error: Skill folder not found: {skill_folder}")
        sys.exit(1)
    
    # Get skill name
    skill_name = get_skill_name(skill_folder)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate ZIP filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"{skill_name}_{timestamp}.zip"
    zip_path = os.path.join(output_dir, zip_filename)
    
    print(f"\n📦 Packaging skill: {skill_name}")
    print(f"📂 Source: {skill_folder}")
    print(f"📄 Output: {zip_path}")
    print("\nAdding files:")
    print("-" * 60)
    
    # Create ZIP
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipdir(skill_folder, zipf, os.path.dirname(skill_folder))
    
    # Get ZIP size
    zip_size = os.path.getsize(zip_path)
    zip_size_mb = zip_size / (1024 * 1024)
    
    print("-" * 60)
    print(f"✅ Package created successfully!")
    print(f"📊 Size: {zip_size_mb:.2f} MB")
    print(f"📍 Location: {zip_path}")

if __name__ == "__main__":
    main()
