"""
Client Ollama - Gestion des requêtes au modèle IA local
"""

import httpx
from typing import List, Dict, Any, Optional
import logging
import os

logger = logging.getLogger(__name__)

class OllamaClient:
    """Client pour communiquer avec Ollama"""
    
    def __init__(
        self,
        base_url: str = None,
        model: str = None
    ):
        self.base_url = base_url or os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        
        self.system_prompt = """Tu es un assistant intelligent pour découvrir Lille et sa région.

**Ton rôle:**
- Aider les utilisateurs à trouver des événements, restaurants, bars et activités à Lille
- Utiliser les tools disponibles pour récupérer des informations actualisées
- Fournir des réponses concises, amicales et pratiques
- Toujours inclure les informations essentielles: dates, prix, lieu

**Comportement:**
- Sois enthousiaste et positif
- Utilise des emojis pour rendre les réponses plus agréables
- Structure tes réponses clairement (titre, infos pratiques, description)
- Si plusieurs options, présente 3-5 suggestions maximum
- Propose d'approfondir si l'utilisateur veut plus d'infos

**Tools disponibles:**
- get_weekend_events() : Récupère les événements du week-end
- search_restaurants(cuisine, diet, price_range) : Recherche restaurants
- search_bars(drink_type, activity) : Recherche bars
- get_weather_forecast(days) : Prévisions météo

**Format de réponse idéal:**
🎭 **Titre de l'événement**
📅 Dates
💰 Prix
📍 Lieu
[Description courte]
"""
        
        logger.info(f"Ollama client initialisé - URL: {self.base_url}, Modèle: {self.model}")
    
    def is_available(self) -> bool:
        """Vérifie si Ollama est disponible"""
        try:
            import httpx
            response = httpx.get(f"{self.base_url}/api/tags", timeout=5.0)
            return response.status_code == 200
        except:
            return False
    
    async def chat(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        tool_results: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Envoie une requête de chat à Ollama
        
        Args:
            messages: Historique de conversation
            tools: Liste des tools disponibles
            tool_results: Résultats des tools appelés précédemment
            
        Returns:
            Réponse d'Ollama incluant le contenu et éventuels tool_calls
        """
        try:
            # Construire les messages avec le system prompt
            full_messages = [
                {"role": "system", "content": self.system_prompt}
            ] + messages
            
            # Ajouter les résultats de tools si présents
            if tool_results:
                for result in tool_results:
                    full_messages.append({
                        "role": "tool",
                        "content": self._format_tool_result(result)
                    })
            
            # Payload pour Ollama
            payload = {
                "model": self.model,
                "messages": full_messages,
                "stream": False
            }
            
            # Ajouter les tools si disponibles
            if tools:
                payload["tools"] = tools
            
            logger.debug(f"Envoi requête à Ollama - Messages: {len(full_messages)}, Tools: {len(tools) if tools else 0}")
            
            # Appel à Ollama
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                
                if response.status_code != 200:
                    logger.error(f"Erreur Ollama: {response.status_code} - {response.text}")
                    raise Exception(f"Ollama error: {response.status_code}")
                
                data = response.json()
                
                # Parser la réponse
                message = data.get("message", {})
                content = message.get("content", "")
                tool_calls = message.get("tool_calls", [])
                
                result = {
                    "content": content,
                    "tool_calls": tool_calls
                }
                
                logger.debug(f"Réponse Ollama - Content length: {len(content)}, Tool calls: {len(tool_calls)}")
                
                return result
                
        except httpx.ConnectError:
            logger.error("Impossible de se connecter à Ollama. Vérifie qu'Ollama est démarré.")
            raise Exception("Ollama n'est pas accessible. Lance 'ollama serve' dans un terminal.")
        
        except httpx.TimeoutException:
            logger.error("Timeout lors de la requête Ollama")
            raise Exception("La requête à Ollama a pris trop de temps.")
        
        except Exception as e:
            logger.error(f"Erreur inattendue Ollama: {str(e)}")
            raise
    
    def _format_tool_result(self, result: Dict) -> str:
        """
        Formate un résultat de tool pour Ollama
        
        Args:
            result: Résultat brut du tool
            
        Returns:
            String formaté pour Ollama
        """
        if result.get("success"):
            data = result.get("data", {})
            
            # Formater selon le type de données
            if isinstance(data, dict):
                # Cas événements
                if "events" in data:
                    events = data["events"]
                    formatted = f"J'ai trouvé {len(events)} événements"
                    if data.get("week_dates"):
                        formatted += f" pour la semaine du {data['week_dates']}"
                    formatted += ":\n\n"
                    
                    for i, event in enumerate(events[:10], 1):  # Max 10 événements
                        formatted += f"{i}. {event.get('title', 'Sans titre')}\n"
                        if event.get('dates'):
                            formatted += f"   📅 {event['dates']}\n"
                        if event.get('price'):
                            formatted += f"   💰 {event['price']}\n"
                        if event.get('location'):
                            formatted += f"   📍 {event['location']}\n"
                        if event.get('description'):
                            desc = event['description'][:150]
                            formatted += f"   {desc}...\n"
                        formatted += "\n"
                    
                    return formatted
                
                # Cas météo
                elif "current" in data or "forecast" in data:
                    formatted = "Météo pour Lille:\n\n"
                    
                    if "current" in data:
                        current = data["current"]
                        formatted += f"Actuellement: {current.get('temp')}°C - {current.get('description')}\n\n"
                    
                    if "forecast" in data:
                        formatted += "Prévisions:\n"
                        for day in data["forecast"]:
                            formatted += f"- {day.get('day')}: {day.get('temp')}°C, {day.get('description')}\n"
                    
                    return formatted
            
            # Cas liste simple (restaurants, bars)
            elif isinstance(data, list):
                formatted = f"J'ai trouvé {len(data)} résultats:\n\n"
                for i, item in enumerate(data[:8], 1):  # Max 8 résultats
                    formatted += f"{i}. {item.get('name', 'Sans nom')}\n"
                    if item.get('description'):
                        desc = item['description'][:100]
                        formatted += f"   {desc}...\n"
                    if item.get('location'):
                        formatted += f"   📍 {item['location']}\n"
                    formatted += "\n"
                return formatted
            
            # Fallback: convertir en string
            return str(data)
        
        else:
            # Erreur dans le tool
            error = result.get("error", "Erreur inconnue")
            return f"Erreur lors de la récupération des données: {error}"
    
    async def test_connection(self) -> bool:
        """Teste la connexion à Ollama"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False
    
    async def list_models(self) -> List[str]:
        """Liste les modèles disponibles dans Ollama"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                if response.status_code == 200:
                    data = response.json()
                    return [model["name"] for model in data.get("models", [])]
                return []
        except:
            return []


# ====================================
# TESTS
# ====================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = OllamaClient()
        
        print("Test connexion Ollama...")
        is_connected = await client.test_connection()
        print(f"Ollama disponible: {is_connected}")
        
        if is_connected:
            print("\nModèles disponibles:")
            models = await client.list_models()
            for model in models:
                print(f"  - {model}")
            
            print("\nTest chat simple...")
            response = await client.chat(
                messages=[
                    {"role": "user", "content": "Bonjour, peux-tu te présenter ?"}
                ]
            )
            print(f"Réponse: {response['content']}")
    
    asyncio.run(test())
