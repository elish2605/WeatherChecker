import streamlit as st
import requests
from datetime import datetime, timezone
import pandas as pd

# Configuration
API_KEY = "67708d0873143f197778ef5ca2e8d90f"  # Remplacez par votre clé OpenWeatherMap

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

# Fonction pour récupérer les prévisions horaires depuis l'API One Call
def get_hourly_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("hourly", [])

# Fonction pour afficher un tableau interactif des prévisions
def display_hourly_forecast(hourly_forecast, start_hour=0, end_hour=24):
    st.subheader("Prévisions horaires")

    # Filtrer les prévisions selon l'intervalle sélectionné
    filtered_forecast = [
        hour_data for hour_data in hourly_forecast
        if start_hour <= datetime.fromtimestamp(hour_data["dt"]).hour < end_hour
    ]

    # Créer une liste pour afficher les données
    forecast_data = []
    for hour_data in filtered_forecast:
        local_time = datetime.fromtimestamp(hour_data["dt"], tz=timezone.utc).strftime("%H:%M")
        temp = hour_data["temp"]
        condition = hour_data["weather"][0]["description"]
        icon_url = f"http://openweathermap.org/img/wn/{hour_data['weather'][0]['icon']}@2x.png"
        forecast_data.append({"Heure": local_time, "Température (°C)": temp, "Conditions": condition, "Icône": icon_url})

    # Convertir en DataFrame
    df = pd.DataFrame(forecast_data)

    # Afficher un tableau avec des icônes météo
    for index, row in df.iterrows():
        st.write(f"**{row['Heure']}** : {row['Température (°C)']}°C, {row['Conditions']}")
        st.image(row["Icône"], width=50)

    return df

# Fonction pour afficher un graphique des variations de température
def display_temperature_chart(hourly_forecast, start_hour=0, end_hour=24):
    st.subheader("Graphique des variations de température")

    # Filtrer les prévisions
    times = [
        datetime.fromtimestamp(hour["dt"]).strftime("%H:%M")
        for hour in hourly_forecast if start_hour <= datetime.fromtimestamp(hour["dt"]).hour < end_hour
    ]
    temps = [hour["temp"] for hour in hourly_forecast if start_hour <= datetime.fromtimestamp(hour["dt"]).hour < end_hour]

    # Afficher le graphique
    chart_data = pd.DataFrame({"Heure": times, "Température (°C)": temps})
    st.line_chart(chart_data.set_index("Heure"))

# Interface utilisateur principale avec Streamlit
def main():
    st.title("Météo par Ville - Prévisions Heure par Heure")
    st.sidebar.title("Paramètres")

    # Entrée du nom de la ville
    city_name = st.sidebar.text_input("Nom de la ville", value="Paris")

    # Intervalle horaire
    start_hour = st.sidebar.slider("Heure de début", 0, 23, 0)
    end_hour = st.sidebar.slider("Heure de fin", start_hour + 1, 24, 24)

    # Récupération des données météo
    try:
        lat, lon = get_city_coordinates(city_name, API_KEY)
        hourly_forecast = get_hourly_forecast(lat, lon, API_KEY)
        st.success(f"Données récupérées avec succès pour {city_name} !")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return

    # Afficher les données dans l'application
    forecast_df = display_hourly_forecast(hourly_forecast, start_hour, end_hour)
    display_temperature_chart(hourly_forecast, start_hour, end_hour)

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
