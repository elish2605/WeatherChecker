import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta, timezone

# Function to format the time with timezone offset
def format_time(unix_time, timezone_offset):
    utc_time = datetime.fromtimestamp(unix_time, tz=timezone.utc)  # Convert to UTC-aware datetime
    local_time = utc_time + timedelta(seconds=timezone_offset)    # Add local timezone offset
    return local_time.strftime("%H:%M:%S")


# Function to get weather data
def get_weather_data(city, api_key="67708d0873143f197778ef5ca2e8d90f"):
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    return data


# Display basic weather information
def display_weather(data):
    main = data["main"]
    weather = data["weather"][0]
    wind = data["wind"]

    st.write(f"**City**: {data['name']}")
    st.write(f"**Temperature**: {main['temp']}°C")
    st.write(f"**Humidity**: {main['humidity']}%")
    st.write(f"**Condition**: {weather['description'].capitalize()}")
    st.write(f"**Wind**: {wind['speed']} m/s")


# Display the map
def display_map(data):
    coords = pd.DataFrame({
        'latitude': [data["coord"]["lat"]],
        'longitude': [data["coord"]["lon"]]
    })
    st.map(coords)


# Display detailed weather information
def display_detailed_weather(data):
    main = data["main"]
    sys = data["sys"]

    st.write(f"**Pressure**: {main['pressure']} hPa")
    st.write(f"**Visibility**: {data['visibility']} meters")
    st.write(f"**Sunrise**: {format_time(sys['sunrise'], data['timezone'])}")
    st.write(f"**Sunset**: {format_time(sys['sunset'], data['timezone'])}")


# Main user interface
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
            api_key = "67708d0873143f197778ef5ca2e8d90f"  # Replace with your API key
            weather_data = get_weather_data(city, api_key)

            if weather_data["cod"] != "404":
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
                st.error("City not found!")
        else:
            st.warning("Please enter a valid city name.")


if __name__ == "__main__":
    main()
