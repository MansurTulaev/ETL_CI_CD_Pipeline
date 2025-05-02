import boto3
import os

INPUT_PATH = os.path.join("data", "processed", "weather_transformed.csv")
BUCKET = "my-lake"
KEY = "raw/weather_transformed.csv"

def upload_to_s3():
    print("📁 Проверка пути:", INPUT_PATH)
    print("📦 Ключ в S3:", KEY)
    print("🪣 Название бакета:", BUCKET)

    if not os.path.exists(INPUT_PATH):
        print("❌ Файл не найден, загрузка отменена.")
        return

    try:
        s3 = boto3.client(
            "s3",
            endpoint_url="http://localstack:4566",
            aws_access_key_id="test",
            aws_secret_access_key="test",
            region_name="us-east-1",
        )
        try:
            s3.head_bucket(Bucket=BUCKET)
        except:
            print(f"ℹ️ Бакет {BUCKET} не найден — создаём.")
            s3.create_bucket(Bucket=BUCKET)

        print("🚀 Загружаем файл в S3...")
        s3.upload_file(INPUT_PATH, BUCKET, KEY)
        print("✅ Файл успешно загружен.")
    except Exception as e:
        print("❌ Ошибка при загрузке файла:", e)
        raise

if __name__ == "__main__":
    upload_to_s3()
