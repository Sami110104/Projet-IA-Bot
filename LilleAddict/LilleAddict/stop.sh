#!/bin/bash

# 🛑 Script d'arrêt Lille Addict Bot

echo "🛑 Arrêt de Lille Addict Bot..."
echo ""

if [ -f ".pids" ]; then
    while read pid; do
        if ps -p $pid > /dev/null 2>&1; then
            kill $pid 2> /dev/null
            echo "✅ Processus $pid arrêté"
        fi
    done < .pids
    rm .pids
    echo ""
    echo "✅ Tous les composants sont arrêtés"
else
    echo "ℹ️  Aucun processus actif trouvé"
fi

# Nettoyer les processus orphelins
pkill -f "ollama serve" 2> /dev/null
pkill -f "uvicorn" 2> /dev/null
pkill -f "http.server 3000" 2> /dev/null

echo ""
echo "🎉 Nettoyage terminé"
