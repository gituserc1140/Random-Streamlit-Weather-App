import requests
import streamlit as st
from urllib.parse import quote

FORECAST_HOUR_INDEX = 4  # ~12:00 PM in wttr.in 3-hour blocks starting at 00:00


def fetch_weather(location: str | None = None) -> dict:
    """Fetch weather JSON from wttr.in for a location or current IP location.

    Args:
        location: Optional city/location text. If None, wttr.in resolves by requester IP.

    Returns:
        Parsed JSON payload as a dictionary.

    Raises:
        ValueError: If the weather service returns an HTTP error or invalid JSON.
        requests.RequestException: If the network request fails.
    """
    endpoint = "https://wttr.in/"
    query = quote(location.strip(), safe="") if location else ""
    url = f"{endpoint}{query}?format=j1"
    response = requests.get(url, timeout=10)
    try:
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as exc:
        raise ValueError(
            "Weather service returned an unexpected response. Please try again."
        ) from exc
    except requests.exceptions.JSONDecodeError as exc:
        raise ValueError(
            "Weather service sent invalid data. Please try again in a moment."
        ) from exc


def safe_get(data: dict | list, *keys, default: str = "N/A") -> str:
    """Safely traverse nested dict/list structures and return a string value.

    The function applies each key/index in order. For list values, integer keys are
    treated as indexes; for dict values, keys are looked up by name. If traversal
    fails at any point, the provided default value is returned.
    """
    current = data
    for key in keys:
        if isinstance(current, list):
            if not current:
                return default
            try:
                current = current[key]
            except (IndexError, TypeError):
                return default
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return default
        if current is None:
            return default
    return str(current)


st.set_page_config(page_title="Weather App", page_icon="🌦️")
st.title("🌦️ Weather App")
st.caption("Powered by wttr.in")

with st.sidebar:
    st.header("Search")
    use_current = st.checkbox("Use my current IP location", value=True)
    city = st.text_input("City", placeholder="e.g. London, Nairobi, New York")

if use_current:
    location_query = None
else:
    location_query = city.strip()
    if not location_query:
        st.info("Enter a city name or enable current location.")
        st.stop()

try:
    data = fetch_weather(location_query)
except ValueError as exc:
    st.error(str(exc))
    st.stop()
except requests.RequestException as exc:
    st.error(
        "Could not connect to the weather service. Check your internet connection and try again."
    )
    st.stop()

area = safe_get(data, "nearest_area", 0, "areaName", 0, "value")
region = safe_get(data, "nearest_area", 0, "region", 0, "value")
country = safe_get(data, "nearest_area", 0, "country", 0, "value")

st.subheader(f"{area}, {region}, {country}")

temp_c = safe_get(data, "current_condition", 0, "temp_C")
feels_like = safe_get(data, "current_condition", 0, "FeelsLikeC")
humidity = safe_get(data, "current_condition", 0, "humidity")
wind_kmph = safe_get(data, "current_condition", 0, "windspeedKmph")
description = safe_get(data, "current_condition", 0, "weatherDesc", 0, "value")

col1, col2, col3 = st.columns(3)
col1.metric("Temperature", f"{temp_c} °C")
col2.metric("Feels like", f"{feels_like} °C")
col3.metric("Humidity", f"{humidity}%")

st.write(f"**Conditions:** {description}")
st.write(f"**Wind speed:** {wind_kmph} km/h")

st.markdown("### 3-Day Forecast")
for day in data.get("weather", [])[:3]:
    date = day.get("date", "Unknown date")
    max_temp = day.get("maxtempC", "N/A")
    min_temp = day.get("mintempC", "N/A")
    avg_temp = day.get("avgtempC", "N/A")
    summary = safe_get(day, "hourly", FORECAST_HOUR_INDEX, "weatherDesc", 0, "value")

    with st.container(border=True):
        st.write(f"**{date}**")
        st.write(f"High: {max_temp} °C  |  Low: {min_temp} °C")
        st.write(f"Average Temperature: {avg_temp} °C")
        st.write(f"Summary: {summary}")
