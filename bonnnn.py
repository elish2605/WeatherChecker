import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

st.set_option('client.showErrorDetails', True)

# Fonction pour formater l'heure avec l'offset du fuseau horaire
def format_time(unix_time, timezone_offset):
    utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)  # Convertir en datetime UTC
    local_time = utc_time + timedelta(seconds=timezone_offset)  # Ajouter l'offset du fuseau horaire local
    return local_time.strftime("%H:%M:%S")


# Fonction pour récupérer les données météo
def get_weather_data(city, api_key=None):
    if api_key is None:
        api_key = os.getenv("OPENWEATHER_API_KEY")  # Charger la clé API depuis les variables d'environnement

    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    # Vérification si la réponse est valide
    if response.status_code == 200:
        return data
    else:
        st.error(f"Failed to retrieve weather data: {data.get('message', 'Unknown error')}")
        return None


# Afficher les informations météo de base
def display_weather(data):
    if "main" not in data:
        st.error("Weather data does not contain expected 'main' information.")
        st.write(data)  # Afficher le contenu de la réponse pour le débogage
        return

    weather_main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]

    st.write(f"**City**: {data['name']}")
    st.write(f"**Temperature**: {weather_main['temp']}°C")
    st.write(f"**Humidity**: {weather_main['humidity']}%")
    st.write(f"**Condition**: {weather['description'].capitalize()}")
    st.write(f"**Wind**: {wind['speed']} m/s")


# Afficher la carte
def display_map(data):
    coords = pd.DataFrame({
        'latitude': [data["coord"]["lat"]],
        'longitude': [data["coord"]["lon"]]
    })
    st.map(coords)


# Afficher les détails météo
def display_detailed_weather(data):
    if "main" not in data or "sys" not in data:
        st.error("Detailed weather data is missing.")
        return

    weather_main = data["main"]
    sys = data["sys"]

    st.write(f"**Pressure**: {weather_main['pressure']} hPa")
    st.write(f"**Visibility**: {data['visibility']} meters")
    st.write(f"**Sunrise**: {format_time(sys['sunrise'], data['timezone'])}")
    st.write(f"**Sunset**: {format_time(sys['sunset'], data['timezone'])}")


# Interface principale
def main():
    st.markdown("""
        <style>
            body {
                background-color: #e0f7fa;
            }
            .title {
                font-family: 'Arial', sans-serif;
                color: #00796b;
                text-align: center;
                font-size: 30px;
            }
            .info {
                font-family: 'Arial', sans-serif;
                color: #004d40;
                margin: 10px 0;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="title">Personalized Weather Application</h1>', unsafe_allow_html=True)
    st.markdown('<p class="info">Enter a city name to get its weather information!</p>', unsafe_allow_html=True)

    city = st.text_input("Enter the city name:", "Paris")

    if st.button("Get Weather"):
        if city:
            weather_data = get_weather_data(city)

            if weather_data:
                # Créer des onglets dynamiques avec Streamlit
                with st.spinner('Fetching weather data...'):
                    tab1, tab2, tab3 = st.tabs(["Summary", "Map", "Details"])

                    with tab1:
                        st.header("Weather Summary")
                        display_weather(weather_data)

                    with tab2:
                        st.header("Map")
                        display_map(weather_data)

                    with tab3:
                        st.header("Weather Details")
                        display_detailed_weather(weather_data)
            else:
                st.error("City not found or failed to retrieve data.")
        else:
            st.warning("Please enter a valid city name.")


if __name__ == "__main__":
    main()
