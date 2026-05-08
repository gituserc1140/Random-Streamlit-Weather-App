# Random Streamlit Weather App

A simple weather app built with Streamlit and the free [wttr.in](https://wttr.in) API.

## Features

- Search weather by city name
- Optional "use my current IP location" mode
- Current temperature, feels-like, humidity, wind, and weather description
- Small 3-day forecast

## Run locally

1. Create and activate a virtual environment (optional but recommended)
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the app:

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. In Streamlit Community Cloud, create a new app from this repo.
3. Set:
   - **Main file path**: `app.py`
4. Deploy.

No API key is required for wttr.in.
