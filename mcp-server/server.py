from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# --- Endpoint météo ---
@app.route("/weather", methods=["GET"])
def get_weather():
    # Expects ?lat=...&lon=...
    lat = request.args.get("lat", default="50.6292")  # Lille latitude par défaut
    lon = request.args.get("lon", default="3.0573")   # Lille longitude par défaut

    # Open-Meteo API
    api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    try:
        response = requests.get(api_url, timeout=5)
        data = response.json()
        return jsonify({
            "status": "success",
            "data": data.get("current_weather", {})
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Endpoint restaurants ---
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    try:
        url = "https://www.restaurantsdelille.com/"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        restaurants = []

        # Exemple : récupérer les noms et types de restaurants
        for r in soup.select(".restaurant-item"):  # À adapter selon le HTML exact
            name = r.select_one(".restaurant-name")
            category = r.select_one(".restaurant-category")
            if name:
                restaurants.append({
                    "name": name.get_text(strip=True),
                    "category": category.get_text(strip=True) if category else ""
                })

        return jsonify({
            "status": "success",
            "restaurants": restaurants
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Test serveur ---
@app.route("/")
def home():
    return jsonify({"status": "ok", "message": "MCP Server is running"})

# --- Lancement serveur ---
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
