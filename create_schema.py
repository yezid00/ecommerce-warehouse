import psycopg2
from dotenv import load_dotenv
import os
from db_connection import get_connection


load_dotenv()


def create_tables():

    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        # Create customer dimension

        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS dim_customer(
          customer_id SERIAL PRIMARY KEY,
          customer_name VARCHAR(100),
          email VARCHAR(100),
          city VARCHAR(50),
          country VARCHAR(50),
          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  
        );               
        """
        )
        print("customer dimension table created successfully")

        # Create product dimension table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS dim_product (
            product_id SERIAL PRIMARY KEY,
            product_name VARCHAR(100),
            category VARCHAR(50),
            price DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        )
        print("Product dimension table created successfully")

        # Create date dimension
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS dim_date (
            date_id SERIAL PRIMARY KEY,
            date DATE UNIQUE,
            year INTEGER,
            month INTEGER,
            day INTEGER,
            quarter INTEGER,
            day_of_week VARCHAR(10)
        );
        """
        )
        print("Date dimension table created successfully")

        # Create sales fact table
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS fact_sales (
            sale_id SERIAL PRIMARY KEY,
            customer_id INTEGER REFERENCES dim_customer(customer_id),
            product_id INTEGER REFERENCES dim_product(product_id),
            date_id INTEGER REFERENCES dim_date(date_id),
            quantity INTEGER,
            total_amount DECIMAL(10, 2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        )

        print("Sales fact table created successfully")

        conn.commit()

        print("Schema created succssfully")
    except Exception as e:
        print(f"An error occured {e}")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    create_tables()
