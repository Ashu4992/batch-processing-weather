import os
import json
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather/"

CITIES= ['London','New York','Tokyo','Sydney','Mumbai']

def fetch_weather(city:str) -> dict:
    params = {"q": city, "appid":API_KEY, "units":"metric"}
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status() #fail loudly if the API call didn't succeed
    return response.json()

def save_raw(data: dict, city:str, run_date: str) -> None:
    folder = f"raw/{run_date}"
    os.makedirs(folder, exist_ok=True)
    filepath = f"{folder}/{city.replace(' ','_')}.json"
    with open(filepath, "w") as f:
        json.dump(data,f,indent=2)
    print(f"Saved raw data for {city} -> {filepath}")

def run(run_date:str = None) -> None:
    run_date= run_date or datetime.utcnow().strftime("%Y-%m-%d")
    for city in CITIES:
        data = fetch_weather(city)
        save_raw(data,city,run_date)

if __name__ == "__main__":
    run()