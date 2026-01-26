import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

    conn.autocommit = True
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE ecommerce_warehouse;")
    print("Database created successfully")

    cursor.close()
    conn.close()
except Exception as e:
    print(f"Database creation failed {e}")
