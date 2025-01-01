import streamlit as st
import requests
import pandas as pd


# Fonction pour récupérer les données météo à partir de l'API OpenWeatherMap
def get_weather_data(city, api_key="67708d0873143f197778ef5ca2e8d90f"):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    return data


# Fonction pour afficher les données météo
def display_weather(data):
    if data["cod"] != "404":
        main = data["main"]
        weather = data["weather"][0]
        wind = data["wind"]

        # Affichage des informations météorologiques
        st.write(f"**Ville**: {data['name']}")
        st.write(f"**Température**: {main['temp']}°C")
        st.write(f"**Humidité**: {main['humidity']}%")
        st.write(f"**Condition**: {weather['description'].capitalize()}")
        st.write(f"**Vent**: {wind['speed']} m/s")

        # Afficher la carte avec les coordonnées GPS
        coords = {
            'latitude': data["coord"]["lat"],
            'longitude': data["coord"]["lon"]
        }
        st.map(pd.DataFrame([coords]))

    else:
        st.error("Ville non trouvée !")


# Interface utilisateur Streamlit
def main():
    st.title("Application Météo")
    st.markdown("""
        Cette application vous permet de récupérer la météo actuelle d'une ville en utilisant l'API OpenWeatherMap.
    """)

    # Entrée de l'utilisateur pour le nom de la ville
    city = st.text_input("Entrez le nom de la ville :", "Paris")

    # Bouton pour soumettre la recherche
    if st.button("Obtenir la météo"):
        if city:
            api_key = "67708d0873143f197778ef5ca2e8d90f"  # Remplacez par votre clé API
            weather_data = get_weather_data(city, api_key)
            display_weather(weather_data)
        else:
            st.warning("Veuillez entrer un nom de ville valide.")


if __name__ == "__main__":
    main()
