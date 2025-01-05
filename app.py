import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz
from timezonefinder import TimezoneFinder
import json
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static


# --- 1. Functions for plotting temperature and humidity ---
def plot_temperature(data):
    if "main" not in data:
        st.error("Weather data does not contain 'main' information.")
        return

    temperature = data["main"]["temp"]
    city_name = data["name"]

    plt.figure(figsize=(6, 4))
    plt.plot([0, 1], [temperature, temperature], marker='o', color='b', label=f'Temperature in {city_name}')
    plt.title(f"Current Temperature in {city_name}")
    plt.xlabel('Time')
    plt.ylabel('Temperature (°C)')
    plt.legend()
    plt.grid(True)

    st.pyplot(plt)


def plot_humidity(data):
    if "main" not in data:
        st.error("Weather data does not contain 'main' information.")
        return

    humidity = data["main"]["humidity"]
    city_name = data["name"]

    plt.figure(figsize=(6, 4))
    plt.bar(city_name, humidity, color='c', label=f'Humidity in {city_name}')
    plt.title(f"Humidity in {city_name}")
    plt.ylabel('Humidity (%)')
    plt.legend()

    st.pyplot(plt)


# --- 2. Settings functions ---
SETTINGS_FILE = "settings.json"


def load_settings():
    """Load settings from the JSON file."""
    try:
        with open(SETTINGS_FILE, "r") as file:
            settings = json.load(file)
        return settings
    except FileNotFoundError:
        return {
            "default_location": "Paris",
            "temperature_unit": "metric",  # 'metric' for Celsius, 'imperial' for Fahrenheit
            "favorite_locations": ["Paris"]
        }

settings = load_settings()

def save_settings(settings):
    """Save updated settings to the JSON file."""
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)


# --- 3. Weather and time functions ---
def format_time(unix_time, timezone_offset):
    """Format the time according to the given timezone offset."""
    utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)
    local_time = utc_time + timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %B %d, %Y, %I:%M %p")


@st.cache_data
def get_weather_data(city, api_key=None):
    """Fetch weather data using OpenWeather API."""
    if api_key is None:
        api_key = st.secrets["openweather"]["api_key"]

    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units={settings['temperature_unit']}"
    response = requests.get(complete_url)
    data = response.json()

    if response.status_code == 200:
        return data
    else:
        st.error(f"Failed to retrieve weather data: {data.get('message', 'Unknown error')}")
        return None


def get_local_time(timezone_name):
    """Fetch local time for a given timezone."""
    try:
        tz = pytz.timezone(timezone_name)
        local_time = datetime.now(tz)
        return local_time.strftime("%A, %B %d, %Y, %I:%M %p")
    except pytz.UnknownTimeZoneError:
        return "Unknown timezone"


# --- 4. Display functions ---
def display_weather(data, timezone_name=None):
    """Display basic weather information."""
    if "main" not in data:
        st.error("Weather data does not contain expected 'main' information.")
        return

    weather_main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]

    user_local_time = datetime.now().strftime("%A, %B %d, %Y, %I:%M %p")

    st.write(f"**City**: {data['name']}, {data['sys']['country']}")
    st.write(f"**Latitude**: {lat}")
    st.write(f"**Longitude**: {lon}")

    if timezone_name:
        city_local_time = get_local_time(timezone_name)
        st.write(f"**Local Time (Your Location):** {user_local_time}")
        st.write(f"**Local Time (City):** {city_local_time}")

    st.write(f"**Temperature**: {weather_main['temp']}°C")
    st.write(f"**Humidity**: {weather_main['humidity']}%")
    st.write(f"**Condition**: {weather['description'].capitalize()}")
    st.write(f"**Wind Speed**: {wind['speed']} m/s")

    display_weather_icon(weather)


def display_weather_icon(weather):
    """Display the weather icon."""
    icon_code = weather.get("icon", "")
    if icon_code:
        icon_url = f"https://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url, width=100)
    else:
        st.warning("Weather icon not available.")


def display_detailed_weather(data):
    """Display detailed weather information."""
    if "main" not in data or "sys" not in data:
        st.error("Detailed weather data is missing.")
        return

    weather_main = data["main"]
    sys = data["sys"]

    st.write(f"**Pressure**: {weather_main['pressure']} hPa")
    st.write(f"**Visibility**: {data['visibility']} meters")
    st.write(f"**Sunrise**: {format_time(sys['sunrise'], data['timezone'])}")
    st.write(f"**Sunset**: {format_time(sys['sunset'], data['timezone'])}")


def display_map(data):
    """Display map with the city coordinates."""
    if "coord" in data:
        lat = data["coord"]["lat"]
        lon = data["coord"]["lon"]

        if lat is None or lon is None:
            st.warning("Coordinates are missing for this city.")
            return

        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup="Requested Location").add_to(m)
        folium_static(m)
    else:
        st.warning("Coordinates not available for this city.")


# --- 5. Settings functions ---
def display_and_update_settings():
    """Allow the user to change settings."""
    st.write("### Change Settings")

    new_location = st.text_input("Set Default Location", settings['default_location'])
    new_temp_unit = st.selectbox("Select Temperature Unit", ["metric", "imperial"],
                                 index=0 if settings['temperature_unit'] == "metric" else 1)
    favorite_location = st.text_input("Add Favorite Location")

    st.write(f"**Favorite Locations**: {', '.join(settings['favorite_locations'])}")

    if st.button("Add Favorite Location"):
        if favorite_location and favorite_location not in settings['favorite_locations']:
            settings['favorite_locations'].append(favorite_location)
            save_settings(settings)
            st.success(f"'{favorite_location}' added to favorites!")
        else:
            st.warning("Location already in favorites or not provided.")

    if st.button("Save Settings"):
        settings['default_location'] = new_location
        settings['temperature_unit'] = new_temp_unit
        save_settings(settings)
        st.success("Settings saved successfully!")


# --- 6. Main Interface ---
def main():
    st.markdown(""" 
        <style> 
            body { background-color: #e0f7fa; } 
            .title { font-family: 'Arial', sans-serif; color: #00796b; text-align: center; font-size: 30px; } 
            .info { font-family: 'Arial', sans-serif; color: #004d40; margin: 10px 0; } 
        </style> 
    """, unsafe_allow_html=True)

    st.title("Weather Checker with Local Time")

    if "openweather" not in st.secrets:
        st.error("The OpenWeatherMap API key is missing in secrets.toml.")
        return

    api_key = st.secrets["openweather"]["api_key"]

    display_and_update_settings()

    city = st.text_input("Enter the city name:", settings['default_location'])

    if st.button("Get Weather"):
        if city:
            weather_data = get_weather_data(city, api_key)

            if weather_data:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                tf = TimezoneFinder()
                timezone_name = tf.timezone_at(lat=lat, lng=lon)

                with st.spinner('Fetching weather data...'):
                    tab1, tab2, tab3 = st.tabs(["Summary", "Map & Graphs", "Weather Details"])

                    with tab1:
                        st.header("Weather Summary")
                        display_weather(weather_data, timezone_name)

                    with tab2:
                        st.header("Map & Graphs")
                        display_map(weather_data)
                        plot_temperature(weather_data)
                        plot_humidity(weather_data)

                    with tab3:
                        st.header("Weather Details")
                        display_detailed_weather(weather_data)
            else:
                st.error("City not found or failed to retrieve data.")
        else:
            st.warning("Please enter a valid city name.")


if __name__ == "__main__":
    main()
