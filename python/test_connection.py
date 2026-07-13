import psycopg2

def main():
    conn = psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="your_password",  # apna postgres password yahan likho
        host="localhost",
        port="5432"
    )

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM stock_prices;")
    print("Rows in stock_prices:", cur.fetchone()[0])

    cur.execute("SELECT * FROM sales;")
    print("Sales data:", cur.fetchall())

    conn.close()

if __name__ == "__main__":
    main()
