import os
import json
import pandas as pd
from datetime import datetime

def load_raw_files(run_date:str) -> list[dict]:
    folder = f"raw/{run_date}"
    records = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        with open(filepath, "r") as f:
            records.append(json.load(f))
    return records

def flatten_record(record:dict, run_date: str) -> dict:
    return{
        "city": record["name"],
        "country": record["sys"]["country"],
        "temperature": record["main"]["temp"],
        "feels_like": record["main"]["feels_like"],
        "humidity": record["main"]["humidity"],
        "pressure": record["main"]["pressure"],
        "weather_condition": record["weather"][0]["main"],
        "wind_speed":record["wind"]["speed"],
        "recorded_at": datetime.utcfromtimestamp(record["dt"]),
        "run_date": run_date,
    }

def save_processed(df: pd.DataFrame, run_date: str ) -> None:
    folder= f"processed/{run_date}"
    os.makedirs(folder, exist_ok = True)
    filepath= f"{folder}/weather.csv"
    df.to_csv(filepath, index=False)
    print(f"Saved processed data -> {filepath}")

def run(run_date: str = None) -> None:
    run_date = run_date or datetime.utcnow().strftime("%Y-%m-%d")
    raw_records = load_raw_files(run_date)
    flattened = [flatten_record(r, run_date) for r in raw_records]
    df= pd.DataFrame(flattened)
    save_processed(df, run_date)

if __name__== "__main__":
    run()