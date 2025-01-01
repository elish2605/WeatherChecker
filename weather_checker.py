import requests


# Fonction pour obtenir les données météo
def get_weather(city):
    api_key = "67708d0873143f197778ef5ca2e8d90f"  # Remplace par ta clé API
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Construire l'URL de requête
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "fr"}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        # Extraire des informations utiles
        city_name = data["name"]
        temp = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        humidity = data["main"]["humidity"]
        print(f"Ville: {city_name}\nTempérature: {temp}°C\nMétéo: {weather}\nHumidité: {humidity}%")
    else:
        print("Erreur : ville introuvable ou problème avec l'API.")


# Demander à l'utilisateur une ville
city = input("Entrez le nom d'une ville : ")
get_weather(city)