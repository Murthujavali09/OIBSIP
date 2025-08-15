# Basic Weather App (Tkinter, Python)

A desktop GUI weather application that fetches real‑time conditions and a 7‑day forecast using Open‑Meteo, with automatic location detection, unit switching (Metric/Imperial), animated weather icons, and a clean two‑page interface (Dashboard → Weather).

## Objective

- Provide a simple GUI to look up weather by city or via auto‑location.
- Display current conditions, hourly snapshot, and weekly forecast.
- Offer usability features: copy‑free navigation, unit toggle, status feedback, and robust error handling.


## Tools and Technologies Used

- Python 3
- Tkinter for GUI (Frames, Labels, Buttons, ttk Combobox/Entry, Toplevel, messagebox)
- requests for HTTP (Open‑Meteo, geocoding, IP geolocation)
- Pillow (PIL) for image loading and animated GIF handling
- Open‑Meteo APIs:
    - Geocoding: resolve city to latitude/longitude
    - Forecast: current weather, hourly, and daily data


## Features

- Search by city with validation against Open‑Meteo geocoding
- Auto locate via IP (ipinfo.io and ipapi.co as fallbacks)
- Current conditions:
    - Temperature, wind, humidity, visibility, sunrise/sunset, condition text, icon
- Forecast views:
    - Weekly: day name, condition + animated icon, min/max temps
    - Hourly: time, temp, condition, wind, humidity
- Units toggle: Metric (°C, km/h, km) or Imperial (°F, mph, mi)
- Animated icons (GIFs) with caching for smooth playback
- Clear loading and error states; input validation and network checks
- Full‑screen friendly, responsive grid layout


## Project Structure

- src/
    - app.py — app bootstrap and page navigation (Tk root, frame stacking)
    - dashboard.py — landing page: city input, auto locate, validation, submit
    - weather.py — detailed weather UI; current panel + forecast tables, unit switch, icon animation
    - api.py — data layer: geocoding, forecast retrieval, parsing/formatting, code→text/icon mapping, simple state store
    - UI/icons/ — weather icons (GIF/PNG) referenced by weather code


## How It Works

1. City to coordinates:
    - api.is_valid() checks input via Open‑Meteo geocoding.
    - dashboard detects city automatically via IP services when requested.
2. Fetch forecast:
    - api.get_weather_data(city) calls Open‑Meteo forecast with current_weather, hourly, and daily parameters for 7 days.
    - Maps Open‑Meteo weather codes to human‑readable conditions and icon files.
    - Normalizes values:
        - Humidity, visibility, wind, sunrise/sunset (formatted), and temperature.
        - Builds three structures: current_weather (dict), hourly_forecast (list), daily_forecast (list).
    - Stores results in module state; weather.py reads via api.get_data().
3. Display:
    - Dashboard → Weather page.
    - Weather page shows:
        - Current panel with city, temp, condition text, icon, visibility, humidity, wind, sunrise/sunset.
        - Forecast panel with toggle between Weekly and Hourly tables.
    - Units combobox triggers in‑place conversion without refetching.
4. Icons and animation:
    - Icon path resolved by weather code.
    - GIFs are read into frames, cached, and looped using Tkinter after().

## Steps Performed 

- Built two‑page Tkinter app shell with a shared container and frame registry.
- Implemented dashboard:
    - Entry + “Get Weather” button, auto‑locate button, status label.
    - Input trimming, empty check, geocoding validation, network error handling.
- Implemented api layer:
    - Geocoding request, forecast request, parsing with safety checks.
    - Weather code→label/icon mapping and unit‑friendly fields.
    - Graceful fallbacks when timestamps/indices don’t align.
- Implemented weather view:
    - Current card: city, temp, icon, condition, stats, sunrise/sunset.
    - Forecast table builders for weekly and hourly modes.
    - Unit conversion helpers (°C↔°F, km/h↔mph).
    - Animated GIF loader with caching and resilient playback.
- Wired navigation and state handoff between pages.


## Usage

- Requirements:
    - Python 3.x
    - pip install the following :
        - requests
        - pillow
- Run:
    - From src/: python app.py
- In the app:
    - Enter a city and click “Get Weather,” or click “Auto Locate.”
    - Switch “Units” to Metric or Imperial as preferred.
    - Toggle Weekly/Hourly in the forecast section.
    - Use “Back” to return to the Dashboard.


## Configuration Notes

- Internet connection is required for geocoding and weather retrieval.
- No API keys are required for Open‑Meteo; IP services are used without keys in this build.
- Ensure UI/icons contains the referenced image filenames:
    - sun.gif, partial_clouds.gif, clouds.gif, foggy.gif, rain.gif, drizzle.gif, rainy.gif, snow.gif, storm.gif, hail.gif, plus rainy.png for the default left‑panel image if present.


## Error Handling and Validation

- Empty city input: warning dialog.
- Invalid city: error dialog after geocoding check.
- Network issues: explicit “network error” message on dashboard and catch‑all exception handling in both dashboard and weather views.
- Defensive parsing: falls back when current time index is missing from hourly data.


## Outcome

- A robust, user‑friendly desktop weather app with real‑time data, animated visuals, and practical UX features.
- City search + auto locate, unit toggling, weekly/hourly views, clear status feedback, and resilient error handling.


## Possible Enhancements

- Persist last searched location and unit preference.
- Add more hourly range with scrolling and day selector.
- Include precipitation probability, pressure, and UV index if available.
- Add theming (dark/light) and accessibility improvements (keyboard navigation, ARIA‑like semantics where applicable).
- Package as an executable (PyInstaller) for easier distribution.

