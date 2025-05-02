import pandas as pd
import os

INPUT_PATH = os.path.join("data", "raw", "weather_raw.csv")
OUTPUT_PATH = os.path.join("data", "processed", "weather_transformed.csv")

def transform_data():
    df = pd.read_csv(INPUT_PATH)

    # Простая трансформация: переименуем столбцы и добавим индекс
    df = df.rename(columns={
        "temperature_2m": "temp_C",
        "relative_humidity_2m": "humidity",
        "precipitation": "precip_mm",
        "cloudcover": "cloud_pct",
        "windspeed_10m": "wind_kph"
    })
    df.insert(0, "id", range(1, 1 + len(df)))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"[INFO] Данные трансформированы и сохранены в {OUTPUT_PATH}")

if __name__ == "__main__":
    transform_data()
