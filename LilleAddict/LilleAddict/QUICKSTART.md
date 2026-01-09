# ⚡ QUICK START GUIDE

## 🎯 Démarrage en 5 minutes

### 1. Installation Ollama (1 min)

**Mac/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2
```

**Windows:**
Télécharge depuis [ollama.ai](https://ollama.ai)

### 2. Installation projet (1 min)

```bash
cd lille-bot-project

# Backend
cd backend
pip install -r requirements.txt

# MCP
cd ../mcp_server
pip install -r requirements.txt
```

### 3. Lancement (1 min)

**Ouvre 4 terminaux:**

```bash
# Terminal 1
ollama serve

# Terminal 2
cd mcp_server && python server.py

# Terminal 3
cd backend && python main.py

# Terminal 4
cd frontend && python -m http.server 3000
```

### 4. Test (1 min)

→ Ouvre http://localhost:3000
→ Clique sur le bouton chat
→ Tape: "Que faire ce week-end à Lille ?"

---

## 🐛 Si ça ne marche pas

### Ollama ne démarre pas ?
```bash
# Vérifie l'installation
ollama list

# Teste un modèle
ollama run llama3.2 "Hello"
```

### Le backend ne se lance pas ?
```bash
# Vérifie les dépendances
pip list | grep fastapi

# Réinstalle
pip install -r requirements.txt
```

### Le chatbot ne répond pas ?
1. Ouvre la console (F12)
2. Vérifie qu'il n'y a pas d'erreur
3. Vérifie que les 4 serveurs tournent

---

## 📝 Prochaines étapes

1. ✅ Lis le `README.md` complet
2. ✅ Charge `CONTEXT_VSCODE_PROJET_IA_BOT.md` dans VS Code
3. ✅ Commence à coder avec Copilot/Claude !

---

**Tout fonctionne ?** → Profite ! 🎉
**Des questions ?** → Consulte la doc complète !
