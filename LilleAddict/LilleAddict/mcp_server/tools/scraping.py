"""
Tools de scraping pour Lille Addict
"""

import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import re
import logging

logger = logging.getLogger(__name__)

BASE_URL = "https://lilleaddict.fr"

# ====================================
# USE CASE 1: ÉVÉNEMENTS DU WEEK-END
# ====================================

def get_weekend_events() -> Dict:
    """
    Scrape les événements du week-end depuis Lille Addict
    
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
                    "hours": "20h-22h"
                }
            ]
        }
    """
    try:
        logger.info("Scraping événements du week-end...")
        
        # TODO: Implémente le scraping réel
        # Pour le MVP, retour de données mock
        
        return {
            "week_dates": "9-15 janvier 2026",
            "events": [
                {
                    "title": "Concert Jazz au Mood",
                    "description": "Soirée jazz avec le trio local",
                    "dates": "Samedi 11 janvier",
                    "price": "Gratuit",
                    "location": "Le Mood, Lille",
                    "hours": "20h-23h"
                },
                {
                    "title": "Marché créateurs",
                    "description": "Artisans locaux et créateurs lillois",
                    "dates": "Dimanche 12 janvier",
                    "price": "Entrée libre",
                    "location": "Grand Place, Lille",
                    "hours": "10h-18h"
                },
                {
                    "title": "Escape Game en plein air",
                    "description": "Parcours énigmes dans le Vieux-Lille",
                    "dates": "Tout le week-end",
                    "price": "15€/personne",
                    "location": "Départ Place du Théâtre",
                    "hours": "14h-17h"
                }
            ]
        }
        
        # VERSION RÉELLE À IMPLÉMENTER:
        """
        # 1. Récupérer la page principale
        response = requests.get(f"{BASE_URL}/que-faire-a-lille-ce-week-end/")
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2. Trouver l'article le plus récent
        latest_article = soup.find('article')
        article_link = latest_article.find('a', href=True)
        article_url = article_link['href']
        
        # 3. Récupérer l'article complet
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.content, 'html.parser')
        
        # 4. Extraire les événements (sections H2)
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
            
            # Parser les infos des éléments suivants
            for sibling in h2.find_next_siblings():
                if sibling.name == 'h2':
                    break
                
                text = sibling.get_text().strip()
                
                # Identifier dates, prix, lieu...
                # TODO: logique de parsing
                
                events.append(event)
        
        return {
            "week_dates": extracted_dates,
            "events": events
        }
        """
        
    except Exception as e:
        logger.error(f"Erreur scraping événements: {str(e)}")
        return {
            "week_dates": "",
            "events": []
        }

# ====================================
# USE CASE 2: RESTAURANTS
# ====================================

def search_restaurants(
    cuisine: str = None,
    diet: str = None,
    price_range: str = None,
    atmosphere: str = None,
    location: str = None
) -> List[Dict]:
    """
    Recherche de restaurants selon critères
    
    Args:
        cuisine: Type de cuisine (italien, japonais, etc.)
        diet: Régime (végétarien, vegan, etc.)
        price_range: Prix (€, €€, €€€)
        atmosphere: Ambiance (terrasse, romantique, etc.)
        location: Quartier (Vieux-Lille, Wazemmes, etc.)
    
    Returns:
        Liste de restaurants
    """
    try:
        logger.info(f"Recherche restaurants - cuisine:{cuisine}, diet:{diet}")
        
        # TODO: Implémente le scraping réel
        # Mock data pour le MVP
        
        restaurants_mock = [
            {
                "name": "La Bottega",
                "cuisine": "Italien",
                "description": "Restaurant italien authentique avec produits frais",
                "price_range": "€€",
                "location": "Vieux-Lille",
                "dietary": "Options végétariennes"
            },
            {
                "name": "Sushi Shop",
                "cuisine": "Japonais",
                "description": "Sushis et spécialités japonaises",
                "price_range": "€€",
                "location": "Centre Lille"
            }
        ]
        
        # Filtrer selon critères
        results = []
        for resto in restaurants_mock:
            if cuisine and cuisine.lower() not in resto['cuisine'].lower():
                continue
            if diet and diet.lower() not in resto.get('dietary', '').lower():
                continue
            results.append(resto)
        
        return results
        
    except Exception as e:
        logger.error(f"Erreur recherche restaurants: {str(e)}")
        return []

# ====================================
# USE CASE 3: BARS
# ====================================

def search_bars(
    drink_type: str = None,
    activity: str = None,
    atmosphere: str = None,
    location: str = None
) -> List[Dict]:
    """
    Recherche de bars selon critères
    """
    try:
        logger.info(f"Recherche bars - drink:{drink_type}, activity:{activity}")
        
        # TODO: Implémente le scraping réel
        # Mock data
        
        bars_mock = [
            {
                "name": "Le Mood",
                "description": "Bar à cocktails avec ambiance jazz",
                "drink_type": "Cocktails",
                "atmosphere": "Jazz, Cosy",
                "location": "Centre Lille"
            },
            {
                "name": "La Capsule",
                "description": "Bar à bières artisanales",
                "drink_type": "Bières",
                "atmosphere": "Décontracté",
                "location": "Wazemmes"
            }
        ]
        
        # Filtrer
        results = []
        for bar in bars_mock:
            if drink_type and drink_type.lower() not in bar['drink_type'].lower():
                continue
            if atmosphere and atmosphere.lower() not in bar.get('atmosphere', '').lower():
                continue
            results.append(bar)
        
        return results
        
    except Exception as e:
        logger.error(f"Erreur recherche bars: {str(e)}")
        return []

# ====================================
# USE CASE 4: ACTIVITÉS INTÉRIEUR/EXTÉRIEUR
# ====================================

def get_indoor_activities() -> List[Dict]:
    """Activités en intérieur (si il pleut)"""
    try:
        logger.info("Récupération activités intérieur...")
        
        # TODO: Scraper depuis https://lilleaddict.fr/que-faire-a-lille-quand-il-pleut
        
        return [
            {
                "name": "Musée de l'Illusion",
                "description": "Musée interactif avec illusions d'optique",
                "category": "Musée",
                "location": "Lille centre"
            },
            {
                "name": "Escape Game XXL",
                "description": "Escape game géant sur plusieurs étages",
                "category": "Jeux",
                "location": "Euralille"
            }
        ]
        
    except Exception as e:
        logger.error(f"Erreur activités intérieur: {str(e)}")
        return []

def get_outdoor_activities() -> List[Dict]:
    """Activités en extérieur (si il fait beau)"""
    try:
        logger.info("Récupération activités extérieur...")
        
        # TODO: Scraper activités extérieures
        
        return [
            {
                "name": "Parc de la Citadelle",
                "description": "Grand parc pour balade, jogging, pique-nique",
                "category": "Parc",
                "location": "Lille"
            },
            {
                "name": "Parc Barbieux",
                "description": "Magnifique parc à Roubaix",
                "category": "Parc",
                "location": "Roubaix"
            }
        ]
        
    except Exception as e:
        logger.error(f"Erreur activités extérieur: {str(e)}")
        return []


# ====================================
# HELPERS
# ====================================

def clean_text(text: str) -> str:
    """Nettoie un texte"""
    if not text:
        return ""
    # Supprimer espaces multiples
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_price(text: str) -> str:
    """Extrait le prix d'un texte"""
    # Chercher patterns: "15€", "À partir de 20€", "Gratuit"
    if 'gratuit' in text.lower() or 'prix libre' in text.lower():
        return "Gratuit"
    
    price_match = re.search(r'(\d+)\s*€', text)
    if price_match:
        return f"{price_match.group(1)}€"
    
    return ""

# ====================================
# TESTS
# ====================================

if __name__ == "__main__":
    print("Test scraping...")
    
    print("\n=== Événements ===")
    events = get_weekend_events()
    print(f"Trouvé {len(events['events'])} événements")
    for event in events['events'][:2]:
        print(f"  - {event['title']}")
    
    print("\n=== Restaurants ===")
    restaurants = search_restaurants(cuisine="italien")
    print(f"Trouvé {len(restaurants)} restaurants italiens")
    
    print("\n=== Bars ===")
    bars = search_bars(drink_type="cocktail")
    print(f"Trouvé {len(bars)} bars à cocktails")
