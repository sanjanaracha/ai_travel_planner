import streamlit as st
import requests

S_URL =st.secrets("s_url")

travel_tab, weather_tab, budget_tab, places_tab = st.tabs(
    [
        "✈️ Travel Planner",
        "🌤 Weather",
        "💰 Budget",
        "📍 Tourist Places"
    ]
)

# ---------------- TRAVEL ---------------- #

with travel_tab:

    st.header("AI Travel Planner")

    city = st.text_input(
        "Destination City",
        key="travel_city"
    )

    days = st.number_input(
        "Trip Duration",
        min_value=1,
        value=5
    )

    if st.button("Generate Travel Plan"):

        response = requests.post(
            f"{S_URL}/travel",
            json={
                "city": city,
                "days": int(days)
            }
        )

        data = response.json()

        st.markdown(data["response"])


# ---------------- WEATHER ---------------- #

with weather_tab:

    city_weather = st.text_input(
        "Enter City",
        key="weather_city"
    )

    if st.button("Get Weather"):

        response = requests.get(
            f"{S_URL}/weather",
            params={
                "city": city_weather
            }
        )

        data = response.json()

        st.write(
            "Temperature:",
            data["main"]["temp"]
        )

        st.write(
            "Humidity:",
            data["main"]["humidity"]
        )

        st.write(
            "Condition:",
            data["weather"][0]["description"]
        )


# ---------------- BUDGET ---------------- #

with budget_tab:

    city_budget = st.text_input(
        "Destination City",
        key="budget_city"
    )

    days_budget = st.number_input(
        "Days",
        min_value=1,
        value=5,
        key="budget_days"
    )

    if st.button("Calculate Budget"):

        response = requests.get(
            f"{S_URL}/budget",
            params={
                "city": city_budget,
                "days": int(days_budget)
            }
        )

        data = response.json()

        st.success(
            f"Estimated Budget: ₹{data['budget']}"
        )


# ---------------- PLACES ---------------- #

with places_tab:

    place = st.text_input(
        "Enter Destination",
        key="place_city"
    )

    if st.button("Get Places"):

        response = requests.get(
            f"{S_URL}/places",
            params={
                "place": place
            }
        )

        data = response.json()

        for p in data["places"]:
            st.write("📍", p)