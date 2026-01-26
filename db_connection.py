import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()


def get_connection():
    """Create and return a db connection"""

    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
        )

        return conn
    except Exception as e:
        print(f"Connection error : {e}")
        return None
