# 🤝 Guide de Contribution - Medical Scribe AI

Merci de votre intérêt pour contribuer à **Medical Scribe AI**! Ce document vous guidera à travers le processus de contribution.

---

## 📋 Table des Matières

- [Code of Conduct](#code-of-conduct)
- [Comment Contribuer](#comment-contribuer)
- [Standards de Code](#standards-de-code)
- [Process de Pull Request](#process-de-pull-request)
- [Signaler des Bugs](#signaler-des-bugs)
- [Proposer des Fonctionnalités](#proposer-des-fonctionnalités)
- [Configuration Développement](#configuration-développement)

---

## 📜 Code of Conduct

### Notre Engagement

Nous nous engageons à faire de la participation à ce projet une expérience sans harcèlement pour tous, indépendamment de:
- L'âge
- La taille corporelle
- Le handicap
- L'ethnicité
- L'identité et l'expression de genre
- Le niveau d'expérience
- La nationalité
- L'apparence personnelle
- La race
- La religion
- L'identité et l'orientation sexuelles

### Nos Standards

**Comportements encouragés:**
- Utiliser un langage accueillant et inclusif
- Respecter les points de vue et expériences différents
- Accepter gracieusement les critiques constructives
- Se concentrer sur ce qui est meilleur pour la communauté
- Faire preuve d'empathie envers les autres membres

**Comportements inacceptables:**
- Langage ou images sexualisés
- Trolling, commentaires insultants/désobligeants
- Harcèlement public ou privé
- Publication d'informations privées sans permission
- Autre conduite inappropriée dans un cadre professionnel

---

## 🚀 Comment Contribuer

### Types de Contributions

Nous acceptons plusieurs types de contributions:

1. **🐛 Corrections de bugs**
2. **✨ Nouvelles fonctionnalités**
3. **📝 Amélioration documentation**
4. **🧪 Tests**
5. **🎨 Améliorations UI/UX**
6. **⚡ Optimisations performance**
7. **🌍 Traductions**

### Workflow de Contribution

1. **Fork** le repository
2. **Clone** votre fork localement
3. **Créer** une branche pour votre contribution
4. **Développer** votre contribution
5. **Tester** vos changements
6. **Commit** avec des messages clairs
7. **Push** vers votre fork
8. **Créer** une Pull Request

---

## 💻 Standards de Code

### Python

**Style:**
- Suivre [PEP 8](https://pep8.org/)
- Utiliser [Black](https://black.readthedocs.io/) pour le formatage
- Maximum 88 caractères par ligne

**Type Hints:**
```python
def transcribe_audio(
    audio_path: str,
    language: str = "fr",
    model_size: str = "base"
) -> Dict[str, Any]:
    """
    Transcrit un fichier audio.
    
    Args:
        audio_path: Chemin vers le fichier audio
        language: Code langue (fr, en, etc.)
        model_size: Taille du modèle Whisper
        
    Returns:
        Dict avec transcription et métadonnées
    """
    pass
```

**Docstrings:**
- Format Google style
- Documenter tous les paramètres
- Inclure exemples si pertinent

**Imports:**
```python
# Standard library
import os
import sys
from pathlib import Path

# Third party
import numpy as np
from fastapi import FastAPI

# Local
from .models import User
from .services import transcription
```

### Tests

**Obligatoire pour:**
- Nouvelles fonctionnalités
- Corrections de bugs
- Modifications API

**Framework:**
```python
import pytest
from fastapi.testclient import TestClient

def test_transcription_service():
    """Test du service de transcription"""
    service = get_transcription_service()
    result = service.transcribe_audio("test.wav")
    
    assert result["text"] is not None
    assert result["duration_seconds"] > 0
```

**Couverture:**
- Minimum 80% pour nouveau code
- Utiliser `pytest-cov`

### Commits

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

**Exemples:**
```bash
feat(transcription): add support for M4A format

- Add M4A to supported formats
- Update file validation
- Add tests for M4A files

Closes #123

fix(api): correct JWT token expiration

The token was expiring too quickly due to incorrect
calculation of expiration time.

Fixes #456
```

---

## 🔄 Process de Pull Request

### Avant de Soumettre

**Checklist:**
- [ ] Code suit les standards
- [ ] Tests ajoutés/mis à jour
- [ ] Tests passent localement
- [ ] Documentation mise à jour
- [ ] Pas de conflits avec main
- [ ] Commits bien formatés

### Soumettre la PR

1. **Titre clair:**
   ```
   feat: Add PDF export for SOAP notes
   ```

2. **Description détaillée:**
   ```markdown
   ## Description
   Ajoute la fonctionnalité d'export PDF pour les comptes-rendus SOAP.
   
   ## Changements
   - Nouveau service `pdf_generator.py`
   - Endpoint `/api/notes/{id}/export/pdf`
   - Tests unitaires
   - Documentation mise à jour
   
   ## Tests
   - [x] Tests unitaires passent
   - [x] Tests d'intégration passent
   - [x] Testé manuellement
   
   ## Screenshots
   [Si applicable]
   
   ## Closes
   #123
   ```

3. **Labels:**
   - `bug` - Correction de bug
   - `enhancement` - Amélioration
   - `documentation` - Documentation
   - `good first issue` - Bon pour débutants
   - `help wanted` - Aide recherchée

### Review Process

1. **Automated checks** doivent passer
2. **Review** par au moins 1 mainteneur
3. **Changements** si demandés
4. **Merge** par mainteneur

---

## 🐛 Signaler des Bugs

### Avant de Signaler

1. **Vérifier** les issues existantes
2. **Reproduire** le bug
3. **Collecter** informations système

### Template Bug Report

```markdown
## Description
[Description claire du bug]

## Reproduction
1. Aller à '...'
2. Cliquer sur '...'
3. Voir l'erreur

## Comportement Attendu
[Ce qui devrait se passer]

## Comportement Actuel
[Ce qui se passe réellement]

## Screenshots
[Si applicable]

## Environnement
- OS: [e.g. macOS 14.0]
- Python: [e.g. 3.10.5]
- Version: [e.g. 1.0.0]

## Logs
```
[Coller les logs pertinents]
```

## Informations Additionnelles
[Tout autre contexte utile]
```

---

## ✨ Proposer des Fonctionnalités

### Template Feature Request

```markdown
## Problème
[Quel problème cette fonctionnalité résout-elle?]

## Solution Proposée
[Description de la solution]

## Alternatives Considérées
[Autres approches envisagées]

## Bénéfices
- Bénéfice 1
- Bénéfice 2

## Complexité Estimée
[Low / Medium / High]

## Informations Additionnelles
[Contexte, exemples, mockups]
```

---

## 🛠️ Configuration Développement

### Setup Initial

```bash
# Fork et clone
git clone https://github.com/VOTRE_USERNAME/scribemed.git
cd scribemed

# Créer environnement virtuel
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Installer dépendances dev
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Installer pre-commit hooks
pre-commit install
```

### Requirements Dev

Créer `requirements-dev.txt`:
```
# Testing
pytest==7.4.3
pytest-cov==4.1.0
pytest-asyncio==0.21.1
httpx==0.25.1

# Code Quality
black==23.11.0
flake8==6.1.0
mypy==1.7.0
pylint==3.0.2

# Pre-commit
pre-commit==3.5.0
```

### Pre-commit Hooks

Créer `.pre-commit-config.yaml`:
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.11.0
    hooks:
      - id: black
        language_version: python3.10

  - repo: https://github.com/pycqa/flake8
    rev: 6.1.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.7.0
    hooks:
      - id: mypy
```

### Lancer les Tests

```bash
# Tous les tests
pytest

# Avec couverture
pytest --cov=backend/app --cov-report=html

# Tests spécifiques
pytest tests/test_transcription.py

# Mode verbose
pytest -v
```

### Lancer les Linters

```bash
# Black (formatage)
black backend/app

# Flake8 (style)
flake8 backend/app

# MyPy (types)
mypy backend/app

# Pylint (qualité)
pylint backend/app
```

---

## 📁 Structure du Projet

```
scribemed/
├── medical-scribe/
│   ├── backend/
│   │   └── app/
│   │       ├── __init__.py
│   │       ├── main.py
│   │       ├── config.py
│   │       ├── database.py
│   │       ├── models/
│   │       ├── routers/
│   │       ├── services/
│   │       ├── schemas/
│   │       └── utils/
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py
│   │   └── test_*.py
│   └── uploads/
│
├── hypocrate/
│   ├── hypocrate_app.py
│   ├── config/
│   ├── services/
│   └── tests/
│
├── docs/
├── .github/
│   ├── workflows/
│   └── ISSUE_TEMPLATE/
├── .gitignore
├── LICENSE
├── README.md
└── CONTRIBUTING.md
```

---

## 🎯 Priorités de Contribution

### High Priority

- [ ] Tests automatisés complets
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] Export PDF/DOCX

### Medium Priority

- [ ] Fine-tuning Llama2 médical FR
- [ ] NER médical français avancé
- [ ] Enregistrement direct micro
- [ ] Templates personnalisables

### Low Priority

- [ ] Traductions (EN, ES, DE)
- [ ] Thèmes UI
- [ ] Plugins système

---

## 📞 Contact

### Questions

- **Issues:** [GitHub Issues](https://github.com/xaviercallens/scribemed/issues)
- **Discussions:** [GitHub Discussions](https://github.com/xaviercallens/scribemed/discussions)

### Mainteneurs

- **Xavier Callens** - [@xaviercallens](https://github.com/xaviercallens)

---

## 🙏 Remerciements

Merci à tous les contributeurs qui aident à améliorer Medical Scribe AI!

### Contributors

<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- Sera rempli automatiquement -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

<div align="center">

**Merci de contribuer à Medical Scribe AI!** 🏥

*Ensemble, améliorons la documentation médicale* ✨

</div>
