import streamlit as st
import requests
import random

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="WeatherMood",
    page_icon="🌤️",
    layout="centered"
)

# ----------------------------
# WMO WEATHER CODE MAP
# ----------------------------
WEATHER_CODES = {
    0: "Clear sky", 1: "Mostly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Depositing rime fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Rain showers", 81: "Heavy rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Severe thunderstorm"
}

def get_condition_category(code):
    if code in [0, 1]:
        return "clear"
    elif code in [2, 3]:
        return "cloudy"
    elif code in [45, 48]:
        return "fog"
    elif code in [51, 53, 55, 61, 63, 65, 80, 81, 82]:
        return "rain"
    elif code in [71, 73, 75]:
        return "snow"
    elif code in [95, 96, 99]:
        return "storm"
    return "unknown"

# ----------------------------
# API CALLS
# ----------------------------
@st.cache_data(ttl=600)
def get_coordinates(city_name):
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city_name, "count": 1, "language": "en", "format": "json"}
    response = requests.get(url, params=params)
    data = response.json()
    if "results" not in data:
        return None
    result = data["results"][0]
    return {
        "lat": result["latitude"],
        "lon": result["longitude"],
        "name": result["name"],
        "country": result.get("country", "")
    }

@st.cache_data(ttl=600)
def get_weather(lat, lon):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,"
                   "precipitation,weather_code,wind_speed_10m",
        "temperature_unit": "fahrenheit",
        "wind_speed_unit": "mph",
        "precipitation_unit": "inch"
    }
    response = requests.get(url, params=params)
    return response.json()

# ----------------------------
# FEATURE 1: CHAOS GENERATOR
# ----------------------------
def chaos_generator(temp, condition, wind, city):
    adventures = {
        "clear": [
            f"Go stand in a parking lot in {city} and stare at the sun like you unlocked a new personality trait.",
            f"Walk to the nearest gas station in {city} and buy a drink you've never tried, just to prove you're spontaneous.",
            f"Find the tallest building in {city} and pretend you're in a movie montage about 'starting over.'"
        ],
        "cloudy": [
            f"Sit on a bench in {city} and make up backstories for strangers walking by. You have {int(temp)}°F of material to work with.",
            f"Go to a thrift store in {city} and buy the ugliest sweater you can find. The clouds support this decision.",
            "Take a walk and practice your 'I'm deep in thought' face for absolutely no reason."
        ],
        "rain": [
            f"Put on a trash bag poncho and go 'puddle hunting' in {city}. You're basically a storm chaser now.",
            "Stand under an awning in dramatic silence like you're in a noir film waiting for someone who's never coming.",
            f"Convince a friend to get soaked with you in {city} and blame it on 'main character energy.'"
        ],
        "snow": [
            f"Build a tiny, deeply unimpressive snowman in {city} and name him something powerful like 'Chad.'",
            "Walk backwards in your own footprints and confuse exactly one (1) passerby.",
            f"It's {int(temp)}°F — go outside, scream into the void, watch your breath confirm you're still alive."
        ],
        "storm": [
            f"Stay inside in {city}, but narrate the thunder like a nature documentary host.",
            "Light a candle, make tea, and pretend you're in a gothic novel having an existential crisis.",
            "Text someone 'we need to talk' then don't say anything else. The storm did this, not you."
        ],
        "fog": [
            f"Walk into the fog in {city} like you're disappearing into another dimension. Very cinematic. 10/10.",
            "Pretend you're in a mystery novel and everyone you pass is a suspect.",
            "Yell 'IS ANYONE THERE' into the fog once. Just once. For the plot."
        ]
    }
    wind_bonus = ""
    if wind > 20:
        wind_bonus = f" Bonus chaos: it's {int(wind)} mph windy, so hold onto your dignity and anything loose."
    pool = adventures.get(condition, adventures["cloudy"])
    return random.choice(pool) + wind_bonus

# ----------------------------
# FEATURE 2: OUTFIT ROAST
# ----------------------------
def outfit_roast(temp):
    if temp >= 90:
        return ("🔥 **The Heatstroke Special**", 
                "Wear as little as socially acceptable. Shorts, a tank top, and the quiet acceptance that you will "
                "sweat through everything today. Deodorant is a suggestion, not a guarantee.")
    elif temp >= 75:
        return ("😎 **Main Character Summer**",
                "T-shirt, shorts, sunglasses you'll lose by 3pm. You look great, you feel great, "
                "ignore the fact you're one iced coffee away from dehydration.")
    elif temp >= 60:
        return ("🧥 **Light Jacket Energy**",
                "A hoodie or light jacket. You'll say 'it's not THAT cold' while internally regretting "
                "not bringing a real coat. Classic.")
    elif temp >= 45:
        return ("🧣 **Transitional Chaos**",
                "Layer like you're preparing for battle: jacket, maybe a scarf, definitely regret. "
                "You'll be sweating indoors and freezing outdoors within the same hour.")
    elif temp >= 30:
        return ("🥶 **Committed to the Bit (Winter Edition)**",
                "Full coat, hat, gloves — the whole uniform. You will still complain about the cold "
                "despite being dressed like you're summiting a mountain.")
    else:
        return ("🧊 **Human Popsicle Mode**",
                "Everything. Wear everything you own. Thermal layers, two pairs of socks, and the "
                "profound regret of ever leaving your house today.")

# ----------------------------
# FEATURE 3: COZY VS TOUCH GRASS SCORE
# ----------------------------
def cozy_vs_grass_score(temp, wind, precip):
    score = 50  # neutral starting point

    # Temperature scoring
    if 60 <= temp <= 78:
        score += 30
    elif 50 <= temp < 60 or 78 < temp <= 85:
        score += 10
    elif temp < 32 or temp > 95:
        score -= 30
    else:
        score -= 10

    # Precipitation scoring
    if precip > 0.1:
        score -= 35
    elif precip > 0:
        score -= 15

    # Wind scoring
    if wind > 25:
        score -= 20
    elif wind > 15:
        score -= 10

    score = max(0, min(100, score))

    if score >= 75:
        verdict = "🌱 TOUCH GRASS IMMEDIATELY"
        advice = "The weather gods have aligned. Going outside is basically mandatory at this point."
    elif score >= 50:
        verdict = "🚶 Cautiously Outdoorsy"
        advice = "It's fine out there. Not perfect, not terrible. A solid 'walk to get coffee' kind of day."
    elif score >= 25:
        verdict = "🛋️ Cozy-Leaning"
        advice = "You *could* go out, but a blanket and bad reality TV are calling your name louder."
    else:
        verdict = "🧸 MAXIMUM COZY — DO NOT ENGAGE WITH OUTSIDE"
        advice = "Nature is not asking nicely today. Stay in, make soup, live your softest life."

    return score, verdict, advice

# ----------------------------
# MAIN APP UI
# ----------------------------
st.title("🌦️ WeatherMood")
st.caption("Live weather data... with opinions.")

city = st.text_input("Enter your city:", placeholder="e.g. Austin, Chicago, Boston")

if city:
    location = get_coordinates(city)

    if location is None:
        st.error("Couldn't find that city 😬 Try checking the spelling or being more specific.")
    else:
        weather_data = get_weather(location["lat"], location["lon"])
        current = weather_data.get("current", {})

        temp = current.get("temperature_2m", 0)
        feels_like = current.get("apparent_temperature", 0)
        humidity = current.get("relative_humidity_2m", 0)
        wind = current.get("wind_speed_10m", 0)
        precip = current.get("precipitation", 0)
        code = current.get("weather_code", 0)
        condition_text = WEATHER_CODES.get(code, "Unknown")
        condition_category = get_condition_category(code)

        st.success(f"📍 {location['name']}, {location['country']}")

        # --- Current Conditions Panel ---
        col1, col2, col3 = st.columns(3)
        col1.metric("Temperature", f"{temp:.0f}°F", f"Feels like {feels_like:.0f}°F")
        col2.metric("Wind", f"{wind:.0f} mph")
        col3.metric("Humidity", f"{humidity:.0f}%")
        st.info(f"**Condition:** {condition_text}")

        st.divider()

        # --- Feature Tabs ---
        tab1, tab2, tab3 = st.tabs(["🎲 Chaos Generator", "👕 Outfit Roast", "🛋️ Cozy vs. Grass"])

        with tab1:
            st.subheader("Your Hyper-Specific Micro-Adventure")
            if st.button("Generate Chaos", type="primary"):
                adventure = chaos_generator(temp, condition_category, wind, location["name"])
                st.write(adventure)
            else:
                st.caption("Click the button. Embrace your fate.")

        with tab2:
            st.subheader("What You Should Wear (According to Us)")
            title, roast = outfit_roast(temp)
            st.markdown(f"### {title}")
            st.write(roast)

        with tab3:
            st.subheader("Should You Go Outside?")
            score, verdict, advice = cozy_vs_grass_score(temp, wind, precip)
            st.markdown(f"### {verdict}")
            st.progress(score / 100)
            st.write(f"**Touch Grass Score:** {score}/100")
            st.write(advice)

else:
    st.info("👆 Enter a city above to get started!")