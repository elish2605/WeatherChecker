import streamlit as st
import requests





def get_weather(city, api_key):
    """Fetch weather data from OpenWeatherMap API."""
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric"}
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return None


# Streamlit App
def main():
    st.title("Weather Checker 🌦️")
    st.markdown(
        """
        <style>
        body {
            background-color: #f0f8ff;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.write("Enter the name of a city to get its current weather data.")


    # Input field for the city
    city = st.text_input("City name:")
    api_key = "67708d0873143f197778ef5ca2e8d90f"  # Replace with your OpenWeatherMap API key

    # Display weather data when the user clicks the button
    if st.button("Check Weather"):
        if city:
            weather_data = get_weather(city, api_key)

            if weather_data:
                st.success(f"Weather in {city.capitalize()}: {weather_data['weather'][0]['description']}")
                st.metric("Temperature", f"{weather_data['main']['temp']}°C")
                st.metric("Humidity", f"{weather_data['main']['humidity']}%")
            else:
                st.error("Could not fetch weather data. Please check the city name or API key.")
        else:
            st.warning("Please enter a city name.")


if __name__ == "__main__":
    main()


