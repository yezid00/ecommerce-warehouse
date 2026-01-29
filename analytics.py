from db_connection import get_connection
import calendar


def get_total_revenue_per_product_category():
    """Get total revenue per product category"""

    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT SUM(total_amount),category FROM fact_sales
            JOIN dim_product ON dim_product.product_id = fact_sales.product_id
            GROUP BY dim_product.category;"""

        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Total revenue per product category \n")
        for row in result:
            print(f"{row[1]} : {row[0]}")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


def get_number_of_sales_per_category():
    conn = get_connection()

    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """
            SELECT COUNT(sale_id),category FROM fact_sales
            JOIN dim_product ON dim_product.product_id = fact_sales.product_id
            GROUP BY dim_product.category;
        """

        cursor.execute(query)
        result = cursor.fetchall()
        print(f"Number of sales per category\n")

        for row in result:
            print(f"{row[1]} : {row[0]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_total_items_sold_per_category():
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT SUM(quantity),category FROM fact_sales
JOIN dim_product ON dim_product.product_id = fact_sales.product_id
GROUP BY dim_product.category;"""
        cursor.execute(query)
        result = cursor.fetchall()

        print("Total items sold per category:")
        for row in result:
            print(f"{row[1]} : {row[0]}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


##Monthly sales trend
def get_revenue_by_month():
    """Get revenue by month for the past 12 months"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT SUM(total_amount),month FROM fact_sales 
        JOIN dim_date USING(date_id)
        WHERE dim_date.date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY dim_date.month ORDER BY month;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Revenue by month")
        for row in result:
            print(f"{calendar.month_name[row[1]]} : {row[0]}")
            # print(row)
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


def get_number_of_transactions_per_month():
    """Get number of transactions per month"""
    conn = get_connection()

    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT COUNT(sale_id),month FROM fact_sales 
JOIN dim_date USING(date_id)
WHERE dim_date.date >= CURRENT_DATE - INTERVAL '12 months'
GROUP BY dim_date.month ORDER BY month;"""

        cursor.execute(query)

        result = cursor.fetchall()
        print("Number of transactions by month")
        for row in result:
            print(f"{calendar.month_name[row[1]]} : {row[0]}")
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


def group_sales_by_year_and_month():
    """Group by year and month"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = """SELECT SUM(fact_sales.total_amount),
        COUNT(fact_sales.sale_id)
        ,month,year FROM fact_sales 
        JOIN dim_date USING(date_id)
        WHERE dim_date.date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY dim_date.year,dim_date.month ORDER BY month;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Sales by year and Month")
        print(f"{'Year':<25} {'Month':<20} {'Total amount':<20} {'# Count':<10}")

        for row in result:
            print(
                f"{row[3]:<25} {calendar.month_name[row[2]]:<20} {row[0]:<20} {row[1]:<10}"
            )
    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


# Customer Analytics
def get_customer_details():
    """Get top customers name,city and country"""


def get_total_amount_spend():
    """Get total amount spent"""


def get_number_of_purchases():
    """Get top customers number of purchases"""


if __name__ == "__main__":
    # get_total_revenue_per_product_category()
    # get_number_of_sales_per_category()
    # get_total_items_sold_per_category()
    get_revenue_by_month()
    get_number_of_transactions_per_month()
    group_sales_by_year_and_month()
