import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

def format_time(unix_time, timezone_offset):
    utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)  # Convertir en datetime timezone-aware UTC
    local_time = utc_time + timedelta(seconds=timezone_offset)    # Ajouter l'offset du fuseau horaire local
    return local_time.strftime("%H:%M:%S")



# Fonction pour récupérer les données météo
def get_weather_data(city, api_key="67708d0873143f197778ef5ca2e8d90f"):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    return data


# Afficher les informations météo de base
def display_weather(data):
    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]

    st.write(f"**Ville**: {data['name']}")
    st.write(f"**Température**: {main['temp']}°C")
    st.write(f"**Humidité**: {main['humidity']}%")
    st.write(f"**Condition**: {weather['description'].capitalize()}")
    st.write(f"**Vent**: {wind['speed']} m/s")


# Afficher la carte
def display_map(data):
    coords = pd.DataFrame({
        'latitude': [data["coord"]["lat"]],
        'longitude': [data["coord"]["lon"]]
    })
    st.map(coords)


# Afficher les détails météo
def display_detailed_weather(data):
    main = data["main"]
    sys = data["sys"]

    st.write(f"**Pression**: {main['pressure']} hPa")
    st.write(f"**Visibilité**: {data['visibility']} mètres")
    st.write(f"**Lever du soleil**: {format_time(sys['sunrise'], data['timezone'])}")
    st.write(f"**Coucher du soleil**: {format_time(sys['sunset'], data['timezone'])}")


from datetime import datetime, timedelta, timezone

def format_time(unix_time, timezone_offset):
    utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)  # Convertir en datetime timezone-aware UTC
    local_time = utc_time + timedelta(seconds=timezone_offset)    # Ajouter l'offset du fuseau horaire local
    return local_time.strftime("%H:%M:%S")



# Interface utilisateur principale
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

    st.markdown('<h1 class="title">Application Météo Personnalisée</h1>', unsafe_allow_html=True)
    st.markdown('<p class="info">Entrez le nom d’une ville pour connaître sa météo !</p>', unsafe_allow_html=True)

    city = st.text_input("Entrez le nom de la ville :", "Paris")

    if st.button("Obtenir la météo"):
        if city:
            api_key = "67708d0873143f197778ef5ca2e8d90f"  # Remplacez par votre clé API
            weather_data = get_weather_data(city, api_key)

            if weather_data["cod"] != "404":
                tab1, tab2, tab3 = st.tabs(["Résumé", "Carte", "Détails"])

                with tab1:
                    st.header("Résumé météo")
                    display_weather(weather_data)

                with tab2:
                    st.header("Carte")
                    display_map(weather_data)

                with tab3:
                    st.header("Détails météo")
                    display_detailed_weather(weather_data)
            else:
                st.error("Ville non trouvée !")
        else:
            st.warning("Veuillez entrer un nom de ville valide.")


if __name__ == "__main__":
    main()
