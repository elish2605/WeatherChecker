import streamlit as st
from datetime import datetime
import pytz
from timezonefinder import TimezoneFinder
import requests  # Pour récupérer les données météo


# Fonction pour obtenir la météo (remplacez par votre propre fonction)
def get_weather_data(api_key, city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Impossible de récupérer les données météo.")
        return None


# Intégrer les fuseaux horaires
def display_weather_with_time(api_key, city):
    data = get_weather_data(api_key, city)
    if data:
        st.write(f"### Météo pour {data['name']}, {data['sys']['country']}")

        # Afficher les coordonnées
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        st.write(f"Latitude : {lat}, Longitude : {lon}")

        # Fuseau horaire et heure locale
        tf = TimezoneFinder()
        timezone_name = tf.timezone_at(lat=lat, lng=lon)

        if timezone_name:
            local_time = get_local_time(timezone_name)
            st.write(f"**Heure locale : {local_time}**")
        else:
            st.write("Impossible de déterminer le fuseau horaire.")

        # Afficher les conditions météo
        weather = data['weather'][0]['description']
        temperature = data['main']['temp']
        st.write(f"**Conditions :** {weather}")
        st.write(f"**Température :** {temperature} °C")

def get_local_time(timezone_name):
    """Récupère l'heure locale pour un fuseau horaire donné."""
    try:
        tz = pytz.timezone(timezone_name)
        local_time = datetime.now(tz)
        return local_time.strftime("%A, %B %d, %Y, %I:%M %p")
    except pytz.UnknownTimeZoneError:
        return "Fuseau horaire inconnu"

# Streamlit App
def main():
    st.title("Weather Checker avec heure locale")

    # Clé API OpenWeatherMap (insérez votre clé API ici)
    api_key = st.secrets["openweather"]["api_key"]

    # Saisie de la ville
    city = st.text_input("Entrez une ville :")
    if city:
        display_weather_with_time(api_key, city)


if __name__ == "__main__":
    main()
