import psycopg2

def main():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="7821029949",  
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    # Average closing price per company
    cur.execute("""
        SELECT company, AVG(close_price) AS avg_close
        FROM stock_prices
        GROUP BY company;
    """)
    print("Average closing price per company:", cur.fetchall())


    cur.execute("""
        SELECT company, MAX(date) AS latest_date, close_price
        FROM stock_prices
        GROUP BY company, close_price;
    """)
    print("Latest closing price per company:", cur.fetchall())

    cur.execute("""
        SELECT product_name, SUM(revenue) AS total_revenue
        FROM sales
        GROUP BY product_name;
    """)
    print("Total revenue per product:", cur.fetchall())

    conn.close()

if __name__ == "__main__":
    main()
