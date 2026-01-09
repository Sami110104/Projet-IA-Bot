# 🎯 PROJET IA BOT - LILLE ADDICT
## Use Case 1 : "Que faire ce week-end à Lille ?"

**Date :** 08/01/2026  
**Durée :** 7 jours  
**Groupe :** 3-5 personnes  

---

## 📋 CONTEXTE

Création d'un agent conversationnel intelligent capable de recommander des événements à Lille en répondant à la question : **"Que faire ce week-end à Lille ?"**

Le bot scrape les données de Lille Addict et répond de manière naturelle aux requêtes utilisateur.

---

## 🎯 OBJECTIF MVP

**User Story :**
> En tant qu'utilisateur, je veux demander "Que faire ce week-end à Lille ?" et obtenir une liste d'événements sympas avec les détails pratiques.

**Exemple de conversation :**
```
User: Salut ! Que faire ce week-end à Lille ?

Bot: Cette semaine à Lille (du 22 au 28 décembre), j'ai repéré quelques événements sympas :

🎪 Cirque de Noël sur l'eau - jusqu'au 4 janvier
Un spectacle aquatique avec 15 artistes internationaux + le Père Noël !
📍 Le Chapitô, Lille Hellemmes
💰 À partir de 15€

🎭 Festival Noël au théâtre - du 27 au 30 décembre
6 spectacles pour toute la famille
📍 Le Zeppelin
💰 5€

🎵 Concert de jazz - samedi 27
Le trio Musidora joue les classiques
📍 La Moulinette, Lille
💰 Prix libre

Tu veux plus d'infos sur un événement en particulier ?
```

---

## 📊 DONNÉES À SCRAPER

### Source principale
**URL :** `https://lilleaddict.fr/que-faire-a-lille-ce-week-end/`

### Structure de la page

Chaque article hebdomadaire contient :

**1. En-tête :**
- Titre : "Que faire à Lille et aux alentours du [dates]"
- Date de publication
- Introduction résumant la semaine

**2. Événements (section par section) :**

Chaque événement contient :
```
Titre de l'événement
├── Description (paragraphe texte)
├── Dates (ex: "Jusqu'au dimanche 4 janvier" ou "Samedi 27")
├── Horaires (ex: "20h30-23h")
├── Prix (ex: "À partir de 15€" ou "Gratuit")
├── Lieu (adresse complète)
├── Informations complémentaires (parking, réservation...)
└── Images (optionnel)
```

**Exemple concret d'événement extrait :**
```json
{
  "title": "Cirque de Noël sur l'eau",
  "description": "2h de spectacle aquatique avec 15 artistes internationaux...",
  "dates": "Jusqu'au dimanche 4 janvier",
  "price": "À partir de 15€",
  "location": "Le Chapitô, 208 rue Faidherbe, Lille Hellemmes",
  "hours": "Variable selon séances",
  "booking": "Réservation en lien dans la bio",
  "category": "Spectacle"
}
```

---

## 🛠️ ARCHITECTURE TECHNIQUE

### Stack obligatoire (selon énoncé)

```
┌─────────────────────────────────────────────────┐
│                   FRONTEND                      │
│              (JavaScript / React)               │
│  Interface web avec chatbot intégré             │
└────────────────┬────────────────────────────────┘
                 │ HTTP/WebSocket
                 ▼
┌─────────────────────────────────────────────────┐
│                   BACKEND                       │
│                  (Python)                       │
│  Orchestrateur IA + Gestion MCP                 │
└────────┬───────────────────┬────────────────────┘
         │                   │
         │                   ▼
         │          ┌─────────────────┐
         │          │   MCP SERVER    │
         │          │   (Python)      │
         │          │                 │
         │          │  Tools:         │
         │          │  - Scraping     │
         │          │  - Data parse   │
         │          └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────┐
│              MODÈLE IA LOCAL                    │
│                 (Ollama)                        │
│  Compréhension langage naturel + Décision       │
└─────────────────────────────────────────────────┘
```

---

## 🔧 COMPOSANTS DÉTAILLÉS

### 1. FRONTEND (JavaScript)

**Responsabilités :**
- Interface utilisateur (chat)
- Envoi des messages user vers backend
- Affichage des réponses du bot
- Gestion de l'historique de conversation

**Technologies suggérées :**
- React / Vue.js / Vanilla JS
- Framework CSS (Tailwind, Bootstrap...)

**Exemple de requête frontend → backend :**
```javascript
// POST /api/chat
{
  "message": "Que faire ce week-end à Lille ?",
  "conversation_id": "abc123"
}
```

---

### 2. BACKEND (Python)

**Responsabilités :**
- Recevoir les requêtes du frontend
- Envoyer le message à Ollama pour analyse
- Décider si un tool MCP doit être appelé
- Orchestrer les appels MCP
- Retourner la réponse formatée au frontend

**Structure suggérée :**
```
backend/
├── main.py              # API Flask/FastAPI
├── ollama_client.py     # Client Ollama
├── mcp_client.py        # Client MCP
└── config.py            # Configuration
```

**Flux backend :**
```python
1. User message → Backend
2. Backend → Ollama : "L'utilisateur demande quoi faire ce week-end"
3. Ollama → Backend : "Je dois appeler le tool get_weekend_events()"
4. Backend → MCP Server : appel get_weekend_events()
5. MCP Server → Backend : données événements
6. Backend → Ollama : "Voici les données, formule une réponse"
7. Ollama → Backend : réponse en langage naturel
8. Backend → Frontend : réponse finale
```

---

### 3. MCP SERVER (Python)

**Responsabilité :**
- Exposer les tools que l'IA peut utiliser
- Exécuter le scraping
- Parser et structurer les données

**Tool principal à implémenter :**

```python
# Tool : get_weekend_events()

def get_weekend_events():
    """
    Scrape la page 'Que faire ce week-end' de Lille Addict
    et retourne une liste structurée d'événements.
    
    Returns:
        dict: {
            "week_dates": "22 au 28 décembre",
            "events": [
                {
                    "title": "Cirque de Noël sur l'eau",
                    "description": "...",
                    "dates": "Jusqu'au 4 janvier",
                    "price": "À partir de 15€",
                    "location": "Le Chapitô, Lille",
                    ...
                },
                ...
            ]
        }
    """
```

**Bibliothèques Python suggérées :**
- `beautifulsoup4` : parsing HTML
- `requests` : requêtes HTTP
- `mcp` : SDK MCP Python (si disponible, sinon créer serveur custom)

**Structure MCP :**
```
mcp_server/
├── server.py           # Serveur MCP
├── tools/
│   └── scraping.py     # Tool de scraping
└── utils/
    └── parser.py       # Parsing HTML
```

---

### 4. MODÈLE IA (Ollama)

**Responsabilité :**
- Comprendre l'intention de l'utilisateur
- Décider quand appeler les tools
- Générer des réponses naturelles

**Configuration Ollama :**
- Modèle recommandé : `llama3.2` ou `mistral` (légers et performants)
- Installation : `ollama pull llama3.2`

**Prompt système suggéré :**
```
Tu es un assistant pour les événements à Lille.
Quand l'utilisateur demande ce qu'il peut faire ce week-end,
utilise le tool get_weekend_events() pour récupérer les événements
et présente-les de manière claire et attractive.

Sois concis, amical et mets en avant les infos pratiques (dates, prix, lieu).
```

---

## 📝 EXEMPLE DE SCRAPING

### Page cible
`https://lilleaddict.fr/que-faire-a-lille-ce-week-end/que-faire-a-lille-et-aux-alentours-du-22-au-28-decembre.html`

### Sélecteurs HTML (à affiner avec inspection)

**Structure observée :**
- Chaque événement est dans une section H2
- Informations dans des listes `<ul>` ou paragraphes `<p>`
- Prix/dates/lieux souvent en début de section

**Pseudo-code scraping :**
```python
import requests
from bs4 import BeautifulSoup

def scrape_weekend_events(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    events = []
    
    # Trouver tous les titres H2 (= événements)
    event_sections = soup.find_all('h2')
    
    for section in event_sections:
        event = {
            'title': section.get_text().strip(),
            'description': '',
            'dates': '',
            'price': '',
            'location': ''
        }
        
        # Parser les infos après le H2
        next_elements = section.find_next_siblings()
        
        for elem in next_elements:
            text = elem.get_text().strip()
            
            # Identifier dates, prix, lieu par mots-clés
            if 'jusqu\'au' in text.lower() or 'samedi' in text.lower():
                event['dates'] = text
            elif '€' in text or 'gratuit' in text.lower():
                event['price'] = text
            elif 'rue' in text.lower() or 'avenue' in text.lower():
                event['location'] = text
            else:
                event['description'] += text + ' '
        
        events.append(event)
    
    return events
```

---

## ✅ CHECKLIST MVP

### Phase 1 : Setup (Jour 1-2)
- [ ] Installer Ollama + télécharger modèle
- [ ] Créer structure projet (frontend / backend / mcp)
- [ ] Tester requête basique Ollama
- [ ] Vérifier autorisation scraping (robots.txt ✅)

### Phase 2 : Backend + MCP (Jour 2-4)
- [ ] Créer le tool MCP `get_weekend_events()`
- [ ] Implémenter le scraping BeautifulSoup
- [ ] Parser les données (titre, dates, prix, lieu)
- [ ] Tester le tool isolé
- [ ] Connecter backend → Ollama
- [ ] Connecter backend → MCP

### Phase 3 : Frontend (Jour 4-5)
- [ ] Interface chat basique
- [ ] Connexion frontend → backend
- [ ] Affichage réponses bot
- [ ] Styling CSS

### Phase 4 : Intégration (Jour 6)
- [ ] Test flux complet : user → bot → scraping → réponse
- [ ] Ajustements prompt IA
- [ ] Gestion d'erreurs (site down, parsing fail...)

### Phase 5 : Documentation (Jour 7)
- [ ] Schéma d'architecture
- [ ] Explication flux de données
- [ ] Justification choix techniques
- [ ] Limites & améliorations

---

## 🚀 ÉVOLUTIONS FUTURES

**V2 - Filtres :**
- "Événements gratuits ce week-end"
- "Spectacles pour enfants"
- "Concerts de jazz"

**V3 - Météo-aware :**
- Intégrer API météo
- Recommander intérieur/extérieur selon la météo

**V4 - Multi-sources :**
- Scraper d'autres sites lillois
- Agrégateur d'événements

---

## 📚 RESSOURCES UTILES

**Ollama :**
- Documentation : https://ollama.ai/
- Models : https://ollama.ai/library

**MCP :**
- Spécification : https://github.com/modelcontextprotocol
- Python SDK : à vérifier disponibilité

**Scraping Python :**
- BeautifulSoup : https://www.crummy.com/software/BeautifulSoup/
- Requests : https://requests.readthedocs.io/

**Site cible :**
- Lille Addict : https://lilleaddict.fr/
- Robots.txt : https://lilleaddict.fr/robots.txt ✅ Autorisé

---

## 🎓 LIVRABLES ATTENDUS

1. **Application fonctionnelle**
   - Site web avec chatbot intégré
   - Scraping réel (pas de mock data)
   - Flux complet frontend → backend → MCP → IA

2. **Documentation technique** (15-20 pages)
   - Architecture globale + schémas
   - Description flux de données
   - Explication + justification choix technos
   - Fonctionnement du MCP
   - Limites + améliorations

3. **Soutenance** (20 minutes)
   - Démo live
   - Explication technique
   - Analyse critique
   - Tous les membres parlent

---

## 📌 NOTES IMPORTANTES

- ✅ Scraping autorisé (vérifié robots.txt)
- ⏱️ Scraper à faible fréquence (pas de spam)
- 🎯 Usage pédagogique uniquement
- 🚫 Pas de modèle open-source local obligatoire (Ollama)
- 📦 Pas de services tiers payants

---

**Prochaine étape :** Commencer par le setup Ollama + premier test de scraping ! 🚀
