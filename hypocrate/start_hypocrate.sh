#!/bin/bash
# Script de lancement Hypocrate

echo "🏥 Démarrage Hypocrate - Assistant Médical IA"
echo "=============================================="
echo ""

# Vérification Ollama
echo "🔍 Vérification Ollama..."
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama n'est pas installé"
    echo "💡 Installation: brew install ollama (macOS) ou https://ollama.ai"
    exit 1
fi

# Vérification modèle Llama2
echo "🔍 Vérification modèle Llama2..."
if ! ollama list | grep -q "llama2"; then
    echo "⚠️  Modèle llama2 non trouvé"
    echo "📥 Téléchargement du modèle (cela peut prendre quelques minutes)..."
    ollama pull llama2
fi

# Vérification Python
echo "🔍 Vérification Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé"
    exit 1
fi

# Vérification dépendances
echo "🔍 Vérification des dépendances..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Dépendances manquantes"
    echo "📦 Installation des dépendances..."
    pip install -r requirements_hypocrate.txt
fi

# Vérification modèles spaCy
echo "🔍 Vérification modèles spaCy..."
if ! python3 -c "import spacy; spacy.load('fr_core_news_md')" 2>/dev/null; then
    echo "📥 Téléchargement modèle spaCy français..."
    python3 -m spacy download fr_core_news_md
fi

if ! python3 -c "import spacy; spacy.load('en_core_web_sm')" 2>/dev/null; then
    echo "📥 Téléchargement modèle spaCy anglais..."
    python3 -m spacy download en_core_web_sm
fi

echo ""
echo "✅ Tous les prérequis sont satisfaits"
echo ""
echo "🚀 Lancement de l'interface Hypocrate..."
echo "📍 L'application s'ouvrira dans votre navigateur"
echo ""
echo "⚠️  Pour arrêter: Ctrl+C"
echo ""

# Lancement Streamlit
streamlit run hypocrate_app.py
