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
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT customer_name,city,country, SUM(total_amount)
FROM dim_customer JOIN fact_sales USING(customer_id)
GROUP BY customer_name,city,country
ORDER BY SUM(total_amount) DESC
LIMIT 10;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Top customer details")
        print(f"{'Name':<25} {'City':<20} {'City':<20} {'# Country':<10}")

        for row in result:
            print(f"{row[0]:<25} {row[1]:<20} {row[2]:<20} {row[3]:<10}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_total_amount_spend():
    """Get total amount spent"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT customer_name, SUM(total_amount)
        FROM dim_customer JOIN fact_sales USING(customer_id)
        GROUP BY customer_name
        ORDER BY SUM(total_amount) DESC
        LIMIT 10;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Top customer details")
        print(f"{'Name':<25} {'Total amount':<20}")

        for row in result:
            print(f"{row[0]:<25} {row[1]:<20}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_number_of_purchases():
    """Get top customers number of purchases"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT customer_name,COUNT(sale_id) FROM dim_customer
        JOIN fact_sales USING(customer_id)
        GROUP BY customer_name
        ORDER BY COUNT(sale_id) DESC
        LIMIT 10;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        print("Number of purchases")
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_average_transaction_value_per_week_day():
    """Average transaction value per day of week"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT AVG(fact_sales.total_amount) AS avg_transaction_value,day_of_week FROM dim_date
        JOIN fact_sales USING(date_id) 
        WHERE dim_date.date >= CURRENT_DATE - INTERVAL '1 week'
        GROUP BY day_of_week
        ORDER BY AVG(fact_sales.total_amount) DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        print("Average transaction value per day of week")
        print(f"{'Day of week':<25} {'Average transaction value':<20}")
        for row in result:
            print(f"{row[1]:<25} {row[0]:<20}")

    except Exception as e:
        print("Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_number_of_sales_per_day_of_week():
    """Number of sales per day of week"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT COUNT(fact_sales.sale_id) AS sales_count,day_of_week FROM dim_date
        JOIN fact_sales USING(date_id) 
        WHERE dim_date.date >= CURRENT_DATE - INTERVAL '1 week'
        GROUP BY day_of_week
        ORDER BY AVG(fact_sales.total_amount) DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        print("Transaction value per day of week")
        print(f"{'Day of week':<25} {'Total transaction count':<20}")
        for row in result:
            print(f"{row[1]:<25} {row[0]:<20}")

    except Exception as e:
        print("Error: {e}")
    finally:
        cursor.close()
        conn.close()


# Quarterly performance
def get_total_revenue_by_quarter():
    """Total revenue by quarter"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT SUM(fact_sales.total_amount) AS revenue,dim_date.quarter,dim_date.year FROM fact_sales
        JOIN dim_date USING(date_id) 
        GROUP BY dim_date.quarter,dim_date.year
        ORDER BY dim_date.year,dim_date.quarter
        """

        cursor.execute(query)
        result = cursor.fetchall()

        print("Total revenue by quarter")
        print(f"{'Year':<25} {'Quarter':<20} {"Revenue":<20}")
        for row in result:
            print(f"{row[2]:<25} {row[1]:<20} {row[0]:<20}")

    except Exception as e:
        print("Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_number_of_transactions_per_quarter():
    """Number of transactions per quarter"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT dim_date.year,dim_date.quarter, COUNT(fact_sales.sale_id)
        FROM fact_sales 
        JOIN dim_date USING(date_id)
        GROUP BY dim_date.quarter,dim_date.year
		ORDER BY dim_date.year,dim_date.quarter DESC
        """

        cursor.execute(query)
        result = cursor.fetchall()

        print(f"Number of transactions per quarter")
        print(f"{'Year':<25} {'Quarter':<20} {'Transaction count':<20}")
        for row in result:
            print(f"{row[0]:<25} {row[1]:<20} {row[2]:<20}")

    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


# Top products


def get_top_products():
    """Top product name and category"""
    conn = get_connection()

    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT dim_product.product_name,dim_product.category,COUNT(fact_sales.product_id)
        FROM dim_product
        JOIN fact_sales USING(product_id)
        GROUP BY dim_product.product_name,dim_product.category
        ORDER BY COUNT(fact_sales.product_id) DESC
        LIMIT 10;
        """

        cursor.execute(query)
        result = cursor.fetchall()

        print(f"Top product name and category")
        for row in result:
            print(row)

    except Exception as e:
        print(f"Error : {e}")
    finally:
        cursor.close()
        conn.close()


def get_total_revenue_generated():
    """Total revenue generated"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()

        query = """SELECT dim_product.product_name,SUM(total_amount) 
        FROM dim_product
        JOIN fact_sales USING(product_id)
		GROUP BY dim_product.product_name
		ORDER BY SUM(total_amount) DESC
		LIMIT 10;
        """
        cursor.execute(query)
        result = cursor.fetchall()

        print("Total revenue generated")
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()


# Customer purchase frequency


def get_customer_purchase_frequency():
    """How many customers made 1,2,3+ purchaes"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = """SELECT dim_customer.customer_name,COUNT(sale_id)
        FROM dim_customer
        JOIN fact_sales USING(customer_id)
        GROUP BY dim_customer.customer_name
        ORDER BY COUNT(sale_id) DESC
        LIMIT 10;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Customer purchase frequency")
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()


def get_average_order_value_by_customer_segment():
    """Average order value by customer segment"""
    conn = get_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        query = """SELECT dim_customer.customer_name,AVG(total_amount) as average_order_value,COUNT(sale_id) as order_count
        FROM dim_customer
        JOIN fact_sales USING(customer_id)
        GROUP BY dim_customer.customer_name
        ORDER BY COUNT(sale_id) DESC
        LIMIT 10;"""

        cursor.execute(query)
        result = cursor.fetchall()

        print("Average order value")
        for row in result:
            print(row)
    except Exception as e:
        print(f"Error: {e}")

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    get_total_revenue_per_product_category()
    get_number_of_sales_per_category()
    get_total_items_sold_per_category()
    get_revenue_by_month()
    get_number_of_transactions_per_month()
    group_sales_by_year_and_month()
    get_customer_details()
    get_total_amount_spend()
    get_number_of_purchases()
    get_average_transaction_value_per_week_day()
    get_number_of_sales_per_day_of_week()
    get_total_revenue_by_quarter()
    get_number_of_transactions_per_quarter()
    get_top_products()
    get_total_revenue_generated()
    get_customer_purchase_frequency()
    get_average_order_value_by_customer_segment()
