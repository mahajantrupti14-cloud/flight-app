import sqlite3

# Connect to your database (creates file if not exists)
conn = sqlite3.connect("stock_data.db")
cursor = conn.cursor()

# Create sales table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT,
    category TEXT,
    revenue REAL,
    sale_date DATE
);
""")

# Insert sample data
sample_data = [
    ("Laptop A", "Electronics", 150000, "2026-06-01"),
    ("Mobile B", "Electronics", 80000, "2026-06-05"),
    ("Shirt C", "Clothing", 25000, "2026-06-10"),
    ("Tablet D", "Electronics", 60000, "2026-06-15"),
    ("Shoes E", "Footwear", 40000, "2026-06-20")
]

cursor.executemany("""
INSERT INTO sales (product_name, category, revenue, sale_date)
VALUES (?, ?, ?, ?);
""", sample_data)

conn.commit()
conn.close()

print("✅ Sales table created and sample data inserted successfully!")
