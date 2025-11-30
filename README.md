# 🏥 Medical Scribe AI - ScribeMed

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29+-red.svg)](https://streamlit.io/)

> **Assistant médical IA 100% local** - Transformez vos consultations en documents cliniques professionnels sans coût API

---

## 🎯 Vue d'Ensemble

**Medical Scribe AI** est une solution complète d'assistance médicale basée sur l'IA qui fonctionne **entièrement en local** sur votre machine. Aucune donnée ne quitte votre ordinateur, garantissant une **confidentialité totale** et une **conformité RGPD**.

### ✨ Deux Applications Complémentaires

| 🔧 **Medical Scribe API** | 🎨 **Hypocrate** |
|---------------------------|------------------|
| API REST FastAPI | Application Streamlit |
| Backend robuste | Interface utilisateur |
| Multi-utilisateurs | Mono-utilisateur |
| Authentification JWT | Utilisation directe |
| Base de données SQLite | Sans stockage |
| Pour développeurs | Pour médecins |

---

## 🚀 Démarrage Rapide

### Prérequis

```bash
# Python 3.10+
python3 --version

# Ollama avec Llama2
brew install ollama  # macOS
ollama pull llama2
```

### Installation

```bash
# Cloner le repository
git clone https://github.com/xaviercallens/scribemed.git
cd scribemed

# Option 1: Medical Scribe API
cd medical-scribe
pip install -r requirements.txt
./setup_env.sh
./start_server.sh
# Accès: http://localhost:8001/docs

# Option 2: Hypocrate
cd hypocrate
pip install -r requirements_hypocrate.txt
python -m spacy download fr_core_news_md
./start_hypocrate.sh
# Accès: http://localhost:8501
```

---

## 📋 Fonctionnalités

### Medical Scribe API (Backend)

- ✅ **API REST complète** (11 endpoints)
- ✅ **Authentification JWT** sécurisée
- ✅ **Upload audio** multi-formats
- ✅ **Transcription Whisper** locale
- ✅ **Génération notes** avec Llama2
- ✅ **Base de données** SQLite
- ✅ **Documentation** Swagger/ReDoc

### Hypocrate (Interface Utilisateur)

- ✅ **Interface Streamlit** intuitive
- ✅ **Transcription automatique**
- ✅ **Extraction entités** médicales (NER)
- ✅ **Comptes-rendus SOAP** structurés
- ✅ **Lettres d'adressage** professionnelles
- ✅ **Alertes de sécurité** (allergies/médicaments)
- ✅ **Visualisation** enrichie

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│         MEDICAL SCRIBE AI                   │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐    ┌──────────────┐     │
│  │ Medical      │    │  Hypocrate   │     │
│  │ Scribe API   │    │  Application │     │
│  │ (FastAPI)    │    │ (Streamlit)  │     │
│  └──────┬───────┘    └──────┬───────┘     │
│         │                   │              │
│  ┌──────▼───────────────────▼──────┐      │
│  │   Services Locaux (100%)        │      │
│  ├─────────────────────────────────┤      │
│  │  • Whisper (Transcription)      │      │
│  │  • Llama2 (Génération)          │      │
│  │  • scispaCy (NER médical)       │      │
│  └─────────────────────────────────┘      │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 💡 Cas d'Usage

### Medical Scribe API

**Pour qui:** Développeurs, intégrateurs système

**Utilisation:**
- Intégration avec DPI/SIH existant
- Application mobile/web custom
- Multi-utilisateurs avec authentification
- Stockage persistant des consultations

**Exemple:**
```bash
# Authentification
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"doctor@clinic.com","password":"pass123"}'

# Upload et transcription
curl -X POST http://localhost:8001/api/recordings/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@consultation.wav"
```

### Hypocrate

**Pour qui:** Médecins, professionnels de santé

**Utilisation:**
- Utilisation directe sans configuration
- Interface visuelle intuitive
- Génération rapide de documents
- Démonstration et prototypage

**Workflow:**
1. Uploader fichier audio
2. Cliquer "Analyser"
3. Voir résultats visuels
4. Copier compte-rendu/lettre

---

## 🔒 Sécurité & Confidentialité

### ✅ Garanties

- **100% Local** - Aucune donnée externe
- **Conforme RGPD** - Contrôle total
- **Secret médical** - Pas de tiers
- **Zéro coût API** - Gratuit

### 🔐 Medical Scribe API

- Authentification JWT
- Passwords hashés (bcrypt)
- Isolation utilisateurs
- Base de données locale

---

## 💰 Économies

### vs OpenAI API (1000 notes/mois)

| Service | OpenAI | ScribeMed | Économie |
|---------|--------|-----------|----------|
| Transcription | $360 | $0 | $360 |
| Génération | $1,200 | $0 | $1,200 |
| **Total/mois** | **$1,560** | **$0** | **$1,560** |
| **Total/an** | **$18,720** | **$0** | **$18,720** |

---

## 📊 Performance

### Temps de Traitement (MacBook Pro M1, 16GB)

| Durée audio | Transcription | Génération | Total |
|-------------|---------------|------------|-------|
| 1 minute | ~10s | ~15s | ~25s |
| 3 minutes | ~30s | ~15s | ~45s |
| 5 minutes | ~50s | ~20s | ~70s |

**Optimisations:**
- GPU (CUDA/MPS): 3-5x plus rapide
- Modèles ajustables selon besoins

---

## 📚 Documentation

### Guides Principaux

- 📖 [Documentation Complète](./PROJET_COMPLET.md)
- 🚀 [Quick Start API](./medical-scribe/QUICKSTART.md)
- 🎨 [Quick Start Hypocrate](./hypocrate/QUICKSTART_HYPOCRATE.md)
- 📝 [Guide Day 1](./DAY1_COMPLETE.md)
- 🏥 [Guide Day 2](./DAY2_HYPOCRATE_COMPLETE.md)

### Documentation Technique

- [Configuration LLM Local](./medical-scribe/LOCAL_LLM_GUIDE.md)
- [Configuration Ports](./medical-scribe/PORT_CONFIGURATION.md)
- [Guide Tests](./medical-scribe/USER_TEST_GUIDE.md)
- [Résultats Tests](./medical-scribe/TEST_RESULTS.md)

---

## 🛠️ Technologies

### Backend
- **FastAPI** - Framework web moderne
- **SQLAlchemy** - ORM
- **Pydantic** - Validation données
- **JWT** - Authentification
- **bcrypt** - Hashage passwords

### IA/ML (100% Local)
- **Whisper** - Transcription audio
- **Llama2** via Ollama - Génération texte
- **scispaCy** - NER médical
- **spaCy** - NLP

### Frontend
- **Streamlit** - Interface utilisateur
- **sounddevice** - Capture audio
- **pydub** - Traitement audio

---

## 📁 Structure du Projet

```
scribemed/
├── medical-scribe/          # API Backend (Day 1)
│   ├── backend/
│   │   └── app/
│   │       ├── main.py
│   │       ├── models/
│   │       ├── routers/
│   │       ├── services/
│   │       └── utils/
│   ├── uploads/
│   ├── requirements.txt
│   └── start_server.sh
│
├── hypocrate/              # Application UI (Day 2)
│   ├── hypocrate_app.py
│   ├── config/
│   ├── services/
│   ├── requirements_hypocrate.txt
│   └── start_hypocrate.sh
│
└── docs/                   # Documentation
    ├── WINDSURF_2DAY_GUIDE.md
    └── ...
```

---

## 🚦 Roadmap

### ✅ Complété (v1.0)

- [x] API REST complète
- [x] Authentification JWT
- [x] Transcription Whisper locale
- [x] Génération SOAP avec Llama2
- [x] Interface Streamlit
- [x] NER médical
- [x] Lettres d'adressage
- [x] Documentation complète

### 🔄 En Cours

- [ ] Tests automatisés complets
- [ ] Docker containerization
- [ ] CI/CD pipeline

### 📅 Futur

- [ ] Export PDF/DOCX
- [ ] Enregistrement direct micro
- [ ] Fine-tuning Llama2 médical FR
- [ ] Intégration HL7 FHIR
- [ ] Mobile apps (iOS/Android)
- [ ] Certification dispositif médical

---

## 🤝 Contribution

Les contributions sont les bienvenues! Voici comment contribuer:

1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

### Standards

- Python 3.10+
- Type hints
- Docstrings
- Tests unitaires
- Code commenté

---

## 📝 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## 👨‍💻 Auteur

**Xavier Callens**

- GitHub: [@xaviercallens](https://github.com/xaviercallens)
- Repository: [scribemed](https://github.com/xaviercallens/scribemed)

---

## 🙏 Remerciements

### Technologies Open Source

- [OpenAI Whisper](https://github.com/openai/whisper) - Transcription
- [Ollama](https://ollama.ai/) - LLM local
- [Meta Llama2](https://ai.meta.com/llama/) - Modèle de langage
- [scispaCy](https://allenai.github.io/scispacy/) - NER médical
- [FastAPI](https://fastapi.tiangolo.com/) - Framework web
- [Streamlit](https://streamlit.io/) - Interface utilisateur

---

## ⚠️ Avertissement

**Cet outil est une aide à la décision médicale.**

- Le médecin reste **responsable** de la validation finale
- Les documents générés doivent être **vérifiés**
- Ne remplace pas le **jugement clinique**
- Respecter les **réglementations locales**

---

## 📞 Support

### Problèmes Courants

**Ollama:**
```bash
ollama serve
ollama list
ollama pull llama2
```

**Python:**
```bash
python3 --version  # 3.10+
pip install --upgrade pip
```

**Ports:**
```bash
lsof -ti:8001 | xargs kill -9  # API
lsof -ti:8501 | xargs kill -9  # Hypocrate
```

### Issues

Pour signaler un bug ou demander une fonctionnalité:
- Ouvrir une [issue](https://github.com/xaviercallens/scribemed/issues)
- Décrire le problème en détail
- Inclure logs et configuration

---

## 🌟 Star History

Si ce projet vous est utile, n'hésitez pas à lui donner une ⭐️!

---

<div align="center">

**Medical Scribe AI - ScribeMed**

*L'assistant médical qui vous redonne du temps pour vos patients* 🏥

[Documentation](./PROJET_COMPLET.md) • [Quick Start](./medical-scribe/QUICKSTART.md) • [Issues](https://github.com/xaviercallens/scribemed/issues)

</div>
