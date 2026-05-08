import streamlit as st
import requests

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Weather App", page_icon="🌤️", layout="centered")

st.title("🌤️ Weather App")
st.markdown("Get current weather conditions for any city using the free [wttr.in](https://wttr.in) service — no API key required.")

# ── Input ─────────────────────────────────────────────────────────────────────
city = st.text_input("Enter a city name", placeholder="e.g. London, Tokyo, New York")

WEATHER_CODES = {
    113: ("☀️", "Sunny / Clear"),
    116: ("⛅", "Partly Cloudy"),
    119: ("☁️", "Cloudy"),
    122: ("☁️", "Overcast"),
    143: ("🌫️", "Mist"),
    176: ("🌦️", "Patchy Rain"),
    179: ("🌨️", "Patchy Snow"),
    182: ("🌧️", "Sleet"),
    185: ("🌧️", "Freezing Drizzle"),
    200: ("⛈️", "Thundery Outbreaks"),
    227: ("🌨️", "Blowing Snow"),
    230: ("❄️", "Blizzard"),
    248: ("🌫️", "Fog"),
    260: ("🌫️", "Freezing Fog"),
    263: ("🌦️", "Light Drizzle"),
    266: ("🌧️", "Drizzle"),
    281: ("🌧️", "Freezing Drizzle"),
    284: ("🌧️", "Heavy Freezing Drizzle"),
    293: ("🌦️", "Light Rain"),
    296: ("🌧️", "Rain"),
    299: ("🌧️", "Moderate Rain"),
    302: ("🌧️", "Heavy Rain"),
    305: ("🌧️", "Heavy Rain"),
    308: ("🌧️", "Very Heavy Rain"),
    311: ("🌧️", "Light Sleet"),
    314: ("🌧️", "Moderate Sleet"),
    317: ("🌧️", "Light Sleet"),
    320: ("🌨️", "Moderate Snow"),
    323: ("🌨️", "Patchy Light Snow"),
    326: ("🌨️", "Light Snow"),
    329: ("❄️", "Patchy Moderate Snow"),
    332: ("❄️", "Moderate Snow"),
    335: ("❄️", "Patchy Heavy Snow"),
    338: ("❄️", "Heavy Snow"),
    350: ("🌧️", "Ice Pellets"),
    353: ("🌦️", "Light Rain Shower"),
    356: ("🌧️", "Rain Shower"),
    359: ("🌧️", "Torrential Rain"),
    362: ("🌧️", "Light Sleet Shower"),
    365: ("🌧️", "Sleet Shower"),
    368: ("🌨️", "Light Snow Shower"),
    371: ("❄️", "Heavy Snow Shower"),
    374: ("🌧️", "Light Ice Pellets"),
    377: ("🌧️", "Ice Pellets"),
    386: ("⛈️", "Light Thunderstorm"),
    389: ("⛈️", "Heavy Thunderstorm"),
    392: ("⛈️", "Patchy Light Snow + Thunder"),
    395: ("⛈️", "Heavy Snow + Thunder"),
}


def fetch_weather(city_name: str) -> dict:
    """Fetch current weather from wttr.in JSON API."""
    url = f"https://wttr.in/{requests.utils.quote(city_name)}?format=j1"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    return resp.json()


def display_weather(data: dict, city_name: str):
    current = data["current_condition"][0]
    nearest = data["nearest_area"][0]

    area = nearest["areaName"][0]["value"]
    country = nearest["country"][0]["value"]
    location_str = f"{area}, {country}"

    temp_c = current["temp_C"]
    temp_f = current["temp_F"]
    feels_c = current["FeelsLikeC"]
    feels_f = current["FeelsLikeF"]
    humidity = current["humidity"]
    wind_kmph = current["windspeedKmph"]
    wind_dir = current["winddir16Point"]
    visibility = current["visibility"]
    pressure = current["pressure"]
    uv_index = current.get("uvIndex", "N/A")
    weather_code = int(current["weatherCode"])
    description = current["weatherDesc"][0]["value"]
    emoji, _ = WEATHER_CODES.get(weather_code, ("🌡️", description))

    st.subheader(f"{emoji} {description}")
    st.caption(f"📍 {location_str}")

    col1, col2, col3 = st.columns(3)
    col1.metric("🌡️ Temperature", f"{temp_c}°C / {temp_f}°F")
    col2.metric("🤔 Feels Like", f"{feels_c}°C / {feels_f}°F")
    col3.metric("💧 Humidity", f"{humidity}%")

    col4, col5, col6 = st.columns(3)
    col4.metric("💨 Wind", f"{wind_kmph} km/h {wind_dir}")
    col5.metric("👁️ Visibility", f"{visibility} km")
    col6.metric("🔵 Pressure", f"{pressure} hPa")

    col7, col8 = st.columns(2)
    col7.metric("☀️ UV Index", uv_index)

    # 3-day forecast
    st.divider()
    st.subheader("📅 3-Day Forecast")
    weather_days = data.get("weather", [])
    fcols = st.columns(len(weather_days))
    for i, day in enumerate(weather_days):
        date = day["date"]
        max_c = day["maxtempC"]
        min_c = day["mintempC"]
        max_f = day["maxtempF"]
        min_f = day["mintempF"]
        midday = day["hourly"][4] if len(day["hourly"]) > 4 else (day["hourly"][0] if day["hourly"] else None)
        noon_humidity = midday["humidity"] if midday else "N/A"
        day_desc = midday["weatherDesc"][0]["value"] if midday else ""
        day_code = int(midday["weatherCode"]) if midday else 113
        day_emoji, _ = WEATHER_CODES.get(day_code, ("🌡️", day_desc))
        with fcols[i]:
            st.markdown(f"**{date}**")
            st.markdown(f"{day_emoji} {day_desc}")
            st.markdown(f"⬆️ {max_c}°C / {max_f}°F")
            st.markdown(f"⬇️ {min_c}°C / {min_f}°F")
            st.markdown(f"💧 {noon_humidity}%")


# ── Main logic ────────────────────────────────────────────────────────────────
if city:
    with st.spinner(f"Fetching weather for **{city}**…"):
        try:
            weather_data = fetch_weather(city)
            display_weather(weather_data, city)
        except requests.exceptions.HTTPError as e:
            st.error(f"Could not find weather data for **{city}**. Please check the city name and try again. ({e})")
        except requests.exceptions.ConnectionError:
            st.error("Network error — please check your internet connection.")
        except requests.exceptions.Timeout:
            st.error("The request timed out. Please try again.")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
else:
    st.info("👆 Enter a city name above to get started.")
