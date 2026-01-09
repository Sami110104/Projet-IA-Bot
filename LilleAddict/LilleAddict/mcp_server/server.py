"""
Serveur MCP - Expose les tools pour le scraping et traitement de données
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

from tools.scraping import (
    get_weekend_events,
    search_restaurants,
    search_bars,
    get_indoor_activities,
    get_outdoor_activities
)
from tools.weather import get_weather_forecast

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ====================================
# APPLICATION FASTAPI
# ====================================

app = FastAPI(
    title="Lille Addict MCP Server",
    description="Serveur MCP exposant les tools de scraping et traitement",
    version="1.0.0"
)

# ====================================
# MODÈLES PYDANTIC
# ====================================

class ToolRequest(BaseModel):
    arguments: Dict[str, Any] = {}

class ToolResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

# ====================================
# ROUTES
# ====================================

@app.get("/")
async def root():
    """Page d'accueil du serveur MCP"""
    return {
        "message": "Lille Addict MCP Server",
        "version": "1.0.0",
        "tools": [
            "get_weekend_events",
            "search_restaurants",
            "search_bars",
            "get_weather_forecast",
            "get_indoor_activities",
            "get_outdoor_activities"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check"""
    return {"status": "ok"}

@app.post("/tools/get_weekend_events", response_model=ToolResponse)
async def tool_weekend_events(request: ToolRequest):
    """
    Tool: Récupère les événements du week-end à Lille
    """
    try:
        logger.info("Tool appelé: get_weekend_events")
        result = get_weekend_events()
        logger.info(f"Résultat: {len(result.get('events', []))} événements récupérés")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur get_weekend_events: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

@app.post("/tools/search_restaurants", response_model=ToolResponse)
async def tool_search_restaurants(request: ToolRequest):
    """
    Tool: Recherche de restaurants selon critères
    """
    try:
        args = request.arguments
        logger.info(f"Tool appelé: search_restaurants avec args: {args}")
        
        result = search_restaurants(
            cuisine=args.get("cuisine"),
            diet=args.get("diet"),
            price_range=args.get("price_range"),
            atmosphere=args.get("atmosphere"),
            location=args.get("location")
        )
        
        logger.info(f"Résultat: {len(result)} restaurants trouvés")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur search_restaurants: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

@app.post("/tools/search_bars", response_model=ToolResponse)
async def tool_search_bars(request: ToolRequest):
    """
    Tool: Recherche de bars selon critères
    """
    try:
        args = request.arguments
        logger.info(f"Tool appelé: search_bars avec args: {args}")
        
        result = search_bars(
            drink_type=args.get("drink_type"),
            activity=args.get("activity"),
            atmosphere=args.get("atmosphere"),
            location=args.get("location")
        )
        
        logger.info(f"Résultat: {len(result)} bars trouvés")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur search_bars: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

@app.post("/tools/get_weather_forecast", response_model=ToolResponse)
async def tool_weather(request: ToolRequest):
    """
    Tool: Récupère les prévisions météo
    """
    try:
        args = request.arguments
        days = args.get("days", 3)
        logger.info(f"Tool appelé: get_weather_forecast pour {days} jours")
        
        result = get_weather_forecast(days=days)
        
        logger.info("Météo récupérée avec succès")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur get_weather_forecast: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

@app.post("/tools/get_indoor_activities", response_model=ToolResponse)
async def tool_indoor_activities(request: ToolRequest):
    """
    Tool: Récupère les activités en intérieur
    """
    try:
        logger.info("Tool appelé: get_indoor_activities")
        result = get_indoor_activities()
        logger.info(f"Résultat: {len(result)} activités trouvées")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur get_indoor_activities: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

@app.post("/tools/get_outdoor_activities", response_model=ToolResponse)
async def tool_outdoor_activities(request: ToolRequest):
    """
    Tool: Récupère les activités en extérieur
    """
    try:
        logger.info("Tool appelé: get_outdoor_activities")
        result = get_outdoor_activities()
        logger.info(f"Résultat: {len(result)} activités trouvées")
        return ToolResponse(success=True, data=result)
    except Exception as e:
        logger.error(f"Erreur get_outdoor_activities: {str(e)}", exc_info=True)
        return ToolResponse(success=False, error=str(e))

# ====================================
# LANCEMENT
# ====================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Démarrage du serveur MCP...")
    logger.info("📡 MCP disponible sur http://localhost:8001")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
