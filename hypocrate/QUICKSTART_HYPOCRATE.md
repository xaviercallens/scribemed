# 🚀 Démarrage Rapide - Hypocrate

## Installation en 5 minutes

### 1. Prérequis

```bash
# Vérifier Python
python3 --version  # Doit être 3.10+

# Installer Ollama (si pas déjà fait)
brew install ollama  # macOS
# ou télécharger depuis https://ollama.ai
```

### 2. Installation

```bash
# Aller dans le dossier Hypocrate
cd hypocrate

# Installer les dépendances
pip install -r requirements_hypocrate.txt

# Télécharger les modèles spaCy
python -m spacy download fr_core_news_md
python -m spacy download en_core_web_sm

# Installer scispaCy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz

# Télécharger Llama2 (si pas déjà fait)
ollama pull llama2
```

### 3. Lancement

```bash
# Option 1: Script automatique
chmod +x start_hypocrate.sh
./start_hypocrate.sh

# Option 2: Manuel
streamlit run hypocrate_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## Utilisation

### Workflow complet

1. **Upload audio**
   - Cliquez sur "Browse files"
   - Sélectionnez un fichier WAV, MP3, M4A, OGG ou FLAC
   - L'audio s'affichera pour vérification

2. **Configuration** (barre latérale)
   - Modèle Whisper: `base` (recommandé)
   - Langue: Français
   - Spécialité: Généraliste
   - Format: SOAP structuré

3. **Traitement**
   - Cliquez sur "🚀 Analyser la consultation"
   - Attendez le traitement (quelques secondes à quelques minutes selon la durée)

4. **Résultats**
   - 📄 Transcription complète
   - 🏷️ Entités médicales (allergies, médicaments, symptômes)
   - 📋 Compte-rendu SOAP structuré
   - 📧 Lettre d'adressage professionnelle

---

## Exemple de consultation test

Créez un fichier audio de test avec ce texte:

```
Médecin: Bonjour, qu'est-ce qui vous amène aujourd'hui?

Patient: Bonjour docteur. J'ai mal à la gorge depuis une semaine maintenant.

Médecin: D'accord. Avez-vous de la fièvre?

Patient: Oui, j'ai eu 38 degrés hier soir.

Médecin: Avez-vous des allergies connues?

Patient: Oui, je suis allergique à la pénicilline.

Médecin: Très bien, je vais examiner votre gorge. 
         *examine* Votre gorge est rouge et inflammée. 
         Je vais vous prescrire du paracétamol pour la douleur 
         et vous recommander du repos pendant 3 jours.

Patient: D'accord, merci docteur.

Médecin: Pas d'antibiotiques car cela semble viral. 
         Revenez me voir si ça ne s'améliore pas dans 5 jours.
```

Utilisez un outil de synthèse vocale ou enregistrez-vous pour créer le fichier audio.

---

## Résultat attendu

### Entités extraites
- ⚠️ **Allergies**: Pénicilline
- 💊 **Médicaments**: Paracétamol
- 🤒 **Symptômes**: Mal de gorge, Fièvre
- 📏 **Constantes**: Température 38°C

### Compte-rendu SOAP

```
MOTIF DE CONSULTATION
Mal de gorge persistant depuis 7 jours

SUBJECTIF
Patient se plaint de douleurs à la gorge depuis une semaine.
Fièvre à 38°C constatée la veille.
Allergie connue: Pénicilline.

OBJECTIF
Examen ORL: gorge rouge et inflammée.
Température: 38°C.

ANALYSE
Pharyngite subaiguë probablement d'origine virale.

PLAN
- Traitement symptomatique: Paracétamol
- Repos recommandé: 3 jours
- Pas d'antibiothérapie (suspicion virale)
- Réévaluation si pas d'amélioration dans 5 jours

⚠️ ALLERGIES
Pénicilline
```

---

## Dépannage

### Ollama ne démarre pas

```bash
# Démarrer Ollama manuellement
ollama serve

# Dans un autre terminal
ollama list
```

### Modèle Llama2 manquant

```bash
ollama pull llama2
ollama list  # Vérifier
```

### Erreur spaCy

```bash
# Réinstaller les modèles
python -m spacy download fr_core_news_md --force
python -m spacy download en_core_web_sm --force
```

### Erreur Whisper / PyTorch

```bash
# Réinstaller PyTorch
pip install --upgrade torch torchaudio
pip install --upgrade openai-whisper
```

### Port 8501 déjà utilisé

```bash
# Utiliser un autre port
streamlit run hypocrate_app.py --server.port 8502
```

---

## Performance

### Temps de traitement typiques

| Durée audio | Whisper base | SOAP | Total |
|-------------|--------------|------|-------|
| 1 minute | ~10s | ~15s | ~25s |
| 3 minutes | ~30s | ~15s | ~45s |
| 5 minutes | ~50s | ~20s | ~70s |

*Sur MacBook Pro M1, 16GB RAM*

### Optimisations

**GPU disponible:**
- Whisper sera 3-5x plus rapide
- Utilisez `medium` ou `large` pour meilleure qualité

**CPU uniquement:**
- Restez sur `base` ou `small`
- Limitez les audios à 3-5 minutes pour la démo

---

## Prochaines étapes

1. ✅ Testez avec vos propres consultations
2. ✅ Ajustez les paramètres selon vos besoins
3. ✅ Explorez les différentes spécialités
4. ✅ Comparez les modèles Whisper

---

## Support

**Problèmes courants:**
- Vérifiez que Ollama est lancé: `ollama serve`
- Vérifiez les modèles: `ollama list`
- Consultez les logs dans le terminal

**Documentation complète:**
- README.md
- Code source commenté

---

**Hypocrate est prêt! 🏥**

Commencez à transformer vos consultations en documents professionnels en quelques clics.
