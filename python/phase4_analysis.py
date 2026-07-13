import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

conn = sqlite3.connect("stock_data.db")

stock_df = pd.read_sql("SELECT * FROM stock_prices", conn, parse_dates=["date"])
sales_df = pd.read_sql("SELECT * FROM sales", conn, parse_dates=["sale_date"])

avg_close = stock_df.groupby("company")["close_price"].mean()
print("\nAverage Closing Price per Company:\n", avg_close)


max_close = stock_df.groupby("company")["close_price"].max()
print("\nHighest Closing Price per Company:\n", max_close)

monthly_volume = stock_df.groupby([stock_df["date"].dt.to_period("M"), "company"])["trading_volume"].sum()
print("\nMonthly Trading Volume:\n", monthly_volume)


total_revenue = sales_df.groupby("product_name")["revenue"].sum()
print("\nTotal Revenue per Product:\n", total_revenue)


avg_revenue = sales_df.groupby("category")["revenue"].mean()
print("\nAverage Revenue per Category:\n", avg_revenue)

monthly_sales = sales_df.groupby(sales_df["sale_date"].dt.to_period("M"))["revenue"].sum()
print("\nMonthly Sales Trend:\n", monthly_sales)

plt.figure(figsize=(8,5))
sns.barplot(x=avg_close.index, y=avg_close.values, palette="viridis")
plt.title("Average Closing Price per Company")
plt.xticks(rotation=45)
plt.show()

plt.figure(figsize=(8,5))
monthly_sales.plot(kind="line", marker="o", title="Monthly Sales Trend")
plt.ylabel("Revenue")
plt.show()
