# 🌤️ Random-Streamlit-Weather-App

A simple weather app built with [Streamlit](https://streamlit.io) that shows
current conditions and a 3-day forecast for any city in the world.

**No API key required** – weather data is sourced from the free
[wttr.in](https://wttr.in) service.

---

## Features

- 🔍 Search weather by city name
- 🌡️ Toggle between °C and °F
- 💧 Humidity, wind speed & direction, UV index, visibility, pressure
- 📅 3-day forecast
- 🎨 Clean, responsive Streamlit UI

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/gituserc1140/Random-Streamlit-Weather-App.git
cd Random-Streamlit-Weather-App

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`.

---

## Project Structure

```
Random-Streamlit-Weather-App/
├── app.py            # Main Streamlit application
├── requirements.txt  # Python dependencies
└── README.md
```

---

## Dependencies

| Package | Version |
|---------|---------|
| streamlit | ≥ 1.32.0 |
| requests | ≥ 2.31.0 |