# 🏥 Hypocrate - Assistant Médical IA

## 🎉 STATUS : OPÉRATIONNEL ✅

**L'application est prête pour les tests utilisateur !**

**Accès immédiat :** http://localhost:8501

👉 **[COMMENCEZ ICI - START_HERE.md](START_HERE.md)** 👈

## 📋 Vue d'ensemble

**Hypocrate** est un assistant médical intelligent 100% local qui transforme les consultations médicales en documents cliniques structurés.

### ✨ Fonctionnalités principales

- 🎤 **Transcription automatique** des consultations (Whisper local)
- 🔍 **Extraction d'entités médicales** (symptômes, diagnostics, médicaments, allergies)
- 📝 **Génération de comptes-rendus SOAP** structurés
- 📧 **Création de lettres d'adressage** professionnelles
- ⚠️ **Alertes de sécurité** (conflits allergies/médicaments)
- 🔒 **100% local** - Aucune donnée ne quitte votre machine

---

## 🚀 Installation rapide

### Prérequis

- Python 3.10+
- Ollama installé avec Llama2
- 8GB RAM minimum (16GB recommandé)

### Installation

```bash
# 1. Installer les dépendances
pip install -r requirements_hypocrate.txt

# 2. Télécharger les modèles spaCy
python -m spacy download fr_core_news_md
python -m spacy download en_core_web_sm

# 3. Installer scispaCy pour NER médical
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz

# 4. Vérifier Ollama
ollama list  # Doit afficher llama2:latest
```

---

## 🎯 Lancement

```bash
# Démarrer l'interface Hypocrate
streamlit run hypocrate_app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## 💻 Utilisation

### 1. Enregistrement audio

- Cliquez sur **"Enregistrer"** pour capturer la consultation
- Ou uploadez un fichier audio (WAV, MP3, M4A)

### 2. Configuration

- **Langue**: Français (par défaut) ou Anglais
- **Spécialité**: Généraliste, Cardiologue, ORL, etc.
- **Format**: SOAP structuré ou texte libre

### 3. Traitement automatique

L'IA traite automatiquement:
1. Transcription de l'audio
2. Extraction des entités médicales
3. Génération du compte-rendu SOAP
4. Création de la lettre d'adressage

### 4. Résultats

Consultez:
- 📄 Transcription complète
- 🏷️ Entités médicales extraites
- 📋 Compte-rendu SOAP
- 📧 Lettre d'adressage
- ⚠️ Alertes de sécurité

---

## 🏗️ Architecture

```
hypocrate/
├── hypocrate_app.py          # Interface Streamlit principale
├── services/
│   ├── transcription.py      # Service Whisper local
│   ├── ner_medical.py        # Extraction entités médicales
│   ├── soap_generator.py     # Génération SOAP avec Llama2
│   └── letter_generator.py   # Génération lettres
├── utils/
│   ├── audio_utils.py        # Traitement audio
│   └── validators.py         # Validation et alertes
└── config/
    └── prompts.py            # Prompts pour LLM
```

---

## 🔧 Technologies utilisées

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **STT** | Whisper (local) | Transcription vocale |
| **NER** | scispaCy | Extraction entités médicales |
| **LLM** | Llama2 via Ollama | Génération texte |
| **UI** | Streamlit | Interface utilisateur |
| **Audio** | sounddevice, pydub | Traitement audio |

---

## 📊 Exemple de sortie

### Compte-rendu SOAP

```
SUBJECTIF
Patient de 35 ans présentant un mal de gorge depuis 7 jours.
Allergie connue: Pénicilline.

OBJECTIF
Examen ORL: gorge rouge, pas d'enduit purulent.
Température: 38°C.

ANALYSE
Pharyngite subaiguë probablement virale.

PLAN
- Traitement symptomatique (paracétamol)
- Repos 3 jours
- Pas d'antibiothérapie (origine virale probable)
```

### Entités extraites

- 💊 **Médicaments**: Paracétamol
- ⚠️ **Allergies**: Pénicilline
- 🤒 **Symptômes**: Mal de gorge, Fièvre
- 🏷️ **Diagnostic**: Pharyngite virale

---

## ⚠️ Limitations (PoC)

- Optimisé pour médecine générale adulte
- Latence variable selon matériel (GPU recommandé)
- Whisper peut faire des erreurs sur termes rares
- LLM peut nécessiter validation humaine

---

## 🔐 Confidentialité & RGPD

✅ **Traitement 100% local**
✅ **Aucune donnée envoyée à des serveurs externes**
✅ **Conforme RGPD**
✅ **Secret médical préservé**

---

## 🚀 Évolutions futures

- [ ] Intégration SIH/DPI (HL7 FHIR)
- [ ] Fine-tuning sur données médicales françaises
- [ ] Support multilingue étendu
- [ ] Spécialisation par discipline
- [ ] Export PDF/DOCX
- [ ] Certification dispositif médical

---

## 📝 Licence

Ce projet est un PoC de démonstration utilisant des technologies open source.

---

## 🤝 Support

Pour toute question ou problème:
- Consultez la documentation complète
- Vérifiez que Ollama est bien lancé: `ollama serve`
- Vérifiez les modèles: `ollama list`

---

**Hypocrate** - L'assistant médical qui vous redonne du temps pour vos patients 🏥
