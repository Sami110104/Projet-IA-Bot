#!/bin/bash

# 🚀 Script de lancement Lille Addict Bot
# Lance automatiquement les 4 composants dans des terminaux séparés

echo "🚀 Lancement de Lille Addict Bot..."
echo ""

# Vérifier qu'Ollama est installé
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama n'est pas installé !"
    echo "   Installe-le depuis https://ollama.ai"
    exit 1
fi

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé !"
    exit 1
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
cd backend
if [ ! -d "venv" ]; then
    echo "   Création de l'environnement virtuel..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi
cd ..

cd mcp_server
if [ ! -d "venv" ]; then
    echo "   Installation des dépendances MCP..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi
cd ..

echo ""
echo "✅ Dépendances OK"
echo ""
echo "🚀 Lancement des composants..."
echo ""

# Lancer Ollama
echo "1️⃣  Lancement d'Ollama..."
ollama serve > /dev/null 2>&1 &
OLLAMA_PID=$!
sleep 2

# Lancer MCP Server
echo "2️⃣  Lancement du serveur MCP..."
cd mcp_server
source venv/bin/activate
python server.py > /dev/null 2>&1 &
MCP_PID=$!
cd ..
sleep 2

# Lancer Backend
echo "3️⃣  Lancement du backend..."
cd backend
source venv/bin/activate
python main.py > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..
sleep 2

# Lancer Frontend
echo "4️⃣  Lancement du frontend..."
cd frontend
python3 -m http.server 3000 > /dev/null 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "✅ Tous les composants sont lancés !"
echo ""
echo "📡 URLs :"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   MCP:       http://localhost:8001"
echo "   Docs API:  http://localhost:8000/docs"
echo ""
echo "💬 Ouvre http://localhost:3000 dans ton navigateur"
echo ""
echo "🛑 Pour arrêter: Ctrl+C puis lance ./stop.sh"
echo ""

# Enregistrer les PIDs
echo "$OLLAMA_PID" > .pids
echo "$MCP_PID" >> .pids
echo "$BACKEND_PID" >> .pids
echo "$FRONTEND_PID" >> .pids

# Attendre
wait
