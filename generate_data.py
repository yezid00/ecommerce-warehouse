from faker import Faker
from db_connection import get_connection
import random
from datetime import datetime, timedelta

fake = Faker()


def generate_customers(num_customers=50):
    """Generate sample customer data"""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        for _ in range(num_customers):
            cursor.execute(
                """
                INSERT INTO dim_customer(customer_name,email,city,country)
                VALUES(%s,%s,%s,%s);
            """,
                (fake.name(), fake.email(), fake.city(), fake.country()),
            )

        conn.commit()
        print("Customers created successfully")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


def generate_products(num_products=30):
    """Generate sample product data"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        categories = [
            "Electronics",
            "Clothing",
            "Books",
            "Home & Garden",
            "Sports",
            "Toys",
        ]

        for _ in range(num_products):
            category = random.choice(categories)

            cursor.execute(
                """
                INSERT INTO dim_product (product_name, category, price)
                VALUES (%s, %s, %s);
            """,
                (
                    fake.catch_phrase(),  # Random product name
                    category,
                    round(random.uniform(10.00, 500.00), 2),  # Price between $10-$500
                ),
            )

        conn.commit()

        print("Products generated successfully")

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        cursor.close()
        conn.close()


def generate_dates(days=365):
    """Generate date dimension for the year"""
    conn = get_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()

        start_date = datetime.now() - timedelta(days=days)

        for i in range(days):
            current_date = start_date + timedelta(days=i)

            cursor.execute(
                """
                INSERT INTO dim_date (date, year, month, day, quarter, day_of_week)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (date) DO NOTHING;
            """,
                (
                    current_date.date(),
                    current_date.year,
                    current_date.month,
                    current_date.day,
                    (current_date.month - 1) // 3 + 1,  # Calculate quarter
                    current_date.strftime("%A"),  # Day name (Monday, Tuesday, etc)
                ),
            )
        conn.commit()
        print(f"{days} dates created")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def generate_sales(num_sales=500):
    """Generate sales transactions"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        # Get ids from dimension tables
        cursor.execute("SELECT customer_id FROM dim_customer;")
        customer_ids = [row[0] for row in cursor.fetchall()]

        cursor.execute("SELECT product_id, price FROM dim_product;")
        products = cursor.fetchall()

        cursor.execute("SELECT date_id FROM dim_date;")
        date_ids = [row[0] for row in cursor.fetchall()]

        for _ in range(num_sales):
            product_id, price = random.choice(products)
            quantity = random.randint(1, 5)

            cursor.execute(
                """
                INSERT INTO fact_sales (customer_id, product_id, date_id, quantity, total_amount)
                VALUES (%s, %s, %s, %s, %s);
            """,
                (
                    random.choice(customer_ids),
                    product_id,
                    random.choice(date_ids),
                    quantity,
                    round(price * quantity, 2),
                ),
            )
        conn.commit()
        print(f"{num_sales} sales transactions created")
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    generate_customers(50)
    generate_products(30)
    generate_dates(365)
    generate_sales(500)
