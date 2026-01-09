"""
Backend API pour Lille Addict Bot
FastAPI + Ollama + MCP
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uuid
import logging

from services.ollama_client import OllamaClient
from services.mcp_client import MCPClient

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================================
# APPLICATION FASTAPI
# ====================================

app = FastAPI(
    title="Lille Addict Bot API",
    description="API du chatbot intelligent pour découvrir Lille",
    version="1.0.0"
)

# ====================================
# CORS MIDDLEWARE
# ====================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production: spécifier les domaines autorisés
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ====================================
# CLIENTS & STOCKAGE
# ====================================

# Clients
ollama_client = OllamaClient()
mcp_client = MCPClient()

# Stockage temporaire des conversations
# En production: utiliser Redis ou une base de données
conversations: Dict[str, List[Dict]] = {}

# ====================================
# MODÈLES PYDANTIC
# ====================================

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    
class EventsPreviewResponse(BaseModel):
    events: List[Dict[str, Any]]
    week_dates: str

# ====================================
# ROUTES API
# ====================================

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Lille Addict Bot API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "events": "/api/events/preview",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check de l'API"""
    return {
        "status": "ok",
        "ollama": ollama_client.is_available(),
        "mcp": mcp_client.is_available()
    }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Endpoint principal du chatbot.
    
    Reçoit un message utilisateur, le traite avec Ollama,
    appelle les tools MCP si nécessaire, et retourne la réponse.
    """
    try:
        # Gérer l'ID de conversation
        conv_id = request.conversation_id or str(uuid.uuid4())
        
        # Initialiser la conversation si nouvelle
        if conv_id not in conversations:
            conversations[conv_id] = []
            logger.info(f"Nouvelle conversation: {conv_id}")
        
        # Ajouter le message utilisateur
        conversations[conv_id].append({
            "role": "user",
            "content": request.message
        })
        
        logger.info(f"[{conv_id}] User: {request.message}")
        
        # Obtenir les tools disponibles
        available_tools = mcp_client.get_available_tools()
        
        # Envoyer à Ollama
        ollama_response = await ollama_client.chat(
            messages=conversations[conv_id],
            tools=available_tools
        )
        
        # Traiter les tool calls si présents
        if "tool_calls" in ollama_response and ollama_response["tool_calls"]:
            logger.info(f"[{conv_id}] Tool calls détectés: {len(ollama_response['tool_calls'])}")
            
            tool_results = []
            
            for tool_call in ollama_response["tool_calls"]:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("arguments", {})
                
                logger.info(f"[{conv_id}] Appel tool: {tool_name} avec args: {tool_args}")
                
                # Appeler le tool MCP
                try:
                    tool_result = await mcp_client.call_tool(tool_name, tool_args)
                    tool_results.append(tool_result)
                    logger.info(f"[{conv_id}] Tool result: Success")
                except Exception as e:
                    logger.error(f"[{conv_id}] Erreur tool {tool_name}: {str(e)}")
                    tool_results.append({
                        "error": str(e),
                        "tool": tool_name
                    })
            
            # Re-soumettre à Ollama avec les résultats des tools
            ollama_response = await ollama_client.chat(
                messages=conversations[conv_id],
                tool_results=tool_results
            )
        
        # Extraire la réponse finale
        final_response = ollama_response.get("content", "Désolé, je n'ai pas pu générer de réponse.")
        
        # Ajouter la réponse du bot à l'historique
        conversations[conv_id].append({
            "role": "assistant",
            "content": final_response
        })
        
        logger.info(f"[{conv_id}] Bot response generated")
        
        return ChatResponse(
            response=final_response,
            conversation_id=conv_id
        )
        
    except Exception as e:
        logger.error(f"Erreur dans chat_endpoint: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors du traitement: {str(e)}"
        )

@app.get("/api/events/preview", response_model=EventsPreviewResponse)
async def get_events_preview():
    """
    Récupère un aperçu des événements du week-end
    pour affichage sur la page d'accueil.
    """
    try:
        # Appeler directement le tool MCP
        result = await mcp_client.call_tool("get_weekend_events", {})
        
        if result.get("success"):
            data = result.get("data", {})
            return EventsPreviewResponse(
                events=data.get("events", []),
                week_dates=data.get("week_dates", "")
            )
        else:
            raise HTTPException(
                status_code=500,
                detail="Erreur lors de la récupération des événements"
            )
            
    except Exception as e:
        logger.error(f"Erreur dans get_events_preview: {str(e)}")
        # Retourner une liste vide plutôt qu'une erreur
        return EventsPreviewResponse(
            events=[],
            week_dates=""
        )

@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Supprime une conversation"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation supprimée"}
    raise HTTPException(status_code=404, detail="Conversation non trouvée")

# ====================================
# LANCEMENT
# ====================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Démarrage du serveur backend...")
    logger.info("📡 API disponible sur http://localhost:8000")
    logger.info("📚 Documentation sur http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
