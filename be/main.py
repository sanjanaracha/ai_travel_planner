from fastapi import FastAPI,Request,Query
from langchain_groq import ChatGroq
from langchain.tools import tool
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import requests
import os


load_dotenv()
app=FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# LLM

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key= os.getenv("GROQ_API_KEY")
)

#TOOLS

OPENWEATHER_API_KEY =os.getenv("OPENWEATHER_API_KEY")


# ---------------- TOOLS ---------------- #

@tool
def get_weather(city: str):
    """Get weather details"""

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}"
        f"&appid={OPENWEATHER_API_KEY}"
        f"&units=metric"
    )

    return requests.get(url).json()


@tool
def tourist_places(place: str):
    """Get tourist places"""

    places = {
        "kerala": [
            "Munnar",
            "Alleppey",
            "Kochi",
            "Wayanad",
            "Thekkady"
        ],
        "goa": [
            "Baga Beach",
            "Calangute Beach",
            "Anjuna Beach",
            "Dudhsagar Falls"
        ],
        "hyderabad": [
            "Charminar",
            "Golconda Fort",
            "Ramoji Film City",
            "Tank Bund"
        ]
    }

    return places.get(place.lower(), ["No places found"])


@tool
def budget_calculator(city: str, days: int):
    """Calculate budget"""

    budget_map = {
        "kerala": 3500,
        "goa": 5000,
        "hyderabad": 2500,
        "mumbai": 6000,
        "delhi": 4500
    }

    per_day = budget_map.get(city.lower(), 3000)

    return {
        "budget": per_day * days
    }


# ---------------- ROOT ---------------- #

@app.get("/")
def home():
    return {
        "message": "Travel Planner API Running"
    }


# ---------------- WEATHER ---------------- #

@app.get("/weather")
def weather(city: str = Query(...)):
    return get_weather.invoke(city)


# ---------------- PLACES ---------------- #

@app.get("/places")
def places(place: str = Query(...)):
    return {
        "places": tourist_places.invoke(place)
    }


# ---------------- BUDGET ---------------- #

@app.get("/budget")
def budget(
    city: str = Query(...),
    days: int = Query(...)
):

    return budget_calculator.invoke(
        {
            "city": city,
            "days": days
        }
    )


# ---------------- TRAVEL ---------------- #

@app.post("/travel")
async def travel(request: Request):

    body = await request.json()

    city = body["city"]
    days = body["days"]

    weather = get_weather.invoke(city)

    places = tourist_places.invoke(city)

    budget = budget_calculator.invoke(
        {
            "city": city,
            "days": days
        }
    )

    temp = weather["main"]["temp"]
    condition = weather["weather"][0]["description"]

    prompt = f"""
You are an expert AI Travel Planner.

Destination: {city}

Trip Duration: {days} days

Weather:
Temperature: {temp}
Condition: {condition}

Places:
{places}

Estimated Budget:
₹{budget["budget"]}

Generate:

1. Day-wise itinerary
2. Places to visit
3. Budget summary
4. Travel tips
"""

    result = llm.invoke(prompt)

    return {
        "response": result.content
    }