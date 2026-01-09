# 🤖 LILLE ADDICT BOT

> Agent conversationnel intelligent pour découvrir Lille - Projet MSI 2028

## 📋 PRÉSENTATION

Ce projet est un chatbot IA intégré à un site web qui recommande des activités, événements, restaurants et bars à Lille. Il utilise :
- **Ollama** (modèle IA local)
- **MCP** (Model Context Protocol) pour les tools
- **Web scraping** de Lille Addict
- **Frontend moderne** en HTML/CSS/JS
- **Backend Python** avec FastAPI

---

## 🎯 FONCTIONNALITÉS

✅ **Événements du week-end** - Découvre ce qu'il se passe à Lille
✅ **Recherche restaurants** - Selon cuisine, régime, prix
✅ **Recherche bars** - Selon boissons, activités, ambiance
✅ **Recommandations météo** - Activités intérieur/extérieur selon le temps
✅ **Interface conversationnelle** - Chatbot intégré au site

---

## 🏗️ ARCHITECTURE

```
Frontend (HTML/CSS/JS)
      ↓
Backend (Python/FastAPI)
      ↓
   Ollama (IA)  +  MCP Server (Tools)
      ↓
Web Scraping (Lille Addict)
```

---

## 📦 STRUCTURE DU PROJET

```
lille-bot-project/
├── frontend/                    # Site web + Chatbot
│   ├── index.html
│   ├── assets/
│   │   ├── css/style.css
│   │   └── js/
│   │       ├── chatbot.js
│   │       └── main.js
│   └── pages/
│
├── backend/                     # API Python
│   ├── main.py
│   ├── services/
│   │   ├── ollama_client.py
│   │   └── mcp_client.py
│   └── requirements.txt
│
├── mcp_server/                  # Serveur MCP (Tools)
│   ├── server.py
│   ├── tools/
│   │   ├── scraping.py
│   │   └── weather.py
│   └── requirements.txt
│
├── CONTEXT_VSCODE_PROJET_IA_BOT.md   # Contexte complet pour VS Code
├── PROJET_IA_BOT_CADRAGE.md          # Document de cadrage
└── README.md                          # Ce fichier
```

---

## 🚀 INSTALLATION

### 1. Prérequis

- **Python 3.10+**
- **Ollama** ([ollama.ai](https://ollama.ai))
- **Git**

### 2. Installation d'Ollama

**Mac/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Télécharge depuis [ollama.ai](https://ollama.ai)

**Télécharger un modèle:**
```bash
ollama pull llama3.2
# ou
ollama pull mistral
```

### 3. Installation du projet

```bash
# Cloner le projet
cd lille-bot-project

# Installer les dépendances backend
cd backend
pip install -r requirements.txt

# Installer les dépendances MCP
cd ../mcp_server
pip install -r requirements.txt
```

---

## ▶️ LANCEMENT

### Démarrer les 4 composants (dans 4 terminaux différents) :

**Terminal 1 - Ollama:**
```bash
ollama serve
```

**Terminal 2 - Serveur MCP:**
```bash
cd mcp_server
python server.py
```
→ Serveur MCP sur http://localhost:8001

**Terminal 3 - Backend API:**
```bash
cd backend
python main.py
```
→ API sur http://localhost:8000
→ Documentation sur http://localhost:8000/docs

**Terminal 4 - Frontend:**
```bash
cd frontend
python -m http.server 3000
```
→ Site web sur http://localhost:3000

---

## 🧪 TESTS

### Tester Ollama
```bash
ollama run llama3.2 "Bonjour, peux-tu te présenter ?"
```

### Tester le serveur MCP
```bash
curl http://localhost:8001/health
# Réponse attendue: {"status":"ok"}
```

### Tester le backend
```bash
curl http://localhost:8000/health
# Réponse attendue: {"status":"ok","ollama":true,"mcp":true}
```

### Tester le chatbot
1. Ouvre http://localhost:3000
2. Clique sur le bouton de chat (en bas à droite)
3. Tape: "Que faire ce week-end à Lille ?"

---

## 📝 UTILISATION

### Exemples de questions:

```
Que faire ce week-end à Lille ?
Restaurant italien végétarien pas cher
Bar à cocktails dans le Vieux-Lille
Que faire s'il pleut ce week-end ?
Activités en extérieur si il fait beau
Où jouer au billard à Lille ?
```

---

## 🛠️ DÉVELOPPEMENT

### Fichiers principaux à modifier:

**Frontend:**
- `frontend/index.html` - Structure de la page
- `frontend/assets/css/style.css` - Styles
- `frontend/assets/js/chatbot.js` - Logique du chatbot

**Backend:**
- `backend/main.py` - Routes API
- `backend/services/ollama_client.py` - Client Ollama
- `backend/services/mcp_client.py` - Client MCP

**MCP Tools:**
- `mcp_server/tools/scraping.py` - Web scraping
- `mcp_server/tools/weather.py` - Météo

### Ajouter un nouveau tool MCP:

1. **Créer le tool** dans `mcp_server/tools/`
2. **L'exposer** dans `mcp_server/server.py`
3. **L'ajouter** dans `backend/services/mcp_client.py` → `get_available_tools()`
4. **Tester** !

---

## 📚 DOCUMENTATION COMPLÈTE

→ **`CONTEXT_VSCODE_PROJET_IA_BOT.md`** - Contexte complet pour coder avec Copilot/Claude
→ **`PROJET_IA_BOT_CADRAGE.md`** - Document de cadrage du projet

Ces fichiers contiennent TOUT le contexte nécessaire pour développer le projet.

---

## 🐛 DÉPANNAGE

### Erreur: "Ollama n'est pas accessible"
```bash
# Vérifie qu'Ollama tourne
ollama serve

# Vérifie que le modèle est téléchargé
ollama list
```

### Erreur: "Le serveur MCP n'est pas accessible"
```bash
# Vérifie que le MCP tourne
curl http://localhost:8001/health

# Relance le serveur MCP
cd mcp_server
python server.py
```

### Le chatbot ne répond pas
1. Vérifie que les 4 composants sont lancés
2. Ouvre la console du navigateur (F12) pour voir les erreurs
3. Vérifie les logs du backend

### Erreur de scraping
- Vérifie ta connexion internet
- Le site Lille Addict peut être temporairement indisponible

---

## 📖 RESSOURCES

- **Ollama:** https://ollama.ai/
- **FastAPI:** https://fastapi.tiangolo.com/
- **Lille Addict:** https://lilleaddict.fr/

---

## 🎓 PROJET PÉDAGOGIQUE

Ce projet est développé dans le cadre du Master MSI 2028.

**Objectif:** Comprendre les architectures d'agents conversationnels modernes avec:
- IA locale (Ollama)
- Model Context Protocol (MCP)
- Web scraping éthique
- API RESTful
- Frontend interactif

---

## ⚖️ LÉGAL

**Usage pédagogique uniquement.**
Les données sont scrap pées depuis Lille Addict à des fins éducatives.
Respecte les conditions d'utilisation du site source.

---

## 🚦 NEXT STEPS

Une fois le projet fonctionnel:

1. ✅ Tester tous les use cases
2. 📸 Faire des screenshots
3. 📄 Préparer la documentation technique
4. 🎤 Préparer la soutenance (20 min)
5. 🎉 Profiter !

---

**Besoin d'aide ?** Charge `CONTEXT_VSCODE_PROJET_IA_BOT.md` dans VS Code et demande à Copilot/Claude ! 🤖
