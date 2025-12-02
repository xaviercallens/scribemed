#!/bin/bash
# Script de correction des dépendances Hypocrate

echo "🔧 Correction des dépendances Hypocrate"
echo "========================================"
echo ""

# Détecter le Python utilisé par Streamlit
STREAMLIT_PATH=$(which streamlit)
if [ -z "$STREAMLIT_PATH" ]; then
    echo "❌ Streamlit n'est pas installé"
    exit 1
fi

echo "📍 Streamlit trouvé : $STREAMLIT_PATH"

# Extraire le shebang pour trouver le Python
PYTHON_PATH=$(head -1 $STREAMLIT_PATH | sed 's/#!//')
echo "🐍 Python utilisé par Streamlit : $PYTHON_PATH"
echo ""

# Vérifier que le Python existe
if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ Python non trouvé : $PYTHON_PATH"
    exit 1
fi

# Installer les dépendances
echo "📦 Installation des dépendances..."
echo ""

echo "1️⃣ Installation openai-whisper..."
$PYTHON_PATH -m pip install openai-whisper

echo ""
echo "2️⃣ Installation torch et torchaudio..."
$PYTHON_PATH -m pip install torch torchaudio

echo ""
echo "3️⃣ Installation spacy..."
$PYTHON_PATH -m pip install spacy

echo ""
echo "4️⃣ Installation des autres dépendances..."
$PYTHON_PATH -m pip install -r requirements_hypocrate.txt

echo ""
echo "5️⃣ Téléchargement modèles spaCy..."
$PYTHON_PATH -m spacy download fr_core_news_md 2>/dev/null || \
    $PYTHON_PATH -m pip install https://github.com/explosion/spacy-models/releases/download/fr_core_news_md-3.7.0/fr_core_news_md-3.7.0-py3-none-any.whl

$PYTHON_PATH -m spacy download en_core_web_sm 2>/dev/null || \
    $PYTHON_PATH -m pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl

echo ""
echo "6️⃣ Installation scispaCy..."
$PYTHON_PATH -m pip install scispacy
$PYTHON_PATH -m pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.0/en_ner_bc5cdr_md-0.5.0.tar.gz 2>/dev/null || echo "⚠️  scispaCy médical optionnel non installé"

echo ""
echo "✅ Installation terminée !"
echo ""
echo "🧪 Vérification des modules..."
$PYTHON_PATH -c "import whisper; print('✅ whisper OK')" 2>/dev/null || echo "❌ whisper manquant"
$PYTHON_PATH -c "import torch; print('✅ torch OK')" 2>/dev/null || echo "❌ torch manquant"
$PYTHON_PATH -c "import spacy; print('✅ spacy OK')" 2>/dev/null || echo "❌ spacy manquant"
$PYTHON_PATH -c "import streamlit; print('✅ streamlit OK')" 2>/dev/null || echo "❌ streamlit manquant"

echo ""
echo "🚀 Vous pouvez maintenant lancer : streamlit run hypocrate_app.py"
