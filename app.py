import streamlit as st
import requests

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="centered",
)

# ── Constants ──────────────────────────────────────────────────────────────────
WTTR_URL = "https://wttr.in/{city}?format=j1"

WEATHER_CODE_MAP = {
    113: ("☀️", "Sunny / Clear"),
    116: ("⛅", "Partly Cloudy"),
    119: ("☁️", "Cloudy"),
    122: ("☁️", "Overcast"),
    143: ("🌫️", "Mist"),
    176: ("🌦️", "Patchy Rain"),
    179: ("🌨️", "Patchy Snow"),
    182: ("🌧️", "Patchy Sleet"),
    185: ("🌧️", "Patchy Freezing Drizzle"),
    200: ("⛈️", "Thundery Outbreaks"),
    227: ("🌨️", "Blowing Snow"),
    230: ("❄️", "Blizzard"),
    248: ("🌫️", "Fog"),
    260: ("🌫️", "Freezing Fog"),
    263: ("🌦️", "Light Drizzle"),
    266: ("🌦️", "Drizzle"),
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
    356: ("🌧️", "Moderate Rain Shower"),
    359: ("🌧️", "Heavy Rain Shower"),
    362: ("🌧️", "Light Sleet Showers"),
    365: ("🌧️", "Moderate Sleet Showers"),
    368: ("🌨️", "Light Snow Showers"),
    371: ("❄️", "Moderate Snow Showers"),
    374: ("🌧️", "Light Ice Pellet Showers"),
    377: ("🌧️", "Moderate Ice Pellet Showers"),
    386: ("⛈️", "Thundery Rain"),
    389: ("⛈️", "Heavy Thundery Rain"),
    392: ("⛈️", "Thundery Snow"),
    395: ("⛈️", "Heavy Thundery Snow"),
}

# wttr.in returns hourly slots for 0 h, 3 h, 6 h, 9 h, 12 h, … (every 3 h).
# Index 4 corresponds to the 12:00 (noon) reading, used for the daily forecast.
FORECAST_NOON_INDEX = 4

WIND_DIR_EMOJI = {
    "N": "⬆️", "NNE": "↗️", "NE": "↗️", "ENE": "↗️",
    "E": "➡️", "ESE": "↘️", "SE": "↘️", "SSE": "↘️",
    "S": "⬇️", "SSW": "↙️", "SW": "↙️", "WSW": "↙️",
    "W": "⬅️", "WNW": "↖️", "NW": "↖️", "NNW": "↖️",
}

UV_LABELS = {
    0: "Low", 1: "Low", 2: "Low",
    3: "Moderate", 4: "Moderate", 5: "Moderate",
    6: "High", 7: "High",
    8: "Very High", 9: "Very High", 10: "Very High",
    11: "Extreme",
}


# ── Helpers ────────────────────────────────────────────────────────────────────

def celsius_to_fahrenheit(c: float) -> float:
    return c * 9 / 5 + 32


def get_weather(city: str) -> tuple[dict | None, str | None]:
    """Fetch weather JSON from wttr.in.

    Returns a (data, error_message) tuple. On success, data is the parsed JSON
    and error_message is None. On failure, data is None and error_message
    contains a human-readable description of the problem.
    """
    try:
        resp = requests.get(WTTR_URL.format(city=requests.utils.quote(city)), timeout=10)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Network error – check your internet connection."
    except requests.exceptions.Timeout:
        return None, "Request timed out – the weather service may be slow. Try again."
    except requests.exceptions.HTTPError as exc:
        return None, f"HTTP error {exc.response.status_code} – city not found or service unavailable."
    except Exception as exc:
        return None, f"Unexpected error: {exc}"


def weather_emoji_desc(code: int) -> tuple[str, str]:
    return WEATHER_CODE_MAP.get(code, ("🌡️", "Unknown"))


def uv_label(index: int) -> str:
    return UV_LABELS.get(min(index, 11), "Extreme")


# ── UI ─────────────────────────────────────────────────────────────────────────

st.title("🌤️ Weather App")
st.markdown("Enter a city name to get the current weather conditions.")

col_input, col_unit = st.columns([3, 1])
with col_input:
    city = st.text_input("City", placeholder="e.g. London, Tokyo, New York")
with col_unit:
    unit = st.radio("Unit", ["°C", "°F"], horizontal=True)

if city:
    with st.spinner(f"Fetching weather for **{city}**…"):
        data, error = get_weather(city)

    if error:
        st.error(f"⚠️ {error}")
    else:
        try:
            current = data["current_condition"][0]
            area_info = data["nearest_area"][0]
            area_name = area_info["areaName"][0]["value"]
            country = area_info["country"][0]["value"]

            temp_c = int(current["temp_C"])
            feels_c = int(current["FeelsLikeC"])
            humidity = int(current["humidity"])
            wind_kmph = int(current["windspeedKmph"])
            wind_dir = current["winddir16Point"]
            visibility_km = int(current["visibility"])
            pressure_mb = int(current["pressure"])
            uv_index = int(current["uvIndex"])
            desc_code = int(current["weatherCode"])
            description = current["weatherDesc"][0]["value"]

            emoji, _ = weather_emoji_desc(desc_code)

            temp_display = temp_c if unit == "°C" else round(celsius_to_fahrenheit(temp_c), 1)
            feels_display = feels_c if unit == "°C" else round(celsius_to_fahrenheit(feels_c), 1)

            # ── Location & main condition ──────────────────────────────────────
            st.divider()
            loc_col, cond_col = st.columns([2, 1])
            with loc_col:
                st.subheader(f"📍 {area_name}, {country}")
                st.markdown(f"### {emoji} {description}")
            with cond_col:
                st.metric("Temperature", f"{temp_display}{unit}")
                st.metric("Feels Like", f"{feels_display}{unit}")

            # ── Details grid ──────────────────────────────────────────────────
            st.divider()
            d1, d2, d3 = st.columns(3)
            with d1:
                st.metric("💧 Humidity", f"{humidity}%")
                st.metric("🔬 UV Index", f"{uv_index} – {uv_label(uv_index)}")
            with d2:
                wind_arrow = WIND_DIR_EMOJI.get(wind_dir, "")
                st.metric("💨 Wind", f"{wind_kmph} km/h")
                st.metric("🧭 Direction", f"{wind_arrow} {wind_dir}")
            with d3:
                st.metric("👁️ Visibility", f"{visibility_km} km")
                st.metric("🌡️ Pressure", f"{pressure_mb} mb")

            # ── 3-day forecast ────────────────────────────────────────────────
            if "weather" in data and data["weather"]:
                st.divider()
                st.subheader("📅 3-Day Forecast")
                forecast_cols = st.columns(len(data["weather"]))
                for i, day in enumerate(data["weather"]):
                    date = day["date"]
                    max_c = int(day["maxtempC"])
                    min_c = int(day["mintempC"])
                    day_code = int(day["hourly"][FORECAST_NOON_INDEX]["weatherCode"])
                    day_emoji, day_desc = weather_emoji_desc(day_code)

                    max_d = max_c if unit == "°C" else round(celsius_to_fahrenheit(max_c), 1)
                    min_d = min_c if unit == "°C" else round(celsius_to_fahrenheit(min_c), 1)

                    with forecast_cols[i]:
                        st.markdown(f"**{date}**")
                        st.markdown(f"{day_emoji} {day_desc}")
                        st.markdown(f"↑ {max_d}{unit}  ↓ {min_d}{unit}")

        except (KeyError, IndexError, ValueError) as exc:
            st.error(f"⚠️ Unexpected data format: {exc}")

st.caption("Data provided by [wttr.in](https://wttr.in) · No API key required")
