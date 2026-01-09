"""
Tool météo - Prévisions météo pour Lille
"""

import requests
from typing import Dict
import logging
import os

logger = logging.getLogger(__name__)

def get_weather_forecast(days: int = 3) -> Dict:
    """
    Récupère les prévisions météo pour Lille
    
    Args:
        days: Nombre de jours de prévisions (1-7)
    
    Returns:
        {
            "current": {
                "temp": 15,
                "condition": "cloudy",
                "description": "Nuageux"
            },
            "forecast": [
                {
                    "day": "Samedi",
                    "condition": "rain",
                    "temp": 12,
                    "description": "Pluie"
                },
                ...
            ]
        }
    """
    try:
        API_KEY = os.getenv("OPENWEATHER_API_KEY")
        
        # Si pas de clé API, retourner mock data
        if not API_KEY or API_KEY == "your_api_key_here":
            logger.info("Pas de clé API météo, retour mock data")
            return get_mock_weather(days)
        
        # Appel API réel
        logger.info(f"Récupération météo pour {days} jours")
        
        CITY = "Lille"
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": CITY,
            "appid": API_KEY,
            "units": "metric",
            "lang": "fr",
            "cnt": days * 8  # 8 prévisions par jour (toutes les 3h)
        }
        
        response = requests.get(url, params=params, timeout=10)
        
        if response.status_code != 200:
            logger.error(f"Erreur API météo: {response.status_code}")
            return get_mock_weather(days)
        
        data = response.json()
        
        # Parser la réponse
        current = {
            "temp": round(data['list'][0]['main']['temp']),
            "condition": map_weather_condition(data['list'][0]['weather'][0]['main']),
            "description": data['list'][0]['weather'][0]['description']
        }
        
        forecast = []
        days_list = ["Samedi", "Dimanche", "Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]
        
        for i, item in enumerate(data['list'][::8][:days]):  # Une prévision par jour
            forecast.append({
                "day": days_list[i % 7],
                "condition": map_weather_condition(item['weather'][0]['main']),
                "temp": round(item['main']['temp']),
                "description": item['weather'][0]['description']
            })
        
        return {
            "current": current,
            "forecast": forecast
        }
        
    except Exception as e:
        logger.error(f"Erreur récupération météo: {str(e)}")
        return get_mock_weather(days)

def get_mock_weather(days: int = 3) -> Dict:
    """
    Données météo mockées pour le développement
    """
    return {
        "current": {
            "temp": 8,
            "condition": "cloudy",
            "description": "Nuageux"
        },
        "forecast": [
            {
                "day": "Samedi",
                "condition": "rain",
                "temp": 7,
                "description": "Pluie"
            },
            {
                "day": "Dimanche",
                "condition": "sunny",
                "temp": 12,
                "description": "Ensoleillé"
            },
            {
                "day": "Lundi",
                "condition": "cloudy",
                "temp": 10,
                "description": "Nuageux"
            }
        ][:days]
    }

def map_weather_condition(condition: str) -> str:
    """
    Mappe les conditions météo OpenWeather vers des catégories simples
    """
    condition = condition.lower()
    
    if "clear" in condition or "sun" in condition:
        return "sunny"
    elif "rain" in condition or "drizzle" in condition:
        return "rain"
    elif "cloud" in condition:
        return "cloudy"
    elif "snow" in condition:
        return "snow"
    elif "storm" in condition or "thunder" in condition:
        return "storm"
    else:
        return "cloudy"

def interpret_weather(forecast: Dict) -> str:
    """
    Interprète la météo pour donner des recommandations
    
    Returns:
        "indoor" si mauvais temps, "outdoor" si beau temps, "mixed" si mitigé
    """
    # Compter les jours de pluie
    rainy_days = sum(1 for day in forecast.get("forecast", []) 
                     if day["condition"] in ["rain", "storm"])
    
    total_days = len(forecast.get("forecast", []))
    
    if total_days == 0:
        return "mixed"
    
    rain_ratio = rainy_days / total_days
    
    if rain_ratio > 0.6:
        return "indoor"  # Majorité de pluie
    elif rain_ratio < 0.3:
        return "outdoor"  # Beau temps
    else:
        return "mixed"  # Mitigé

# ====================================
# TESTS
# ====================================

if __name__ == "__main__":
    print("Test météo...")
    
    forecast = get_weather_forecast(days=3)
    print(f"\nActuellement: {forecast['current']['temp']}°C - {forecast['current']['description']}")
    
    print("\nPrévisions:")
    for day in forecast['forecast']:
        print(f"  {day['day']}: {day['temp']}°C - {day['description']}")
    
    recommendation = interpret_weather(forecast)
    print(f"\nRecommandation: activités en {recommendation}")
