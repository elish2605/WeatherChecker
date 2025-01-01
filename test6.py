import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configuration
API_KEY = "2f86563393384a7294080afc9c3c1621"  # Remplacez par votre clé OpenWeatherMap

# Fonction pour récupérer les coordonnées géographiques d'une ville
def get_city_coordinates(city_name, api_key):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={api_key}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    if data:
        return data[0]["lat"], data[0]["lon"]
    else:
        raise ValueError("Ville introuvable. Vérifiez le nom de la ville.")

# Fonction pour récupérer les conditions météo actuelles
def get_current_weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

# Fonction pour récupérer les prévisions quotidiennes (plan gratuit)
def get_daily_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast/daily?lat={lat}&lon={lon}&cnt=7&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("list", [])

# Fonction pour afficher les conditions météo actuelles
def display_current_weather(weather_data):
    st.subheader("Conditions météo actuelles")
    temp = weather_data["main"]["temp"]
    condition = weather_data["weather"][0]["description"]
    icon_url = f"http://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png"
    st.write(f"**Température** : {temp}°C")
    st.write(f"**Conditions** : {condition}")
    st.image(icon_url, width=50)

# Fonction pour afficher un tableau des prévisions quotidiennes
def display_daily_forecast(daily_forecast):
    st.subheader("Prévisions quotidiennes")

    # Créer une liste pour afficher les données
    forecast_data = []
    for day_data in daily_forecast:
        date = datetime.utcfromtimestamp(day_data["dt"]).strftime("%Y-%m-%d")
        temp_min = day_data["temp"]["min"]
        temp_max = day_data["temp"]["max"]
        condition = day_data["weather"][0]["description"]
        icon_url = f"http://openweathermap.org/img/wn/{day_data['weather'][0]['icon']}@2x.png"
        forecast_data.append({"Date": date, "Température Min (°C)": temp_min, "Température Max (°C)": temp_max, "Conditions": condition, "Icône": icon_url})

    # Convertir en DataFrame
    df = pd.DataFrame(forecast_data)

    # Afficher un tableau avec des icônes météo
    for index, row in df.iterrows():
        st.write(f"**{row['Date']}** : Min {row['Température Min (°C)']}°C, Max {row['Température Max (°C)']}°C, {row['Conditions']}")
        st.image(row["Icône"], width=50)

    return df

# Interface utilisateur principale avec Streamlit
def main():
    st.title("Météo par Ville - Conditions Actuelles et Prévisions")
    st.sidebar.title("Paramètres")

    # Entrée du nom de la ville
    city_name = st.sidebar.text_input("Nom de la ville", value="Paris", key="city_input")

    # Récupération des données météo
    try:
        lat, lon = get_city_coordinates(city_name, API_KEY)
        current_weather = get_current_weather(lat, lon, API_KEY)
        daily_forecast = get_daily_forecast(lat, lon, API_KEY)
        st.success(f"Données récupérées avec succès pour {city_name} !")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return

    # Afficher les données dans l'application
    display_current_weather(current_weather)
    display_daily_forecast(daily_forecast)

    # Ajout de l'arrière-plan personnalisé
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Exécuter l'application
if __name__ == "__main__":
    main()
