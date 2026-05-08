from __future__ import annotations

from random import choice, randint
from typing import Any

import streamlit as st


def get_weather() -> dict[str, Any]:
    return {
        "temperature": randint(-5, 35),
        "feels_like": randint(-8, 37),
        "humidity": randint(20, 95),
        "wind_speed": randint(0, 40),
        "condition": choice(
            ["Sunny", "Partly Cloudy", "Cloudy", "Rainy", "Windy", "Stormy"]
        ),
    }


def main() -> None:
    st.set_page_config(page_title="Weather App", page_icon="🌤️")
    st.title("🌤️ Weather App")
    st.write("Enter a city to see the current weather.")

    city = st.text_input("City", value="London").strip()

    if not city:
        st.info("Enter a city name to get started.")
        return

    if st.button("Get weather", type="primary"):
        weather = get_weather()

        st.subheader(f"Current weather in {city}")
        st.metric("Temperature", f'{weather["temperature"]}°C')
        st.metric("Feels like", f'{weather["feels_like"]}°C')

        col1, col2, col3 = st.columns(3)
        col1.metric("Humidity", f'{weather["humidity"]}%')
        col2.metric("Wind", f'{weather["wind_speed"]} km/h')
        col3.metric("Condition", weather["condition"])


if __name__ == "__main__":
    main()
