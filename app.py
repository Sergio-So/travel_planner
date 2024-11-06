from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

# Cargar las variables de entorno
load_dotenv()

app = Flask(__name__)

# Obtener las claves de API desde las variables de entorno
AMADEUS_API_KEY = os.getenv("AMADEUS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "")
OPENMETEO_API_KEY = os.getenv("OPENMETEO_API_KEY", "")  # No es necesario para OpenMeteo

# Endpoint para la propuesta de viaje (Amadeus)
@app.route('/trip-proposal', methods=['POST'])
def trip_proposal():
    data = request.get_json()
    origin = data.get("origin")
    destination = data.get("destination")
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    
    # Ejemplo de llamada a la API de Amadeus
    amadeus_url = "https://api.amadeus.com/v1/shopping/flight-offers"
    headers = {"Authorization": f"Bearer {AMADEUS_API_KEY}"}
    params = {
        "originLocationCode": origin,
        "destinationLocationCode": destination,
        "departureDate": start_date,
        "returnDate": end_date
    }
    response = requests.get(amadeus_url, headers=headers, params=params)
    return jsonify(response.json())

# Endpoint para generar una agenda diaria (Chat GPT)
@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    data = request.get_json()
    destination = data.get("destination")
    
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}
    prompt = f"Genera una agenda de viaje de 5 días para visitar {destination}."
    openai_url = "https://api.openai.com/v1/completions"
    payload = {
        "model": "text-davinci-003",
        "prompt": prompt,
        "max_tokens": 100
    }
    response = requests.post(openai_url, headers=headers, json=payload)
    return jsonify(response.json())

# Endpoint para obtener lugares a visitar (Geoapify)
@app.route('/places', methods=['POST'])
def places():
    data = request.get_json()
    destination = data.get("destination")
    
    geoapify_url = f"https://api.geoapify.com/v2/places?categories=tourism.sights&filter=place:{destination}&apiKey={GEOAPIFY_API_KEY}"
    response = requests.get(geoapify_url)
    return jsonify(response.json())

# Endpoint para obtener información del clima (OpenMeteo)
@app.route('/weather', methods=['POST'])
def weather():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    start_date = data.get("startDate")
    end_date = data.get("endDate")
    
    # Construcción de la URL de OpenMeteo
    openmeteo_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
    response = requests.get(openmeteo_url)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
