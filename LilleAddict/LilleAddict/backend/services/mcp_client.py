"""
Client MCP - Gestion des appels aux tools du serveur MCP
"""

import httpx
from typing import Dict, Any, List, Optional
import logging
import os

logger = logging.getLogger(__name__)

class MCPClient:
    """Client pour communiquer avec le serveur MCP"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("MCP_URL", "http://localhost:8001")
        logger.info(f"MCP client initialisé - URL: {self.base_url}")
    
    def is_available(self) -> bool:
        """Vérifie si le serveur MCP est disponible"""
        try:
            import httpx
            response = httpx.get(f"{self.base_url}/health", timeout=5.0)
            return response.status_code == 200
        except:
            return False
    
    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Retourne la liste des tools disponibles au format Ollama
        
        Returns:
            Liste des définitions de tools
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "get_weekend_events",
                    "description": "Récupère la liste des événements à faire à Lille ce week-end. Utilise ce tool quand l'utilisateur demande ce qu'il peut faire ce week-end, les événements de la semaine, ou les sorties à Lille.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_restaurants",
                    "description": "Recherche des restaurants à Lille selon des critères spécifiques. Utilise ce tool quand l'utilisateur cherche un restaurant avec des préférences de cuisine, régime alimentaire ou gamme de prix.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "cuisine": {
                                "type": "string",
                                "description": "Type de cuisine recherchée (ex: italien, japonais, français, mexicain, indien, chinois, thaï, coréen, végétarien, etc.)"
                            },
                            "diet": {
                                "type": "string",
                                "description": "Régime alimentaire spécifique (ex: végétarien, vegan, sans gluten, halal)"
                            },
                            "price_range": {
                                "type": "string",
                                "description": "Gamme de prix (€ pour pas cher, €€ pour moyen, €€€ pour cher)"
                            },
                            "atmosphere": {
                                "type": "string",
                                "description": "Type d'ambiance recherchée (ex: terrasse, romantique, groupe, familial, branché)"
                            },
                            "location": {
                                "type": "string",
                                "description": "Quartier ou ville spécifique (ex: Vieux-Lille, Wazemmes, Roubaix)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "search_bars",
                    "description": "Recherche des bars à Lille selon des critères. Utilise ce tool quand l'utilisateur cherche un bar, un endroit pour boire un verre, ou une activité de soirée.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "drink_type": {
                                "type": "string",
                                "description": "Type de boisson (ex: cocktail, bière, vin, café, thé, chocolat chaud)"
                            },
                            "activity": {
                                "type": "string",
                                "description": "Activité disponible (ex: billard, babyfoot, fléchettes, jeux de société, karaoké, concert, quiz)"
                            },
                            "atmosphere": {
                                "type": "string",
                                "description": "Ambiance recherchée (ex: calme, animé, terrasse, cosy, branché, jazz, rock)"
                            },
                            "location": {
                                "type": "string",
                                "description": "Quartier ou ville (ex: centre Lille, Vieux-Lille, Wazemmes)"
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_weather_forecast",
                    "description": "Récupère les prévisions météo pour Lille. Utilise ce tool quand l'utilisateur pose une question sur la météo ou demande des activités adaptées au temps qu'il va faire.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "days": {
                                "type": "integer",
                                "description": "Nombre de jours de prévisions (1-7)",
                                "default": 3
                            }
                        }
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_indoor_activities",
                    "description": "Récupère les activités en intérieur à Lille. Utilise ce tool quand l'utilisateur demande quoi faire s'il pleut, ou des activités à l'abri.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_outdoor_activities",
                    "description": "Récupère les activités en extérieur à Lille. Utilise ce tool quand l'utilisateur demande des activités de plein air, parcs, terrasses.",
                    "parameters": {
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                }
            }
        ]
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """
        Appelle un tool MCP
        
        Args:
            tool_name: Nom du tool à appeler
            arguments: Arguments du tool
            
        Returns:
            Résultat du tool
        """
        try:
            logger.info(f"Appel MCP tool: {tool_name} avec args: {arguments}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.base_url}/tools/{tool_name}",
                    json={"arguments": arguments}
                )
                
                if response.status_code != 200:
                    logger.error(f"Erreur MCP: {response.status_code} - {response.text}")
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}"
                    }
                
                data = response.json()
                logger.info(f"MCP tool {tool_name} - Success: {data.get('success')}")
                return data
                
        except httpx.ConnectError:
            logger.error("Impossible de se connecter au serveur MCP")
            return {
                "success": False,
                "error": "Le serveur MCP n'est pas accessible. Vérifie qu'il est démarré sur le port 8001."
            }
        
        except httpx.TimeoutException:
            logger.error(f"Timeout lors de l'appel du tool {tool_name}")
            return {
                "success": False,
                "error": f"Le tool {tool_name} a pris trop de temps à répondre."
            }
        
        except Exception as e:
            logger.error(f"Erreur inattendue lors de l'appel du tool {tool_name}: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def test_connection(self) -> bool:
        """Teste la connexion au serveur MCP"""
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{self.base_url}/health")
                return response.status_code == 200
        except:
            return False
    
    async def list_tools(self) -> List[str]:
        """Liste les tools disponibles"""
        tools = self.get_available_tools()
        return [tool["function"]["name"] for tool in tools]


# ====================================
# TESTS
# ====================================

if __name__ == "__main__":
    import asyncio
    
    async def test():
        client = MCPClient()
        
        print("Test connexion MCP...")
        is_connected = await client.test_connection()
        print(f"MCP disponible: {is_connected}")
        
        if is_connected:
            print("\nTools disponibles:")
            tools = await client.list_tools()
            for tool in tools:
                print(f"  - {tool}")
            
            print("\nTest tool get_weekend_events...")
            result = await client.call_tool("get_weekend_events", {})
            print(f"Success: {result.get('success')}")
            if result.get('success'):
                data = result.get('data', {})
                print(f"Nombre d'événements: {len(data.get('events', []))}")
    
    asyncio.run(test())
