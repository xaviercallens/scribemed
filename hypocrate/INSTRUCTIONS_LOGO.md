# Instructions pour ajouter le logo SUMY

## ✅ Modifications effectuées

L'application a été mise à jour pour utiliser "SUMY" au lieu de "Hypocrate" :

1. ✅ Titre de la page : "SUMY - Assistant Médical IA"
2. ✅ En-tête principal : Logo SUMY (à ajouter)
3. ✅ Sidebar : "SUMY utilise..."
4. ✅ Footer : "SUMY - Assistant Médical IA"

---

## 📁 Ajout du logo

### Étape 1 : Sauvegarder le logo
Sauvegardez l'image du logo SUMY (celle avec le stéthoscope bleu et turquoise) dans :

```
/Users/xcallens/CascadeProjects/windsurf-project/hypocrate/assets/sumy_logo.png
```

### Étape 2 : Vérifier le fichier
```bash
ls -lh assets/sumy_logo.png
```

### Étape 3 : Redémarrer l'application
```bash
# Arrêter
pkill -f streamlit

# Relancer
streamlit run hypocrate_app.py
```

---

## 🎨 Spécifications du logo

- **Format :** PNG avec fond transparent
- **Dimensions recommandées :** 800x300 pixels (ou ratio similaire)
- **Largeur d'affichage :** 400px dans l'application
- **Position :** Centré en haut de la page

---

## 🔧 Si le logo ne s'affiche pas

### Option 1 : Vérifier le chemin
```python
# Dans hypocrate_app.py, ligne 123
st.image("assets/sumy_logo.png", width=400)
```

### Option 2 : Utiliser un chemin absolu
```python
from pathlib import Path
logo_path = Path(__file__).parent / "assets" / "sumy_logo.png"
st.image(str(logo_path), width=400)
```

### Option 3 : Encoder en base64
Si problème de chemin, on peut encoder le logo directement dans le code.

---

## 📝 Fichiers modifiés

- ✅ `hypocrate_app.py` - Toutes les références "Hypocrate" → "SUMY"
- ⏳ `assets/sumy_logo.png` - À ajouter manuellement

---

## 🚀 Après ajout du logo

L'application affichera :
- Logo SUMY centré en haut
- "Assistant Médical IA - 100% Local & Confidentiel" sous le logo
- Badge de confidentialité
- Toutes les références à "SUMY" dans l'interface

---

**Note :** Le dossier `assets/` a été créé. Il suffit d'y copier le fichier `sumy_logo.png`.
