import requests
import pandas as pd
import os
from datetime import datetime, timedelta

LATITUDE = 55.75  # Москва
LONGITUDE = 37.62
OUTPUT_PATH = os.path.join("data", "raw", "weather_raw.csv")

def fetch_weather_data():
    today = datetime.utcnow().date()
    start_date = today - timedelta(days=1)
    end_date = today

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={LATITUDE}&longitude={LONGITUDE}&start_date={start_date}&end_date={end_date}"
        f"&hourly=temperature_2m,relative_humidity_2m,precipitation,cloudcover,windspeed_10m"
        f"&timezone=UTC"
    )

    print(f"[INFO] Запрос данных: {url}")
    response = requests.get(url)
    response.raise_for_status()
    json_data = response.json()

    df = pd.DataFrame(json_data["hourly"])
    print(f"[INFO] Получено строк: {len(df)}")

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[INFO] Данные сохранены в {OUTPUT_PATH}")

if __name__ == "__main__":
    fetch_weather_data()
