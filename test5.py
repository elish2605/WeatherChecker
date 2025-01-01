import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configuration
API_KEY = "67708d0873143f197778ef5ca2e8d90f"  # Remplacez par votre clé API OpenWeatherMap


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


# Fonction pour récupérer les prévisions actuelles et sur 5 jours
def get_weather_forecast(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    response.raise_for_status()
    return response.json().get("list", [])


# Fonction pour afficher la météo actuelle
def display_current_weather(weather_data):
    st.subheader("Météo actuelle")
    current_weather = weather_data[0]
    current_time = datetime.utcfromtimestamp(current_weather["dt"]).strftime("%H:%M")
    temp = current_weather["main"]["temp"]
    condition = current_weather["weather"][0]["description"]
    icon_url = f"http://openweathermap.org/img/wn/{current_weather['weather'][0]['icon']}@2x.png"

    st.write(f"**Heure actuelle :** {current_time}")
    st.write(f"**Température actuelle :** {temp}°C")
    st.write(f"**Conditions :** {condition}")
    st.image(icon_url, width=50)


# Fonction pour afficher les prévisions à venir sur 5 jours
def display_forecast(forecast_data):
    st.subheader("Prévisions sur 5 jours")
    forecast_list = []

    # Récupérer les prévisions par jour (toutes les 3 heures dans l'API gratuite)
    for day_data in forecast_data:
        time = datetime.utcfromtimestamp(day_data["dt"]).strftime("%Y-%m-%d %H:%M")
        temp = day_data["main"]["temp"]
        condition = day_data["weather"][0]["description"]
        icon_url = f"http://openweathermap.org/img/wn/{day_data['weather'][0]['icon']}@2x.png"
        forecast_list.append({"Heure": time, "Température (°C)": temp, "Conditions": condition, "Icône": icon_url})

    # Convertir en DataFrame
    df = pd.DataFrame(forecast_list)

    # Afficher le tableau des prévisions
    for index, row in df.iterrows():
        st.write(f"**{row['Heure']}** : {row['Température (°C)']}°C, {row['Conditions']}")
        st.image(row["Icône"], width=50)

    return df


# Interface utilisateur principale avec Streamlit
def main():
    st.title("Météo par Ville - Prévisions sur 5 jours")
    st.sidebar.title("Paramètres")

    # Entrée du nom de la ville avec un key unique
    city_name = st.sidebar.text_input("Nom de la ville", value="Paris", key="city_name_input")

    # Vérifier si une ville a été entrée
    if city_name:
        # Récupération des données météo
        try:
            lat, lon = get_city_coordinates(city_name, API_KEY)
            forecast_data = get_weather_forecast(lat, lon, API_KEY)
            st.success(f"Données récupérées avec succès pour {city_name} !")
        except Exception as e:
            st.error(f"Erreur lors de la récupération des données : {e}")
            return

        # Afficher les données dans l'application
        display_current_weather(forecast_data)
        display_forecast(forecast_data)
    else:
        st.warning("Veuillez entrer le nom d'une ville.")

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


# Fonction pour afficher la météo actuelle
def display_current_weather(weather_data):
    st.subheader("Météo actuelle")
    current_weather = weather_data[0]
    current_time = datetime.utcfromtimestamp(current_weather["dt"]).strftime("%H:%M")
    temp = current_weather["main"]["temp"]
    condition = current_weather["weather"][0]["description"]
    icon_url = f"http://openweathermap.org/img/wn/{current_weather['weather'][0]['icon']}@2x.png"

    st.write(f"**Heure actuelle :** {current_time}")
    st.write(f"**Température actuelle :** {temp}°C")
    st.write(f"**Conditions :** {condition}")
    st.image(icon_url, width=50)


# Fonction pour afficher les prévisions à venir sur 5 jours
def display_forecast(forecast_data):
    st.subheader("Prévisions sur 5 jours")
    forecast_list = []

    # Récupérer les prévisions par jour (toutes les 3 heures dans l'API gratuite)
    for day_data in forecast_data:
        time = datetime.utcfromtimestamp(day_data["dt"]).strftime("%Y-%m-%d %H:%M")
        temp = day_data["main"]["temp"]
        condition = day_data["weather"][0]["description"]
        icon_url = f"http://openweathermap.org/img/wn/{day_data['weather'][0]['icon']}@2x.png"
        forecast_list.append({"Heure": time, "Température (°C)": temp, "Conditions": condition, "Icône": icon_url})

    # Convertir en DataFrame
    df = pd.DataFrame(forecast_list)

    # Afficher le tableau des prévisions
    for index, row in df.iterrows():
        st.write(f"**{row['Heure']}** : {row['Température (°C)']}°C, {row['Conditions']}")
        st.image(row["Icône"], width=50)

    return df


# Interface utilisateur principale avec Streamlit
def main():
    st.title("Météo par Ville - Prévisions sur 5 jours")
    st.sidebar.title("Paramètres")

    # Entrée du nom de la ville
    city_name = st.sidebar.text_input("Nom de la ville", value="Paris")

    # Récupération des données météo
    try:
        lat, lon = get_city_coordinates(city_name, API_KEY)
        forecast_data = get_weather_forecast(lat, lon, API_KEY)
        st.success(f"Données récupérées avec succès pour {city_name} !")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données : {e}")
        return

    # Afficher les données dans l'application
    display_current_weather(forecast_data)
    display_forecast(forecast_data)

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
