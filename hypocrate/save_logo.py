#!/usr/bin/env python3
"""
Script pour sauvegarder le logo SUMY
Exécutez ce script après avoir copié l'image dans le même dossier
"""
import shutil
from pathlib import Path

# Chemins
current_dir = Path(__file__).parent
assets_dir = current_dir / "assets"
assets_dir.mkdir(exist_ok=True)

# Chercher l'image dans le dossier courant
possible_names = [
    "sumy_logo.png",
    "SUMY.png", 
    "logo.png",
    "image.png"
]

source_file = None
for name in possible_names:
    test_path = current_dir / name
    if test_path.exists():
        source_file = test_path
        break

if source_file:
    dest_file = assets_dir / "sumy_logo.png"
    shutil.copy(source_file, dest_file)
    print(f"✅ Logo copié : {dest_file}")
    print(f"   Taille : {dest_file.stat().st_size / 1024:.1f} KB")
else:
    print("❌ Aucune image trouvée dans le dossier courant")
    print("   Copiez le logo SUMY dans ce dossier et relancez le script")
    print(f"   Dossier : {current_dir}")
