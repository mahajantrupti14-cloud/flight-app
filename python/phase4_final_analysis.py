import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to SQLite database
conn = sqlite3.connect("stock_data.db")

# Load tables into DataFrames
stock_df = pd.read_sql("SELECT * FROM stock_prices", conn, parse_dates=["date"])
sales_df = pd.read_sql("SELECT * FROM sales", conn, parse_dates=["sale_date"])

# ---------------- STOCK ANALYSIS ----------------
avg_close = stock_df.groupby("company")["close_price"].mean()
max_close = stock_df.groupby("company")["close_price"].max()
monthly_volume = stock_df.groupby([stock_df["date"].dt.to_period("M"), "company"])["trading_volume"].sum()

print("\nAverage Closing Price per Company:\n", avg_close)
print("\nHighest Closing Price per Company:\n", max_close)
print("\nMonthly Trading Volume:\n", monthly_volume)

# ---------------- SALES ANALYSIS ----------------
total_revenue = sales_df.groupby("product_name")["revenue"].sum()
avg_revenue = sales_df.groupby("category")["revenue"].mean()
monthly_sales = sales_df.groupby(sales_df["sale_date"].dt.to_period("M"))["revenue"].sum()

print("\nTotal Revenue per Product:\n", total_revenue)
print("\nAverage Revenue per Category:\n", avg_revenue)
print("\nMonthly Sales Trend:\n", monthly_sales)

# ---------------- VISUALIZATION ----------------

# 1. Bar chart - Average Closing Price per Company
plt.figure(figsize=(8,5))
sns.barplot(x=avg_close.index, y=avg_close.values, palette="viridis")
plt.title("Average Closing Price per Company")
plt.ylabel("Price")
plt.xticks(rotation=45)
plt.show()

# 2. Line chart - Stock Price Trends
plt.figure(figsize=(10,6))
for company in stock_df["company"].unique():
    company_data = stock_df[stock_df["company"] == company]
    plt.plot(company_data["date"], company_data["close_price"], label=company)

plt.title("Stock Price Trends Over Time")
plt.xlabel("Date")
plt.ylabel("Closing Price")
plt.legend()
plt.show()

# 3. Pie chart - Revenue Share by Category
plt.figure(figsize=(6,6))
sales_df.groupby("category")["revenue"].sum().plot(
    kind="pie", autopct="%1.1f%%", startangle=90, cmap="Set3")
plt.title("Revenue Share by Category")
plt.ylabel("")
plt.show()

# 4. Bar chart - Top Products by Revenue
plt.figure(figsize=(8,5))
total_revenue_sorted = total_revenue.sort_values(ascending=False)
sns.barplot(x=total_revenue_sorted.index, y=total_revenue_sorted.values, palette="coolwarm")
plt.title("Top Products by Revenue")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.show()
