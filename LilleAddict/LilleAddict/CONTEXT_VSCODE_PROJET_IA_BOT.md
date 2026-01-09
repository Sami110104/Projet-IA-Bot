# 🤖 PROJET IA BOT - LILLE ADDICT
## Fichier de contexte pour VS Code / GitHub Copilot / Claude

> **Instructions :** Charge ce fichier dans ton IDE pour donner le contexte complet du projet à ton assistant IA.

---

## 📋 CONTEXTE GÉNÉRAL DU PROJET

### Objectif
Créer un agent conversationnel intelligent intégré à un site web qui scrape les données de Lille Addict (https://lilleaddict.fr/) pour recommander des activités, restaurants, bars et événements à Lille.

### Stack technique imposée
- **Frontend :** JavaScript (React / Vue.js / Vanilla JS au choix)
- **Backend :** Python (Flask ou FastAPI)
- **Model IA :** Ollama (modèle local open-source)
- **MCP Server :** Python (pour le tooling et scraping)
- **Scraping :** BeautifulSoup4 + Requests

### Architecture globale
```
┌──────────────────────────────────────────────────┐
│              SITE VITRINE (Frontend)             │
│         Interface web + Chatbot intégré          │
│              (HTML/CSS/JavaScript)               │
└────────────────┬─────────────────────────────────┘
                 │ HTTP/WebSocket
                 ▼
┌──────────────────────────────────────────────────┐
│            BACKEND PYTHON (Orchestrateur)        │
│      Flask/FastAPI + Client Ollama + MCP        │
└─────┬────────────────────────┬───────────────────┘
      │                        │
      │                        ▼
      │               ┌─────────────────┐
      │               │   MCP SERVER    │
      │               │   (Python)      │
      │               │                 │
      │               │  Tools exposés: │
      │               │  • Scraping     │
      │               │  • Parsing      │
      │               │  • Météo        │
      │               └─────────────────┘
      │
      ▼
┌──────────────────────────────────────────────────┐
│              MODÈLE IA LOCAL (Ollama)            │
│       Compréhension NLP + Décision Tools         │
└──────────────────────────────────────────────────┘
```

---

## 🎯 USE CASES DÉTAILLÉS

### USE CASE 1 : Événements du week-end (MVP)
**User Story :** "En tant qu'utilisateur, je veux savoir quoi faire ce week-end à Lille"

**Exemple de conversation :**
```
User: Que faire ce week-end à Lille ?

Bot: Cette semaine à Lille, j'ai repéré des événements sympas :

🎪 Cirque de Noël sur l'eau
📅 Jusqu'au 4 janvier
📍 Le Chapitô, Lille Hellemmes
💰 À partir de 15€

🎭 Festival Noël au théâtre
📅 Du 27 au 30 décembre
📍 Le Zeppelin
💰 5€

Tu veux plus d'infos sur un événement ?
```

**URL cible :** `https://lilleaddict.fr/que-faire-a-lille-ce-week-end/`

**Tool MCP à créer :**
```python
def get_weekend_events():
    """
    Scrape l'article hebdomadaire "Que faire ce week-end".
    
    Returns:
        {
            "week_dates": "22-28 décembre",
            "events": [
                {
                    "title": "Cirque de Noël",
                    "description": "...",
                    "dates": "Jusqu'au 4 janvier",
                    "price": "15€",
                    "location": "Le Chapitô, Lille",
                    "category": "spectacle"
                }
            ]
        }
    """
```

**Données à extraire :** Titre, description, dates, prix, lieu, horaires

---

### USE CASE 2 : Recommandation restaurants
**User Story :** "En tant qu'utilisateur, je veux trouver un resto selon mes critères (cuisine, budget, options)"

**Exemples de conversation :**
```
User: Je cherche un restaurant italien végétarien pas cher

Bot: J'ai trouvé 3 restaurants italiens végétariens à Lille :

🍕 Annie's Kitchen
Cuisine végane/végétarienne, Italien
💰 € (prix modéré)
📍 Lille centre

🥗 La Canopée
Plats végétariens, Italien
💰 €€
📍 Entre le parc Jean-Baptiste Lebas et Wazemmes

---

User: Un resto avec une décoration atypique ?

Bot: Je te recommande ces adresses avec une déco unique :

🎨 ARTCHIVES La Cantine Urbaine
Bar à cocktails + resto gastronomique + galerie d'art
📍 Lille

🎭 Madré
Ambiance espagnole chaleureuse
📍 Lille
```

**URL cible :** `https://lilleaddict.fr/bonnes-adresses/manger`

**Tools MCP à créer :**
```python
def search_restaurants(
    cuisine: str = None,      # "italien", "japonais", "français"...
    diet: str = None,         # "végétarien", "vegan", "sans gluten"
    price_range: str = None,  # "€", "€€", "€€€"
    atmosphere: str = None,   # "terrasse", "romantique", "groupe"
    location: str = None      # "Vieux-Lille", "Wazemmes"...
):
    """
    Recherche de restaurants selon critères.
    Scrape la page restaurants avec filtres.
    """

def get_restaurant_details(restaurant_id: str):
    """
    Récupère les détails complets d'un restaurant.
    """
```

**Données à extraire :**
- Nom du restaurant
- Type de cuisine
- Régime spécial (végé, vegan...)
- Fourchette de prix
- Adresse
- Ambiance / Décoration
- Horaires
- Spécialités

---

### USE CASE 3 : Recommandation bars
**User Story :** "En tant qu'utilisateur, je veux trouver un bar selon l'ambiance et le type de boissons"

**Exemples de conversation :**
```
User: Un bar à cocktails pour sortir ce soir ?

Bot: Voici mes tops bars à cocktails :

🍹 HØME
Bar de quartier, cocktails expérimentaux
📍 Lille
Spécialité : 5 cocktails signatures qui changent selon les saisons

🍸 Brutus
Cocktails classiques ou créations originales
📍 Lille

---

User: Où jouer au billard ?

Bot: Pour jouer au billard à Lille :

🎱 Barrel
Bar + billard + arcade
📍 Lille

🎱 Chess'nBar
Bar à jeux avec billard
📍 Lille centre
```

**URL cible :** `https://lilleaddict.fr/bonnes-adresses/boire`

**Tools MCP à créer :**
```python
def search_bars(
    drink_type: str = None,    # "cocktail", "bière", "vin", "thé"
    activity: str = None,      # "billard", "babyfoot", "jeux"
    atmosphere: str = None,    # "calme", "animé", "terrasse"
    location: str = None
):
    """
    Recherche de bars selon critères.
    """
```

**Données à extraire :** Nom, type de boissons, activités, ambiance, adresse, spécialités

---

### USE CASE 4 : Activités selon la météo
**User Story :** "En tant qu'utilisateur, je veux des recommandations adaptées à la météo"

**Exemples de conversation :**
```
User: Qu'est-ce que je peux faire ce week-end s'il pleut ?

Bot: S'il pleut ce week-end, voici des activités en intérieur :

🎭 Le Spotlight
Comedy club incontournable à Lille
📍 Lille centre

🎨 Le Musée de l'Illusion
Musée interactif avec illusions d'optique
📍 Lille

🧘 Ban Sawadee
Spa avec cabines de flottaison et massages
📍 Lille

---

User: Activités en extérieur si il fait beau ?

Bot: Si il fait beau, profite de :

🌳 Parc Barbieux
Grand parc à Roubaix, parfait pour une balade
📍 Roubaix

🚴 La Citadelle
Balade, jogging, pique-nique
📍 Lille
```

**URLs cibles :**
- Intérieur : `https://lilleaddict.fr/que-faire-a-lille-quand-il-pleut`
- Extérieur : `https://lilleaddict.fr/bonnes-adresses/sortir` (filtrer parcs, terrasses...)

**Tools MCP à créer :**
```python
def get_weather_forecast(days: int = 3):
    """
    Récupère les prévisions météo pour Lille.
    Utilise une API météo gratuite (OpenWeatherMap).
    
    Returns:
        {
            "current": {"temp": 15, "condition": "rain"},
            "forecast": [
                {"day": "samedi", "condition": "sunny", "temp": 18},
                {"day": "dimanche", "condition": "cloudy", "temp": 16}
            ]
        }
    """

def get_indoor_activities():
    """
    Scrape les activités en intérieur.
    """

def get_outdoor_activities():
    """
    Scrape les activités en extérieur (parcs, terrasses...).
    """
```

**Logique IA :**
1. User demande une activité
2. Bot appelle `get_weather_forecast()`
3. Si pluie → appelle `get_indoor_activities()`
4. Si beau → appelle `get_outdoor_activities()`
5. Présente les résultats

---

### USE CASE 5 : Top adresses selon les Lillois
**User Story :** "En tant qu'utilisateur, je veux connaître les adresses préférées des habitants"

**Exemples de conversation :**
```
User: Quels sont les meilleurs restos japonais selon les Lillois ?

Bot: D'après les votes des Lillois, voici les meilleurs restos japonais :

🥢 Kyoto
Restaurant près de la gare, idéal avant de prendre le train
📍 Gare Lille Flandres

🍣 La Table du Siam
Cuisine thaïlandaise de qualité
📍 Lille

---

User: Meilleures guinguettes à Lille ?

Bot: Les guinguettes préférées des Lillois :

🌳 La Guinguette de la Ferme (Bondues)
Ambiance bohème, tentes nomades
📍 Bondues

🚣 La Guinguette de la Marine
À deux pas de la Citadelle
📍 Lille
```

**URL cible :** `https://lilleaddict.fr/meilleur/`

**Tool MCP à créer :**
```python
def get_top_rated(category: str):
    """
    Récupère les tops adresses votées par les utilisateurs.
    
    Args:
        category: "restaurant", "bar", "activité"...
    
    Returns:
        Liste des adresses avec leur description et pourquoi elles sont tops
    """
```

**Données à extraire :** Nom, catégorie, description, pourquoi c'est top, adresse

---

## 🛠️ STRUCTURE DU PROJET

```
lille-addict-bot/
│
├── frontend/                    # Site vitrine + Chatbot
│   ├── index.html              # Page d'accueil
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.css       # Styles du site
│   │   ├── js/
│   │   │   ├── main.js         # Logic frontend
│   │   │   └── chatbot.js      # Interface chatbot
│   │   └── images/
│   └── pages/
│       ├── events.html         # Page événements
│       ├── restaurants.html    # Page restaurants
│       └── bars.html           # Page bars
│
├── backend/                     # API Python
│   ├── main.py                 # Point d'entrée FastAPI/Flask
│   ├── requirements.txt        # Dépendances Python
│   ├── config.py               # Configuration
│   ├── routes/
│   │   └── chat.py             # Routes API chatbot
│   ├── services/
│   │   ├── ollama_client.py    # Client Ollama
│   │   └── mcp_client.py       # Client MCP
│   └── utils/
│       └── helpers.py
│
├── mcp_server/                  # Serveur MCP (Tools)
│   ├── server.py               # Serveur MCP
│   ├── tools/
│   │   ├── scraping.py         # Tools de scraping
│   │   ├── weather.py          # Tool météo
│   │   └── __init__.py
│   └── utils/
│       ├── parser.py           # Parsing HTML
│       └── cache.py            # Cache optionnel
│
├── docs/                        # Documentation
│   ├── architecture.md
│   ├── api.md
│   └── deployment.md
│
├── tests/                       # Tests (optionnel)
│   ├── test_scraping.py
│   └── test_mcp.py
│
├── .env.example                 # Variables d'environnement
├── .gitignore
├── README.md
└── docker-compose.yml           # Optionnel : Docker setup
```

---

## 🔧 IMPLÉMENTATION TECHNIQUE

### 1. FRONTEND - Site vitrine

**index.html** (structure de base)
```html
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lille Addict Bot - Découvre Lille</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <!-- Header -->
    <header>
        <nav>
            <div class="logo">Lille Addict Bot</div>
            <ul class="nav-links">
                <li><a href="#home">Accueil</a></li>
                <li><a href="#events">Événements</a></li>
                <li><a href="#restaurants">Restaurants</a></li>
                <li><a href="#bars">Bars</a></li>
            </ul>
        </nav>
    </header>

    <!-- Hero Section -->
    <section id="home" class="hero">
        <h1>Découvre le meilleur de Lille</h1>
        <p>Ton assistant IA pour trouver les meilleures activités, restos et bars à Lille</p>
    </section>

    <!-- Chatbot Widget (fixed bottom right) -->
    <div id="chatbot-widget">
        <button id="chat-toggle">💬</button>
        <div id="chat-window" class="hidden">
            <div class="chat-header">
                <h3>Assistant Lille</h3>
                <button id="chat-close">✕</button>
            </div>
            <div id="chat-messages"></div>
            <div class="chat-input">
                <input type="text" id="user-input" placeholder="Pose ta question...">
                <button id="send-btn">Envoyer</button>
            </div>
        </div>
    </div>

    <!-- Sections du site -->
    <section id="events">
        <!-- Contenu événements -->
    </section>

    <section id="restaurants">
        <!-- Contenu restaurants -->
    </section>

    <section id="bars">
        <!-- Contenu bars -->
    </section>

    <footer>
        <p>© 2026 Lille Addict Bot - Projet pédagogique</p>
    </footer>

    <script src="assets/js/chatbot.js"></script>
    <script src="assets/js/main.js"></script>
</body>
</html>
```

**chatbot.js** (logique chat)
```javascript
// Configuration
const API_URL = 'http://localhost:8000/api/chat';

// État du chat
let conversationId = null;

// Éléments DOM
const chatToggle = document.getElementById('chat-toggle');
const chatWindow = document.getElementById('chat-window');
const chatClose = document.getElementById('chat-close');
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

// Toggle chat window
chatToggle.addEventListener('click', () => {
    chatWindow.classList.toggle('hidden');
});

chatClose.addEventListener('click', () => {
    chatWindow.classList.add('hidden');
});

// Envoyer message
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    // Afficher message user
    addMessage(message, 'user');
    userInput.value = '';

    // Afficher "typing..."
    const typingIndicator = addMessage('...', 'bot', true);

    try {
        // Appel API
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                conversation_id: conversationId
            })
        });

        const data = await response.json();
        
        // Retirer "typing..."
        typingIndicator.remove();

        // Afficher réponse bot
        addMessage(data.response, 'bot');
        
        // Sauvegarder conversation ID
        if (data.conversation_id) {
            conversationId = data.conversation_id;
        }

    } catch (error) {
        typingIndicator.remove();
        addMessage('Désolé, une erreur est survenue. 😞', 'bot');
        console.error('Error:', error);
    }
}

function addMessage(text, sender, isTyping = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    if (isTyping) messageDiv.classList.add('typing');
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return messageDiv;
}
```

---

### 2. BACKEND - API Python

**main.py** (FastAPI)
```python
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from services.ollama_client import OllamaClient
from services.mcp_client import MCPClient

app = FastAPI()

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En prod : spécifier le domaine frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Clients
ollama = OllamaClient()
mcp = MCPClient()

# Stockage conversations (en prod : utiliser Redis/DB)
conversations = {}

class ChatRequest(BaseModel):
    message: str
    conversation_id: str = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal du chatbot.
    """
    # Gérer conversation ID
    conv_id = request.conversation_id or str(uuid.uuid4())
    
    if conv_id not in conversations:
        conversations[conv_id] = []
    
    # Ajouter message user à l'historique
    conversations[conv_id].append({
        "role": "user",
        "content": request.message
    })
    
    # Envoyer à Ollama
    response = await ollama.chat(
        messages=conversations[conv_id],
        tools=mcp.get_available_tools()
    )
    
    # Si Ollama veut utiliser un tool
    if response.get("tool_calls"):
        for tool_call in response["tool_calls"]:
            tool_name = tool_call["name"]
            tool_args = tool_call["arguments"]
            
            # Appeler le MCP tool
            tool_result = await mcp.call_tool(tool_name, tool_args)
            
            # Renvoyer le résultat à Ollama
            response = await ollama.chat(
                messages=conversations[conv_id],
                tool_results=[tool_result]
            )
    
    # Ajouter réponse bot à l'historique
    conversations[conv_id].append({
        "role": "assistant",
        "content": response["content"]
    })
    
    return ChatResponse(
        response=response["content"],
        conversation_id=conv_id
    )

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**services/ollama_client.py**
```python
import httpx
from typing import List, Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.model = "llama3.2"  # ou "mistral"
        
        self.system_prompt = """
        Tu es un assistant pour découvrir Lille et sa région.
        
        Tu peux aider les utilisateurs à :
        - Trouver des événements du week-end
        - Recommander des restaurants selon critères
        - Suggérer des bars
        - Proposer des activités selon la météo
        
        Utilise les tools disponibles quand nécessaire.
        Sois concis, amical et pratique.
        Fournis toujours les informations essentielles : dates, prix, lieu.
        """
    
    async def chat(
        self,
        messages: List[Dict],
        tools: List[Dict] = None,
        tool_results: List[Dict] = None
    ) -> Dict[str, Any]:
        """
        Envoie une requête à Ollama.
        """
        # Construire le prompt
        prompt_messages = [
            {"role": "system", "content": self.system_prompt}
        ] + messages
        
        if tool_results:
            # Ajouter les résultats des tools
            for result in tool_results:
                prompt_messages.append({
                    "role": "tool",
                    "content": str(result)
                })
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": prompt_messages,
                    "tools": tools,
                    "stream": False
                },
                timeout=60.0
            )
            
            if response.status_code != 200:
                raise Exception(f"Ollama error: {response.text}")
            
            return response.json()
```

**services/mcp_client.py**
```python
import httpx
from typing import Dict, Any, List

class MCPClient:
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
    
    def get_available_tools(self) -> List[Dict]:
        """
        Liste des tools disponibles pour Ollama.
        """
        return [
            {
                "name": "get_weekend_events",
                "description": "Récupère les événements du week-end à Lille",
                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            {
                "name": "search_restaurants",
                "description": "Recherche des restaurants selon critères",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cuisine": {
                            "type": "string",
                            "description": "Type de cuisine (italien, japonais...)"
                        },
                        "diet": {
                            "type": "string",
                            "description": "Régime alimentaire (végétarien, vegan...)"
                        },
                        "price_range": {
                            "type": "string",
                            "description": "Fourchette de prix (€, €€, €€€)"
                        }
                    }
                }
            },
            {
                "name": "search_bars",
                "description": "Recherche des bars selon critères",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "drink_type": {
                            "type": "string",
                            "description": "Type de boisson (cocktail, bière, vin...)"
                        },
                        "activity": {
                            "type": "string",
                            "description": "Activité (billard, jeux...)"
                        }
                    }
                }
            },
            {
                "name": "get_weather_forecast",
                "description": "Récupère la météo pour Lille",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "days": {
                            "type": "integer",
                            "description": "Nombre de jours de prévision"
                        }
                    }
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict) -> Dict[str, Any]:
        """
        Appelle un tool MCP.
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/tools/{tool_name}",
                json=arguments,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"MCP tool error: {response.text}")
            
            return response.json()
```

---

### 3. MCP SERVER - Tools

**server.py**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from tools.scraping import (
    get_weekend_events,
    search_restaurants,
    search_bars
)
from tools.weather import get_weather_forecast

app = FastAPI()

class ToolRequest(BaseModel):
    arguments: Dict[str, Any] = {}

@app.post("/tools/get_weekend_events")
async def tool_weekend_events(request: ToolRequest):
    """
    Tool : Récupère les événements du week-end.
    """
    try:
        result = get_weekend_events()
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/search_restaurants")
async def tool_search_restaurants(request: ToolRequest):
    """
    Tool : Recherche de restaurants.
    """
    try:
        result = search_restaurants(**request.arguments)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/search_bars")
async def tool_search_bars(request: ToolRequest):
    """
    Tool : Recherche de bars.
    """
    try:
        result = search_bars(**request.arguments)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tools/get_weather_forecast")
async def tool_weather(request: ToolRequest):
    """
    Tool : Météo.
    """
    try:
        result = get_weather_forecast(**request.arguments)
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
```

**tools/scraping.py**
```python
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re

BASE_URL = "https://lilleaddict.fr"

def get_weekend_events() -> Dict:
    """
    Scrape les événements du week-end.
    """
    # 1. Récupérer la page principale
    response = requests.get(f"{BASE_URL}/que-faire-a-lille-ce-week-end/")
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # 2. Trouver l'article le plus récent
    latest_article = soup.find('article') or soup.find('div', class_='post')
    
    if not latest_article:
        return {"week_dates": "", "events": []}
    
    article_link = latest_article.find('a', href=True)
    if not article_link:
        return {"week_dates": "", "events": []}
    
    # 3. Récupérer l'article complet
    article_url = article_link['href']
    if not article_url.startswith('http'):
        article_url = BASE_URL + article_url
    
    article_response = requests.get(article_url)
    article_soup = BeautifulSoup(article_response.content, 'html.parser')
    
    # 4. Extraire le titre pour les dates
    title = article_soup.find('h1')
    week_dates = ""
    if title:
        # "Que faire à Lille et aux alentours du 22 au 28 décembre"
        match = re.search(r'du (\d+.*?(?:janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre))', title.get_text())
        if match:
            week_dates = match.group(1)
    
    # 5. Extraire les événements
    events = []
    event_sections = article_soup.find_all('h2')
    
    for h2 in event_sections:
        event = {
            'title': h2.get_text().strip(),
            'description': '',
            'dates': '',
            'price': '',
            'location': '',
            'hours': ''
        }
        
        # Parcourir les éléments suivants jusqu'au prochain h2
        for sibling in h2.find_next_siblings():
            if sibling.name == 'h2':
                break
            
            text = sibling.get_text().strip()
            
            # Parser les infos
            if not text:
                continue
            
            # Dates
            if any(keyword in text.lower() for keyword in ['jusqu\'au', 'samedi', 'dimanche', 'lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi']):
                if not event['dates']:
                    event['dates'] = text
            
            # Prix
            elif '€' in text or 'gratuit' in text.lower() or 'prix libre' in text.lower():
                if not event['price']:
                    event['price'] = text
            
            # Lieu (recherche d'adresse)
            elif any(keyword in text.lower() for keyword in ['rue', 'avenue', 'boulevard', 'place', 'lille', 'roubaix', 'tourcoing']):
                if not event['location']:
                    event['location'] = text
            
            # Horaires
            elif 'h' in text and len(text) < 30:
                if not event['hours']:
                    event['hours'] = text
            
            # Description (par défaut)
            else:
                if len(event['description']) < 200:  # Limite de la description
                    event['description'] += text + ' '
        
        # Nettoyer la description
        event['description'] = event['description'].strip()
        
        # Ajouter si au moins le titre existe
        if event['title']:
            events.append(event)
    
    return {
        "week_dates": week_dates,
        "events": events[:10]  # Limiter à 10 événements
    }

def search_restaurants(
    cuisine: str = None,
    diet: str = None,
    price_range: str = None,
    atmosphere: str = None,
    location: str = None
) -> List[Dict]:
    """
    Recherche de restaurants selon critères.
    """
    # Construction URL avec filtres
    url = f"{BASE_URL}/bonnes-adresses/manger"
    
    # Note : Lille Addict utilise un système de filtres frontend
    # Il faudrait soit :
    # 1. Scraper toutes les pages restaurants et filtrer côté Python
    # 2. Utiliser leur API si elle existe
    # 3. Simuler les clics JavaScript (plus complexe)
    
    # Pour le MVP, on scrape la page principale et on filtre
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    restaurants = []
    
    # Trouver les cartes de restaurants
    restaurant_cards = soup.find_all('div', class_='adresse') or soup.find_all('article')
    
    for card in restaurant_cards[:20]:  # Limiter à 20
        # Extraire infos
        title_elem = card.find('h3') or card.find('h2') or card.find('a')
        if not title_elem:
            continue
        
        title = title_elem.get_text().strip()
        description = ""
        
        desc_elem = card.find('p')
        if desc_elem:
            description = desc_elem.get_text().strip()
        
        # Filtrer selon critères
        text_content = (title + " " + description).lower()
        
        if cuisine and cuisine.lower() not in text_content:
            continue
        if diet and diet.lower() not in text_content:
            continue
        
        restaurants.append({
            'name': title,
            'description': description[:200],
            'url': title_elem.get('href', '')
        })
    
    return restaurants

def search_bars(
    drink_type: str = None,
    activity: str = None,
    atmosphere: str = None,
    location: str = None
) -> List[Dict]:
    """
    Recherche de bars selon critères.
    Même logique que search_restaurants.
    """
    url = f"{BASE_URL}/bonnes-adresses/boire"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    bars = []
    bar_cards = soup.find_all('div', class_='adresse') or soup.find_all('article')
    
    for card in bar_cards[:20]:
        title_elem = card.find('h3') or card.find('h2') or card.find('a')
        if not title_elem:
            continue
        
        title = title_elem.get_text().strip()
        description = ""
        
        desc_elem = card.find('p')
        if desc_elem:
            description = desc_elem.get_text().strip()
        
        # Filtrer
        text_content = (title + " " + description).lower()
        
        if drink_type and drink_type.lower() not in text_content:
            continue
        if activity and activity.lower() not in text_content:
            continue
        
        bars.append({
            'name': title,
            'description': description[:200],
            'url': title_elem.get('href', '')
        })
    
    return bars
```

**tools/weather.py**
```python
import requests
from typing import Dict

def get_weather_forecast(days: int = 3) -> Dict:
    """
    Récupère la météo pour Lille via OpenWeatherMap API.
    
    Note : Nécessite une clé API gratuite sur openweathermap.org
    """
    # TODO : Ajouter votre clé API dans .env
    API_KEY = "YOUR_API_KEY"  # À remplacer
    CITY = "Lille"
    
    if API_KEY == "YOUR_API_KEY":
        # Retourner des données mock pour le développement
        return {
            "current": {
                "temp": 15,
                "condition": "cloudy",
                "description": "Nuageux"
            },
            "forecast": [
                {"day": "Samedi", "condition": "rain", "temp": 12, "description": "Pluie"},
                {"day": "Dimanche", "condition": "sunny", "temp": 18, "description": "Ensoleillé"}
            ]
        }
    
    # Appel API réel
    url = f"https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr",
        "cnt": days * 8  # 8 prévisions par jour (toutes les 3h)
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    # Parser la réponse
    current = {
        "temp": data['list'][0]['main']['temp'],
        "condition": data['list'][0]['weather'][0]['main'].lower(),
        "description": data['list'][0]['weather'][0]['description']
    }
    
    forecast = []
    for item in data['list'][::8]:  # Une prévision par jour
        forecast.append({
            "day": item['dt_txt'][:10],
            "condition": item['weather'][0]['main'].lower(),
            "temp": item['main']['temp'],
            "description": item['weather'][0]['description']
        })
    
    return {
        "current": current,
        "forecast": forecast
    }
```

---

## 📦 FICHIERS DE CONFIGURATION

**requirements.txt** (backend + mcp_server)
```
fastapi==0.104.1
uvicorn==0.24.0
httpx==0.25.2
beautifulsoup4==4.12.2
requests==2.31.0
python-dotenv==1.0.0
pydantic==2.5.0
```

**.env.example**
```
# Backend
BACKEND_PORT=8000
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2

# MCP Server
MCP_PORT=8001

# API Keys
OPENWEATHER_API_KEY=your_key_here

# Frontend
FRONTEND_URL=http://localhost:3000
```

---

## 🚀 COMMANDES DE DÉMARRAGE

### Installation
```bash
# Backend
cd backend
pip install -r requirements.txt

# MCP Server
cd mcp_server
pip install -r requirements.txt

# Ollama (si pas installé)
# macOS/Linux:
curl -fsSL https://ollama.ai/install.sh | sh
# Windows: télécharger depuis ollama.ai

ollama pull llama3.2
```

### Lancement
```bash
# Terminal 1 : Ollama
ollama serve

# Terminal 2 : MCP Server
cd mcp_server
python server.py

# Terminal 3 : Backend
cd backend
python main.py

# Terminal 4 : Frontend (serveur local)
cd frontend
python -m http.server 3000
# Ou utiliser Live Server dans VS Code
```

### Tests
```bash
# Test MCP tool
curl -X POST http://localhost:8001/tools/get_weekend_events \
  -H "Content-Type: application/json" \
  -d '{}'

# Test Backend
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Que faire ce week-end ?"}'
```

---

## 📚 RESSOURCES ADDITIONNELLES

- **Ollama :** https://ollama.ai/
- **BeautifulSoup :** https://www.crummy.com/software/BeautifulSoup/
- **FastAPI :** https://fastapi.tiangolo.com/
- **MCP Spec :** https://github.com/modelcontextprotocol
- **Lille Addict :** https://lilleaddict.fr/

---

## ✅ TODO LIST

### Sprint 1 (MVP - Use Case 1)
- [ ] Setup Ollama + test modèle
- [ ] Créer structure projet
- [ ] Implémenter tool `get_weekend_events()`
- [ ] Tester scraping weekend
- [ ] Créer MCP server
- [ ] Créer backend API
- [ ] Créer frontend basique + chatbot
- [ ] Test end-to-end

### Sprint 2 (Use Cases 2-3)
- [ ] Tool `search_restaurants()`
- [ ] Tool `search_bars()`
- [ ] Tool `get_weather_forecast()`
- [ ] Intégration météo dans recommandations

### Sprint 3 (Polish + Docs)
- [ ] Design CSS du site
- [ ] Gestion d'erreurs
- [ ] Cache optionnel
- [ ] Documentation complète
- [ ] Préparation soutenance

---

**Ce fichier contient TOUT le contexte nécessaire pour développer le projet. Charge-le dans VS Code et commence à coder ! 🚀**
